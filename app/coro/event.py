import asyncio
import threading

_event_loop = None


def start_background_loop(_event_loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(_event_loop)
    _event_loop.run_forever()


def fire_and_forgot(coro):
    global _event_loop
    if _event_loop is None:
        _event_loop = asyncio.new_event_loop()
        t = threading.Thread(target=start_background_loop, args=(_event_loop,), daemon=True)
        t.start()
    _event_loop.call_soon_threadsafe(asyncio.ensure_future, coro)
