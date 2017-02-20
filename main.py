from scripts.traffic_engine import TrafficController, TrafficLight

lane_config = {
    'traffic-0': {
        'lights': {
            'pin-red': 2,
            'pin-orange': 3,
            'pin-green': 4
        },
        'sensors': {
            'sensor-pin-1': 17,
            'sensor-pin-2':27,
            'sensor-pin-3': 22
        }
    },
    'traffic-1': {
        'lights': {
            'pin-red': 10,
            'pin-orange': 9,
            'pin-green': 11
        },
        'sensors': {
            'sensor-pin-1': 5,
            'sensor-pin-2': 6,
            'sensor-pin-3': 13
        }
    },
    'traffic-2': {
        'lights': {
            'pin-red': 19,
            'pin-orange': 26,
            'pin-green': 14
        },
        'sensors': {
            'sensor-pin-1': 15,
            'sensor-pin-2': 16,
            'sensor-pin-3': 18
        }
    }
}


class Main(object):

    def __init__(self, **kwargs):
        self.lanes = {}
        self.max_lanes = 3
        self.prepareLanes()
        self.allowed_lane = None
        super(Main, self).__init__(**kwargs)

    def prepareLanes(self):
        for i in range(self.max_lanes):
            config = lane_config['traffic-{0}'.format(i)]
            pin_red = config['lights']['pin-red']
            pin_orange = config['lights']['pin-orange']
            pin_green = config['lights']['pin-green']

            sensor_pin_1 = config['sensors']['sensor-pin-1']
            sensor_pin_2 = config['sensors']['sensor-pin-2']
            sensor_pin_3 = config['sensors']['sensor-pin-3']

            data = {
                'traffic-light': TrafficLight(pin_red, pin_orange, pin_green),
                'traffic-controller': TrafficController(sensor_pin_1, sensor_pin_2, sensor_pin_3)
            }

            self.lanes['lane-{0}'.format(i)] = data

    def logicController(self):

        if not self.allowed_lane:
            for i in range(self.max_lanes):
                current_lane = self.lanes['lane-{0}'.format(i)]
                tL = current_lane['traffic-light']
                tC = current_lane['traffic-controller']

                if tC.checkPriority() > 2:
                    tL.toGreen()
                    self.allowed_lane = current_lane

        else:
            tC = self.allowed_lane['traffic-controller']
            tL = self.allowed_lane['traffic-light']
            if tC.checkPriority() < 1:
                tL.toRed()
                self.allowed_lane = None

    def run(self):
        try:
            while True:
                self.logicController()
        except Exception as e:
            print("Error: An error occured in the main loop\n{0}".format(e))
        except KeyboardInterrupt:
            print("Exit: Application is exiting")


if __name__ == "__main__":
    Main().run()
