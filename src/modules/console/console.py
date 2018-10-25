from src.modules.command.command_factory import CommandFactory


class Console:
    def __init__(self):
        self.command_factory = CommandFactory()

    def get_next_command(self):
        return self.command_factory.get_command(input())

    def get_next_text(self):
        return input()