import dask
from time import sleep

@dask.delayed
def inc(x):
    sleep(1)
    return x + 1

@dask.delayed
def double(x):
    sleep(1)
    return x + 2

@dask.delayed
def add(x, y):
    sleep(1)
    return x + y

data = [1, 2, 3, 4, 5]

output = []
for x in data:
    a = inc(x)
    b = double(x)
    c = add(a, b)
    output.append(c)

total = dask.delayed(sum)(output)

print(total.compute())

print(total.visualize())