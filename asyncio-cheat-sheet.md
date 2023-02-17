# Asyncio

Asyncio provides coroutine-based concurrency suited to non-blocking socket IO applications

## COROUTINE

### Define a coroutine
```py
async def custom_coroutine():
    ...
```

### Create coroutine object
```
coro = custom_coroutine()
```

### Run coroutine as entry point
```
asyncio.run(main())
```

### Suspend and run coroutine from a coroutine
```py
await custom_coroutine()
```

### Sleep a coroutine
```py
await asyncio.sleep(1)
```

## Async Comprehensions and Loops

### Asynchronous comprehension
```py
res = [a async for a in aiterable]
```

### Await comprehension
```py
res = [r await a in awaitable]
```

### Asynchronous for-loop
```py
async for item in async_gen():
    print(item)
```

## TASK

A Task schedules a coroutine to run independently

### Create and schedule task (high-level)
```py
task = asyncio.create_task(coro)
```

### Create and schedule task (low-level)
```py
task = asyncio.create_future(coro)
```

### Suspend and wait for a task to finish
```
await task
```

### Get the current task
```py
taks = asyncio.current_task()
```

### Get all running tasks
```py
tasks = asyncio.all_tasks()
```

### Get task result
```py
value = task.result()
```

### Get task unhandled exception
```py
ex = task.exception()
```

### Cancel a task result
```py
was_canceled = task.cancel()
```

### Check if the task is done (not running)
```py
if task.done():
    ...
```

### Check if the task is cancelled
```py
if task.cancelled():
    ...
```

### Add done callback function
```py
task.add_done_callback(handler)
```

### Remove done callback function
```py
task.remove_done_callback(handler)
```

### Set and get task name
```py
task.set_name("MyTask")
name = task.get_name()
```

## TASKS

### Wait for awaitable with a timeout
```py
try:
    await asyncio.wait_for(tk, timeout=1)
except:
    asyncio.TimeoutError:
        ...
```

### Shield a task from cancellation
```py
shielded = asyncio.shield(task)
```

### Run blocking function in a new thread
```py
coro = asyncio.to_thread(myfunc)
```

### Run coroutine an asyncio event loop
```py
fut = run_coroutine_threadsafe(coro, loop)
```

### Run many awaitables as a group
```py
await asyncio.gather(c1(), c2())
```

### Wait for all tasks in a collection
```py
done, pending = await asyncio.wait(tasks)
```

### Wait for all tasks with a timeout in seconds
```py
try:
    done, pending = await asyncio.wait(tasks, timeout=5)
except:
    asyncio.TimeoutError:
        ...
```

### Wait for the first task in a collection
```py
done, pending = await asyncio.wait(tasks, return_when=FIRST_COMPLETED)
```

### Wait for the first task to fail
```py
done, pending = await asyncio.wait(tasks, return_when=FIRST_EXCEPTION)
```

### Get results in task completion order
```py
for c in asyncio.as_completed(tasks):
    result = await c
```

