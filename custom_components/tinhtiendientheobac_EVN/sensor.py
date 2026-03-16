from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    ANH_XA_KHOA_CU_SANG_MOI,
    DANH_SACH_TRUONG_GIA_DIEN,
    GIA_DIEN_MAC_DINH_THEO_BAC,
    KICH_THUOC_BAC_KWH,
    PHI_CO_DINH_MAC_DINH,
    TEN_MAC_DINH,
    TINH_VAT_MAC_DINH,
    TRUONG_PHI_CO_DINH,
    TRUONG_TEN,
    TRUONG_THUC_THE_NGUON,
    TRUONG_TINH_VAT,
    TRUONG_TY_LE_VAT,
    TY_LE_VAT_MAC_DINH,
)


def _lay_gia_tri_tu_entry(entry: ConfigEntry, khoa_moi: str, gia_tri_mac_dinh: Any) -> Any:
    if khoa_moi in entry.options:
        return entry.options[khoa_moi]
    if khoa_moi in entry.data:
        return entry.data[khoa_moi]

    for khoa_cu, khoa_moi_tuong_ung in ANH_XA_KHOA_CU_SANG_MOI.items():
        if khoa_moi_tuong_ung != khoa_moi:
            continue
        if khoa_cu in entry.options:
            return entry.options[khoa_cu]
        if khoa_cu in entry.data:
            return entry.data[khoa_cu]

    return gia_tri_mac_dinh


@dataclass
class DuLieuTinhToanEVN:

    dien_nang_tieu_thu_kwh: float
    chi_tiet_tung_bac: list[dict[str, float | int]]
    chi_phi_nen_vnd: float
    phi_co_dinh_vnd: float
    tam_tinh_truoc_vat_vnd: float
    tinh_vat: bool
    ty_le_vat_phan_tram: float
    tien_vat_vnd: float
    tong_chi_phi_vnd: float
    don_gia_trung_binh_vnd_kwh: float | None


def _tinh_chi_phi_luy_tien(
    dien_nang_tieu_thu_kwh: float,
    ds_gia_dien: list[float],
) -> tuple[float, list[dict[str, float | int]]]:
    con_lai_kwh = max(dien_nang_tieu_thu_kwh, 0.0)
    tong_chi_phi = 0.0
    chi_tiet_tung_bac: list[dict[str, float | int]] = []

    for chi_so, don_gia in enumerate(ds_gia_dien):
        kich_thuoc_bac = KICH_THUOC_BAC_KWH[chi_so]
        if con_lai_kwh <= 0:
            san_luong_bac = 0.0
        elif kich_thuoc_bac is None:
            san_luong_bac = con_lai_kwh
        else:
            san_luong_bac = min(con_lai_kwh, float(kich_thuoc_bac))

        chi_phi_bac = san_luong_bac * don_gia
        tong_chi_phi += chi_phi_bac
        con_lai_kwh -= san_luong_bac

        chi_tiet_tung_bac.append(
            {
                "bac": chi_so + 1,
                "san_luong_kwh": round(san_luong_bac, 3),
                "don_gia_vnd_kwh": float(don_gia),
                "chi_phi_vnd": round(chi_phi_bac, 3),
            }
        )

    return tong_chi_phi, chi_tiet_tung_bac


