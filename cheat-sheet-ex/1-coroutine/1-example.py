import asyncio

# define a coroutine
async def my_coroutine():
    print("Hello")
    await asyncio.sleep(1)
    print("World")


coro = my_coroutine()

# run the coroutine
asyncio.run(coro)
