[Source](https://realpython.com/python-concurrency/)

threading = pre-emptive multitasking
asyncio = cooperative multitasking

With multiprocessing, Python creates new processes. A process here can be thought of as almost a completely different program, though technically they're usually defined as a collection of resources where the resources include memory, file handles and things like that. One way to think about it is that each process runs in its own Python interpreter.

When is concurrency useful?

Concurrency can make a big difference for two types of problems. These are generally called CPU-bound and I/O-bound.

Asyncio Version

asyncio Basics

The general concept of asyncio is that a single Python object, called the event loop, controls how and when each task gets run. The event loop is aware of each task and knows what state it's in. In reality, there are many states that tasks could be in, but for now let's imagine a simplified event loop that just has two states.

The ready state will indicate that a task has work to do and is ready to be run, and the waiting state means that the task is waiting for some external thing to finish, such as a network operation.

Your simplified event loop maintains two lists of tasks, one for each these states. It selects one of the ready tasks and starts it back to running. That task is in complete control until it cooperatively hands the control back to the event loop.

When the running task gives control back to the event loop, the event loop places that task into either the ready of waiting list and then goes through each of the tasks in the waiting list to see if it has become ready by an IO operation completing. It knows that the tasks in the ready list are still ready because they haven't run yet.

An important point of asyncio is that the tasks never give up control without intentionally doing so. They never get interrupted in the middle of an operation. This allows us to share resources a bit more easily in asyncio than in threading. You don't have to worry about making your code thread-safe.

### Stackoverflow

[Source](https://stackoverflow.com/questions/49005651/how-does-asyncio-actually-work/51116910#51116910)

#### Generators

Generators are objects that allow us to suspend the execution of a python function. User curated generators are implemented using the keyword yield. By creating a normal function containing the yield keyword, we turn that function into a generator:

```py
>>> def test():
...     yield 1
...     yield 2
...
>>> gen = test()
>>> next(gen)
1
>>> next(gen)
2
>>> next(gen)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

#### Communicating with a generator

A less-known feature of generators is the fact that you can communicate with them using two methods: send() and throw().

```py
>>> def test():
...     val = yield 1
...     print(val)
...     yield 2
...     yield 3
...
>>> gen = test()
>>> next(gen)
1
>>> gen.send("abc")
abc
2
>>> gen.throw(Exception())
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 4, in test
Exception
```

Upon calling gen.send(), the value is passed a a return value from the yield keyword.

Coroutines are functions that can be stopped and resumed while being run. In Python, they are defined using the async def keyword. Much like generators, they too use their own form of yield from which is await.

Futures are objects that have the __await()__ method implemented, and their job is to hold a certain state and result. The state can be one of the following:

1. PENDING - future does not have any result or exception set.
2. CANCELLED - future was cancelled using fut.cancel()
3. FINISHED - future was finished, either by a result set using fut.set_result() or by an exception set using fut.set_exception()

The result can either be a Python object, that will be returned, or an exception which may be raised.

Another important feature of future objects, is that they contain a method called add_done_callback(). This method allows function to be called as soon as the task is done - whether it raised an exception or finished.

Tasks

Tasks objects are special futures, which wrap around coroutines, and communicate with the inner-most and outer-most coroutines. Every time a coroutine await's a future, the future is passed all the way back to the task (just like in yield from), and the task receives it.

Next, the task binds itself to the future. It does so by calling add_done_callback() on the future. From now on, if the future will ever be done, by either being cancelled, passed an exception or passed a Python object as a result, the task's callback will be called, and it will rise back up to existence.

### Back to real python

async and await

Now let's talk about two new keywords that were added to Python: async and await. In light of the discussing above, you can view await as the magic that allows the task to hand control back to the event loop. When you code awaits a function call, it's a signal to that the call is likely to be something that takes a while and that the task should give up control.

It's easiest to think of async as a flag to Python telling it that the function about to be defined uses await. There are some cases where this is not strictly true, like asynchronous generators, but it holds for many cases and gives you a simple mode while you're getting started.

The Problems with the asyncio version

There are a couple of issues with asyncio at this point. You need special async version of libraries to gain the full advantage of asyncio. Had you just used requests for downloading the sitess, it would have been much slower because requests is not designed to notify the event loop that it's blocked. This issues is getting smaller and smaller as time goes on and more libraries embrace asyncio.

Another, more subtle, issues is that all of the advantages of cooperative multitasking get thrown away if one of the tasks doesn't cooperate. A minor mistake in code can cause a task to run off and hold the processor for a long time, starving other tasks that need running. There is no way for the event loop to break in if a task does not hand control back to it.

### Developing with asyncio

[Source](https://docs.python.org/3/library/asyncio-dev.html)

To enable asyncio debug mode:

- Set PYTHONASYNCIODEBUG environment variable to 1.

    export PYTHONASYNCIODEBUG=1

When the debug mode is enabled:

- asyncio checks for coroutines that were not awaited and logs them; this mitigates the forgotten await pitfall.
- Many non-threadsafe asyncio APIs (such as loop.call_soon() and loop.call_at() methods) raise an exception if they are called from a wrong thread.
- The execution time of the IO selector is logged if it takes too long to perform an IO operation
- Callbacks lasting longer than 100 milliseconds are logged. The loop.slow_callback_duration attribute can be used to set the minimum execution duration in seconds that is considered slow.

Concurrency and Multithreading

An event loop runs in a thread (typically the main thread) and executes all callbacks and Tasks in its thread. While a Task is running in the event loop, no other Tasks can run in the same thread. When a Task executes an await expression, the running Task gets suspended, and the event loop executes the next Task.

To schedule a callback from another OS thread, the loop.call_soon_threadsafe() method should be used.

To schedule a coroutine objecct from a different OS thread, the run_coroutine_threadsafe() function should be used. It returns a concurrent.futures.Future to access the result:

```py
async def coro_func():
    return await asyncio.sleep(1, 42)

# Later in another OS thread:

future = asyncio.run_coroutine_threadsafe(coro_func(), loop)
# Wait for the result:
result = future.result()
```

To handle signals and to execute subprocesses, the event loop must be run in the main thread.

There is currently no way to schedule coroutines or callbacks directly from another process (such as one started with multiprocessing). The Event Loop Methods section lists APIs that can read from pipes and watch file descriptors without blocking the event loop. In addition, asyncio's Subprocess API provide a way to start a process and communicate with it from the event loop.

### Difference between coroutine and future/task

#### COROUTINES

Coroutines declared with the async/await syntax is the preferred way of writing asyncio applications. For example, the following snippet of code print "hello", waits 1 second, and then prints "world".

To actually run a coroutine, asyncio provides the following mechanisms:

- The asyncio.run() function to run the top-level entry point main() function
- Awaiting on a coroutine. The following snippet of code will print "hello" after waiting for 1 second, and then print "world" after waiting for another 2 seconds.
- The asyncio.create_task() function to run coroutines concurrently as asyncio Tasks.
- (New in version 3.11) The asyncio.TaskGroup class provides a more modern alternative to create_task()

#### AWAITABLES

We say that an object is an awaitable object if it can be used in an await expression. Many asyncio APIs are designed to accept awaitables.

There are three main types of awaitables objects: coroutines, Tasks and Futures.

Coroutines

Python coroutines are awaitables and therefor can be awaited from other coroutines:

```py
import asyncio

async def nested():
    return 42

async def main():
    # Nothing happens if we just call "nested()".
    # A coroutine object is created but not awaited,
    # so it *won't run at all*.
    nested()

    # Let's do it differently now and await it:
    print(await nested())  # will print "42".

asyncio.run(main())
```

Important: in this documentation the term coroutine can be used for two closely related concepts:
- a coroutine function: an async def function
- a coroutine object: an object returned by calling a coroutine function

Tasks

Tasks are used to schedule coroutines concurrently.

When a coroutine is wrapped into a Task with function like asyncio.create_task() the coroutine is automatically scheduled to run soon:

```py
import asyncio

async def nested():
    return 42

async def main():
    # Schedule nested() to run soon concurrently
    # with "main()".
    task = asyncio.create_task(nested())

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await task

asyncio.run(main())
```

