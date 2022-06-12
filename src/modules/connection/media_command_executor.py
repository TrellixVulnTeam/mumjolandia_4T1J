from src.external import keyboard


class MediaCommandExecutor:
    def __init__(self):
        pass

    def execute(self, string_command):
        return_message = 'command \'' + string_command + '\' not recognized'
        try:
            if string_command == 'play':
                keyboard.press_and_release('play/pause')
                return_message = 'play/pause ok'
            elif string_command == 'pause':
                keyboard.press_and_release('play/pause')
                return_message = 'play/pause ok'
            elif string_command == 'stop':
                keyboard.press_and_release('play/pause')
                return_message = 'play/pause ok'
            elif string_command == 'start':
                keyboard.press_and_release('play/pause')
                return_message = 'play/pause ok'
            elif string_command == 'vol+':
                keyboard.press_and_release('B')
                return_message = 'vol+ ok'
            elif string_command == 'vol-':
                keyboard.press_and_release('C')
                return_message = 'vol- ok'
            elif string_command == 'mute':
                keyboard.press_and_release('D')
                return_message = 'mute ok'
            elif string_command == 'unmute':
                keyboard.press_and_release('D')
                return_message = 'mute ok'
            elif string_command == 'next':
                keyboard.press_and_release('P')
                return_message = 'next song ok'
            elif string_command == 'prev':
                keyboard.press_and_release('Q')
                return_message = 'previous song ok'
            elif string_command == 'previous':
                keyboard.press_and_release('Q')
                return_message = 'previous song ok'
        except ImportError as e:
            return_message = 'keyboard module - ' + str(e)
        return return_message
