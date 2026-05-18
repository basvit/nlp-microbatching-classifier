import asyncio
import random

import httpx

CLASSIFIER_URL = "http://localhost:8000/classify"

COMMENTS = [
    "Die Politiker erzählen wieder völligen Unsinn.",
    "Das ist endlich mal ein sinnvoller Artikel.",
    "Klar, die Erde ist natürlich flach.",
    "Ich habe den Artikel nicht gelesen, aber bin dagegen.",
    "Warum spricht niemand über das eigentliche Problem?",
    "Das ist reine Panikmache der Medien.",
    "Interessante Analyse, danke dafür.",
    "Dieser Kommentar hat gar nichts mit dem Artikel zu tun.",
    "Das ist doch wieder typisch für diese Regierung.",
    "Endlich spricht jemand die Wahrheit aus.",
    "Ich glaube kein Wort von diesem Artikel.",
    "Gute Einordnung, das war hilfreich.",
    "Was hat das mit dem Thema zu tun?",
    "Die Medien verschweigen wie immer die Wahrheit.",
    "Das ist sehr sachlich erklärt.",
    "Ironisch, dass genau diese Leute jetzt empört sind.",
]


async def send_comment(
    client: httpx.AsyncClient,
    comment: str,
) -> None:
    """Send one comment to the classifier service."""

    try:
        # Send the comment to the classifier endpoint and wait for the response
        response = await client.post(
            CLASSIFIER_URL,
            json={"comment": comment},
        )

        response.raise_for_status()

    except httpx.HTTPError as error:
        print(f"Request failed: {error}")


async def send_wave(
    client: httpx.AsyncClient,
    wave_size: int,
) -> None:
    """Send a wave of concurrent classification requests."""

    # Create a list of tasks to send comments concurrently
    tasks = [
        send_comment(
            client,
            random.choice(COMMENTS),
        )
        for _ in range(wave_size)
    ]

    # Wait for all tasks in the wave to complete
    await asyncio.gather(*tasks)


async def main() -> None:
    """Continuously generate variable load for Grafana metrics."""

    # Use a single HTTP client for all requests to benefit from connection pooling
    async with httpx.AsyncClient(timeout=120.0) as client:
        while True:
            wave_size = random.choice([1, 2, 3, 4, 6, 8, 12, 16])

            print(f"Sending wave with {wave_size} comments")

            await send_wave(
                client,
                wave_size,
            )

            # Sleep for a random interval between waves to create variable load
            await asyncio.sleep(
                random.uniform(0.5, 3.0),
            )


if __name__ == "__main__":
    asyncio.run(main())
