class Task:
    def __init__(self, name, description, date_added, date_to_finish, priority, task_type, status):
        self.name = name
        self.description = description
        self.date_added = date_added
        self.date_to_finish = date_to_finish
        self.priority = priority
        self.type = task_type
        self.status = status

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
