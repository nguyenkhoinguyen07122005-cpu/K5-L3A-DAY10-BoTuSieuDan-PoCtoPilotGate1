# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): BoTuSieuDan
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-BoTuSieuDan-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): (ghi số thẻ sau phút 125)

## Thành viên

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Khôi Nguyên | 2A202603453 | Kỹ sư cổng | ✅ |
|   2 | Dương Văn Công | 2A202603468 | Sản phẩm và kinh doanh | |
|   3 | Lê Quang Huy | 2A202603470 | Vận hành và pháp lý | |
|   4 | Vũ Xuân Trường | 2A202603433 | Kỹ sư cổng | |

`members` trong `submission/submission.json`: `NguyenKhoiNguyen-2A202603453`, `DuongVanCong-2A202603468`, `LeQuangHuy-2A202603470`, `VuXuanTruong-2A202603433`.

Ghi chú: Bản tiêu chí (`config/acceptance_criteria.json`) ký một lần lúc 2026-11-18T15:18:25 (commit `71e16ae`): người ký Dương Văn Công, chứng kiến Nguyễn Khôi Nguyên, Lê Quang Huy và Vũ Xuân Trường. File bị khoá bằng hash nên không sửa sau khi ký. Cả bàn 4 người cùng chịu trách nhiệm về các ngưỡng trong Phiếu A.

## Cá nhân

## NguyenKhoiNguyen-2A202603453

### Phần việc phụ trách

Kỹ sư cổng, trưởng nhóm. Viết `lab10/guards.py` (cổng G0–G4: ghim chính sách theo ngày, đối chiếu số tiền hoàn và phê duyệt với sổ cái, lỗi hãng cần nguyên nhân đã ghi, lọc trường gửi hãng) và `lab10/monitors.py` (chỉ số theo dõi mới). Chạy lệnh 1–5, chốt cổng vòng 1. Phiếu B mục B7–B8 (các số đo base, after, prepared) và các câu 2.6–2.10.

### Đóng góp cụ thể

- Dựng `pre_guard` và `write_gate` cho bốn loại ghi: hoàn tiền, báo lỗi hãng, báo hãng, trả lời khách.
- Thêm các chỉ số theo dõi: tỉ lệ model bị cổng sửa, tỉ lệ ticket có chỉ thị lạ, chi phí mỗi ticket, tải hàng chờ giờ cao điểm.
- Ký tiêu chí rồi mới đo; đối chiếu số đo `base` → `after` → `prepared` và ghi vào Phiếu B.
- Dùng trợ lý AI (Claude) để đọc code, soạn nháp cổng và soát câu chữ phiếu. Cả bàn đã đọc lại; các ngưỡng và quyết định do cả bàn chốt.

### Bằng chứng

Commit `71e16ae` (Sign acceptance criteria), commit "LAB 10: chốt cổng vòng 1, quyết định v1" (chốt cổng vòng 1). Mã lần chạy: `R-base-before-20261118-151902-455ee1`, `R-base-after-20261118-151902-455ee1`, `R-base-prepared-20261118-151903-455ee1`.

### Exit ticket

Điều học được: cổng nằm ngoài model và đối chiếu với sổ cái đáng tin hơn là dặn model trong prompt. Điều còn chưa chắc: cổng đã đủ cho các ca ngoài bộ test đo hay chưa.

## DuongVanCong-2A202603468

### Phần việc phụ trách

Sản phẩm và kinh doanh. Phiếu A (A1–A5), `config/acceptance_criteria.json` (ngưỡng `pass_rate`, `pass_k`, trần hoàn sai, trần lỗi hãng oan, chi phí mỗi ticket, ROI), người ký tiêu chí. Mục `business` trong `config/operating_gates.json` (ngân sách chi phí mỗi ticket, phạm vi pilot, `roi_min`), quyết định v1 ở Phiếu B mục B8.

### Đóng góp cụ thể

- Chọn ngưỡng bắt buộc (`pass_rate` ≥ 0,95; `pass_k` ≥ 0,9; hoàn sai 0đ; lỗi hãng oan 0; lộ PII 0) và ngưỡng kinh doanh (chi phí ≤ 8.000đ/ticket, ROI ≥ 0,5, không ca ùn).
- Viết các câu tiêu chí "Nếu … thì chúng tôi sẽ …" và luật quyết định Tiếp tục / Chỉnh / Dừng.
- Ký tiêu chí trước lần đánh giá đầu tiên.
- Đọc chi phí mỗi ticket và ROI khi tính lại với 1 và 2 người trực (4.456đ, ROI 1,24 với 1 người; 5.820đ, ROI 0,72 với 2 người), từ đó chọn giữ 1 người trực.
- Dùng trợ lý AI (Claude) để soạn nháp và soát câu chữ Phiếu A; ngưỡng do bàn chọn và Công giải thích được.

