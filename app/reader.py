from asyncio import CancelledError
from asyncio import Queue, QueueFull, Event
from asyncio import sleep
from logging import getLogger
from random import choice
from string import ascii_uppercase


async def reader(queue: Queue, quit_event: Event, logger=getLogger('runner.reader')):
    """Gets new data and pass to queue."""

    logger.info("Starting...")

    try:
        while True:
            if quit_event.is_set():
                logger.info("Finishing work...")
                return

            data = choice(ascii_uppercase)
            logger.info("Putting work `%s` to queue", data)

            try:
                queue.put_nowait(data)
            except QueueFull:
                await sleep(0.1)

    except CancelledError:
        logger.info("Cancelled!!!")