class BoTinhToanEVN:

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.thuc_the_nguon = str(_lay_gia_tri_tu_entry(entry, TRUONG_THUC_THE_NGUON, ""))
        self.ds_gia_dien = [
            float(_lay_gia_tri_tu_entry(entry, truong, GIA_DIEN_MAC_DINH_THEO_BAC[chi_so]))
            for chi_so, truong in enumerate(DANH_SACH_TRUONG_GIA_DIEN)
        ]
        self.tinh_vat = bool(_lay_gia_tri_tu_entry(entry, TRUONG_TINH_VAT, TINH_VAT_MAC_DINH))
        self.ty_le_vat = float(_lay_gia_tri_tu_entry(entry, TRUONG_TY_LE_VAT, TY_LE_VAT_MAC_DINH))
        self.phi_co_dinh = float(
            _lay_gia_tri_tu_entry(entry, TRUONG_PHI_CO_DINH, PHI_CO_DINH_MAC_DINH)
        )
        self._danh_sach_lang_nghe: list[Callable[[], None]] = []
        self._huy_theo_doi = None
        self.du_lieu: DuLieuTinhToanEVN | None = None

    def bat_dau(self) -> None:
        self._cap_nhat_tu_nguon()
        self._huy_theo_doi = async_track_state_change_event(
            self.hass,
            [self.thuc_the_nguon],
            self._xu_ly_khi_thuc_the_nguon_thay_doi,
        )

    def dung(self) -> None:
        if self._huy_theo_doi is not None:
            self._huy_theo_doi()
            self._huy_theo_doi = None

    def dang_co_lang_nghe(self) -> bool:
        return bool(self._danh_sach_lang_nghe)

    def dang_ky_lang_nghe(self, ham_lang_nghe: Callable[[], None]) -> Callable[[], None]:
        self._danh_sach_lang_nghe.append(ham_lang_nghe)

        def _go_bo() -> None:
            if ham_lang_nghe in self._danh_sach_lang_nghe:
                self._danh_sach_lang_nghe.remove(ham_lang_nghe)

        return _go_bo

    @callback
    def _thong_bao_cap_nhat(self) -> None:
        for ham_lang_nghe in list(self._danh_sach_lang_nghe):
            ham_lang_nghe()

    @callback
    def _xu_ly_khi_thuc_the_nguon_thay_doi(self, _event) -> None:
        self._cap_nhat_tu_nguon()
        self._thong_bao_cap_nhat()

    @callback
    def _cap_nhat_tu_nguon(self) -> None:
        state_nguon = self.hass.states.get(self.thuc_the_nguon)

        if state_nguon is None or state_nguon.state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            self.du_lieu = None
            return

        try:
            dien_nang_tieu_thu_kwh = float(state_nguon.state)
        except (TypeError, ValueError):
            self.du_lieu = None
            return

        dien_nang_tieu_thu_kwh = round(max(dien_nang_tieu_thu_kwh, 0.0), 3)
        chi_phi_nen_vnd, chi_tiet_tung_bac = _tinh_chi_phi_luy_tien(
            dien_nang_tieu_thu_kwh,
            self.ds_gia_dien,
        )
        tam_tinh_truoc_vat_vnd = chi_phi_nen_vnd + self.phi_co_dinh
        tien_vat_vnd = tam_tinh_truoc_vat_vnd * (self.ty_le_vat / 100.0) if self.tinh_vat else 0.0
        tong_chi_phi_vnd = tam_tinh_truoc_vat_vnd + tien_vat_vnd

        don_gia_trung_binh_vnd_kwh = None
        if dien_nang_tieu_thu_kwh > 0:
            don_gia_trung_binh_vnd_kwh = tong_chi_phi_vnd / dien_nang_tieu_thu_kwh

        self.du_lieu = DuLieuTinhToanEVN(
            dien_nang_tieu_thu_kwh=dien_nang_tieu_thu_kwh,
            chi_tiet_tung_bac=chi_tiet_tung_bac,
            chi_phi_nen_vnd=round(chi_phi_nen_vnd, 3),
            phi_co_dinh_vnd=round(self.phi_co_dinh, 3),
            tam_tinh_truoc_vat_vnd=round(tam_tinh_truoc_vat_vnd, 3),
            tinh_vat=self.tinh_vat,
            ty_le_vat_phan_tram=round(self.ty_le_vat, 3),
            tien_vat_vnd=round(tien_vat_vnd, 3),
            tong_chi_phi_vnd=round(tong_chi_phi_vnd, 3),
            don_gia_trung_binh_vnd_kwh=(
                round(don_gia_trung_binh_vnd_kwh, 3)
                if don_gia_trung_binh_vnd_kwh is not None
                else None
            ),
        )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    bo_tinh_toan = BoTinhToanEVN(hass, entry)
    bo_tinh_toan.bat_dau()

    danh_sach_sensor: list[SensorEntity] = [
        CamBienTongTienEVN(entry, bo_tinh_toan),
        CamBienDonGiaTrungBinhEVN(entry, bo_tinh_toan),
    ]
    danh_sach_sensor.extend(
        CamBienChiPhiBacEVN(entry, bo_tinh_toan, chi_so_bac)
        for chi_so_bac in range(len(DANH_SACH_TRUONG_GIA_DIEN))
    )
    async_add_entities(danh_sach_sensor)


class CamBienCoSoEVN(SensorEntity):

    _go_bo_lang_nghe = None

    def __init__(self, entry: ConfigEntry, bo_tinh_toan: BoTinhToanEVN) -> None:
        self._entry = entry
        self._bo_tinh_toan = bo_tinh_toan
        self._ten_co_so = str(_lay_gia_tri_tu_entry(entry, TRUONG_TEN, TEN_MAC_DINH))

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def available(self) -> bool:
        return self._bo_tinh_toan.du_lieu is not None

    async def async_added_to_hass(self) -> None:
        self._go_bo_lang_nghe = self._bo_tinh_toan.dang_ky_lang_nghe(self._cap_nhat_state)

    async def async_will_remove_from_hass(self) -> None:
        if self._go_bo_lang_nghe is not None:
            self._go_bo_lang_nghe()
            self._go_bo_lang_nghe = None

        if not self._bo_tinh_toan.dang_co_lang_nghe():
            self._bo_tinh_toan.dung()

    @callback
    def _cap_nhat_state(self) -> None:
        self.async_write_ha_state()


