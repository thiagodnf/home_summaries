from homeassistant.components.sensor import SensorDeviceClass

from .GroupSensor import GroupSensor

class AverageHumiditySensor(GroupSensor):
    
    def __init__(self, hass, device):
        super().__init__(
            hass, 
            device,
            SensorDeviceClass.HUMIDITY, 
            "Average Humidity", 
            "mean"
        )