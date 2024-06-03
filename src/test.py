import asyncio

from components.worker import Worker


async def main() -> None:
    worker = Worker()
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
