import asyncio

from components.worker import MainWorker

async def main() -> None:
    worker = MainWorker()
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())