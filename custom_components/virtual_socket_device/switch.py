# switch.py
from homeassistant.components.switch import SwitchEntity

class VirtualSocketSwitch(SwitchEntity):
    """Virtual Socket Switch."""

    def __init__(self, name: str, entry_id: str):
        self._attr_name = name
        self._is_on = False
        self._entry_id = entry_id
        # Create a unique ID combining entry ID and switch name
        self._unique_id = f"{entry_id}_{name}"

    @property
    def is_on(self):
        return self._is_on

    @property
    def unique_id(self):
        """Return a unique ID for the entity."""
        return self._unique_id

    async def async_turn_on(self):
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self):
        self._is_on = False
        self.async_write_ha_state()


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up switch from config entry."""
    switch_name = entry.data["switch_name"]
    async_add_entities([VirtualSocketSwitch(switch_name, entry.entry_id)])

