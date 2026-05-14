import asyncio

import httpx


COMMENTS = [
    "Die Politiker erzählen wieder völligen Unsinn.",
    "Das ist endlich mal ein sinnvoller Artikel.",
    "Klar, die Erde ist natürlich flach.",
    "Ich habe den Artikel nicht gelesen, aber bin dagegen.",
    "Warum spricht niemand über das eigentliche Problem?",
    "Das ist reine Panikmache der Medien.",
    "Interessante Analyse, danke dafür.",
    "Dieser Kommentar hat gar nichts mit dem Artikel zu tun.",
]


async def send_comment(
    client: httpx.AsyncClient,
    comment: str,
) -> None:
    """Send a single classification request and print the response"""

    response = await client.post(
        "http://localhost:8000/classify",
        json={"comment": comment},
    )

    print(response.json())


async def main() -> None:
    """Send multiple requests concurrently to test the microbatching implementation"""

    async with httpx.AsyncClient(timeout=60.0) as client:
        tasks = [send_comment(client, comment) for comment in COMMENTS]

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
