from mumjolandia.tasks.task import Task


class TaskFactory:
    @staticmethod
    def get_task(name):
        return Task(name)
