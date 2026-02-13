import statistics

from ..utils.Entity import get_state_value_as_float
from ..HSSensorEntity import HSSensorEntity

class AverageSensorEntity(HSSensorEntity):

  def async_calculate_state(self):
    """Perform the mean calculation."""
    values = []

    for entity_id in self._entity_ids:

      state = get_state_value_as_float(self.hass, entity_id)

      if not state:
        continue

      values.append(state)

    if not values:
      return None

    return round(statistics.mean(values), 2)
