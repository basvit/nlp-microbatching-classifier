from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram


# Total number of classified comments
comments_classified_total = Counter(
    "comments_classified_total",
    "Total number of classified comments",
)

# Total number of processed microbatches
batches_processed_total = Counter(
    "batches_processed_total",
    "Total number of processed microbatches",
)

# Distribution of batch sizes
batch_size_histogram = Histogram(
    "batch_size",
    "Distribution of processed batch sizes",
    buckets=(1, 2, 4, 8, 16),
)

# Batch inference duration
batch_inference_duration_seconds = Histogram(
    "batch_inference_duration_seconds",
    "Batch inference duration in seconds",
)

# Time spent waiting inside the queue
batch_wait_time_seconds = Histogram(
    "batch_wait_time_seconds",
    "Time a comment waited in the microbatch queue",
)

# Current queue size
microbatch_queue_size = Gauge(
    "microbatch_queue_size",
    "Current microbatch queue size",
)

# Classified comments grouped by predicted label
comments_classified_by_label_total = Counter(
    "comments_classified_by_label_total",
    "Total classified comments by label",
    ["label"],
)
