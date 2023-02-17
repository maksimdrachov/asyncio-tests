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