[Source](https://devopedia.org/asynchronous-programming-in-python)

Asynchronous programming is a programming paradigm that enables better concurrency, that is, multiple threads running concurrently. In Python, `asyncio` module provides this capability. Multiple tasks can run concurrently on a single thread, which is scheduled on a single CPU core.

In Python's asynchronous programming, scheduling is done by what's called the event loop. Developers specify in their code when a task voluntarily gives up the CPU so that the event loop can schedule some other task. For this reason this is also called cooperative multitasking.

Anatomy of an async method

```py
# Begin by making method async
async def process_data(num: int, data: asyncio.Queue):
    processed = 0

    while processed < num:
        item = await data.get() # await all async methods you call
        # work with item
```

Executing asynchronous code requires an event loop. Python provides a default event loop implementation. It's also possible to use alternative implementations such as `uvloop`, which has shown at least 2x better performance.

The event loop executes coroutines, one at a time. A coroutine is simply a method or function defined with `async` keyword. A coroutine needs to be added to the event loop, such as uing `asyncio.run()`.

When a coroutine waits for the result of another coroutine using the `await` keyword, it gets suspended. The event loop then schedules another coroutine that is ready to run. More formally, a coroutine waits for an awaitable object. This can be another coroutine, a Task or a Future.

A Task is really a wrapper on a coroutine typically created with `asyncio.create_task()`. Via the Task, the coroutine is automatically scheduled.

A Future is a low-level object that represents the eventual result of an asynchronous operation. When a future is awaited, it means the coroutine will wait until the Future is resolved in some other place.

What are some basic API calls worth knowing for a beginner?

We can create multiple event loops in a thread but only one can be active at a time.
Relevant APIs:
- `asyncio.new_event_loop()`
- `asyncio.set_event_loop()`
- `asyncio.get_event_loop()`
- `asyncio.get_running_loop()`

If `asyncio.get_event_loop()` is called without a prior call to `asyncio.set_event_loop()`, a new event loop is automatically created and set as the current one.

Event loop methods include:
- `run_until_complete()`
- `run_forever()`
- `is_running()`
- `is_closed()`
- `stop()`
- `close()`
- `create_task()`/`asyncio.create_task()`

Callbacks can be scheduled with:
- `call_soon()`
- `call_soon_threadsafe()`
- `call_later()`
- `call_at()`

Loops also include methods to manage connections and entities:
- `create_connection()`
- `create_datagram_endpoint()`
- `create_server()`
- `sendfile()`
- `start_tls()`
- plus low-level methods to work directly with sockets.

`asyncio.run()` runs a coroutine, in the process creating an event loop and closing it at the end. This can't be called if an event loop is already running in the current thread. To run many tasks concurrently, call `asyncio.gather()`. Other useful methods include `asyncio.wait()`, `asyncio.wait_for()`, `asyncio.current_task()` and `asyncio.all_tasks()`. To sleep asynchronously, use `asyncio.sleep()` rather than `time.sleep()`.

What are some essential tips when working with asynchronous Python code?

An event loop can run in any thread but it must run in the main thread if it has to handle signals and execute subprocesses.

To schedule callbacks from another thread, use:
- `loop.call_soon_threadsafe()` rather than `loop.call_soon()`

Note that calling a coroutine function doesn't actually execute the function and return the result.