import logging
import sys
from threading import Thread

from src.interface.mumjolandia.mumjolandia_mode import MumjolandiaMode
from src.modules.tasks.task_supervisor import TaskSupervisor


class MumjolandiaThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.taskSupervisor = TaskSupervisor()
        self.mode = MumjolandiaMode.none

    def run(self):
        logging.info('mumjolandia thread started')
        while True:
            command = self.__get_next_command()
            if command.arguments[0] == 'task':
                arg_placeholder = command.arguments.pop(0)
                if self.taskSupervisor.execute(command):
                    command.arguments.insert(0, arg_placeholder)
                    print(command.arguments, '- Command not recognized :(')
                    continue
            elif command.arguments[0] == 'exit':
                logging.info('mumjolandia thread exiting')
                break
            else:
                print('Unrecognized command: ', command.arguments, sep=' ', end='\n', file=sys.stdout, flush=False)

    def __get_next_command(self):
        command = self.queue.get()
        self.queue.task_done()
        return command

