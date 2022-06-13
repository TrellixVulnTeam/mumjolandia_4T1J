import logging

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.connection.mumjolandia_connection_handler import MumjolandiaConnectionHandler
from src.modules.mumjolandia.config_loader import ConfigLoader
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.mumjolandia.mumjolandia_updater import MumjolandiaUpdater
from src.utils.helpers import RandomUtils
from src.utils.socket.socket_client import SocketClient


class ConnectionSupervisor(MumjolandiaSupervisor):
    def __init__(self):
        super().__init__()
        self.__init()

    def __init(self):
        self.__add_command_parsers()

    def __add_command_parsers(self):
        self.command_parsers['help'] = self.__command_help
        self.command_parsers['server'] = self.__command_start_server
        self.command_parsers['send'] = self.__command_send_message
        self.command_parsers['update'] = self.__command_update
        self.command_parsers['get'] = self.__command_get

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_help,
                                         arguments=['server\n'
                                                    'server [x] (session)\n'
                                                    'send [msg]\n'
                                                    'send exit (shutdown server)\n'
                                                    'get [filename] \n'
                                                    'update\n'])

    def __command_start_server(self, args):
        run_server_once = True
        if len(args) > 0:
            run_server_once = False
            logging.info("Starting server\nip: " + RandomUtils.get_ip() + "\nport: " + ConfigLoader.get_config().server_port)
        # todo: workaround for broken cmd logger
        if RandomUtils.get_platform() == 'windows':
            print("Starting server\nip: " + RandomUtils.get_ip() + "\nport: " + ConfigLoader.get_config().server_port)
        return_value = MumjolandiaConnectionHandler(int(ConfigLoader.get_config().server_port)).start_server(run_server_once)
        return MumjolandiaResponseObject(return_value.status, return_value.arguments)

    def __command_send_message(self, args):
        config = ConfigLoader.get_config()
        return_value = MumjolandiaConnectionHandler(int(config.server_port),
                                                    server_address=config.server_address).send_message(" ".join(args))
        if return_value.status == MumjolandiaReturnValue.rootfs_get_file_ok:
            return MumjolandiaResponseObject(return_value.status, [return_value.arguments[0]])
        return MumjolandiaResponseObject(return_value.status, return_value.arguments[0].decode('utf-8'))

    def __command_update(self, args):
        try:
            s = SocketClient(ConfigLoader.get_config().server_address, int(ConfigLoader.get_config().server_port))
            path = s.get_mumjolandia_update_package('mumjolandia.tar.gz')
            MumjolandiaUpdater.install_source(path)
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_client_send_ok,
                                             arguments=['ok'])
        except ConnectionRefusedError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_failed,
                                             arguments=['Can\'t connect to server'])

    def __command_get(self, args):
        try:
            s = SocketClient(ConfigLoader.get_config().server_address, int(ConfigLoader.get_config().server_port))
            path = s.get_file(args[0])
            if path is None:
                return_value = 'Connection ok, but received file empty'
            else:
                return_value = 'received file: ' + path
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_client_send_ok,
                                             arguments=[return_value])
        except ConnectionRefusedError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_failed,
                                             arguments=['Can\'t connect to server'])
