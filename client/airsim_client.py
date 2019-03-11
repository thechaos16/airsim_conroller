

class AirsimClient:
    def __init__(self, interval=5):
        self.interval = interval

    def destroy(self):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()

    def get_state(self):
        raise NotImplementedError()

    def get_collision_info(self):
        raise NotImplementedError()

    def get_images(self, image_type=''):
        raise NotImplementedError()

    def move(self, move_type, *args):
        raise NotImplementedError()
