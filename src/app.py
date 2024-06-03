import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from components.worker import Worker
from config import STARTUP_PARAMS


async def main() -> None:
    worker = Worker()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(worker.run, 'cron', **STARTUP_PARAMS)
    scheduler.start()
    print("waiting to: ", STARTUP_PARAMS)

    try:
        while True:
            await asyncio.sleep(3600)  # Keep the loop running
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    asyncio.run(main())
