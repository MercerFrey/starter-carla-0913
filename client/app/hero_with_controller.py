from turtle import distance
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
        self.tick_count = 0

    def start(self, world):
        self.world = world
        spawn_point = carla.Transform(
            self.location, self.rotation
        )
        self.actor = self.world.spawn_hero("vehicle.audi.tt", spawn_point)

        self.controller = PurePursuitController()

        self.world.register_actor_waypoints_to_draw(self.actor, self.waypoints)
        #self.actor.set_autopilot(True, world.args.tm_port)

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

    def distance_between_others(self):
        vehicles = self.world.get_vehicles()
        others = [actor for actor in vehicles if self.actor.id != actor.id]

        # for other in others:
        #     distance = self.actor.get_location().distance(other.get_location())
        #     print(other.id, distance)

    def location_printer(self, interval):
        self.tick_count += 1
        if self.tick_count == interval:
            print("""
        {{ 
            "x": {x},
            "y": {y},
            "z": {z}
        }},""".format(x=self.actor.get_location().x, y=self.actor.get_location().y, z=self.actor.get_location().z))
            self.tick_count %= interval