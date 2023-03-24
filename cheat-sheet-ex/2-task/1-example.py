import asyncio

# new running event loop
loop = asyncio.new_event_loop()

# define a coroutine
async def my_coroutine():
    print("Hello")
    await asyncio.sleep(1)
    print("World")


# create a coroutine object
coro = my_coroutine()

# create and schedule a task
task = loop.create_task(coro)

# Set task name
task.set_name("My first task")

# add done callback
def done_callback(task):
    print("Task done:", task)


task.add_done_callback(done_callback)

# get current task
print("Current task:", asyncio.current_task(loop=loop))

# run the task
loop.run_until_complete(task)
