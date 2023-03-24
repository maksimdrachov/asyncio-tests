import asyncio

# new running event loop
loop = asyncio.new_event_loop()

# define a coroutine, that takes a parameter
async def my_coroutine(param):
    print(f"my_coroutine() #{param} started!")
    await asyncio.sleep(1)
    print(f"my_coroutine() #{param} ended!")


def my_callback(task):
    print(f"my_callback() called for task {task.get_name()}")
    # print(f"task result: {task.result()}")
    # print(f"task exception: {task.exception()}")
    background_tasks.remove(task)


background_tasks = []

for i in range(10):
    task = loop.create_task(my_coroutine(i))

    # add the task to the list of background tasks
    background_tasks.append(task)

    # To prevent keeping references to finished tasks forever
    task.add_done_callback(my_callback)

loop.run_until_complete(asyncio.gather(*background_tasks))
