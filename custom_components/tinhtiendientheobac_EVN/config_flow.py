from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    ANH_XA_KHOA_CU_SANG_MOI,
    DANH_SACH_TRUONG_GIA_DIEN,
    DOMAIN,
    GIA_DIEN_MAC_DINH_THEO_BAC,
    PHI_CO_DINH_MAC_DINH,
    TEN_MAC_DINH,
    TINH_VAT_MAC_DINH,
    TRUONG_GIA_DIEN_BAC_1,
    TRUONG_GIA_DIEN_BAC_2,
    TRUONG_GIA_DIEN_BAC_3,
    TRUONG_GIA_DIEN_BAC_4,
    TRUONG_GIA_DIEN_BAC_5,
    TRUONG_GIA_DIEN_BAC_6,
    TRUONG_PHI_CO_DINH,
    TRUONG_TEN,
    TRUONG_THUC_THE_NGUON,
    TRUONG_TINH_VAT,
    TRUONG_TY_LE_VAT,
    TY_LE_VAT_MAC_DINH,
)


def _gia_tri_tu_mapping_theo_khoa_cu(
    mapping_du_lieu: Mapping[str, Any],
    khoa_moi: str,
    gia_tri_mac_dinh: Any,
) -> Any:
    if khoa_moi in mapping_du_lieu:
        return mapping_du_lieu[khoa_moi]

    for khoa_cu, khoa_moi_tuong_ung in ANH_XA_KHOA_CU_SANG_MOI.items():
        if khoa_moi_tuong_ung == khoa_moi and khoa_cu in mapping_du_lieu:
            return mapping_du_lieu[khoa_cu]

    return gia_tri_mac_dinh


def _tao_luoc_do_form(mac_dinh: Mapping[str, Any]) -> vol.Schema:
    mac_dinh_thuc_the = _gia_tri_tu_mapping_theo_khoa_cu(
        mac_dinh,
        TRUONG_THUC_THE_NGUON,
        None,
    )
    truong_thuc_the: Any
    if mac_dinh_thuc_the:
        truong_thuc_the = vol.Required(TRUONG_THUC_THE_NGUON, default=mac_dinh_thuc_the)
    else:
        truong_thuc_the = vol.Required(TRUONG_THUC_THE_NGUON)

    return vol.Schema(
        {
            vol.Optional(
                TRUONG_TEN,
                default=_gia_tri_tu_mapping_theo_khoa_cu(mac_dinh, TRUONG_TEN, TEN_MAC_DINH),
            ): str,
            truong_thuc_the: selector.EntitySelector(
                selector.EntitySelectorConfig(
                    multiple=False,
                )
            ),
            vol.Optional(
                TRUONG_GIA_DIEN_BAC_1,
                default=_gia_tri_tu_mapping_theo_khoa_cu(
                    mac_dinh, TRUONG_GIA_DIEN_BAC_1, GIA_DIEN_MAC_DINH_THEO_BAC[0]
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=100000,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="VND/kWh",
                )
            ),
            vol.Optional(
                TRUONG_GIA_DIEN_BAC_2,
                default=_gia_tri_tu_mapping_theo_khoa_cu(
                    mac_dinh, TRUONG_GIA_DIEN_BAC_2, GIA_DIEN_MAC_DINH_THEO_BAC[1]
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=100000,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="VND/kWh",
                )
            ),
            vol.Optional(
                TRUONG_GIA_DIEN_BAC_3,
                default=_gia_tri_tu_mapping_theo_khoa_cu(
                    mac_dinh, TRUONG_GIA_DIEN_BAC_3, GIA_DIEN_MAC_DINH_THEO_BAC[2]
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=100000,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="VND/kWh",
                )
            ),
            vol.Optional(
                TRUONG_GIA_DIEN_BAC_4,
                default=_gia_tri_tu_mapping_theo_khoa_cu(
                    mac_dinh, TRUONG_GIA_DIEN_BAC_4, GIA_DIEN_MAC_DINH_THEO_BAC[3]
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=100000,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="VND/kWh",
                )
            ),
            vol.Optional(
                TRUONG_GIA_DIEN_BAC_5,
                default=_gia_tri_tu_mapping_theo_khoa_cu(
                    mac_dinh, TRUONG_GIA_DIEN_BAC_5, GIA_DIEN_MAC_DINH_THEO_BAC[4]
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=100000,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="VND/kWh",
                )
            ),
            vol.Optional(
                TRUONG_GIA_DIEN_BAC_6,
                default=_gia_tri_tu_mapping_theo_khoa_cu(
                    mac_dinh, TRUONG_GIA_DIEN_BAC_6, GIA_DIEN_MAC_DINH_THEO_BAC[5]
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=100000,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="VND/kWh",
                )
            ),
            vol.Optional(
                TRUONG_TINH_VAT,
                default=_gia_tri_tu_mapping_theo_khoa_cu(
                    mac_dinh,
                    TRUONG_TINH_VAT,
                    TINH_VAT_MAC_DINH,
                ),
            ): selector.BooleanSelector(),
            vol.Optional(
                TRUONG_TY_LE_VAT,
                default=_gia_tri_tu_mapping_theo_khoa_cu(
                    mac_dinh,
                    TRUONG_TY_LE_VAT,
                    TY_LE_VAT_MAC_DINH,
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=100,
                    step=0.1,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="%",
                )
            ),
            vol.Optional(
                TRUONG_PHI_CO_DINH,
                default=_gia_tri_tu_mapping_theo_khoa_cu(
                    mac_dinh,
                    TRUONG_PHI_CO_DINH,
                    PHI_CO_DINH_MAC_DINH,
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=1000000000,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="VND",
                )
            ),
        }
    )


