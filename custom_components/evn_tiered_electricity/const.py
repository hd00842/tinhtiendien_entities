from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "evn_tiered_electricity"
NEN_TANG: list[Platform] = [Platform.SENSOR]

TRUONG_TEN = "ten"
TRUONG_THUC_THE_NGUON = "thuc_the_nguon"
TRUONG_GIA_DIEN_BAC_1 = "gia_dien_bac_1"
TRUONG_GIA_DIEN_BAC_2 = "gia_dien_bac_2"
TRUONG_GIA_DIEN_BAC_3 = "gia_dien_bac_3"
TRUONG_GIA_DIEN_BAC_4 = "gia_dien_bac_4"
TRUONG_GIA_DIEN_BAC_5 = "gia_dien_bac_5"
TRUONG_GIA_DIEN_BAC_6 = "gia_dien_bac_6"
TRUONG_TINH_VAT = "tinh_vat"
TRUONG_TY_LE_VAT = "ty_le_vat"
TRUONG_PHI_CO_DINH = "phi_co_dinh"

DANH_SACH_TRUONG_GIA_DIEN = [
    TRUONG_GIA_DIEN_BAC_1,
    TRUONG_GIA_DIEN_BAC_2,
    TRUONG_GIA_DIEN_BAC_3,
    TRUONG_GIA_DIEN_BAC_4,
    TRUONG_GIA_DIEN_BAC_5,
    TRUONG_GIA_DIEN_BAC_6,
]


GIA_DIEN_MAC_DINH_THEO_BAC: list[float] = [1984.0, 2050.0, 2380.0, 2998.0, 3350.0, 3460.0]



KICH_THUOC_BAC_KWH: list[int | None] = [50, 50, 100, 100, 100, None]

TEN_MAC_DINH = "Tiền điện EVN"
TINH_VAT_MAC_DINH = False
TY_LE_VAT_MAC_DINH = 10.0
PHI_CO_DINH_MAC_DINH = 0.0


ANH_XA_KHOA_CU_SANG_MOI = {
    "name": TRUONG_TEN,
    "source_entity": TRUONG_THUC_THE_NGUON,
    "tier_1_rate": TRUONG_GIA_DIEN_BAC_1,
    "tier_2_rate": TRUONG_GIA_DIEN_BAC_2,
    "tier_3_rate": TRUONG_GIA_DIEN_BAC_3,
    "tier_4_rate": TRUONG_GIA_DIEN_BAC_4,
    "tier_5_rate": TRUONG_GIA_DIEN_BAC_5,
    "tier_6_rate": TRUONG_GIA_DIEN_BAC_6,
    "include_vat": TRUONG_TINH_VAT,
    "vat_rate": TRUONG_TY_LE_VAT,
    "fixed_fee": TRUONG_PHI_CO_DINH,
}

