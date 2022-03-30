import carla

from .controller import PurePursuitController


class Hero(object):
    def __init__(self, location, rotation, waypoints, target_speed):
        self.world = None
        self.actor = None
        self.control = None
        self.controller = None
        self.location = location
        self.rotation = rotation
        self.waypoints = waypoints
        self.target_speed = target_speed  # meters per second

    def start(self, world):
        self.world = world
        spawn_point = carla.Transform(
            self.location, self.rotation
        )
        self.actor = self.world.spawn_hero("vehicle.audi.tt", spawn_point)



        #self.target_speed = 12  # meters per second
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
