import asyncio

# define a master coroutine
async def master():
    print("Master coroutine started")
    # Suspend and run coroutine from a master
    await slave()
    print("Master coroutine finished")


# define a slave coroutine
async def slave():
    print("Slave coroutine started")
    # Each coroutine needs an await
    await asyncio.sleep(1)
    print("Slave coroutine finished")


# run the master coroutine
asyncio.run(master())
