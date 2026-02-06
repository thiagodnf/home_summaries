from homeassistant.components.sensor import SensorDeviceClass

from .GroupSensor import GroupSensor

class AverageHumiditySensor(GroupSensor):

    def __init__(self, hass, device, label_id):
        super().__init__(
            hass,
            device,
            label_id,
            SensorDeviceClass.HUMIDITY,
            "Average Humidity",
            "mean"
        )
