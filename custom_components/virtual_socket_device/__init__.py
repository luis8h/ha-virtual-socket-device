from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "virtual_socket_device"

async def async_setup(hass: HomeAssistant, config: dict):
    # If your integration only works via config entries, you can skip this
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the integration from a config entry."""
    # This is called when the user enables the integration via the UI
    # You can store info in hass.data if needed
    hass.data.setdefault(DOMAIN, {})
    # For example, store an empty dict or connection object
    hass.data[DOMAIN][entry.entry_id] = {}
    return True

