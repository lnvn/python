from perf.execution_time import timer

@timer
def task():
    print("Hello")

task()