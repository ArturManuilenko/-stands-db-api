from typing import Tuple


class Client:
    def __init__(self, cmd_id=None):
        self.request = {}
        self.answer = {}
        self.cmd_id = cmd_id

    def start_command(self, cmd: str, *args, **kwargs) -> None:
        self.request = {'type': 'start', 'cmd': cmd, 'args': args, 'kwargs': kwargs}
        self.make_command()
        self.cmd_id = self.answer['id']

    def check_progress(self) -> Tuple[str, bool]:
        self.request = {'id': self.cmd_id, 'type': 'progress'}
        self.make_command()
        return self.answer['progress'], self.answer['ready']

    def service_command(self, command_type: str) -> None:
        self.request = {'type': command_type}
        self.make_command()

    def kill(self):
        self.request = {'id': self.cmd_id, 'type': 'kill'}
        self.make_command()

    def stop(self):
        self.request = {'id': self.cmd_id, 'type': 'stop'}
        self.make_command()

    def keep(self):
        self.request = {'id': self.cmd_id, 'type': 'keep'}
        self.make_command()

    def temp_path(self) -> str:
        self.request = {'id': self.cmd_id, 'type': 'tmppath'}
        self.make_command()
        return self.answer['path']

    def get_data(self):
        self.request = {'id': self.cmd_id, 'type': 'data'}
        self.make_command()
        return self.answer['data'], self.answer['files']

    def make_command(self):
        pass

    def uuid(self):
        return self.cmd_id
