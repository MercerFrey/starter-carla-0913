import carla

from .controller import PurePursuitController


class Other(object):
    def __init__(self):
        self.world = None
        self.actor = None
        self.control = None
        self.controller = None
        self.waypoints = []
        self.target_speed = None  # meters per second

    def start(self, world):
        self.world = world
        spawn_point = carla.Transform(
            carla.Location(x=24.6, y=16.5, z=0.6), carla.Rotation(yaw=180.0)
        )
        self.actor = self.world.spawn_hero("vehicle.audi.tt", spawn_point)

        self.waypoints = [
            carla.Location(x=0.6, y=16.5, z=0.6),
            carla.Location(x=-114, y=16.5, z=0.6),
        ]

        self.target_speed = 9  # meters per second
        self.controller = PurePursuitController()

        self.world.register_actor_waypoints_to_draw(self.actor, self.waypoints)
        # self.actor.set_autopilot(True, world.args.tm_port)

    def tick(self, clock):

        throttle, steer = self.controller.get_control(
            self.actor,
            self.waypoints,
            self.target_speed,
            self.world.fixed_delta_seconds,
        )

        ctrl = carla.VehicleControl()
        ctrl.throttle = throttle
        ctrl.steer = steer
        self.actor.apply_control(ctrl)

    def destroy(self):
        """Destroy the hero actor when class instance is destroyed"""
        if self.actor is not None:
            self.actor.destroy()
