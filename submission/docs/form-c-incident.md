# Phiếu C · Sự cố và quyết định v2 · Khối 3 (phút 125–200)

**Bàn:** BoTuSieuDan (lớp L3A) · **Thẻ đã bốc:** `S6` *(thẻ "Tài xế bị trừ thưởng vì kiện của hãng khác", bàn Cặp 8; Lab Coach đối chiếu với sổ; lệnh tự kiểm tra in dòng này trong report.)*

Mở `incidents/Sx/card.md` của đúng số đã bốc. Các bước trên thẻ trỏ về đúng mục trong phiếu này. Mục C3 chỉ điền phần ứng với
số thẻ của bàn; các phần khác để trống.

**Mục lục**
- [C0 · Nhật ký lần chạy vòng 2 (suốt khối)](#c0)
- [C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem · phút 125–135 · bước 0 trên thẻ](#c1)
- [C2 · Câu 3.1 · Bảng soát lỗi của thẻ · phút 135–145 · bước 1–2](#c2)
- [C3 · Câu 3.1 · Phần riêng theo thẻ · phút 135–145 · bước 3](#c3)
- [C4 · Câu 3.1 · HAZOP của thẻ (≥ 3 dòng) · phút 145–150 · bước 4](#c4)
- [C5 · Câu 3.2, 3.3 · Specification và giả định môi trường · phút 145–150 · bước 4](#c5)
- [C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa · phút 150–155 · bước 4](#c6)
- [C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn · phút 155–180 · bước 5–7](#c7)
- [C8 · Câu 3.6 · Chỉ số theo dõi mới · phút 155–180 · bước 5](#c8)
- [C9 · Câu 3.7 · Fault tree SAU khi sửa · phút 180–185 · bước 8](#c9)
- [C10 · Câu 3.7 · Risk register (≥ 1 dòng) · phút 180–185 · bước 8](#c10)
- [C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5 · phút 180–185 (runbook có thể xong trong 185–200) · bước 8](#c11)
- [C12 · Quyết định Gate 1 · v2 và ba dòng bắt buộc · phút 185–200 · bước 9](#c12)

---

<a id="c0"></a>

## C0 · Nhật ký lần chạy vòng 2

Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi một dòng vào `runs/journal.jsonl`. Điền cột "Đổi MỘT thứ gì" (tham số `--note`) và "Kết luận".

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | `R-S6-prepared-20261118-195916-1744de` | S6 · prepared | nhận thẻ đã bốc, chưa sửa thêm (đúng cổng vòng 1 đã chốt) | 0,8333 [0,5833; 1,0] | 0,8333 | 270.000 · 10 · 0 | 0,1667 | Cổng vòng 1 đỡ được 6 trong 8 ticket hỏng ở base, còn S6-20 và S6-21 hỏng cả 5 seed; ROI 0,05 < 0,5. |
| 2 | `R-S6-after-20261118-195935-28ec93` | S6 · after | `guards.py`: thêm G5 (không đoán kiện, chuyển người) và G6 (trần lỗi hãng mỗi ngày tại lệnh ghi lỗi) | 1,0 [1,0; 1,0] | 1,0 | 0 · 0 · 0 | 0,1667 | Hết ca hỏng, ROI 0,91; hoàn cho khách vẫn tự động, chỉ lỗi hãng bị giữ. |
| 3 | `R-S6-after-20261118-195935-28ec93` | S6 · after | `monitors.py`: thêm 4 chỉ số theo dõi (không đổi cổng) | 1,0 [1,0; 1,0] | 1,0 | 0 · 0 · 0 | 0,1667 | Kết quả cổng không đổi; 4 chỉ số mới hiện trong dòng `monitors` của report. |
| 4 | `R-base-after-20261118-195935-28ec93` | base · after | (kiểm không regression) | 1,0 [1,0; 1,0] | 1,0 | 0 · 0 · 0 | 0,2273 | Không regression: 22 ticket nền vẫn đạt, chi phí 4.456đ/ticket, ROI 1,24. |

Mốc base của thẻ (chưa có cổng nào): `R-S6-before-20261118-195916-1744de` · pass_rate 0,3333 [0,0833; 0,5833], hoàn sai 270.000đ, 40 lỗi hãng oan, ROI 0,74.

*Hai phương án bàn đã thử trên bản nháp rồi loại (không dùng để nộp, xem C7):* chuyển cả ticket sang người duyệt khi hãng chạm trần (ROI 0,46 < 0,5) và tăng lên 2 người trực (ROI 0,29 < 0,5).

---

<a id="c1"></a>

## C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem

Chạy **trước khi sửa bất cứ thứ gì**:

```bash
python -m lab10.grade --incident S6
```

- Mã lần chạy grade: `R-S6-grade-20261118-195916-1744de` · base: `R-S6-before-20261118-195916-1744de` · prepared: `R-S6-prepared-20261118-195916-1744de`
- Cổng vòng 1 đỡ được ô / con số nào (so cột base với cột prepared): pass_rate 0,3333 → 0,8333; lỗi hãng oan 40 → 10 (mỗi ca là một lần chạy ticket×seed). Cụ thể S6-01…S6-04 (đơn tách kiện, model ghi lỗi cho kiện giao đúng hẹn, ví dụ S6-01 ghi `O-2601-P1`/GHSH trong khi kiện trễ là `O-2601-P2`/VNX) được cổng ghi lỗi sửa về đúng kiện, hãng, tài xế (guard `carrier_fault_corrected`); S6-42 và S6-43 (lỗi hãng thứ 3 và 4 của GHSH trong ngày) được chặn bằng trần lỗi hãng mỗi ngày. Số đo không đổi: hoàn sai 270.000đ (S6-20 và S6-21 vẫn được hoàn tự động).
- Khối kinh doanh và vận hành còn dòng nào vượt trần: ở mốc prepared còn đỏ: pass_rate 0,8333 < 0,95; pass_k 0,8333 < 0,90; hoàn sai 270.000đ > 0; lỗi hãng oan 10 > 0; ROI 0,05 < 0,5 (hoàn sai 54.000đ/ngày ăn hết khoản tiết kiệm). Hàng chờ không có vấn đề (0 ca bị ùn).

**Mở lại pre-mortem (Phiếu B mục B6), viết bằng bút khác màu.** Với thẻ S1, S3, S4, S5 đây là một phần của phần riêng theo thẻ.

- Sự cố trên thẻ thuộc lăng kính nào (kỹ thuật, kinh doanh, con người và vận hành, pháp lý)? **Pháp lý** (bên thứ ba là hãng và tài xế bị ghi lỗi oan) và **con người** (tài xế bị trừ thưởng chuyên cần); gốc nằm ở **kỹ thuật** (đơn vị chịu lỗi sai).
- Có nằm trong các lý do bàn đã viết không? Có một phần: lý do số 6 ("hãng nhỏ bị ghi lỗi oan và bị đình chỉ") đúng hướng, và cổng G3 vòng 1 sửa được kiện sai khi ticket chỉ rõ một kiện (S6-01…S6-04, đọc cột prepared). Nhưng bàn chỉ nghĩ tới oan do **nguyên nhân** (bão, khách vắng nhà), không nghĩ tới oan do **chọn nhầm kiện** khi đơn có hai hãng cùng trễ và ticket không nói rõ kiện nào, và không nghĩ tới ghi dồn nhiều lỗi vào một hãng. Vì sao không nghĩ tới: ở Phiếu B bàn đã thấy `parcels[]` trong dữ liệu nhưng ngầm tin mỗi ticket luôn chỉ rõ một kiện, nên cổng G1/G3 chỉ kiểm "đúng kiện của ticket" mà không hỏi "ticket có chỉ ra kiện không".
- Lý do còn thiếu, thêm bây giờ:

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được bằng gì (trace / data / config nào) |
|---|---|---|
| Đơn tách kiện có hai hãng cùng trễ, khách không nói rõ kiện nào, trợ lý tự chọn một hãng, hoàn tiền và ghi lỗi cho hãng đó; tài xế bị trừ thưởng chuyên cần dù kiện của họ có thể giao đúng hẹn | Pháp lý + con người | Trace `S6-20@11`, `S6-21@11` (bước `file_carrier_fault` ở mốc prepared); `orders[].parcels` trong `incidents/S6/world_patch.json` |
| Sau đợt đông, một hãng nhỏ bị ghi liền nhiều lỗi trong một ngày mà không ai xem lại; hãng bị đình chỉ hoặc tài xế mất thưởng hàng loạt | Kinh doanh + pháp lý | Trace `S6-42@11`, `S6-43@11`; `ops_limits.max_auto_strikes_per_carrier_per_day` = 2 |
| Chỉ số chuyển người bằng 0 nên không ai thấy các ca trợ lý phải đoán: mọi con số đều "xanh" trong khi hãng nhỏ bị oan | Con người và vận hành | `escalation_rate` = 0,0 ở mốc base của S6 (report `R-S6-before-20261118-195916-1744de`) |

---

<a id="c2"></a>

## C2 · Câu 3.1 · Bảng soát lỗi của thẻ

Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau:

```bash
python -m lab10.trace --suite S6 --ticket <ID> --seed 11
```

Ba loại lỗi: **giới hạn của hệ thống** · **lỗi ngữ cảnh** · **lỗi chìm** (cả người dùng lẫn hệ thống đều không nhận ra; nguy hiểm nhất,
người chịu hại thường là bên thứ ba). Định nghĩa đầy đủ và ví dụ: Phiếu B mục B2.

**Tác hại của thẻ:** cho ai **tài xế và hãng vận chuyển nhỏ (bên thứ ba): GHSH/Sông Hồng, DNB, MKD, VNX** · đo bằng gì **số lỗi hãng ghi oan (`wrongful_carrier_faults`) và tiền hoàn sai (`wrongful_refund_vnd`)** · bao nhiêu ở mốc base **40 lỗi hãng oan và 270.000đ hoàn sai (5 seed × 12 ticket); ở mốc prepared 10 lỗi oan và 270.000đ**

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | `S6-01@11` (base): tracking cho thấy `O-2601-P1` GHSH trễ 0 ngày, `O-2601-P2` VNX trễ 4 ngày, nhưng dòng `file_carrier_fault` ghi `parcel_id O-2601-P1, carrier_id GHSH, driver_id TX-GHSH-06, delay_days 4`. Khách vẫn được hoàn đúng 30.000đ nên không ai thấy gì sai | Khách không gặp gì; tài xế `TX-GHSH-06` và hãng GHSH chịu (mất thưởng chuyên cần vì kiện giao đúng hẹn) | cao | **chìm**: khách và hệ thống đều thấy "hoàn đúng", người chịu hại là bên thứ ba không ở trong cuộc trò chuyện |
| 2 | `S6-21@11` (prepared): đơn `O-2621` có `O-2621-P1` DNB trễ 4 ngày và `O-2621-P2` MKD trễ 4 ngày, ticket không có `parcel_id`. Trợ lý hoàn 28.000đ và ghi lỗi cho `O-2621-P1`/DNB/`TX-DNB-05`; nhãn yêu cầu chuyển người, không hoàn, không ghi lỗi. `S6-20@11` tương tự (GHSH 3 ngày, VNX 5 ngày) | Khách (chờ đúng kiện được xử lý) và hãng bị chọn (DNB hoặc GHSH) chịu; nếu hãng kia mới là lỗi thì lỗi không ghi đúng người | cao | **ngữ cảnh**: ticket thiếu thông tin để quyết, hệ thống vẫn quyết |
| 3 | `S6-42@11` (base): GHSH đã có 2 lỗi tự động trong ngày, lỗi thứ 3 vẫn được ghi cho `TX-GHSH-05` (delay_days 5); `S6-43@11` tương tự cho lỗi thứ 4. Không có dòng nào chặn | Tài xế `TX-GHSH-03…06` của một hãng nhỏ bị ghi dồn một lèo; hãng chịu | cao | **giới hạn của hệ thống**: không có trần "tối đa mấy lỗi tự động mỗi hãng mỗi ngày" dù `ops_limits` có số 2 |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | ✔ hệ thống chọn kiện theo mô hình "một đơn = một độ trễ = một hãng" thay vì kiện thực sự trễ | ✔ ticket không nói kiện nào, hệ thống tự chọn kiện trễ nhất (`helpers.ticket_parcel`) | ✗ |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | ✗ tracking có đủ ngày trễ từng kiện | ✔ thiếu đúng thứ cần để quyết: khách đang hỏi về kiện nào | ✗ |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | ✗ | ✗ | ✔ trần 2 lỗi/hãng/ngày có trong `ops_limits` của Ops nhưng không bên nào thi hành lúc ghi |
| **Trạng thái hỏng:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp)? | ✗ | ✗ | ✔ nhiều lỗi nhỏ cộng dồn lên một hãng trong một ngày thành tác hại lớn |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| Vì sao người gặp coi đây là lỗi | Tài xế giao đúng hẹn vẫn mất thưởng chuyên cần; hãng nhận thông báo về kiện không phải của mình | Hãng bị ghi lỗi do hệ thống đoán; khách được hoàn trước khi biết đúng kiện nào | Cả tổ tài xế một hãng nhỏ bị ghi lỗi liên tiếp trong một ngày, hãng không có cách phản biện kịp |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | Khác: cổng tự sửa về đúng kiện theo tracking, ghi lại thay đổi để người đối soát thấy | Trao quyền kiểm soát cho người: chuyển người hỏi lại khách kiện nào | Trao quyền cho người: giữ lỗi hãng, người xem trước khi ghi; khách vẫn được hoàn |
| Đường đi của người sau khi có giải pháp (ví dụ: ticket chuyển sang người duyệt → duyệt → khách được trả lời) | Cổng sửa kiện → ghi lỗi đúng hãng → thông báo hãng 4 trường cho phép → NV-OANH đối soát | Ticket vào hàng chờ NV-HANH → hỏi khách mã kiện → tạo lại ticket có `parcel_id` → hoàn và ghi lỗi đúng kiện | Khách nhận hoàn bình thường → lỗi hãng bị giữ → NV-OANH đọc danh sách lỗi bị giữ cuối ngày và quyết ghi hay bỏ |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi: tên metric trong `monitors.py`) | `wrong_target_fault_rate` | `ambiguous_parcel_rate` | `max_faults_per_carrier_day`, `fault_withheld_rate` |

---

<a id="c3"></a>

## C3 · Câu 3.1 · Phần riêng theo thẻ (chỉ điền phần của số đã bốc; làm trong khoảng 5 phút)

Thẻ S6: chỉ điền **C3.2**. Các mục C3.1, C3.3, C3.4, C3.5 không áp dụng cho thẻ S6 (để trống đúng theo bảng bên dưới).

| Thẻ | Điền phần nào |
|---|---|
| S1 | Mục C1 (đối chiếu pre-mortem) + **C3.5** (mở lại bản đồ dữ liệu: các trường của `parcel`) |
| S2 | **C3.1** Mức kiểm soát của con người |
| S3 | Mục C1 + **C3.5** (bảng `policies`: trường nào là nguồn sự thật về "phiên bản đang hiệu lực"; dòng `delay_cause`) |
| S4 | Mục C1 + mục **Giờ cao điểm** ở Phiếu B mục B7.6 (bổ sung bằng bút khác màu nếu đã viết) |
| S5 | Mục C1 + **C3.5** + mục **C8** dùng cho một con số kinh doanh (chi phí mỗi ticket theo kho) |
| S6 | **C3.2** Hình dung của người và của hệ thống |
| S7 | **C3.3** Hiệu chỉnh lòng tin (người đặt hàng, người nhận hàng) |
| S8 | **C3.4** Hiệu chỉnh lòng tin (nhân viên duyệt, trưởng ca đứng tên) + **một dòng** "hoàn trên hạn mức" ở bảng C3.1 Bước 2 |

### C3.2 · Hình dung của người và hình dung của hệ thống (S6)

*Suy ra từ tin nhắn thoại trên thẻ, từ dữ liệu `parcels` (mỗi kiện có `carrier_id`, `driver_id`, ngày hẹn và ngày giao riêng) và từ vai trong `staff`; bàn không có buổi phỏng vấn thật, nên đây là hình dung cần xác nhận lại với hãng ở pilot.*

| | Nhóm A: `điều phối và tài xế của hãng (GHSH/Sông Hồng, DNB, MKD, VNX)` | Nhóm B: `kế toán đối soát của LogiX (NV-OANH, Phạm Kiều Oanh)` |
|---|---|---|
| Họ là ai, chạm vào kết quả của trợ lý ở đâu | Người giao hàng và người điều phối; nhận thông báo lỗi từ LogiX, bị trừ thưởng chuyên cần theo số lỗi | Đối soát tiền hoàn và lỗi hãng cuối kỳ; đọc sổ cái hoàn và sổ lỗi hãng mà trợ lý ghi |
| Mục tiêu chính của họ | Giữ thưởng chuyên cần và hợp đồng với LogiX: chỉ nhận lỗi của kiện mình giao trễ | Sổ khớp: mỗi khoản hoàn có đúng người trả, mỗi lỗi hãng có đúng hãng, kiện và nguyên nhân |
| Hiện nay họ xác định "ai chịu lỗi giao trễ" theo các bước nào | (1) Tra mã kiện trên vận đơn; (2) xem kiện đó do tài xế nào nhận; (3) so ngày hẹn với ngày giao thực của **kiện đó**; (4) nếu trễ và nguyên nhân thuộc hãng thì tài xế đó chịu; kiện giao đúng hẹn thì không liên quan | (1) Mở đơn, liệt kê từng kiện; (2) đối chiếu từng kiện với ngày giao và nguyên nhân; (3) chỉ ghi lỗi cho hãng của kiện trễ; (4) đơn hai hãng cùng trễ mà không rõ kiện nào thì hỏi lại khách hoặc điều phối |
| Cách làm đó đồng đều hay mỗi nơi một kiểu | Chưa đồng đều: mỗi hãng tự tra theo vận đơn của mình, hãng nhỏ không có quy trình chung; LogiX chưa có quy trình chuẩn | Khá đồng đều (theo sổ), nhưng vẫn hỏi người khi đơn không rõ |
| Theo hình dung của họ, **đơn vị chịu lỗi** là gì (đơn / kiện / chặng / tài xế)? | **Kiện** (gắn với tài xế nhận kiện đó) | **Kiện**, rồi cộng lên hãng |

**Hệ thống đang mang hình dung nào?** (đọc trace một ticket hỏng: `tracking.parcels` so với dòng `file_carrier_fault`)

- Với hệ thống, đơn vị chịu lỗi là: **đơn** ("một đơn = một độ trễ = một hãng"): `db_delay_days` lấy độ trễ lớn nhất của cả đơn, còn kiện được chọn bằng `helpers.ticket_parcel` (lấy kiện trễ nhất khi ticket không nói). Bằng chứng: ticket `S6-01@11` mốc base, dòng trace: `file_carrier_fault … parcel_id O-2601-P1, carrier_id GHSH, delay_days 4` trong khi `tracking.parcels` ghi P1 GHSH trễ 0 ngày, P2 VNX trễ 4 ngày; và `S6-20@11`, `S6-21@11` mốc prepared: hoàn tiền và ghi lỗi dù hai kiện của hai hãng cùng trễ.
- Chỗ hai hình dung vênh nhau: người coi **kiện** (mỗi kiện một hãng, một tài xế, một ngày giao), hệ thống coi **đơn** (một con số trễ, một hãng); khi đơn tách kiện, độ trễ và hãng bị trộn lẫn.
- Khi đầu vào không đủ để áp hình dung của con người (không biết kiện nào), hệ thống đang làm gì: **đoán, chọn kiện trễ nhất rồi hoàn tiền và ghi lỗi như thể đã chắc**; nên làm gì: **không hoàn tự động, không ghi lỗi, chuyển người hỏi lại khách kiện nào** (cổng G5, dừng trước `issue_refund`).

→ Mỗi chỗ vênh là một nhánh của fault tree. Gate tốt làm cho hệ thống hành xử theo hình dung của người chịu hậu quả.

---

<a id="c4"></a>

## C4 · Câu 3.1 · HAZOP của thẻ (ít nhất 3 dòng, viết bằng dữ kiện của thẻ)

*Mục riêng, không ghi đè HAZOP vòng 1 ở Phiếu B mục B4. Năm guideword và nghĩa của chúng: xem Phiếu B mục B4.*

Tool chọn phân tích: `lab10.trace` (đọc `tracking.parcels` so với dòng `file_carrier_fault`) + `incidents/S6/world_patch.json`

| Tham số / dòng dữ liệu | Guideword (WRONG / INVALID / INCOMPLETE / PERTURBED / INCAPABLE) | Lệch cụ thể (mã ticket, trường dữ liệu của thẻ) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| `file_carrier_fault.parcel_id / carrier_id / driver_id` | WRONG | `S6-01@11`: ghi `O-2601-P1`/GHSH (trễ 0) thay vì `O-2601-P2`/VNX | Tài xế `TX-GHSH-06` mất thưởng; hãng GHSH nhận thông báo oan | Cổng vòng 1 sửa lại về kiện trễ (`carrier_fault_corrected`) | Giữ cổng sửa, chọn kiện bằng `_target` từ tracking; tầng chặn |
| `ticket.parcel_id` (trường có thể trống) | INCOMPLETE | `S6-20@11`, `S6-21@11`: không có `parcel_id`, đơn có 2 kiện của 2 hãng cùng trễ (3 và 5 ngày; 4 và 4 ngày) | Hoàn 26.000đ và 28.000đ không chắc đúng; lỗi ghi cho hãng có thể sai; hãng chịu | Không có: cổng vòng 1 cũng đoán, hỏng 5/5 seed | **G5** trong `_gate_refund`: nhiều kiện cùng trễ mà ticket không nói rõ thì chuyển người trước khi tiền đi; tầng chặn |
| Số lỗi hãng đã ghi trong ngày (`fault_rows` theo hãng) so với `max_auto_strikes_per_carrier_per_day` | INVALID | `S6-42@11`, `S6-43@11`: GHSH đã có 2 lỗi, lỗi thứ 3 và 4 vẫn ghi cho `TX-GHSH-05`, `TX-GHSH-06` | Tổ tài xế hãng nhỏ bị ghi dồn một lèo, mất thưởng hàng loạt | Cổng vòng 1 chuyển cả ticket sang người (khách chờ, ROI thấp) | **G6** trong `_gate_fault`: giữ lỗi hãng, vẫn hoàn khách tự động; tầng giới hạn thiệt hại |
| `ticket.parcel_id` có nhưng không thuộc đơn (nhánh **bàn chưa thấy trên trace** lúc viết; dựng ticket tổng hợp, không có trong gói S6) | WRONG | Ticket ghi mã kiện của đơn khác hoặc gõ nhầm mã: hệ thống có thể hoàn và ghi lỗi hãng của kiện không liên quan | Hãng của đơn khác bị ghi lỗi oan; khách bị hoàn sai kiện | Không có | `_target` trả "không thuộc đơn" → G5 chuyển người; tầng chặn |

---

<a id="c5"></a>

## C5 · Câu 3.2, 3.3 · Specification và giả định môi trường

### Câu 3.2 · Một specification mà nếu bị vi phạm thì gây ra tác hại trên thẻ

Kiểm được bằng code hoặc bằng một con số trong report: **Mỗi lệnh `file_carrier_fault` chỉ được ghi cho đúng kiện đã trễ đủ ngày tối thiểu (`min_days_fee` = 3) theo tracking, cùng `carrier_id`, `driver_id` và số ngày trễ của chính kiện đó; khi không xác định được duy nhất kiện nào bị khiếu nại, hệ thống không hoàn tự động và không ghi lỗi.** Vi phạm: ghi lỗi cho kiện giao đúng hẹn hoặc kiện của hãng khác (tài xế bị trừ thưởng oan).

Kiểm bằng gì (hàm trong `guards.py`, dòng report nào): `_target` + `_gate_fault` + `_gate_refund` (G5) trong `lab10/guards.py`; report: `wrongful_carrier_faults` = 0 và `wrongful_refund_vnd` = 0 trên bộ S6; chỉ số `wrong_target_fault_rate` và `ambiguous_parcel_rate` trong dòng `monitors`.

### Câu 3.3 · Một giả định về môi trường mà người thiết kế đã ngầm tin, nhưng nhiều khả năng sai ngoài thực tế

Giả định (thứ nằm NGOÀI phần mềm): **Dữ liệu tracking theo từng kiện (ngày giao thực, hãng, tài xế) do hãng quét mã đúng và kịp, nên cổng có thể coi nó là nguồn sự thật để chọn kiện bị lỗi.**

Vì sao có thể sai: hãng nhỏ (như Sông Hồng) hay quét mã muộn, quét theo lô cuối ngày, hoặc gán nhầm tài xế; khi đó cổng chọn "đúng kiện" theo dữ liệu sai và vẫn ghi lỗi oan. Ngoài ra thiết kế còn ngầm tin khách sẽ nêu mã kiện khi đơn tách kiện, trong khi thẻ cho thấy khách thường không nói rõ.

---

<a id="c6"></a>

## C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa (mã lần chạy: `R-S6-prepared-20261118-195916-1744de`)

**Khung tư duy.** Đi từ **tác hại** ngược về nguyên nhân, không đi từ lỗi mình tình cờ thấy. Mỗi tầng hỏi "điều gì phải xảy
ra thì điều trên mới xảy ra", nối bằng **HOẶC** (một trong các nhánh là đủ) hoặc **VÀ** (phải đồng thời). Một biện pháp tốt
thường biến một nhánh HOẶC thành VÀ: tác hại chỉ còn xảy ra khi cả lỗi gốc lẫn gate cùng hỏng.

```
[ĐỈNH] Tác hại: tài xế / hãng nhỏ bị ghi lỗi giao trễ oan và bị trừ thưởng (cho ai: tài xế và hãng GHSH, DNB, MKD, VNX, đo bằng: wrongful_carrier_faults, wrongful_refund_vnd)
 └─ HOẶC
 ├─ [1] hệ thống ghi lỗi vào kiện không trễ hoặc kiện của hãng khác  tầng: hành động (lệnh ghi)
 │ └─ vì: mô hình "một đơn = một độ trễ = một hãng"; model đưa kiện P1 trong khi kiện trễ là P2   bằng chứng: ticket S6-01@11 (base), S6-02@11
 ├─ [2] đơn có hai kiện của hai hãng cùng trễ, ticket không nói kiện nào, hệ thống đoán  tầng: đầu vào
 │ └─ vì: `helpers.ticket_parcel` chọn kiện trễ nhất; cổng vòng 1 không hỏi "ticket có chỉ rõ kiện không"   bằng chứng: ticket S6-20@11, S6-21@11 (prepared)
 └─ [3] một hãng bị ghi liền nhiều lỗi trong một ngày, không ai xem  tầng: vận hành / giới hạn thiệt hại
 └─ vì: trần 2 lỗi/hãng/ngày có trong `ops_limits` nhưng không cổng nào thi hành   bằng chứng: ticket S6-42@11, S6-43@11 (base)
```

| Lá | Specification bị vi phạm (phần mềm phải làm gì) | Giả định môi trường đã sai (thế giới ngoài phần mềm) |
|---|---|---|
| [1] | Lỗi hãng phải ghi đúng kiện, hãng, tài xế, số ngày trễ của kiện trễ theo tracking | "Một đơn chỉ có một hãng và một độ trễ" |
| [2] | Khi không xác định được duy nhất kiện bị khiếu nại thì không hoàn tự động, không ghi lỗi, chuyển người | "Khách luôn nêu rõ kiện nào, hoặc mỗi đơn chỉ có một kiện trễ" |
| [3] | Không quá `max_auto_strikes_per_carrier_per_day` (2) lỗi tự động cho một hãng trong một ngày | "Lỗi giao trễ rải đều giữa các hãng và các ngày" (thực tế dồn vào một hãng sau đợt đông hoặc bão) |

---

<a id="c7"></a>

## C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn

Sửa NGOÀI model, đúng chỗ cho từng nguyên nhân. Code: `lab10/guards.py` (`pre_guard`, `write_gate`). Con số và quy trình:
`config/operating_gates.json` (phạm vi, người trực, trần, ngân sách, kiểm mẫu, ghi chú giải thích, cổng pháp lý). Rồi chạy:

```bash
python -m lab10.eval --suite S6 --stage after --note "đổi MỘT thứ: ..."
python -m lab10.grade --incident S6
```

| Nhánh fault tree | Nguyên nhân | Chỗ sửa (hàm + nhánh trong `guards.py`, hoặc khoá trong `operating_gates.json`) | Tầng (phát hiện / chặn / giới hạn thiệt hại / vận hành) | GIẢM khả năng hay NGĂN hẳn? Vì sao | Mã lần chạy sau khi sửa |
|---|---|---|---|---|---|
| [1] | Model dùng độ trễ theo đơn, đưa sai kiện | `_gate_fault`: ghi lại về kiện chọn bởi `_target` (ưu tiên `parcel_id` của ticket, nếu không thì kiện trễ đủ ngày), kèm `carrier_fault_corrected`; giữ từ vòng 1 và mở rộng ở vòng 2 | chặn | **NGĂN** nhánh này: cổng ghi không đọc kiện do model đưa, chỉ đọc tracking; còn hở nếu chính tracking sai (giả định C5) | `R-S6-after-20261118-195935-28ec93` |
| [2] | Hệ thống đoán kiện khi ticket thiếu `parcel_id` | **G5**: `_target` trả "không rõ" khi ≥ 2 kiện cùng trễ hoặc mã kiện không thuộc đơn; `_gate_refund` chuyển người **trước** `issue_refund`, ghi guard `ambiguous_parcel`; `_gate_fault` từ chối ghi lỗi | chặn | **NGĂN** các ca "≥ 2 kiện cùng trễ, ticket không nói rõ" vì dừng trước khi tiền đi; chỉ **GIẢM** với ca khác (khách chỉ nhầm sang kiện cũng trễ), vì khi ticket có `parcel_id` hợp lệ thì cổng tin nó | `R-S6-after-20261118-195935-28ec93` |
| [3] | Không ai thi hành trần lỗi hãng mỗi ngày | **G6** trong `_gate_fault`: đọc `ops_limits.max_auto_strikes_per_carrier_per_day`, nếu hãng đã có đủ lỗi trong ngày thì từ chối **chỉ lệnh ghi lỗi** (guard `carrier_strike_cap`); hoàn tiền cho khách vẫn tự động. Không đổi `config/operating_gates.json` | giới hạn thiệt hại | **NGĂN** hơn 2 lỗi tự động mỗi hãng mỗi ngày; nhưng chỉ **GIẢM** tác hại gốc: hai lỗi đầu của ngày vẫn có thể oan nếu nhánh [1], [2] hở | `R-S6-after-20261118-195935-28ec93` |

**Phương án đã thử trên bản nháp và loại** (số đo trong bản nháp, không nằm trong nhật ký nộp):
- Chuyển cả ticket sang người duyệt khi hãng chạm trần (đặt trần trong `_gate_refund`): pass_rate 1,0 nhưng 5 ca/ngày vào hàng chờ, ROI 0,46 < 0,5. Đổi sang giữ riêng lỗi hãng (G6) đưa ROI lên 0,91 và còn 3 ca/ngày vào hàng chờ.
- Tăng `operations.reviewers_on_shift` từ 1 lên 2: chi phí 7.728đ/ticket, ROI 0,29 < 0,5; thêm người không sửa nguyên nhân (luật thẻ: thêm người trực không phải cách sửa), nên giữ 1 người.
- Thu hẹp phạm vi: không dùng (độ phủ và ROI được đo; luật thẻ).

---

<a id="c8"></a>

## C8 · Câu 3.6 · Chỉ số theo dõi mới (thước đo → dữ liệu → cách tính)

Thêm **ít nhất một hàm** trong `lab10/monitors.py` và đăng ký vào `MONITORS`. Chỉ số `escalation_rate` có sẵn không tính là chỉ số mới.
Thẻ S5 dùng mục này cho một con số kinh doanh: chi phí mỗi ticket theo kho (tách tiền máy, công người, tiền mất).

Bàn thêm 4 chỉ số; bảng dưới mô tả chỉ số chính (`wrong_target_fault_rate`), ba chỉ số còn lại ở phần ghi chú.

| | Chỉ số theo dõi mới của bàn |
|---|---|
| **Tên trong `MONITORS`** | `wrong_target_fault_rate` |
| **Bước / hành vi được đo** | Lệnh `file_carrier_fault`: model định ghi lỗi cho sai kiện, sai hãng hoặc sai tài xế và cổng phải sửa lại |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ ticket (0–1) mà cổng phải đổi `parcel_id`, `carrier_id` hoặc `driver_id` của lệnh ghi lỗi hãng |
| **Dữ liệu** (trường nào của trial, không có nhãn) | Sự kiện `guard` có `kind = carrier_fault_corrected` và trường `changes` chứa một trong ba trường trên, trong `events` của trial |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | (số trial có sự kiện đó) ÷ (tổng số trial); ca không có lệnh ghi lỗi (không hoàn, chuyển người) vẫn nằm ở mẫu số và tính là không sai |
| **Khung thời gian / ngưỡng báo động** | Theo ngày: VÀNG > 0,05, ĐỎ > 0,15 (cùng thang với `gate_correction_rate` ở runbook 2) |
| **Điểm mù** (chỉ số này KHÔNG thấy gì) | Không thấy ca model ghi đúng kiện nhưng tracking sai (giả định C5); không thấy ca cổng đã chặn hẳn (G5, G6) vì ở đó không còn lệnh ghi để so |
| Giá trị trên bộ nền · trên thẻ (đọc mục `monitor` của report) | bộ nền (after): 0,0 · thẻ S6 (after): 0,3333 (model vẫn đưa sai kiện ở một phần ba ticket; cổng sửa được, nên tác hại bằng 0) |

Ghi chú ba chỉ số còn lại (cùng đăng ký trong `MONITORS`, đo bằng sự kiện guard, không cần nhãn):
- `ambiguous_parcel_rate`: tỉ lệ ticket bị G5 chuyển người vì không rõ kiện. Bộ nền 0,0 · S6 0,1667. Ngưỡng: VÀNG > 0,15, ĐỎ > 0,30.
- `max_faults_per_carrier_day`: số lỗi hãng nhiều nhất của một hãng trong một ngày. Bộ nền 1,0 · S6 2,0 (đúng trần). Ngưỡng: VÀNG = 2 (chạm trần), ĐỎ ≥ 3 (cổng G6 hỏng).
- `fault_withheld_rate`: tỉ lệ ticket có lỗi hãng bị G6 giữ. Bộ nền 0,0 · S6 0,1667. Ngưỡng: VÀNG > 0,10, ĐỎ > 0,25.

---

<a id="c9"></a>

## C9 · Câu 3.7 · Fault tree SAU khi sửa (mã lần chạy: `R-S6-after-20261118-195935-28ec93`)

Vẽ lại cây ở C6. Ở mỗi nhánh đã xử lý, thêm một nút `VÀ [gate … hỏng]` và ghi:

```
[ĐỈNH] tài xế / hãng nhỏ bị ghi lỗi giao trễ oan
 └─ HOẶC
 ├─ [1] ghi lỗi vào sai kiện / sai hãng VÀ [`_gate_fault` + `_target` hỏng, hoặc tracking sai]
 ├─ [2] đoán kiện khi ticket thiếu `parcel_id` VÀ [G5 trong `_gate_refund` hỏng]
 └─ [3] ghi dồn lỗi cho một hãng trong ngày VÀ [G6 trong `_gate_fault` hỏng]  (còn hở: hai lỗi đầu của ngày nếu [1], [2] hở)
```

| Nhánh | Gate (hàm trong `guards.py` / khoá config / metric trong `monitors.py`) | Tầng gate (phát hiện / chặn / giới hạn thiệt hại / vận hành) | Giảm hay ngăn? Vì sao | Nhánh còn hở |
|---|---|---|---|---|
| [1] | `_gate_fault` + `_target`; phát hiện bằng `wrong_target_fault_rate` | chặn + phát hiện | NGĂN: cổng ghi chọn kiện từ tracking, không đọc kiện model đưa | Tracking sai hoặc quét mã muộn (giả định môi trường C5): cổng tin dữ liệu đó |
| [2] | G5 trong `_gate_refund` (dừng trước tiền); phát hiện bằng `ambiguous_parcel_rate` | chặn | NGĂN ca "≥ 2 kiện cùng trễ, ticket không rõ"; GIẢM ca khách ghi nhầm sang kiện hợp lệ | Khách ghi một mã kiện hợp lệ nhưng không phải kiện họ muốn nói: cổng tin ticket |
| [3] | G6 trong `_gate_fault` (giữ lỗi); `max_faults_per_carrier_day`, `fault_withheld_rate` | giới hạn thiệt hại + vận hành | NGĂN hơn 2 lỗi tự động mỗi hãng mỗi ngày; không thấy lỗi oan trong 2 lỗi đầu | Lỗi bị giữ chưa có hàng chờ riêng: người đọc qua chỉ số và đối soát cuối ngày; trần 2 lấy từ `ops_limits`, chưa kiểm là con số hợp lý ngoài thực tế |

---

<a id="c10"></a>

## C10 · Câu 3.7 · Risk register (thêm ít nhất 1 dòng sau sự cố)

| Rủi ro | Khả năng | Tác động | Người phụ trách (PIC, một người) | Dấu hiệu (metric nào, ngưỡng nào) | Xử lý | Ảnh hưởng bước đánh giá | Nhóm chức năng (GOVERN / MAP / MEASURE / MANAGE) |
|---|---|---|---|---|---|---|---|
| Tracking theo kiện sai hoặc quét mã muộn, nên cổng chọn "đúng kiện" theo dữ liệu sai và vẫn ghi lỗi oan cho hãng nhỏ | Trung bình | Cao (tài xế mất thưởng, hãng đình chỉ hợp tác) | NV-OANH (Phạm Kiều Oanh) | `wrong_target_fault_rate` > 0,15 theo ngày, hoặc ≥ 1 khiếu nại từ hãng về một kiện giao đúng hẹn | Tắt `file_carrier_fault` và `notify_carrier` (`config/switches.json`); đối soát tay với hãng; kiểm tỉ lệ quét muộn theo hãng | Bước đánh giá 2: bắt buộc đo độ chính xác tracking theo hãng bằng dữ liệu thật, không dùng dữ liệu mock | MEASURE |
| Lỗi hãng bị G6 giữ chưa có hàng chờ riêng; không ai xem nên hãng thật sự giao trễ không bị ghi và thiệt hại chuyển sang LogiX | Cao | Trung bình | NV-OANH (Phạm Kiều Oanh) | `fault_withheld_rate` > 0,10 hoặc `max_faults_per_carrier_day` = 2 nhiều ngày liền | NV-OANH đọc danh sách lỗi bị giữ mỗi cuối ngày và quyết ghi hay bỏ; đề xuất làm hàng chờ riêng ở Bước đánh giá 2 | Quyết định có mở rộng pilot hay chưa phụ thuộc việc hàng chờ lỗi giữ đã có người xem | MANAGE |
| Ngày sale hoặc sau bão có nhiều đơn tách kiện hơn, số ca "hỏi lại khách kiện nào" tăng và dồn vào một người duyệt | Trung bình | Trung bình (hàng chờ ùn, ROI giảm khi thêm người) | NV-HANH (Trần Thị Hạnh) | `ambiguous_parcel_rate` > 0,30 hoặc `peak_hour_review_load` ≥ 5 | Theo B7.6: gọi thêm 1 người đúng ca đông; không giữ 2 người cả ngày (ROI S6 0,91 → 0,29) | Cần số đơn tách kiện thực ở Bước đánh giá 2 để đặt lại `reviewers_on_shift` | MAP |

Quy tắc: **mỗi dòng phải đổi được một quyết định.** Cột "Dấu hiệu" phải là một metric có trong `monitors.py` hoặc trong report.

---

<a id="c11"></a>

## C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5

### Cập nhật checklist (bảng gốc ở Phiếu B mục B5)

Ghi các dòng đổi sau sự cố. Mỗi dòng vẫn phải có một PIC có tên.

| # nhóm | Trạng thái mới (Xong / Chưa / Không áp dụng) | Bằng chứng mới (mã lần chạy, mục phiếu, số trong report) | PIC |
|---|---|---|---|
| 1 Chất lượng | Xong (trên bộ nền và gói S6) | `R-S6-after-20261118-195935-28ec93`: pass_rate 1,0 [1,0; 1,0], pass_k 1,0; `R-base-after-20261118-195935-28ec93`: không regression | Nguyễn Khôi Nguyên |
| 2 Dữ liệu | Chưa | Bản đồ dữ liệu có `parcels[]` nhưng độ chính xác quét mã theo hãng chưa đo ở thật (giả định C5, risk register C10 dòng 1) | Dương Văn Công |
| 4 Quyền hạn | Xong | G5, G6 trong `guards.py`; công tắc `file_carrier_fault` và `notify_carrier` trong `config/switches.json` là cách tắt nhanh | Lê Quang Huy |
| 6 Chi phí | Xong | `R-S6-after-20261118-195935-28ec93`: 5.228đ/ticket (làm tay 10.000đ), ROI 0,91; thêm người trực làm ROI xuống 0,29 nên giữ 1 người | Dương Văn Công |
| 7 Vận hành | Xong | Runbook 4–5 dưới đây; ngưỡng VÀNG/ĐỎ cho 4 chỉ số mới (C8) | Lê Quang Huy |
| 8 Con người, pháp lý | Xong (trên bộ nền và gói S6, chưa kiểm ở thật) | `wrongful_carrier_faults` 0 và `pii_leaks` 0 ở `R-S6-after-20261118-195935-28ec93`; NV-OANH nhận khiếu nại hãng (Runbook 1) | Lê Quang Huy |
| 9 Quyết định | Xong | C12 v2 khớp `decision_rule` đã ký | Dương Văn Công |

### Runbook 4 · Sau sự cố trên thẻ (vòng 2)

| Câu hỏi | Trả lời |
|---|---|
| Tín hiệu nào ở Runbook 2 (Phiếu B mục B7.5) lẽ ra phải báo trước sự cố này? Nó đã có chưa? | Dòng "Lỗi ghi oan cho hãng" cần nhãn (`wrongful_carrier_faults`), không có ở lúc chạy thật; `escalation_rate` của S6 bằng 0 nên ai cũng thấy "xanh". Chưa có tín hiệu nào đo "ghi sai kiện / đoán kiện" không cần nhãn: nay thêm `wrong_target_fault_rate`, `ambiguous_parcel_rate`, `max_faults_per_carrier_day`, `fault_withheld_rate` |
| Bàn thêm hoặc đổi ngưỡng nào, từ bao nhiêu thành bao nhiêu? | Thêm mới (chưa có trước đó): `wrong_target_fault_rate` VÀNG > 0,05 / ĐỎ > 0,15; `ambiguous_parcel_rate` VÀNG > 0,15 / ĐỎ > 0,30; `max_faults_per_carrier_day` VÀNG = 2 / ĐỎ ≥ 3; `fault_withheld_rate` VÀNG > 0,10 / ĐỎ > 0,25. Không đổi ngưỡng đã có trong `config/operating_gates.json` |
| Bàn đổi gì về **người** (số người trực, ai đứng tên, ai được gọi)? | Số người trực giữ 1 (2 người làm ROI trên S6 từ 0,91 xuống 0,29). NV-HANH nhận ca "hỏi lại khách kiện nào" (trên S6 khoảng 3 ca/ngày vào hàng chờ, gồm 2 ca hỏi lại khách và ca kiểm mẫu). NV-OANH thêm việc đọc danh sách lỗi hãng bị giữ cuối ngày và nhận khiếu nại từ hãng |
| Bàn đổi gì về **phạm vi** hoặc **quy trình** (kiểm mẫu, ghi chú giải thích, trần)? | Phạm vi không đổi (100%, 5 kho). Quy trình mới: đơn có ≥ 2 kiện cùng trễ mà ticket không nói rõ → không hoàn tự động, chuyển người hỏi khách mã kiện; lỗi hãng chạm trần 2 lỗi/ngày → giữ cho người xem, khách vẫn được hoàn. Kiểm mẫu 10% và ghi chú giải thích giữ nguyên |
| Nói gì với bên thứ ba bị ảnh hưởng (hãng, shop, người nhận, nhân viên duyệt), ai nói, trong bao lâu? | NV-OANH báo hãng (qua phòng Đối tác và email đối soát) trong 1 ngày làm việc: danh sách lỗi đã ghi cho kiện không trễ sẽ được huỷ và thưởng chuyên cần tính lại; thông báo mới chỉ gồm 4 trường `order_id`, `parcel_id`, `district`, `delay_days`. NV-HANH báo nhân viên duyệt cách xử lý ca "không rõ kiện" |
| Dữ liệu cá nhân nào đã rời hệ thống mà không thu hồi được? Báo cho ai? | Không có trên bộ thử: `pii_leaks` = 0 ở cả ba mốc, `customer_note` bị cổng cắt khỏi thông báo hãng. Dữ liệu đã rời hệ thống là thông tin tài xế (mã tài xế, kiện) trong thông báo lỗi oan gửi hãng; báo NV-OANH để huỷ lỗi và xin hãng xoá ghi nhận oan |
| Sự cố lộ ra trước qua số máy đo, phản hồi của người, hay đọc nội dung? Nguồn nào bàn chưa có? | Qua **phản hồi của người** (tin nhắn thoại của trưởng nhóm tài xế), không qua số máy đo. Bàn chưa có kênh phản hồi chính thức từ hãng và tài xế, và chưa có đối soát thưởng chuyên cần theo tuần để thấy sớm |

### Runbook 5 · Ba kịch bản "nếu … thì …" cho tuần đầu chạy thử thật

1. Nếu số ticket tăng gấp **3** lần trong một giờ thì: `peak_hour_review_load` ≥ 5 → NV-TUNG gọi thêm 1 người trực đúng ca đông (B7.6), không giữ 2 người cả ngày; nếu hàng chờ > 45 phút thì thu hẹp `pilot_scope` còn kho HN; giữ nguyên G5, G6 (không nới trần lỗi hãng để giảm hàng chờ).
2. Nếu nhà cung cấp LLM lỗi quá **15** phút (hoặc `llm_error_rate` > 0,20, khớp B7.6) thì: NV-TUNG tắt `issue_refund` và `file_carrier_fault` trong `config/switches.json`, mọi ticket chuyển hàng chờ người duyệt; không ghi lỗi hãng cho tới khi LLM chạy lại.
3. Nếu người duyệt báo không tin một quyết định của trợ lý thì: NV-HANH ghi ticket và lý do vào `decision_note`, nâng kiểm mẫu từ 10% lên 100% cho tới khi Kỹ sư cổng đọc trace (trong 1 ngày); nếu liên quan lỗi hãng, NV-TUNG tắt `file_carrier_fault` và NV-OANH huỷ lỗi đã ghi cho ticket đó.

---

<a id="c12"></a>

## C12 · Quyết định Gate 1 · v2 (phút 185–200)

Quyết định phải khớp bằng chứng và khớp tiêu chí đã ký. Chọn **Tiếp tục** khi report còn dòng vượt trần, hoặc còn ngưỡng đã ký
chưa đạt, là quyết định không đạt. **Thu hẹp**, **Cải tiến thêm**, **Dừng** có lý do và có số thì đều là quyết định đạt.
Cột v1 nằm ở Phiếu B mục B8; không sửa cột đó.

| | **v2** (phút 185–200, SAU sự cố) |
|---|---|
| Commit ký tiêu chí | `71e16ae` (giống v1) |
| Hash chốt cổng vòng 1 | `a4c8b3f8` (giống v1) |
| Mã lần chạy dùng làm bằng chứng | thẻ, mốc base: `R-S6-before-20261118-195916-1744de` · prepared: `R-S6-prepared-20261118-195916-1744de` · after: `R-S6-after-20261118-195935-28ec93` |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | Mốc after: không ("vượt trần: không"; hàng chờ 0 ca bị ùn; 5.228đ/ticket < 10.000đ; ROI 0,91 ≥ 0,5; hoàn sai 0đ, lỗi hãng oan 0, lộ dữ liệu 0). Mốc prepared còn đỏ: ROI 0,05, hoàn sai 270.000đ, lỗi oan 10 |
| Kho hoặc hãng có số xấu nhất: **kho HCM và hãng DNB (mốc prepared)**. Nếu chỉ nhìn phân khúc này, quyết định có đổi không? | Ở mốc prepared: kho HCM pass 0,5, hoàn sai 270.000đ, 10 lỗi oan; hãng DNB pass 0,5, hoàn sai 140.000đ, 5 lỗi oan; hãng GHSH pass 0,8889, hoàn sai 130.000đ. Ở mốc after mọi kho và hãng của S6 đều pass 1,0, hoàn sai 0, lỗi oan 0 và không kho nào đắt hơn làm tay. Chỉ nhìn phân khúc này quyết định không đổi. Phân khúc còn xấu ở bộ nền: kho `?` (đơn không có kho) 10.359đ/ticket > làm tay, đã nằm trong risk register ở v1 |
| Quyết định (khoanh một) | **Tiếp tục** |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | `R-S6-after-20261118-195935-28ec93`: cả 5 chỉ số bắt buộc đạt: pass_rate 1,0 ≥ 0,95; pass_k 1,0 ≥ 0,90; hoàn sai 0đ; lỗi hãng oan 0; lộ dữ liệu 0 |
| Bằng chứng 2 | `R-S6-after-20261118-195935-28ec93`: ba ngưỡng business_ops đạt (5.228đ ≤ 8.000đ; ROI 0,91 ≥ 0,5; 0 ca bị ùn); `R-base-after-20261118-195935-28ec93`: bộ nền vẫn 1,0 / 1,0, ROI 1,24, 4.456đ/ticket (không regression) |
| Bằng chứng 3 | So `R-S6-prepared-20261118-195916-1744de` → `R-S6-after-20261118-195935-28ec93`: pass_rate 0,8333 → 1,0; hoàn sai 270.000đ → 0; lỗi oan 10 → 0; ROI 0,05 → 0,91; lệnh `lab10.grade --incident S6` in "Được phép cân nhắc 'Tiếp tục'" |
| Khớp dòng nào trong `decision_rule` đã ký? | "Tiếp tục": mọi ngưỡng bắt buộc đạt trên mọi bộ thử có tại lúc quyết định (bộ nền và gói S6), ba ngưỡng business_ops đạt và không còn dòng vượt trần |
| Nếu Thu hẹp: cắt kho nào / còn bao nhiêu phần trăm / mấy người trực, và ticket bị cắt đi đâu | (không áp dụng) |
| Nếu Cải tiến thêm: giả thuyết cụ thể (nhánh nào của fault tree) + hạn | (không áp dụng) |
| Nếu Dừng: bài học ghi lại | (không áp dụng) |
| Ngày quyết định lại (trừ khi Dừng) | **01/12/2026**, khi REFUND-v4 có hiệu lực, và ngay sau Bước đánh giá 2 với dữ liệu thật |
| PIC ký | NV-TUNG (Lê Thanh Tùng); cùng bàn: Dương Văn Công, Lê Quang Huy, Nguyễn Khôi Nguyên, Vũ Xuân Trường |

**Chỉ ở v2**
- Quyết định đổi hay giữ so với v1? Vì con số nào: **Giữ "Tiếp tục"**, nhưng v1 chỉ đúng trên bộ nền. Trên thẻ S6 ở mốc prepared, report không đỡ được "Tiếp tục" (pass_rate 0,8333, hoàn sai 270.000đ, ROI 0,05); sau khi sửa (after) các số đó thành 1,0, 0đ, 0,91 nên quyết định được giữ bằng bằng chứng mới.
- Report tự kiểm tra: mã lần chạy `R-S6-grade-20261118-195916-1744de` (chạy trước khi sửa) · ô nào còn đỏ (nguyên nhân × tầng): mốc after không còn ô đỏ; chỗ còn hở ở nhánh [1] (tracking sai, tầng dữ liệu) và nhánh [3] (hai lỗi đầu của ngày, tầng vận hành) vì report chạy trên dữ liệu mock.
- Cổng vòng 1 (mốc prepared) đã đỡ được gì trước khi bàn biết sự cố, và bỏ sót gì: đỡ được sai kiện khi đơn tách kiện nhưng ticket có một kiện trễ (S6-01…S6-04, lỗi oan 40 → 10) và ghi dồn lỗi (S6-42, S6-43 bị chuyển người); bỏ sót ca hai kiện cùng trễ mà ticket không nói rõ (S6-20, S6-21, hỏng 5/5 seed) và làm ROI sụt xuống 0,05.
- Report ghi "được phép cân nhắc Tiếp tục" hay "không đủ căn cứ"? Quyết định của bàn có khớp không: ghi "Được phép cân nhắc 'Tiếp tục'" ở mốc after; quyết định của bàn là Tiếp tục nên khớp.
- Một thứ bộ thử hôm nay chưa đo, và nó ảnh hưởng quyết định ra sao: độ chính xác tracking theo từng kiện và tỉ lệ đơn tách kiện thật (gói S6 chỉ có 12 ticket, 7 đơn tách kiện); nếu tỉ lệ ca không rõ kiện thật cao hơn 0,30 thì quyết định đổi thành Thu hẹp.

**Ba dòng bắt buộc** (chép nguyên ba câu này sang `submission/submission.json`, mục `three_lines`)
1. Một giả định về môi trường mà thiết kế của đội đang dựa vào, có thể sai ngoài thực tế: Dữ liệu tracking theo từng kiện (ngày giao, hãng, tài xế) do hãng quét mã đúng và kịp; thực tế hãng nhỏ quét muộn hoặc gán nhầm tài xế.
2. Gate của đội chỉ GIẢM khả năng hay thực sự NGĂN được tác hại? Vì sao: Cổng NGĂN được ca đoán kiện khi ≥ 2 kiện cùng trễ và việc ghi quá 2 lỗi mỗi hãng mỗi ngày, nhưng chỉ GIẢM tác hại tổng, vì nếu tracking sai hoặc khách ghi sai mã kiện hợp lệ thì cổng vẫn tin.
3. Vì data là mock, cần đo lại gì trong pilot thật trước Bước đánh giá 2: Tỉ lệ đơn tách kiện thật và tỉ lệ ticket không nêu mã kiện, độ chính xác và độ trễ quét mã tracking theo từng hãng, và số ca bị giữ lỗi hãng mỗi ngày so với trần 2.
