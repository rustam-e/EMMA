import asyncio
import rx
from rx import operators as ops

class StateManager:
    def __init__(self, initial_state):
        self.state = initial_state
        self.state_subject = rx.subject.Subject()
        self.update_queue = asyncio.Queue()
        self.on_change_callbacks = []

    def get_state(self):
        return self.state

    def update_state(self, update_fn):
        self.update_queue.put_nowait(update_fn)

    def on_change(self, callback):
        self.on_change_callbacks.append(callback)

    async def run(self):
        while True:
            update_fn = await self.update_queue.get()
            new_state = update_fn(self.state)
            self.state = new_state
            self.state_subject.on_next(new_state)
            for callback in self.on_change_callbacks:
                callback(new_state)
            self.update_queue.task_done()

    def subscribe(self, observer):
        return self.state_subject.subscribe(observer)

# Example usage
async def main():
    initial_state = {'count': 0}
    state_manager = StateManager(initial_state)

    def increment(state):
        return {'count': state['count'] + 1}

    def decrement(state):
        return {'count': state['count'] - 1}

    async def update_loop():
        while True:
            state_manager.update_state(increment)
            await asyncio.sleep(1)
            state_manager.update_state(decrement)
            await asyncio.sleep(1)

    def state_observer(state):
        print(f"New state: {state}")

    def on_change_callback(state):
        print(f"State changed: {state}")

    state_manager.subscribe(state_observer)
    state_manager.on_change(on_change_callback)
    update_task = asyncio.create_task(update_loop())
    state_task = asyncio.create_task(state_manager.run())

    await asyncio.gather(update_task, state_task)

asyncio.run(main())
