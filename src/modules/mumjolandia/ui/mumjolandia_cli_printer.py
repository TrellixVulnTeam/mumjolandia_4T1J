import logging
import sys
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue


class MumjolandiaCliPrinter:
    def __init__(self, exit_flag):
        self.views = {}
        self.exit_flag = exit_flag
        self.__init()

    def execute(self, return_value):
        try:
            self.views[return_value.status.name](return_value)
        except KeyError:
            self.views['unrecognized_status_response'](return_value)

    def __init(self):
        self.views['unrecognized_status_response'] = self.view_unrecognized_status_response
        self.views[MumjolandiaReturnValue.task_get.name] = self.view_print
        self.views[MumjolandiaReturnValue.task_added.name] = self.view_task_added
        self.views[MumjolandiaReturnValue.mumjolandia_unrecognized_command.name] = self.view_unrecognized_command
        self.views[MumjolandiaReturnValue.mumjolandia_exit.name] = self.view_exit
        self.views[MumjolandiaReturnValue.task_unrecognized_parameters.name] = self.view_task_unrecognized_parameters
        self.views[MumjolandiaReturnValue.task_delete_success.name] = self.view_task_delete_success
        self.views[MumjolandiaReturnValue.task_delete_incorrect_index.name] = self.view_task_delete_incorrect_index
        self.views[MumjolandiaReturnValue.task_delete_incorrect_name.name] = self.view_task_delete_incorrect_name

    def view_print(self, return_value):
        print(len(return_value.arguments), 'items:')
        for t in return_value.arguments:
            print(str(t))

    def view_task_added(self, return_value):
        print('Added: ' + str(return_value.arguments[0]))

    def view_exit(self, return_value):
        print('exiting')
        self.exit_flag.change(True)

    def view_unrecognized_command(self, return_value):
        print('Unrecognized command: ', return_value.arguments, sep=' ', end='\n', file=sys.stdout, flush=False)

    def view_unrecognized_status_response(self, return_value):
        print('Unrecognized status response: ' + return_value.status.name)
        logging.error("Unrecognized status response: '" + return_value.status.name + "'")

    def view_task_unrecognized_parameters(self, return_value):
        print("Unrecognized parameters for command 'task': ",
              return_value.arguments,
              sep=' ',
              end='\n',
              file=sys.stdout,
              flush=False)

    def view_task_delete_success(self, return_value):
        print("Deleted " + return_value.arguments[1] + " element(s) using parameter: " + return_value.arguments[0])

    def view_task_delete_incorrect_index(self, return_value):
        print("Can't delete - incorrect index value: " + return_value.arguments[0])

    def view_task_delete_incorrect_name(self, return_value):
        print("Can't delete - incorrect task name: " + return_value.arguments[0])