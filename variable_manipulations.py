import math
import random
import string
import asyncio

first_value = -math.pi
second_value = -math.pi


async def calculate_sin(var_ref):
    global first_value
    await var_ref.set_value(math.sin(first_value))
    first_value += 0.1
    if first_value > math.pi:
        first_value = -math.pi


async def calculate_cos(var_ref):
    global second_value
    await var_ref.set_value(math.cos(second_value))
    second_value += 0.1
    if second_value > math.pi:
        second_value = -math.pi


async def increaser(var_ref, step):
    await var_ref.set_value(await var_ref.get_value() + step)


async def text_generator(var_ref, length=16):
    await var_ref.set_value(''.join(random.choice(string.ascii_lowercase) for i in range(length)))


async def update_vars(vars_ref):
    while True:
        await calculate_sin(vars_ref[0])
        await increaser(vars_ref[1], 1)
        await increaser(vars_ref[2], -1)
        await text_generator(vars_ref[3])
        await calculate_cos(vars_ref[4])
        await calculate_sin(vars_ref[5])
        await increaser(vars_ref[6], 5)
        await increaser(vars_ref[7], -0.1)
        await calculate_cos(vars_ref[8])
        await text_generator(vars_ref[9], 20)
        await increaser(vars_ref[10], 2)
        await asyncio.sleep(1)
