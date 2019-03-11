
class Agent:
    def __init__(self, client, move_type):
        self.client = client
        self.move_type = move_type

    def get_state(self, *args, **kwargs):
        raise NotImplementedError()

    def act(self, *args, **kwargs):
        raise NotImplementedError()

    def run(self, *args, **kwargs):
        raise NotImplementedError()

    def train(self, *args, **kwargs):
        raise NotImplementedError()