def _chuan_hoa_du_lieu_nhap(du_lieu_nhap: dict[str, Any]) -> dict[str, Any]:
    du_lieu = dict(du_lieu_nhap)
    for chi_so, truong_gia in enumerate(DANH_SACH_TRUONG_GIA_DIEN):
        gia_tri = du_lieu.get(truong_gia, GIA_DIEN_MAC_DINH_THEO_BAC[chi_so])
        du_lieu[truong_gia] = float(gia_tri)

    du_lieu[TRUONG_TINH_VAT] = bool(du_lieu.get(TRUONG_TINH_VAT, TINH_VAT_MAC_DINH))
    du_lieu[TRUONG_TY_LE_VAT] = float(du_lieu.get(TRUONG_TY_LE_VAT, TY_LE_VAT_MAC_DINH))
    du_lieu[TRUONG_PHI_CO_DINH] = float(du_lieu.get(TRUONG_PHI_CO_DINH, PHI_CO_DINH_MAC_DINH))
    du_lieu[TRUONG_TEN] = du_lieu.get(TRUONG_TEN, TEN_MAC_DINH)
    return du_lieu


class EVNTinhTienDienConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(
        self,
        du_lieu_nhap: dict[str, Any] | None = None,
    ) -> config_entries.FlowResult:
        loi: dict[str, str] = {}

        if du_lieu_nhap is not None:
            du_lieu_nhap = _chuan_hoa_du_lieu_nhap(du_lieu_nhap)
            thuc_the_nguon = du_lieu_nhap[TRUONG_THUC_THE_NGUON]

            if self.hass.states.get(thuc_the_nguon) is None:
                loi["base"] = "khong_tim_thay_thuc_the"
            elif any(du_lieu_nhap[truong] < 0 for truong in DANH_SACH_TRUONG_GIA_DIEN):
                loi["base"] = "gia_tri_khong_hop_le"
            elif du_lieu_nhap[TRUONG_TY_LE_VAT] < 0 or du_lieu_nhap[TRUONG_PHI_CO_DINH] < 0:
                loi["base"] = "gia_tri_khong_hop_le"
            else:
                await self.async_set_unique_id(thuc_the_nguon)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=du_lieu_nhap[TRUONG_TEN],
                    data=du_lieu_nhap,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=_tao_luoc_do_form({}),
            errors=loi,
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "EVNTinhTienDienOptionsFlow":
        return EVNTinhTienDienOptionsFlow(config_entry)


class EVNTinhTienDienOptionsFlow(config_entries.OptionsFlow):

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(
        self,
        du_lieu_nhap: dict[str, Any] | None = None,
    ) -> config_entries.FlowResult:
        loi: dict[str, str] = {}

        if du_lieu_nhap is not None:
            du_lieu_nhap = _chuan_hoa_du_lieu_nhap(du_lieu_nhap)
            thuc_the_nguon = du_lieu_nhap[TRUONG_THUC_THE_NGUON]

            if self.hass.states.get(thuc_the_nguon) is None:
                loi["base"] = "khong_tim_thay_thuc_the"
            elif any(du_lieu_nhap[truong] < 0 for truong in DANH_SACH_TRUONG_GIA_DIEN):
                loi["base"] = "gia_tri_khong_hop_le"
            elif du_lieu_nhap[TRUONG_TY_LE_VAT] < 0 or du_lieu_nhap[TRUONG_PHI_CO_DINH] < 0:
                loi["base"] = "gia_tri_khong_hop_le"
            else:
                return self.async_create_entry(title="", data=du_lieu_nhap)

        mac_dinh = {**self._config_entry.data, **self._config_entry.options}
        return self.async_show_form(
            step_id="init",
            data_schema=_tao_luoc_do_form(mac_dinh),
            errors=loi,
        )
