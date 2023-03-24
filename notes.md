Next steps:

- read/study [python-concurrency](https://realpython.com/python-concurrency/)
- implement simple queue example
  - 1 producer
  - 1 consumer
- study how execution model in pycyphal currently works
  - why thread? -> input, UDP
    - is it used anywhere else?
    - i thought it was supposed to be all tasks/coroutines?
  - is the task getting cancelled (see [asyncio-walkthrough](https://realpython.com/async-io-python/))
- try to implement my own small version of what is needed for pycyphal
  - multicast sockets passing data between each other
  - using queue
- compare current implementation to my small example
- how to debug asyncio

---

- Is there any reason why we are using `threading` (pre-emptive multitasking) in input session, while everything else is based on `asyncio` (cooperative multitasking)?
- Argument 2: if the argument is that reader thread is required to always be active, then threading does not provide this? It is concurrency, not parallelism.

- Debugging-related
  - It works if done without loop.call_soon_threadsafe
    - checked with unit test
  - All packets are sent in both cases
    - checked with wireshark
  - The issue seems to be that the task passed to call_soon_threadsafe never gets executed.