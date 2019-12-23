from aiohttp import ClientSession
from asyncio import CancelledError
from asyncio import Queue, Event
from logging import getLogger


async def worker(wid: str, queue: Queue, quit_event: Event, session: ClientSession,
                 logger=getLogger('runner.worker')):
    """Gets new data from queue and push to queue."""

    logger.debug("Starting worker `%s`...", wid)

    while True:
        try:
            if quit_event.is_set():
                logger.info("`%s` goes down...", wid)
                return

            data = await queue.get()
            logger.info("`%s` takes work `%s`...", wid, data)
            await work(data, session)

        except CancelledError:
            logger.info("`%s` is cancelled!", wid)
            return


async def work(data, session: ClientSession):
    """Do real work"""

    try:
        data = await session.get("http://localhost/")
        # print("Result:", data)
    except Exception:
        logger.exception("Somethings goes wrong in worker `%s`", wid)
