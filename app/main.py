import signal
from aiohttp import ClientSession
from asyncio import PriorityQueue, Event
from asyncio import get_event_loop, gather
from logging import getLogger

from .reader import reader
from .settings import Settings
from .worker import worker


def main(settings: Settings, logger=getLogger('runner.main')):
    """Prepares environment and start."""

    loop = get_event_loop()
    queue = PriorityQueue(settings.queue_size)
    quit_event = Event()
    session = ClientSession()

    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, loop.stop)

    logger.info('Starting runner...')

    reader_task = loop.create_task(reader(queue, quit_event))
    workers_tasks = [loop.create_task(worker(str(wid), queue, quit_event, session)) for wid in range(settings.workers)]

    loop.run_forever()

    logger.info('Stopping work...')

    quit_event.set()

    loop.run_until_complete(reader_task)
    loop.run_until_complete(gather(*workers_tasks))
    loop.run_until_complete(session.close())

    logger.info('Finished. Bye!')
