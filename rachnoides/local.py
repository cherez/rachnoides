from asyncio import Task
from weakref import WeakKeyDictionary


class Local:
    __task_dicts = WeakKeyDictionary()

    def __local_dict(self):
        task = Task.current_task()
        if task not in self.__task_dicts:
            self.__task_dicts[task] = object()
        return self.__task_dicts[task]

    def __getattr__(self, key):
        return getattr(self.__local_dict(), key)

    def __setattr__(self, key, value):
        return setattr(self.__local_dict(), key, value)

    def __delattr__(self, key):
        return delattr(self.__local_dict(), key)
