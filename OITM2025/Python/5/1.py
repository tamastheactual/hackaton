import sys, time, threading, multiprocessing as mp, gc, math

def square(x): 
    return x * x

def bench_map_vs_list(n=2_000_00):
    t0 = time.perf_counter()
    list(map(square, range(n)))
    t1 = time.perf_counter()
    [square(x) for x in range(n)]
    t2 = time.perf_counter()
    return t1 - t0, t2 - t1

map_t, list_t = bench_map_vs_list()
print(f"map() time:             {map_t:.4f}s")
print(f"list comprehension time:{list_t:.4f}s\n")

N = 50_0000

def cpu_task():
    s = 0
    for i in range(1, N):
        s += math.sqrt(i)
    return s

def run_threads(k=4):
    threads = []
    for _ in range(k):
        t = threading.Thread(target=cpu_task)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def run_processes(k=4):
    procs = []
    for _ in range(k):
        p = mp.Process(target=cpu_task)
        procs.append(p)
        p.start()
    for p in procs:
        p.join()

print("CPU‑bound test (4 workers)")
t0 = time.perf_counter()
run_threads()
t1 = time.perf_counter()
run_processes()
t2 = time.perf_counter()
print(f"Threads:    {t1 - t0:.4f}s")
print(f"Processes:  {t2 - t1:.4f}s\n")

import os, psutil
proc = psutil.Process()

def rss_mb():
    return proc.memory_info().rss / (1024 * 1024)

big = [0] * 5_000_000
print(f"RSS before del: {rss_mb():.1f} MB")
del big
gc.collect()
print(f"RSS after del+gc: {rss_mb():.1f} MB")
