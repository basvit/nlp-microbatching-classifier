import asyncio
from time import monotonic

from fastapi import APIRouter

from app.metrics import microbatch_queue_size
from app.microbatch import QueueItem, request_queue
from app.models import (
    ClassificationRequest,
    ClassificationResponse,
)

router = APIRouter()


@router.post(
    "/classify",
    response_model=ClassificationResponse,
)
async def classify(
    request: ClassificationRequest,
) -> ClassificationResponse:
    """Queue a comment for microbatch classification"""

    # Create a future that will be set with the classification result
    future: asyncio.Future = asyncio.get_running_loop().create_future()

    # Create a queue item with the comment and future, and enqueue it
    queue_item = QueueItem(
        comment=request.comment,
        future=future,
        enqueue_time=monotonic(),
    )

    print(f"Received comment: {request.comment}")

    # Put the queue item into the global request queue for processing by the batch worker
    await request_queue.put(queue_item)

    # Update Prometheus metric for current queue size
    microbatch_queue_size.set(request_queue.qsize())

    # Wait for the batch worker to process the batch and set the result in the future
    result = await future

    return ClassificationResponse(**result)
