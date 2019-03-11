

def parse_state(state):
    gps = state.gps_location
    kinematic = state.kinematics_estimated
    time_stamp = state.timestamp
    return gps, kinematic, time_stamp


def detect_collision(collision):
    has_collide = collision.has_collided
    position = collision.position
    position = position.x_val, position.y_val, position.z_val
    return [has_collide, *position]


def get_position(kinematic):
    pos = kinematic.position
    return pos.x_val, pos.y_val, pos.z_val


def get_gps_info(gps_val):
    return gps_val.altitude, gps_val.latitude, gps_val.longitude
