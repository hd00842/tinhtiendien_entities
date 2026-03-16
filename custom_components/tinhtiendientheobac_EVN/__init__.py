from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import ANH_XA_KHOA_CU_SANG_MOI, NEN_TANG


def _doi_khoa_cu_sang_moi(du_lieu: dict) -> dict:
    du_lieu_moi = {}
    for khoa, gia_tri in du_lieu.items():
        khoa_moi = ANH_XA_KHOA_CU_SANG_MOI.get(khoa, khoa)
        du_lieu_moi[khoa_moi] = gia_tri
    return du_lieu_moi


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    du_lieu_da_doi = _doi_khoa_cu_sang_moi(dict(entry.data))
    tuy_chon_da_doi = _doi_khoa_cu_sang_moi(dict(entry.options))

    if du_lieu_da_doi != entry.data or tuy_chon_da_doi != entry.options:
        hass.config_entries.async_update_entry(
            entry,
            data=du_lieu_da_doi,
            options=tuy_chon_da_doi,
        )

    await hass.config_entries.async_forward_entry_setups(entry, NEN_TANG)
    entry.async_on_unload(entry.add_update_listener(_xu_ly_cap_nhat_tuy_chon))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, NEN_TANG)


async def _xu_ly_cap_nhat_tuy_chon(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)

