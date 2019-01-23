
import airsim


class AirsimClient:
    def __init__(self, agent_type, interval=5):
        if agent_type == 'drone':
            self.client = airsim.MultirotorClient()
            self.client.confirmConnection()
            self.client.enableApiControl(True)
            self.client.armDisarm(True)
        else:
            raise NotImplementedError()
        self.interval = interval

    def destroy(self):
        self.client.enableApiControl(False)

    def start(self):
        self.client.takeoffAsync().join()

    def get_state(self):
        return self.client.getMultirotorState()

    def get_collision_info(self):
        return self.client.simGetCollisionInfo()

    def get_images(self, image_type=''):
        responses = self.client.simGetImages([
            airsim.ImageRequest('0', airsim.ImageType.DepthVis),  # depth visualization image
            airsim.ImageRequest('1', airsim.ImageType.DepthPerspective, True),  # depth in perspective projection
            airsim.ImageRequest('1', airsim.ImageType.Scene),  # scene vision image in png format
            airsim.ImageRequest('1', airsim.ImageType.Scene, False, False)
            # scene vision image in uncompressed RGBA array
        ])
        return responses

    def move(self, move_type, *args):
        if move_type == 'position':
            self._go_to_loc(*args)
        elif move_type == 'velocity':
            self._move_by_velocity(*args)
        else:
            raise NotImplementedError()

    def _go_to_loc(self, mx, my, mz, velocity):
        self.client.moveToPositionAsync(mx, my, mz, velocity).join()

    def _move_by_velocity(self, vx, vy, vz):
        self.client.moveByVelocityAsync(vx, vy, vz, self.interval).join()


if __name__ == '__main__':
    controller = AirsimClient('drone', 5)
    controller.destroy()
