from .const import DOMAIN

async def async_setup(hass, config):
    """Set up the integration (does nothing for now)."""
    return True

async def async_setup_entry(hass, entry):
    """Forward the entry to the switch platform."""
    # Forward the entry to the switch platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["switch"])
    )
    return True

