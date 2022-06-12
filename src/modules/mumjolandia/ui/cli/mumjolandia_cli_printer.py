import logging
import sys
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.utils.polish_utf_to_ascii import PolishUtfToAscii


class MumjolandiaCliPrinter:
    def __init__(self):
        self.views = {}
        self.__init()

    def execute(self, return_value):
        try:
            self.views[return_value.status.name](return_value)
        except KeyError:
            self.views['unrecognized_status_response'](return_value)

    def __init(self):
        self.views['unrecognized_status_response'] = self.view_unrecognized_status_response
        self.views[MumjolandiaReturnValue.mumjolandia_none.name] = self.view_mumjolandia_none
        self.views[MumjolandiaReturnValue.mumjolandia_unrecognized_command.name] = self.view_unrecognized_command
        self.views[MumjolandiaReturnValue.mumjolandia_exit.name] = self.view_exit
        self.views[MumjolandiaReturnValue.mumjolandia_unrecognized_parameters.name] = \
            self.view_unrecognized_parameters
        self.views[MumjolandiaReturnValue.mumjolandia_help.name] = self.view_default_list_response

        self.views[MumjolandiaReturnValue.task_get.name] = self.view_task_print
        self.views[MumjolandiaReturnValue.task_added.name] = self.view_task_added
        self.views[MumjolandiaReturnValue.task_delete_success.name] = self.view_task_delete_success
        self.views[MumjolandiaReturnValue.task_delete_incorrect_index.name] = self.view_task_delete_incorrect_index
        self.views[MumjolandiaReturnValue.task_delete_incorrect_name.name] = self.view_task_delete_incorrect_name
        self.views[MumjolandiaReturnValue.task_edit_ok.name] = self.view_task_edit_ok
        self.views[MumjolandiaReturnValue.task_edit_wrong_index.name] = self.view_task_edit_wrong_index
        self.views[MumjolandiaReturnValue.task_help.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.task_name_not_given.name] = self.view_task_name_not_given
        self.views[MumjolandiaReturnValue.task_get_wrong_data.name] = self.view_task_get_wrong_data
        self.views[MumjolandiaReturnValue.task_set_ok.name] = self.view_task_set_ok
        self.views[MumjolandiaReturnValue.task_set_incorrect_parameter.name] = self.view_task_set_incorrect_parameter
        self.views[MumjolandiaReturnValue.task_done_ok.name] = self.view_task_done
        self.views[MumjolandiaReturnValue.task_undone_ok.name] = self.view_task_undone
        self.views[MumjolandiaReturnValue.task_done_wrong_parameter.name] = self.view_task_done_wrong_parameter
        self.views[MumjolandiaReturnValue.task_bump_ok.name] = self.view_task_bump_ok
        self.views[MumjolandiaReturnValue.task_bump_nook.name] = self.view_task_bump_nook
        self.views[MumjolandiaReturnValue.task_find.name] = self.view_task_search

        self.views[MumjolandiaReturnValue.food_get_ok.name] = self.view_food_get_ok
        self.views[MumjolandiaReturnValue.food_list_ok.name] = self.view_food_list_ok
        self.views[MumjolandiaReturnValue.food_get_wrong_index.name] = self.view_food_get_wrong_index
        self.views[MumjolandiaReturnValue.food_help.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.food_file_broken.name] = self.view_food_file_broken
        self.views[MumjolandiaReturnValue.food_ingredient_ok.name] = self.view_food_ingredient_ok
        self.views[MumjolandiaReturnValue.food_set_ok.name] = self.view_food_set_ok
        self.views[MumjolandiaReturnValue.food_meal_ok.name] = self.view_food_meal_ok

        self.views[MumjolandiaReturnValue.fat_get_ok.name] = self.view_fat_get_ok
        self.views[MumjolandiaReturnValue.fat_delete_success.name] = self.view_fat_delete_ok
        self.views[MumjolandiaReturnValue.fat_delete_incorrect_index.name] = self.view_fat_delete_incorrect_index
        self.views[MumjolandiaReturnValue.fat_value_not_given.name] = self.view_fat_value_not_given
        self.views[MumjolandiaReturnValue.fat_add_must_be_float.name] = self.view_fat_add_must_be_float
        self.views[MumjolandiaReturnValue.fat_added.name] = self.view_fat_added

        self.views[MumjolandiaReturnValue.game_value_not_given.name] = self.view_game_value_not_given
        self.views[MumjolandiaReturnValue.game_added.name] = self.view_game_added
        self.views[MumjolandiaReturnValue.game_exist.name] = self.view_game_exist
        self.views[MumjolandiaReturnValue.game_delete_incorrect_index.name] = self.view_game_delete_incorrect_index
        self.views[MumjolandiaReturnValue.game_delete_success.name] = self.view_game_delete_success
        self.views[MumjolandiaReturnValue.game_get_ok.name] = self.view_game_get_ok
        self.views[MumjolandiaReturnValue.game_help.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.game_current_get.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.game_set_ok.name] = self.view_game_set_ok
        self.views[MumjolandiaReturnValue.game_set_wrong_id.name] = self.view_game_set_wrong_id

        self.views[MumjolandiaReturnValue.note_get_ok.name] = self.view_note_get_ok
        self.views[MumjolandiaReturnValue.note_delete_success.name] = self.view_note_delete_ok
        self.views[MumjolandiaReturnValue.note_delete_incorrect_index.name] = self.view_note_delete_incorrect_index
        self.views[MumjolandiaReturnValue.note_add_nook.name] = self.view_note_add_nook
        self.views[MumjolandiaReturnValue.note_add_ok.name] = self.view_note_add_ok
        self.views[MumjolandiaReturnValue.note_help.name] = self.view_default_response

        self.views[MumjolandiaReturnValue.connection_help.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.connection_server_start.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.connection_server_start_fail.name] = self.view_connection_server_start_fail
        self.views[MumjolandiaReturnValue.connection_client_send_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.connection_failed.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.connection_pwd.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.connection_get.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.connection_ls.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.connection_command_fail.name] = self.view_default_response

        self.views[MumjolandiaReturnValue.event_get_ok.name] = self.view_event_get_ok
        self.views[MumjolandiaReturnValue.event_help.name] = self.view_default_response

        self.views[MumjolandiaReturnValue.weather_get_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.weather_get_nook.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.weather_help.name] = self.view_default_response

        self.views[MumjolandiaReturnValue.password_set_ok.name] = self.view_password_set_ok
        self.views[MumjolandiaReturnValue.password_set_incorrect.name] = self.view_password_set_incorrect
        self.views[MumjolandiaReturnValue.password_incorrect_value.name] = self.view_password_incorrect_value
        self.views[MumjolandiaReturnValue.password_not_set.name] = self.view_password_not_set
        self.views[MumjolandiaReturnValue.password_help.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.password_add_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.password_rm_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.password_get_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.password_list_ok.name] = self.view_default_response

        self.views[MumjolandiaReturnValue.pompejanka_message.name] = self.view_default_response

        self.views[MumjolandiaReturnValue.utils_get.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.utils_help.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.utils_shared_preferences_get.name] = self.view_utils_shared_preferences_get
        self.views[MumjolandiaReturnValue.utils_update_ok.name] = self.view_utils_update_ok
        self.views[MumjolandiaReturnValue.utils_update_fail.name] = self.view_utils_update_fail

        self.views[MumjolandiaReturnValue.planner_help.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.planner_get_ok.name] = self.view_planner_get
        self.views[MumjolandiaReturnValue.planner_get_fail.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.planner_add_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.planner_add_fail.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.planner_remove_fail.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.planner_remove_ok.name] = self.view_default_response

        self.views[MumjolandiaReturnValue.rootfs_cd_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.rootfs_ls_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.rootfs_no_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.rootfs_pwd_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.rootfs_crc_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.rootfs_crc_fail.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.rootfs_get_file_fail.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.rootfs_get_file_ok.name] = self.view_rootfs_get_file_ok

        self.views[MumjolandiaReturnValue.config_set_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.config_set_nook.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.config_get_ok.name] = self.view_default_response
        self.views[MumjolandiaReturnValue.config_get_fail.name] = self.view_default_response

    def view_mumjolandia_none(self, return_value):
        pass

    def view_task_print(self, return_value):
        print(len(return_value.arguments[0]), 'items:')
        max_width = 0
        for i in return_value.arguments[0]:
            if len(str(i)) > max_width:
                max_width = len(str(i))
        for i, t in zip(return_value.arguments[0], return_value.arguments[1]):
            print('[' + str(i).rjust(max_width, ' ') + ']' + str(t))

    def view_task_added(self, return_value):
        print('Added: ' + str(return_value.arguments[0]) + ' [' + str(return_value.arguments[1]) + ']')

    def view_exit(self, return_value):
        pass

    def view_default_response(self, return_value):
        print(str(return_value.arguments[0]))

    def view_default_list_response(self, return_value):
        for argument in return_value.arguments:
            print(str(argument))

    def view_unrecognized_command(self, return_value):
        print('Unrecognized command: ', return_value.arguments, sep=' ', end='\n', file=sys.stdout, flush=False)

    def view_unrecognized_status_response(self, return_value):
        print('Unrecognized status response: ' + return_value.status.name)
        logging.error("Unrecognized status response: '" + return_value.status.name + "'")

    def view_unrecognized_parameters(self, return_value):
        print("Unrecognized parameters: ",
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

    def view_task_edit_ok(self, return_value):
        print("Task edited: " + return_value.arguments[0])

    def view_task_edit_wrong_index(self, return_value):
        print("Edit aborted - wrong index: " + return_value.arguments[0])

    def view_task_name_not_given(self, return_value):
        print("Task name not given")

    def view_task_get_wrong_data(self, return_value):
        print("Wrong parameter " + return_value.arguments[0])

    def view_task_set_incorrect_parameter(self, return_value):
        print("Wrong parameters " + str(return_value.arguments))

    def view_task_set_ok(self, return_value):
        print("Set '" + return_value.arguments[0] + "' to " + return_value.arguments[1] + " days ahead")

    def view_task_done(self, return_value):
        print("Done: " + return_value.arguments[0])

    def view_task_undone(self, return_value):
        print("Undone: " + return_value.arguments[0])

    def view_task_done_wrong_parameter(self, return_value):
        print("Wrong parameters " + str(return_value.arguments))

    def view_task_bump_ok(self, return_value):
        print("'" + return_value.arguments[1] + "' bumped to id: " + return_value.arguments[0])

    def view_task_bump_nook(self, return_value):
        print("Wrong parameters " + str(return_value.arguments))

    def view_task_search(self, return_value):
        print(len(return_value.arguments[0]), 'items found:')
        max_width = 0
        for i in return_value.arguments[0]:
            if len(str(i)) > max_width:
                max_width = len(str(i))
        for i, t in zip(return_value.arguments[0], return_value.arguments[1]):
            print('[' + str(i).rjust(max_width, ' ') + ']' + str(t))

    def view_food_get_ok(self, return_value):
        print(PolishUtfToAscii.translate(return_value.arguments[0][0]))
        print()
        for row in return_value.arguments[1]:
            print(row)
        print()
        print(PolishUtfToAscii.translate(return_value.arguments[0][1]))

    def view_food_list_ok(self, return_value):
        for row in return_value.arguments:
            print(row)

    def view_food_get_wrong_index(self, return_value):
        print('Wrong meal index: ' + return_value.arguments[0])

    def view_food_file_broken(self, return_value):
        print('Database file: "' + return_value.arguments[0] + '" is broken')

    def view_food_ingredient_ok(self, return_value):
        def __view_food_ingredient_ok_print(recipe):
            sorted_list = recipe
            sorted_list.sort()
            for i in sorted_list:
                print(" " + PolishUtfToAscii.translate(i))
        print("\nBreakfast (" + PolishUtfToAscii.translate(return_value.arguments[0][0]) + "): ")
        __view_food_ingredient_ok_print(return_value.arguments[0][1])
        print("\nSecond breakfast (" + PolishUtfToAscii.translate(return_value.arguments[1][0]) + "): ")
        __view_food_ingredient_ok_print(return_value.arguments[1][1])
        print("\nDinner (" + PolishUtfToAscii.translate(return_value.arguments[2][0]) + "): ")
        __view_food_ingredient_ok_print(return_value.arguments[2][1])
        print("\nTea (" + PolishUtfToAscii.translate(return_value.arguments[3][0]) + "): ")
        __view_food_ingredient_ok_print(return_value.arguments[3][1])
        print("\nSupper (" + PolishUtfToAscii.translate(return_value.arguments[4][0]) + "): ")
        __view_food_ingredient_ok_print(return_value.arguments[4][1])
        print("")

    def view_food_set_ok(self, return_value):
        print(str(return_value.arguments[0]) + ' set to: ' + str(return_value.arguments[1]))

    def view_food_meal_ok(self, return_value):
        def __print_meal_name(name, meal):
            if meal[0] is None:
                print(name + '[-]: None')
            else:
                print(name + '[' + str(meal[0]) + ']: ' + meal[1])

        __print_meal_name('    Breakfast', return_value.arguments[0][0])
        __print_meal_name('2nd breakfast', return_value.arguments[0][1])
        __print_meal_name('       Dinner', return_value.arguments[0][2])
        __print_meal_name('          Tea', return_value.arguments[0][3])
        __print_meal_name('       Supper', return_value.arguments[0][4])
        print()
        for ingredient in return_value.arguments[1]:
            print(ingredient[0] + ' ' + str(ingredient[2]) + ' ' + ingredient[1])

    def view_fat_get_ok(self, return_value):
        try:
            for i, t in enumerate(return_value.arguments):
                print('[' + str(i) + '] ' + str(t))
        except TypeError:
            print('0 elements')

    def view_fat_delete_ok(self, return_value):
        print("Deleted " + return_value.arguments[1] + " element(s) using parameter: " + return_value.arguments[0])

    def view_fat_delete_incorrect_index(self, return_value):
        print("Can't delete - incorrect index value: " + return_value.arguments[0])

    def view_fat_value_not_given(self, return_value):
        print("Value not given")

    def view_fat_add_must_be_float(self, return_value):
        print('Parameter must be a number')

    def view_fat_added(self, return_value):
        print('Added: ', return_value.arguments[0])

    def view_game_delete_success(self, return_value):
        print("Deleted " + str(return_value.arguments[0]) + " element(s) using parameter: " + str(return_value.arguments[1]))

    def view_game_delete_incorrect_index(self, return_value):
        print("Incorrect name")

    def view_game_value_not_given(self, return_value):
        print("Value not given")

    def view_game_added(self, return_value):
        print('Added: ', return_value.arguments[0])

    def view_game_exist(self, return_value):
        print('Game already exist: ', return_value.arguments[0])

    def view_game_get_ok(self, return_value):
        for g in return_value.arguments:
            print(str(g))

    def view_game_set_ok(self, return_value):
        print('Done')

    def view_game_set_wrong_id(self, return_value):
        print('wrong game id')

    def view_note_get_ok(self, return_value):
        for i, t in enumerate(return_value.arguments):
            print('[' + str(i) + '] ' + str(t))

    def view_note_delete_ok(self, return_value):
        print("Deleted " + return_value.arguments[1] + " element(s) using parameter: " + return_value.arguments[0])

    def view_note_delete_incorrect_index(self, return_value):
        print("Can't delete - incorrect index value: " + return_value.arguments[0])

    def view_note_add_nook(self, return_value):
        print("Wrong index")

    def view_note_add_ok(self, return_value):
        print('Added: ', return_value.arguments[0])

    def view_connection_server_start_fail(self, return_value):
        if "Errno 98" in return_value.arguments[0]:
            print("Server already up (is mumjonadia set to run background server by default?)")
        else:
            print(return_value.arguments[0])

    def view_event_get_ok(self, return_value):
        for e in return_value.arguments[0]:
            print(str(e))

    def view_password_set_ok(self, return_value):
        print('password set')

    def view_password_set_incorrect(self, return_value):
        print('incorrect password :(')

    def view_password_incorrect_value(self, return_value):
        print('incorrect parameter')

    def view_password_not_set(self, return_value):
        print('Password is not set! Please run "init" command first')

    def view_utils_shared_preferences_get(self, return_value):
        print(str(len(return_value.arguments[0])) + ' items stored: ')
        for key, value in return_value.arguments[0].items():
            print(str(key) + " " + str(value))

    def view_utils_update_ok(self, return_value):
        print("Updated with branch '" + return_value.arguments[0] + "'")

    def view_utils_update_fail(self, return_value):
        print("Update failed")
        print(return_value.arguments[0])

    def view_planner_get(self, return_value):
        def print_plan(plan):
            print("Date: " + str(plan.date))
            for planner_task in plan.planner_tasks:
                print(planner_task.time + "| " + str(planner_task.description))
        if isinstance(return_value.arguments[0], list):
            print("plans:")
            for plan in return_value.arguments[0]:
                print_plan(plan)
        else:
            print("plan:")
            print_plan(return_value.arguments[0])

    def view_rootfs_get_file_ok(self, return_value):
        print("got file")
        f = open('new.file', 'wb')
        f.write(return_value.arguments[0])
        f.close()
