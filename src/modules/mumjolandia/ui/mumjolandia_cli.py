from threading import Thread

import logging

from src.modules.console.console import Console


class MumjolandiaCli(Thread):
    def __init__(self, queue_to_pass, queue_for_me):
        Thread.__init__(self)
        self.passable_queue = queue_to_pass
        self.my_queue = queue_for_me    # not used yet
        self.console = Console()

    def run(self):
        logging.info('mumjolandia cli started')
        while True:
            command = self.console.get_next_text()
            self.__pass_command(command)
            if self.__command_exit(command):
                break
        logging.info('mumjolandia cli exiting')

    def __pass_command(self, command):
        self.passable_queue.put(command)

    def __command_exit(self, command):
        if command.startswith("exit"):
            return True
        return False