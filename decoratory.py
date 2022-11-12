def benchmark(func):
    def wrapper():
        import time
        start = time.time()
        func()
        finish = time.time()
        print(f'Время выполнения функции {func.__name__}, заняло: {finish - start}')
    return wrapper