class CamBienTongTienEVN(CamBienCoSoEVN):

    _attr_icon = "mdi:cash-multiple"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "VND"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, entry: ConfigEntry, bo_tinh_toan: BoTinhToanEVN) -> None:
        super().__init__(entry, bo_tinh_toan)
        self._attr_unique_id = f"{entry.entry_id}_tong_tien_dien"
        self._attr_name = f"{self._ten_co_so} - Tổng tiền điện"

    @property
    def native_value(self) -> int | None:
        if self._bo_tinh_toan.du_lieu is None:
            return None
        return int(round(self._bo_tinh_toan.du_lieu.tong_chi_phi_vnd))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        du_lieu = self._bo_tinh_toan.du_lieu
        if du_lieu is None:
            return {}

        return {
            "thuc_the_nguon": self._bo_tinh_toan.thuc_the_nguon,
            "dien_nang_tieu_thu_kwh": du_lieu.dien_nang_tieu_thu_kwh,
            "gia_dien_theo_bac_vnd_kwh": self._bo_tinh_toan.ds_gia_dien,
            "chi_phi_nen_vnd": int(round(du_lieu.chi_phi_nen_vnd)),
            "phi_co_dinh_vnd": int(round(du_lieu.phi_co_dinh_vnd)),
            "tam_tinh_truoc_vat_vnd": int(round(du_lieu.tam_tinh_truoc_vat_vnd)),
            "tinh_vat": du_lieu.tinh_vat,
            "ty_le_vat_phan_tram": du_lieu.ty_le_vat_phan_tram,
            "tien_vat_vnd": int(round(du_lieu.tien_vat_vnd)),
            "don_gia_trung_binh_vnd_kwh": du_lieu.don_gia_trung_binh_vnd_kwh,
            "chi_tiet_tung_bac": du_lieu.chi_tiet_tung_bac,
            "phuong_phap_tinh": "luy_tien_6_bac",
        }


class CamBienDonGiaTrungBinhEVN(CamBienCoSoEVN):

    _attr_icon = "mdi:sigma"
    _attr_native_unit_of_measurement = "VND/kWh"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, entry: ConfigEntry, bo_tinh_toan: BoTinhToanEVN) -> None:
        super().__init__(entry, bo_tinh_toan)
        self._attr_unique_id = f"{entry.entry_id}_don_gia_trung_binh"
        self._attr_name = f"{self._ten_co_so} - Đơn giá trung bình/kWh"

    @property
    def native_value(self) -> float | None:
        if self._bo_tinh_toan.du_lieu is None:
            return None
        return self._bo_tinh_toan.du_lieu.don_gia_trung_binh_vnd_kwh

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        du_lieu = self._bo_tinh_toan.du_lieu
        if du_lieu is None:
            return {}
        return {
            "dien_nang_tieu_thu_kwh": du_lieu.dien_nang_tieu_thu_kwh,
            "tong_chi_phi_vnd": int(round(du_lieu.tong_chi_phi_vnd)),
            "tinh_vat": du_lieu.tinh_vat,
            "ty_le_vat_phan_tram": du_lieu.ty_le_vat_phan_tram,
            "phi_co_dinh_vnd": int(round(du_lieu.phi_co_dinh_vnd)),
        }


class CamBienChiPhiBacEVN(CamBienCoSoEVN):

    _attr_icon = "mdi:stairs"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "VND"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        entry: ConfigEntry,
        bo_tinh_toan: BoTinhToanEVN,
        chi_so_bac: int,
    ) -> None:
        super().__init__(entry, bo_tinh_toan)
        self._chi_so_bac = chi_so_bac
        so_bac = chi_so_bac + 1
        self._attr_unique_id = f"{entry.entry_id}_chi_phi_bac_{so_bac}"
        self._attr_name = f"{self._ten_co_so} - Chi phí bậc {so_bac}"

    @property
    def native_value(self) -> int | None:
        du_lieu = self._bo_tinh_toan.du_lieu
        if du_lieu is None:
            return None
        du_lieu_bac = du_lieu.chi_tiet_tung_bac[self._chi_so_bac]
        return int(round(float(du_lieu_bac["chi_phi_vnd"])))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        du_lieu = self._bo_tinh_toan.du_lieu
        if du_lieu is None:
            return {}
        du_lieu_bac = du_lieu.chi_tiet_tung_bac[self._chi_so_bac]
        return {
            "bac": du_lieu_bac["bac"],
            "san_luong_kwh": du_lieu_bac["san_luong_kwh"],
            "don_gia_vnd_kwh": du_lieu_bac["don_gia_vnd_kwh"],
            "chi_phi_vnd": int(round(float(du_lieu_bac["chi_phi_vnd"]))),
        }