### Bằng chứng

Commit `71e16ae` (ký tiêu chí); `config/acceptance_criteria.json` và `.lock` (hash `a1a2c3dc`); Phiếu A mục A1–A5; Phiếu B mục B8.

### Exit ticket

Điều học được: ngưỡng phải ký trước khi biết kết quả đo, nếu không thì ngưỡng chỉ là cách giải thích cho số đã có. Điều còn chưa chắc: ngưỡng chi phí 8.000đ/ticket có còn hợp lý khi số người trực tăng lên lúc mở rộng pilot.

## LeQuangHuy-2A202603470

### Phần việc phụ trách

Vận hành và pháp lý. `config/operating_gates.json` mục `operations` và `legal` (trần hoàn tiền ngày, người trực NV-TUNG, người duyệt NV-HANH, năng lực duyệt mỗi giờ, thời gian chờ tối đa, điều kiện dừng, kênh cảnh báo, các trường dữ liệu cấm gửi bên thứ ba). Phiếu B: HAZOP mở rộng, checklist 9 nhóm việc có PIC, runbook phần 1–3 và giờ cao điểm. Sẽ gom bài nộp (`submission/`) ở vòng 2.

### Đóng góp cụ thể

- Xác định người trực, người duyệt, 6 ca duyệt mỗi giờ và mức chờ tối đa 45 phút; điều kiện dừng một phần và dừng hẳn.
- Liệt kê các trường PII bị chặn khi gửi hãng (`recipient_contact`, `customer_note`, `recipient`, `name`, `phone`, `street`, `address`, `email`) và quy tắc lỗi hãng chỉ ghi khi có nguyên nhân đã được ghi.
- Viết các dòng HAZOP ngoài kỹ thuật (người duyệt, bên thứ ba, quy trình) và gắn PIC có tên cho từng nhóm việc trong checklist.
- Viết runbook 1–3 khớp với con số trong config (trần 1.500.000đ/ngày, 45 phút, 1 người trực).
- Dùng trợ lý AI (Claude) để soạn nháp và soát câu chữ; Huy đã đọc lại các con số trong config và runbook.

### Bằng chứng

`config/operating_gates.json` và bản chốt `config/operating_gates.round1.json`; Phiếu B mục B4–B6 và runbook; `config/round1.lock` (hash `a4c8b3f8`); commit "LAB 10: chốt cổng vòng 1, quyết định v1".

### Exit ticket

Điều học được: cổng con số (trần tiền, hàng chờ, điều kiện dừng) và cổng code bổ trợ nhau, và con số nào cũng cần một người có tên chịu trách nhiệm. Điều còn chưa chắc: một người duyệt trực ca có chịu nổi giờ cao điểm thật không, vì mô phỏng chỉ có 22 ticket mỗi ngày.

## VuXuanTruong-2A202603433

### Phần việc phụ trách

Kỹ sư cổng (người thứ hai cùng Nguyên). Đọc trace và đối chiếu cổng với số đo: dò trace ca `T-002@55`, soát lại cổng G1–G4 theo từng loại ghi, kiểm chéo các số trong Phiếu B mục B7 với report. Ở vòng 2: dò trace sự cố, sửa cổng và thêm chỉ số theo dõi trong `lab10/guards.py` và `lab10/monitors.py` cùng Nguyên.

### Đóng góp cụ thể

- Đọc trace `T-002@55` từng bước: model lấy 5 ngày trễ từ lời khách trong khi sổ vận đơn ghi 2 ngày, dẫn tới hoàn 20.000đ sai và ghi lỗi hãng oan cho VNX.
- Soát từng cổng: G1–G2 đối chiếu số tiền và phê duyệt với DB, G3 lỗi hãng cần nguyên nhân đã ghi, G4 chỉ gửi hãng các trường được phép.
- Kiểm chéo số liệu ba mốc: base `pass_rate` 0,9909; after và prepared 1,0; hoàn sai 20.000đ → 0đ.
- Dùng trợ lý AI (Claude) để giải thích code và soát câu chữ; Trường đã đọc lại cổng và số liệu trước khi nộp.

### Bằng chứng

Mã lần chạy `R-base-before-20261118-151902-455ee1`, `R-base-after-20261118-151902-455ee1`, `R-base-prepared-20261118-151903-455ee1`; trace `T-002@55`; `lab10/guards.py` và Phiếu B mục B7.

### Exit ticket

Điều học được: một ca hỏng trong 110 lần chạy (0,9909) vẫn có thể là 20.000đ hoàn sai và một lỗi ghi oan cho hãng, nên phải đọc trace chứ không chỉ nhìn tỉ lệ. Điều còn chưa chắc: các cổng đã chặn được những ca tương tự mà bộ test ẩn đưa vào hay chưa.
