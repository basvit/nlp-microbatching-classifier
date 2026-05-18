import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_client import make_asgi_app

from app.microbatch import batch_worker
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start background workers during application startup"""

    # Start the batch worker in the background
    worker_task = asyncio.create_task(batch_worker())

    yield

    # Cancel the batch worker on shutdown
    worker_task.cancel()


metrics_app = make_asgi_app()

app = FastAPI(
    title="NLP Microbatch Classifier",
    lifespan=lifespan,
)

app.mount("/metrics", metrics_app)

app.include_router(router)
