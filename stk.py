stack = []

def push(n):
    stack.append(n)
def pop():
    return stack.pop()
def peep():
    return stack[-1]
def is_empty():
    return len(stack) == 0

def push_algorithm(n):
    stack.clear()
    for i in range(n):
        push(i)

def pop_algorithm(n):
    stack.clear()
    for i in range(n):
        push(i)
    for i in range(n):
        pop()

def peep_algorithm(n):
    stack.clear()
    for i in range(n):
        push(i)
    for i in range(n):
        peep()

def isempty_algorithm(n):
    stack.clear()
    for i in range(n):
        is_empty()
