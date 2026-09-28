import time
import numpy as np
import matplotlib
matplotlib.use('TkAgg') #interactive backend
import matplotlib.pyplot as plt

def time_complexity_visualizer(algorithm, n_min, n_max, n_step):
    times = []
    input_sizes = list(range(n_min, n_max + n_step, n_step))
    plt.ion() #Turn on interactive mode
    fig, ax = plt.subplots()
    ax.set_xlabel('Input Size(n)')
    ax.set_ylabel('Execution Time(seconds)')
    ax.set_title('Algorithm time Complexity visualization (live)')
    line, = ax.plot([], [], 'o-') #Initialize empty line

    for i, n in enumerate(input_sizes):
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)

        line.set_data(input_sizes[:i + 1], times)
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.01)

    plt.ioff()
    plt.savefig("time_complexity.png")
    return "time_complexity.png"

def linear_search(n):
    arr = list(range(n))
    target = n - 1
    for i in range(len(arr)):
        if arr[i] == target:
            return i

def bubble_sort(n):
    arr = list(range(n))
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[i]:
                arr[i], arr[j] = arr[j], arr[i]
    return n

def binary_search(n):  
    n = list(range(n))
    left = 0
    right = len(n) - 1
    target = n - 1
   

    while left <= right:
        middle = int(left + right / 2)
        if target == n[middle]:
            return middle
        elif target > n[middle]:
            left = middle + 1
        else:
            right = middle - 1
    return -1
def nested_loop(n):
    arr = list(range(n))
    ans = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            for k in range(i + 2, len(arr)):
                if arr[i] + arr[j] - arr[k] == -1:
                    ans.append((i, j, k))
    return ans

def two_pointer(n):
    n = list(range(n))
    target = 13
    arr = sorted(n)
    left = 0
    right = len(arr) - 1
    while left < right:
        total = arr[left] - arr[right]
        if total == target:
            return True
        elif total < target:
            left += 1
        else:
            right -= 1
    return False

def unique_users(n):
    users = []
    for k in range(n):
        users.append({'id': k})
    seen = set()

    for user in users:
        if user['id'] not in seen:
            seen.add(user['id'])
        return seen
        
