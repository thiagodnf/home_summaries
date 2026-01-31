from homeassistant.components.sensor import SensorDeviceClass

from .GroupSensor import GroupSensor

class AverageTemperatureSensor(GroupSensor):
    
    def __init__(self, hass, device):
        super().__init__(
            hass, 
            device,
            SensorDeviceClass.TEMPERATURE,
            "Average Temperature", 
            "mean"
        )