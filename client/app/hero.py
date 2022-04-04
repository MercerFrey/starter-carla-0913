import carla


class Hero(object):
    def __init__(self):
        self.world = None
        self.actor = None
        self.control = None

    def start(self, world):
        self.world = world


        self.Location = carla.Location(x=-400, y=37.8, z=0.281942)
        self.Rotation = carla.Rotation(pitch=0.000000, yaw=-0.368408, roll=0.000000)
        self.spawn_point = carla.Transform(self.Location, self.Rotation)
        self.actor = self.world.spawn_hero(blueprint_filter=world.args.filter, spawn_point=self.spawn_point)
#        self.actor.set_autopilot(True, world.args.tm_port)

    def tick(self, clock):
        pass

        # Uncomment and modify to control manually, disable autopilot too
        #
        ctrl = carla.VehicleControl()
        ctrl.throttle = 1
        ctrl.steer = 0
        self.actor.apply_control(ctrl)

    def destroy(self):
        """Destroy the hero actor when class instance is destroyed"""
        if self.actor is not None:
            self.actor.destroy()
