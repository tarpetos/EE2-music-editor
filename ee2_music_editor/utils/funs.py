import asyncio
import os
from collections import abc
from typing import Any, Iterable


async def wait_for_first(*coros: abc.Awaitable[Any] | Iterable[abc.Awaitable[Any]]) -> Any:
    flat_coros = []
    for coro in coros:
        if isinstance(coro, abc.Awaitable):
            flat_coros.append(coro)
        else:
            flat_coros.extend(coro)

    tasks = [asyncio.ensure_future(coro) for coro in flat_coros]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for task in pending:
        task.cancel()

    for task in done:
        return task.result()


def get_desired_thread_number(desired: int | None = None, *, reserved: int = 1) -> int:
    available_threads: int = max(os.cpu_count() - abs(reserved), 1)
    return min(available_threads, desired) if (desired := abs(desired)) else available_threads
