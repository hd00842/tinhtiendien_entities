# Tính tiền điện EVN (Home Assistant Custom Component)

Component tùy chỉnh để tính tiền điện lũy tiến 6 bậc từ một thực thể điện năng (kWh).

## Thêm nhanh vào HACS

[![Mở Home Assistant của bạn và thêm repository này vào HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=trungdung&repository=tinh_tien_theo_EVN&category=integration)

> Nếu bạn đổi tên repo hoặc owner trên GitHub, hãy cập nhật lại `owner` và `repository` trong link badge ở trên.

## Tính năng

- Chọn thực thể nguồn điện năng (ví dụ: `sensor.dien_nang_thang`).
- Tính tiền theo 6 bậc EVN.
- Cho phép tùy chỉnh giá điện từng bậc.
- Nếu không nhập, dùng giá gợi ý:
  - 1984, 2050, 2380, 2998, 3350, 3460 (VND/kWh).
- Có tùy chọn:
  - Bật/tắt VAT (`tinh_vat`)
  - Tỷ lệ VAT (`ty_le_vat`)
  - Phí cố định (`phi_co_dinh`)
- Tạo nhiều sensor:
  - Tổng tiền điện
  - Đơn giá trung bình/kWh
  - Chi phí từng bậc (1 đến 6)

## Cài đặt

1. Chép thư mục `custom_components/evn_tiered_electricity` vào thư mục config Home Assistant:

   ```text
   <config>/custom_components/evn_tiered_electricity
   ```

2. Khởi động lại Home Assistant.
3. Vào `Cài đặt -> Thiết bị & Dịch vụ -> Thêm tích hợp`.
4. Chọn `Tính tiền điện EVN`.
