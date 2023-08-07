from uuid import UUID


class Client:
    def __init__(self, id = None) -> None:
        self.request = {}
        self.answer = {}
        self.cmd_id = id

    def start_command(self, cmd: str, *args, **kwargs) -> None:
        self.request = {'type': 'start', 'cmd': cmd, 'args': args, 'kwargs': kwargs}
        self.make_command()
        self.cmd_id = self.answer['id']

    def check_progress(self):
        self.request = {'id': self.cmd_id, 'type': 'progress'}
        self.make_command()
        return self.answer['progress'], self.answer['ready']

    def service_command(self, cmd_type: str) -> None:
        self.request = {'type': cmd_type}
        self.make_command()

    def kill(self) -> None:
        self.request = {'id': self.cmd_id, 'type': 'kill'}
        self.make_command()

    def stop(self) -> None:
        self.request = {'id': self.cmd_id, 'type': 'stop'}
        self.make_command()

    def keep(self) -> None:
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

    def make_command(self) -> None:
        pass

    def uuid(self) -> UUID:
        return self.cmd_id
