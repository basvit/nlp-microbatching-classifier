import asyncio
from dataclasses import dataclass
from time import monotonic

from app.classifier import classify_comments_batch
from app.config import (
    BATCH_TIMEOUT_SECONDS,
    MAX_BATCH_SIZE,
)

from app.metrics import (
    batch_inference_duration_seconds,
    batches_processed_total,
    batch_size_histogram,
    batch_wait_time_seconds,
    comments_classified_by_label_total,
    comments_classified_total,
    microbatch_queue_size,
)


@dataclass
class QueueItem:
    """Represents a queued classification request"""

    comment: str
    future: asyncio.Future
    enqueue_time: float


# Global queue for incoming classification requests
request_queue: asyncio.Queue[QueueItem] = asyncio.Queue()


async def process_batch(
    batch: list[QueueItem],
) -> None:
    """Run inference for a complete microbatch"""

    print(f"Processing batch with {len(batch)} comments")
    print("Running batch inference...")

    comments = [item.comment for item in batch]

    inference_start = monotonic()

    # Classify the batch of comments and get the results
    results = classify_comments_batch(comments)

    inference_duration = monotonic() - inference_start

    # Update Prometheus metrics
    batches_processed_total.inc()
    batch_size_histogram.observe(len(batch))
    batch_inference_duration_seconds.observe(inference_duration)

    # Set the classification results in the corresponding futures for each request in the batch
    for item, result in zip(batch, results, strict=True):
        # Update Metrics queue wait time per request
        wait_time = monotonic() - item.enqueue_time
        batch_wait_time_seconds.observe(wait_time)
        comments_classified_total.inc()
        comments_classified_by_label_total.labels(label=result["label"]).inc()

        # Set the classification result in the future to unblock the request handler
        item.future.set_result(result)


async def batch_worker() -> None:
    """Continuously collect and process microbatches."""

    while True:
        batch: list[QueueItem] = []

        # Wait for the first request indefinitely
        first_item = await request_queue.get()

        # Update Prometheus metric for current queue size
        microbatch_queue_size.set(request_queue.qsize())

        batch.append(first_item)

        batch_start_time = monotonic()

        # Collect additional requests until timeout or batch size limit
        while len(batch) < MAX_BATCH_SIZE:
            elapsed_time = monotonic() - batch_start_time
            remaining_time = BATCH_TIMEOUT_SECONDS - elapsed_time

            # Stop collecting if timeout is reached
            if remaining_time <= 0:
                break

            try:
                item = await asyncio.wait_for(
                    request_queue.get(),
                    timeout=remaining_time,
                )
                batch.append(item)

                # Update Prometheus metric for current queue size
                microbatch_queue_size.set(request_queue.qsize())

            except TimeoutError:
                # Batch window expired
                break

        await process_batch(batch)
