queue = []

def enqueue(n):
    queue.append(n)
def dequeue():
    return queue.pop(0)
def peek():
    return queue[0]
def queis_empty():
    return len(queue) == 0

def enqueue_algorithm(n):
    queue.clear()
    for i in range(n):
        enqueue(i)
def dequeue_algorithm(n):
    queue.clear()
    for i in range(n):
        enqueue(i)
    for i in range(n):
        dequeue()
def peek_algorithm(n):
    queue.clear()
    for i in range(n):
        enqueue(i)
    for i in range(n):
        peek()
def queis_empty_algorithm(n):
    queue.clear()
    for i in range(n):
        queis_empty()
