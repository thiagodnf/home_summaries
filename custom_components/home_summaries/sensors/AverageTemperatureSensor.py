from homeassistant.components.sensor import SensorDeviceClass

from .GroupSensor import GroupSensor

class AverageTemperatureSensor(GroupSensor):

    def __init__(self, hass, device, label_id):
        super().__init__(
            hass,
            device,
            label_id,
            SensorDeviceClass.TEMPERATURE,
            "Average Temperature",
            "mean"
        )
