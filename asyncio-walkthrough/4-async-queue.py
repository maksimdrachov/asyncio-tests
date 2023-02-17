import asyncio
import itertools as it
import os
import random
import time


async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()


async def rand_sleep(caller=None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f"{caller} sleeping for {i} seconds")
    await asyncio.sleep(i)


async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):  # Synchronous loop for each single producer
        await rand_sleep(caller=f"Producer {name}")
        item = await makeitem()
        t = time.perf_counter()
        await q.put((item, t))  # Put item into queue
        print(f"Producer {name} added {item} to queue")


async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await rand_sleep(caller=f"Consumer {name}")
        item, t = await q.get()  # Get item from queue
        now = time.perf_counter()
        print(f"Consumer {name} got {item} in {now - t:0.5f} seconds")
        q.task_done()  # Mark task as done


async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(i, q)) for i in range(nprod)]
    consumers = [asyncio.create_task(consume(i, q)) for i in range(ncon)]
    await asyncio.gather(*producers)
    await q.join()  # Wait until all items in queue are processed
    for c in consumers:
        c.cancel()  # Cancel consumers


if __name__ == "__main__":
    import argparse

    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--nprod", type=int, default=5)
    parser.add_argument("-c", "--ncon", type=int, default=10)
    ns = parser.parse_args()
    start = time.perf_counter()
    asyncio.run(main(ns.nprod, ns.ncon))
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
