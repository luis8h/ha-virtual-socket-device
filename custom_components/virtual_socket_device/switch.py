from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_ON

class VirtualSocketSwitch(SwitchEntity):
    """Virtual Socket Switch."""

    def __init__(self, name: str, entry):
        self._attr_name = name
        self._is_on = False
        self._entry = entry
        self._unique_id = f"{entry.entry_id}_{name}"

    @property
    def is_on(self):
        # If a linked switch is set, mirror its state
        linked = self._entry.options.get("linked_switch")
        if linked:
            return self.hass.states.is_state(linked, STATE_ON)
        return self._is_on

    @property
    def unique_id(self):
        return self._unique_id

    async def async_turn_on(self):
        linked = self._entry.options.get("linked_switch")
        if linked:
            await self.hass.services.async_call(
                "switch", "turn_on", {"entity_id": linked}
            )
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self):
        linked = self._entry.options.get("linked_switch")
        if linked:
            await self.hass.services.async_call(
                "switch", "turn_off", {"entity_id": linked}
            )
        self._is_on = False
        self.async_write_ha_state()


async def async_setup_entry(hass, entry, async_add_entities):
    switch_name = entry.data["switch_name"]
    async_add_entities([VirtualSocketSwitch(switch_name, entry)])

