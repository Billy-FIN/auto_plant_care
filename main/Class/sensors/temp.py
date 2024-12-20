import machine, utime
from machine import I2C, Pin
from lcd1602 import LCD1602
from dht20 import DHT20

class Temp:
    def __init__(self, scl, sda):
        i2c0 = I2C(0, scl=Pin(scl), sda=Pin(sda), freq=100000)
        self.sensor = DHT20(0x38, i2c0)
        self.read = 0
    
    def work(self):
        self.read = self.sensor.measurements['t']
        print(f'Temperature: {self.read} °C')

    def get_read(self):
        self.work()
        return self.read
