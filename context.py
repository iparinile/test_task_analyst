

class ContextLockedException(Exception):
    pass


class Context:

    def __init__(self):
        self.is_locked = False

    def lock(self):
        self.is_locked = True

    def unlock(self):
        self.is_locked = False

    def set(self, key, value):
        if self.is_locked:
            raise ContextLockedException
        setattr(self, key, value)
