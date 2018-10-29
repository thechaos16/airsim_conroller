
import os
import tempfile
import pprint

import airsim
import numpy as np


def create_client(agent_type=''):
    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    return client


def destroy_client(client):
    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False)


def get_state(client):
    # TODO: get type of client
    return client.getMultirotorState()


def start_client(client):
    # TODO: get type of client
    client.takeoffAsync().join()


def move_client(client, move_type, *args):
    if move_type == 'position':
        client.moveToPositionAsync(*args).join()
    elif move_type == 'velocity':
        client.moveByVelocityAsync(*args).join()
    else:
        raise NotImplementedError()


def get_images(client, image_type=''):
    responses = client.simGetImages([
        airsim.ImageRequest('0', airsim.ImageType.DepthVis),  # depth visualization image
        airsim.ImageRequest('1', airsim.ImageType.DepthPerspective, True),  # depth in perspective projection
        airsim.ImageRequest('1', airsim.ImageType.Scene),  # scene vision image in png format
        airsim.ImageRequest('1', airsim.ImageType.Scene, False, False)  # scene vision image in uncompressed RGBA array
    ])
    return responses


if __name__ == '__main__':
    client = create_client()

    state = get_state(client)
    s = pprint.pformat(state)
    print('state: %s' % s)

    airsim.wait_key('Press any key to takeoff')
    start_client(client)

    # NOTE: it looks like position is reversed coordination
    airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')
    move_client(client, 'position', *[-10, 10, -10, 5])
    # move_client(client, 'velocity', *[-2, 1, -2, 5])

    client.hoverAsync().join()
    airsim.wait_key('Press any key to take images')
    # get camera images from the car

    # NOTE: images are in byte format
    responses = get_images(client)
    print('Retrieved images: %d' % len(responses))

    tmp_dir = os.path.join(tempfile.gettempdir(), 'airsim_drone')
    print('Saving images to %s' % tmp_dir)
    try:
        os.makedirs(tmp_dir)
    except OSError:
        if not os.path.isdir(tmp_dir):
            raise

    for idx, response in enumerate(responses):
        filename = os.path.join(tmp_dir, str(idx))
        if response.pixels_as_float:
            print('Type %d, size %d' % (response.image_type, len(response.image_data_float)))
            airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
        elif response.compress:  # png format
            print('Type %d, size %d' % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
        else:  # uncompressed array
            print('Type %d, size %d' % (response.image_type, len(response.image_data_uint8)))
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)  # get numpy array
            img_rgba = img1d.reshape(response.height, response.width, 4)  # reshape array to 4 channel image array H X W X 4
            img_rgba = np.flipud(img_rgba)  # original image is flipped vertically
            img_rgba[:, :, 1:2] = 100  # just for fun add little bit of green in all pixels
            airsim.write_png(os.path.normpath(filename + '.greener.png'), img_rgba)  # write to png

    airsim.wait_key('Press any key to reset to original state')
    client.armDisarm(False)
    client.reset()
    destroy_client(client)
