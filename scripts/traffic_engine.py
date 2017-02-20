from time import sleep
import threading
try:
    import RPi.GPIO as gpio
    print ("Using GPIO version: {0}".format(gpio.VERSION))
    gpio.setmode(gpio.BOARD)
    print("Setting GPIO mode to BOARD")
except Exception as e:
    print ("Error: GPIO is unavailable")
    raise SystemExit


class TrafficController(object):

    def __init__(self, sensor_pin_1, sensor_pin_2, sensor_pin_3, **kwargs):
        gpio.setup(sensor_pin_1, gpio.IN)
        gpio.setup(sensor_pin_2, gpio.IN)
        gpio.setup(sensor_pin_3, gpio.IN)

        self.sensor_pin_1 = sensor_pin_1
        self.sensor_pin_2 = sensor_pin_2
        self.sensor_pin_3 = sensor_pin_3

        self.priority = 0

        super(TrafficController, self).__init__(**kwargs)

    def checkPriority(self):
        __checkSensor()
        return self.priority

    def __checkSensor(self):
        sensorList = [self.sensor_pin_1, self.sensor_pin_2, self.sensor_pin_3]
        count = 0
        for sensor in sensorList:
            value = gpio.INPUT(sensor)
            if value:
                count += 1

            self.priority = count

class TrafficLight(object):

    def __init__(self, red_pin, orange_pin, green_pin, **kwargs):
        gpio.setup(red_pin, gpio.OUT)
        gpio.setup(orange_pin, gpio.OUT)
        gpio.setup(green_pin, gpio.OUT)

        self.red_pin = red_pin
        self.orange_pin = orange_pin
        self.green_pin = green_pin
        self.state = False

        self.resetState()  # make sure all the lights are red

        super(TrafficLight, self).__init__(**kwargs)

    def resetState(self):
        self.state = False
        self.toRed()

    def toggleState(self):
        if self.state:
            self.toRed()
        else:
            self.toGreen()

        self.state != self.state

    def toGreen(self):
        t = threading.Thread(name="Traffic Light - Green",
                             target=self.__toGreen)
        t.daemon = True
        t.start()

    def __toGreen(self):
        '''Turn traffic light green'''
        self.trafficRed(False)
        self.trafficOrange(True)
        sleep(100)
        self.trafficGreen(True)
        sleep(100)
        self.trafficOrange(False)

    def toRed(self):
        t = threading.Thread(name="Traffic Light - Red", target=self.__toRed)
        t.daemon = True
        t.start()

    def __toRed(self):
        '''Turn traffic light red'''
        self.trafficGreen(False)
        self.trafficOrange(True)
        sleep(100)
        self.trafficRed(True)
        sleep(100)
        self.trafficOrange(True)

    def trafficRed(self, active=True):
        if active:
            gpio.output(self.red_pin, 1)
        else:
            gpio.output(self.red_pin, 0)
        pass

    def trafficOrange(self, active=True):
        if active:
            gpio.output(self.orange_pin, 1)
        else:
            gpio.output(self.orange_pin, 0)

    def trafficGreen(self, active=True):
        if active:
            gpio.output(self.green_pin, 1)
        else:
            gpio.output(self.green_pin, 0)


if __name__ == "__main__":
    print("Error: Please run main.py")
