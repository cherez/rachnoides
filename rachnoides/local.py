from asyncio import Task
from weakref import WeakKeyDictionary


class Local:
    __task_dicts = WeakKeyDictionary()

    def __local_dict(self):
        task = Task.current_task()
        if task not in self.__task_dicts:
            self.__task_dicts[task] = {}
        return self.__task_dicts[task]

    def __getattr__(self, key):
        return self.__local_dict()[key]

    def __setattr__(self, key, value):
        self.__local_dict()[key] = value

    def __delattr__(self, key):
        del self.__local_dict()[key]
