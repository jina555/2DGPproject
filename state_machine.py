class State:
    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        pass
    def handle_event(self,e):
        pass

class StateMachine:
    def __init__(self,start_state,transitions):
        self.current=None
        self.transitions=transitions
        self.set_state(start_state,e=None)

    def set_state(self,next_state,e):
        if self.current is not None:
            try:
                self.current.exit(e)
            except:
                pass
        self.current=next_state
        if self.current is not None:
            try:
                self.current.enter(e)
            except:
                pass
    def handle_state_event(self,e):
        if self.current is None:
            return False

        table=self.transitions.get(self.current,{})
        for cond_fn,next_state in table.items():
            try:
                if cond_fn(e):
                    try:
                        self.current.exit(e)
                    finally:
                        self.current=next_state
                        try:
                            self.current.enter(e)
                        finally:
                            return True
            except:
                continue
        try:
            self.current.handle_event(e)
        except:
            pass
        return False

    def update(self):
        if self.current is not None:
            try:
                self.current.do()
            except:
                pass

    def draw(self):
        if self.current is not None:
            try:
                self.current.draw()
            except:
                pass