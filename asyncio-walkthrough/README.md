
Wiki: Thread safety

Thread safety is a computer programming concept applicable to multi-threaded code. Thread-safe code only manipulates shared data structures in a manner that ensures that all threads behave properly and fulfill their design specifications without unintended interactions. There are various strategies for making thread-safe data structures.

A program may execute code in several threads simultanously in a shared address space where each of those threads has access to virtually of the memory of every other thread. Thread safety is a property that allows code to run in multithreaded environments by re-establishing some of the correspondence between the actual flow of control and the text of the program, by means of synchronization. 

Wiki: Multiprocessing

Multiprocessing is the use of two or more central processing units (CPU) within a single computer system. The term also refers to the ability of a system to support more than one processor or the ability to allocate tasks between them.

Wiki: Multithreading

Multithreading is the ability of a central processing unit (CPU) to provide multiple threads of execution concurrently, supported by the operating system. This approach differs from multiprocessing. In a multithreaded application, the threads share the resources of a single of multiple cores, which include the computing units, the CPU caches, and the translation lookaside buffer (TLB).


## Speed Up Your Python Program With Concurrency

[Source](https://realpython.com/python-concurrency/)


## Async IO in Python: A Complete Walkthrough

[Source](https://realpython.com/async-io-python/)

Threading is a concurrent execution model whereby multiple threads can take turns executing tasks. One process can contain multiple threads. Python has a complicated relationship with threading thanks to its GIL, but that's beyond scope.

What's important to know about threading is that it's better for IO-bound tasks. While a CPU-bound task is characterized by the computer's cores continually working hard from start to finish, an IO-bound job is dominated by a lot of waiting on input/output to complete.

To recap the above, concurrency encompasses both multiprocessing (ideal for CPU-bound tasks) and threading (suited for IO-bound tasks). Multiprocessing is a form of parallelism, with parallelism being a specific type (subset) of concurrency.

Now it's time to bring a new member to the mix. Over the last few years, a separate design has been more comprehensively built into CPython: asynchronous IO, enabled through the standard library's asyncio package and the new `async` and `await` language keywords. To be clear, async IO is not a newly invented concept, and it has existed or is being built into other languages and runtime environments, such as Go, C#, or Scala.

The `asyncio` package is billed by the Python documentation as a library to write concurrent code. However, async IO is not threading, nor is it multiprocessing. It is not built on top of either of these.

In face, async IO is a single-threaded, single-process design: it uses cooperative multitasking, a term that you'll flesh out by the end of this tutorial. Coroutines (a central feature of async IO) can be scheduled concurrently, but they are not inherently concurrent.

That leaves one more term. What does it mean for something to be asynchronous? This isn't a rigorous definition, but for our purposes here, I can think of two properties:

- Asynchronous routines are able to pause while waiting on their ultimate result and let other routines run in the meantime.
- Asynchronous code, through the mechanism above, facilitates concurrent execution. To put it differently, asynchronous code gives the look and feel of concurrency.

Async IO takes long waiting periods in which functions would otherwise be blocking and allows other functions to run during that downtime. (A function that blocks effectively forbids others from running from the time that it starts until the time that it returns.)

At the heart of async IO are coroutines. A coroutine is a specialized version of a Python generator function. Let's start with a baseline definition and then build off of it as you progress here: a coroutine is a function that can suspend its execution before reaching `return`, and it can indirectly pass control to another coroutine for some time.

The order of this output is the heart of async IO. Talking to each of the calls to `count()` is a single event loop, or coordinator. When each task reaches `await asyncio.sleep(1)`, the function yells up to the event loop and gives control back to it, saying, "I'm going to be sleeping for 1 second. Go ahead and let something else meaningful be done in the meantime."

At this point, a more formal definition of `async`, `await`, and the coroutine functions that they create are in order. 

- The syntax `async def` introduces either a native coroutine or an asynchronous generator.
- The keyword `await` passes function control back to the event loop. (It suspends the execution of the surrounding coroutine.) If Python encounters an `await f()` expression in the scope of `g()`, this is how `await` tells the event loop, "Suspend execution of `g()` until whatever I'm waiting on -- the result of f() -- is returned. In the meantime, go let something else run."

There's also a strict set of rules around when and how you can and cannot use async/await. These can be handy whether you are still picking up the syntax or already have exposure to using `async`/`await`:

- A function that you introduce with `async def` is a coroutine. It may use `await`, `return`, or `yield`, but all of these are optional. Declaring `async def noop(): pass` is valid:
  - Using `await` and/or `return` creates a coroutine function. To call a coroutine function, you must `await` it to get its results.
  - It is less common to use `yield` in an `async def` block. This creates an asynchronous generator, which you can iterate over with `async for`. Forget about async generators for the time being and focus on getting down the syntax for coroutine functions, which use `await` and/or `return`.
  - Anything defined with `async def` may not use `yield from`, which will raise a SyntaxError.
- Just like it's a SyntaxError to use yield outside of a def function, it is a SyntaxError to use `await` outside of an async def coroutine. You can only use `await` in the body of coroutines.

This program uses one main coroutine, `makerandom()`, and runs it concurrently across 3 different inputs. Most programs will contain small, modular coroutines and one wrapper function that server to chain each of the smaller routines together. `main()` is then used to gather tasks (futures) by mapping the central coroutine across some iterable of pool.

In this miniature example, the pool is range(3). In a fuller example presented later, it is a set of URLs that need to be requested, parsed, and processed concurrently, and `main()` encapsulates that entire routine for each URL.

Async IO Design Patterns

Async IO comes with its own set of possible script designs, which you'll get introduced to in this section.

Chaining coroutines

A key feature of coroutines is that they can be chained together. (Remember, a coroutine object is awaitable, so another coroutine can `await` it.) This allows you to break programs into smaller, manageable, recyclable coroutines:

Using a Queue

The `asyncio` package provides queue classes that are designed to be similar to classes of the queue module. In our examples so far, we haven't really had a need for a queue structure. In `chained.py`, each task (future) is composed of a set of coroutines that explicitly await each other and pass through a single input per chain.

There is an alternative structure that can also work with async IO: a number of producers, which are not associated with each other, add items to a queue. Each producer may add multiple items to the queue at staggered, random, unannounced times. A group of consumers pulls items from the queue as they show up, greedily and without waiting for any other signal.

In this design, there is no chaining of any individual consumers to a producer. The consumers don't know the number of producers, or even the cumulative number of items that will be added to the queue, in advance.

It takes an individual producer or consumer a variable amount of time to put and extract items from the queue respectively. The queue serves as a throughput that can communicate with the producers and consumers without them talking to each other directly.

Other Top-Level asyncio Functions

In addition to `asyncio.run()`, you've seen a few other package-level functions such as `asyncio.create_task()` and `asyncio.gather()`. 

You can use `create_task()` to schedule the execution of a coroutine object, followed by `asyncio.run()`

There's a subtlety to this pattern: if you don't `await t` within `main()`, it may finish before `main()` itself signals that is is complete. Because `asyncio.run(main())` calls `loop.run_until_complete(main())`, the event loop is only concerned (without `await t` present) that `main()` is done, not that the tasks that get created within `main()` are done. Without `await t`, the loop's other tasks will be cancelled, possibly before they are completed. If you need to get a list of currently pending tasks, you can use `asyncio.Task.all_tasks()`.

Seperately, there's `asyncio.gather()`. While it doesn't do anything tremendously special, `gather()` is meant to neatly put a collection of coroutines (futures) into a single future. As a result, it returns a single future object, and, if you `await asyncio.gather()` and specify multiple tasks or coroutines, you're waiting for all of them to be completed. (This somewhat parallels `queue.join()` from our earlier example.) The result of `gather()` will be a list of the results across the inputs.

You probably noticed that `gather()` waits on the entire result set of the Futures or coroutines that you pass it. Alternatively, you can loop over `asyncio.as_completed()` to get tasks as they are completed, in the order of completion. The function returns an iterator that yields tasks as they finish. Below, the result of `coro([3, 2, 1])` will be available before `coro([10, 5, 0])` is complete, which is not the case with `gather()`: