from performance import measure_time

@measure_time
def slow_function():
    # Simula um processo lento
    for i in range(1000000):
        pass

slow_function()  # Saída: Elapsed time: 0.0675s
