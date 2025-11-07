stack=None
running=True

def run(start_mode):
    global running,stack
    running=True
    stack=[start_mode]
    start_mode.init()

    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

    while len(stack)>0:
        stack[-1].finish()
        stack.pop()

def change_mode(mode):
    global stack
    if len(stack)>0:
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.init()

def push_mode(mode):
    global stack
    if len(stack)>0:
        stack[-1].pause()
    stack.append(mode)
    mode.init()

def pop_mode():
    global stack
    if len(stack)>0:
        stack[-1].finish()
        stack.pop()
    if len(stack)>0:
        stack[-1].resume()

def quit():
    global running
    running=False