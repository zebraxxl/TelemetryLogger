from control_thread import ControlThread

__author__ = 'zebraxxl'

server_thread = None


def start(control_addr, control_port):
    global server_thread

    server_thread = ControlThread((control_addr, control_port))
    server_thread.start()


def subscribe_to_command(command, handler):
    global server_thread

    server_thread.event_handlers[command] = handler
