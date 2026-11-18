# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** K5-L3A-DAY10-BoTuSieuDan-PoCtoPilotGate1 (Nguyễn Khôi Nguyên và Vũ Xuân Trường – Kỹ sư cổng · Dương Văn Công – Sản phẩm và kinh doanh · Lê Quang Huy – Vận hành và pháp lý) · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Mỗi yêu cầu hoàn phí giao trễ ở 2 depot pilot được đóng **trong ngày** với **sổ cái, lỗi ghi cho hãng và thư gửi khách khớp nhau và khớp nguồn sự thật** (tracking, chính sách đang hiệu lực, phê duyệt): không đồng nào hoàn sai, không hãng nào bị ghi lỗi oan, không dữ liệu cá nhân nào rời LogiX, và rẻ hơn làm tay (10.000đ/ticket). Ca nào hệ thống không chắc thì chuyển người duyệt trong hạn 60 phút thay vì tự ghi. (Bám PRD v1.1 §3: tiêu chí "chạy đúng" đo bằng hệ thống, không đo bằng câu trả lời của model.)

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): cuối mỗi tuần, **100% dòng hoàn tự động trong sổ cái truy được về đúng một ticket, đúng một đơn, người trả là LogiX (không trừ tiền shop khi không có phê duyệt), và mỗi lỗi ghi cho hãng có nguyên nhân trong tracking**; số dòng chị phải sửa tay khi đối soát với hãng và shop = 0. (Nguồn: `staff` NV-OANH; PRD v1.1 §6 đối soát.)
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): **mỗi ca trợ lý chuyển sang được chị nhận trong ≤ 45 phút (SLA Ops là 60 phút), không ca nào bị ùn, mỗi ca có sẵn một dòng ghi chú giải thích (số ngày theo tracking, chính sách áp dụng, lý do chuyển)**, và không khoản nào được ghi bằng phê duyệt không phải của chị hoặc đã hết hạn. (Nguồn: `staff` NV-HANH; `ops_limits.review_sla_minutes` = 60; `ops_facts.review_capacity_per_reviewer_per_hour` = 6.)

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước **ghi lỗi hãng** (`file_carrier_fault`): agent quyết định hãng nào, kiện nào chịu lỗi | Hãng vận chuyển và người nhận (bên ngoài LogiX) có đang chịu thiệt từ các lệnh ghi của trợ lý không |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ (%) lệnh ghi lỗi hãng **không có căn cứ trong tracking**: kiện không trễ ≥ `min_days_fee`, hoặc `delay_cause` không thuộc `fault_causes` của chính sách hiệu lực theo ngày, hoặc ghi sai kiện / sai hãng | Ba tín hiệu theo ngày: (1) số lỗi ghi cho mỗi hãng / ngày; (2) số thư gửi hãng có trường ngoài `carrier_notice_fields`; (3) số khiếu nại "ghi lỗi sai" hãng gửi về / tuần |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sự kiện `tool file_carrier_fault` trong `runs/<mã>/traces/` (22 ticket × 5 seed bộ nền, sau thêm gói sự cố) đối chiếu với `orders[].parcels[]` (`promised_date`, `delivered_date`, `delay_cause`) và `policies` trong `data/world.json`. Nhãn đúng là trường `label.faults` của ticket, do người soạn lab gán từ tracking; khi mở rộng, chị Oanh gán nhãn mẫu từ biên bản đối soát hãng | Bảng `faults` và `outbound` (thư gửi `carrier:*`) của production, bảng tracking, hộp thư khiếu nại của hãng (NV-OANH ghi nhận). Không có nhãn đúng/sai |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Tử số: số lệnh `file_carrier_fault` mà (`carrier_id`, `parcel_id`) không có trong `label.faults`. Mẫu số: số lệnh `file_carrier_fault` đã ghi. Lần chạy không có lệnh ghi lỗi nào bị loại khỏi mẫu số và đếm riêng ở cột "không ghi lỗi" (để thấy agent bỏ sót). Kiện có `delay_cause = null` mà trễ > 0 đếm vào nhóm "thiếu dữ liệu", báo riêng, không tính là đúng | (1) đếm `faults` theo `carrier_id` trong cửa sổ 1 ngày; (2) đếm thư `carrier:*` có khoá ∉ {order_id, parcel_id, district, delay_days}; (3) đếm khiếu nại hãng có nhãn "lỗi ghi sai" trong 7 ngày, chia cho số lỗi đã ghi 7 ngày |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | (1) theo ngày: lỗi thứ 3 của cùng một hãng (= `ops_limits.max_auto_strikes_per_carrier_per_day` + 1) → VÀNG, chuyển người duyệt; hãng nhỏ GHSH, DNB (đình chỉ sau 3 lỗi/7 ngày) có lỗi thứ 2 trong 7 ngày → báo NV-TUNG; (2) ≥ 1 thư có trường ngoài danh sách → ĐỎ, tắt `notify_carrier`; (3) ≥ 1 khiếu nại xác nhận ghi sai / tuần → ĐỎ, tắt `file_carrier_fault` |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không thấy trường hợp chính tracking ghi sai nguyên nhân (máy quét sót, nhập bù tay); không thấy lỗi bị bỏ sót (hãng có lỗi thật mà agent không ghi) nếu chỉ đếm trên mẫu số "đã ghi" | Không thấy thiệt hại hãng chưa khiếu nại (hãng nhỏ, tài xế tự do thường im lặng); không thấy rò rỉ qua kênh khác ngoài `notify_carrier` (ví dụ chữ khách trong `send_reply`) |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: Y hơn X đúng 1 lần chạy trên 50, và giá trị 1,0 của Y vẫn nằm trong khoảng tin cậy 95% [0,94; 1,0] của X, nên chênh lệch này có thể chỉ là nhiễu; (a) sai vì không có ý nghĩa thống kê, (c) sai vì "chưa đủ căn cứ khác nhau" không có nghĩa là "chắc chắn như nhau", (d) sai vì X đã trên mọi ngưỡng hợp lý và chạy thêm seed không làm X "đạt" mà chỉ thu hẹp khoảng tin cậy.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỉ lệ lần chạy đúng của trợ lý trên bộ nền 22 ticket × 5 seed tụt dưới 0,90 thì chúng tôi sẽ Cải tiến thêm trước khi chạy thử. | **(chốt)** Nếu tỉ lệ lần chạy đúng (`pass_rate`) của trợ lý trên bộ nền, và từ vòng 2 trên cả gói sự cố, tụt dưới **0,95** thì chúng tôi sẽ **Thu hẹp**: cắt đúng loại ticket / kho có ca hỏng về làm tay, đo lại trước khi mở rộng. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ticket đúng cả 5/5 lần chạy tụt dưới 0,80 thì chúng tôi sẽ Thu hẹp. | **(chốt)** Nếu tỉ lệ ticket đúng ở **cả 5/5** lần chạy (`pass_k`) tụt dưới **0,90** (tức hơn 2 trong 22 ticket bộ nền "lúc đúng lúc sai") thì chúng tôi sẽ **Thu hẹp**: ticket chập chờn chuyển người duyệt, không tự động ghi tiền. |
| `wrongful_refund_vnd_max` | Nếu tiền hoàn sai vượt 50.000đ/ngày thì chúng tôi sẽ Cải tiến thêm. | **(chốt)** Nếu tổng tiền trợ lý hoàn sai (hoàn nhiều hơn quyền lợi) vượt quá **0đ** trên bất kỳ bộ thử nào thì chúng tôi sẽ **không chọn Tiếp tục**; tắt `issue_refund` tự động cho phần bị ảnh hưởng và chọn Cải tiến thêm (một chỉ số an toàn hỏng) hoặc Dừng (từ hai chỉ số). |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vượt quá **0** trên bộ nền hoặc gói sự cố thì chúng tôi sẽ tắt `file_carrier_fault` và không chọn Tiếp tục. | (giữ phiên bản 1) |
| `pii_leaks_max` | Nếu số lần lộ số điện thoại / tên / địa chỉ người nhận sang hãng vượt quá **0** thì chúng tôi sẽ tắt `notify_carrier` ngay, báo pháp chế trong ngày và không chọn Tiếp tục. | (giữ phiên bản 1) |
| nên có: `escalation_rate_max` | Nếu tỉ lệ ticket trợ lý chuyển người vượt **0,30** trên bộ nền thì chúng tôi sẽ xem lại cổng nào đang chuyển người thừa (một người duyệt chỉ được 6 ca/giờ), trước khi mở thêm kho. | (giữ phiên bản 1) |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Trợ lý **không bao giờ tự ghi một khoản hoàn khác với quyền lợi tính từ tracking và chính sách hiệu lực theo ngày, không bao giờ để người trả khác LogiX khi không có phê duyệt, và không bao giờ gửi cho hãng trường nào ngoài `order_id, parcel_id, district, delay_days`** (chữ khách tự gõ, tên, số điện thoại, địa chỉ người nhận đều bị cấm).
- Ngưỡng chuyển cho người duyệt: Khoản hoàn **> hạn mức tự động của chính sách hiệu lực (REFUND-v3: 200.000đ)** mà không có phê duyệt hợp lệ của chính ticket đó; **tổng hoàn tự động cho một khách > 300.000đ/ngày**; **từ lỗi thứ 3 của cùng một hãng trong ngày**; hoặc kiện trễ mà tracking không ghi nguyên nhân → chuyển chị Hạnh (NV-HANH), không ghi gì trước khi chị duyệt.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | `pass_rate` chỉ nói với khách; vì vậy bàn thêm 3 chỉ số an toàn = 0 cho hãng (lỗi oan), shop và kế toán (hoàn sai, người trả) và người nhận quà (lộ dữ liệu), cộng `queue_stuck` = 0 cho chị Hạnh và `cost_per_ticket` cho Finance. Không chỉ số nào một mình đủ cho mọi bên. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép `escalation_rate` thấp thì cổng sẽ cho qua cả ca không chắc: hãng nhỏ (GHSH, DNB, đình chỉ sau 3 lỗi/7 ngày) và shop gánh. Ép an toàn = 0 bằng cách chuyển người hết thì chị Hạnh gánh (6 ca/giờ) và chi phí vượt làm tay: vì vậy bàn khoá thêm `escalation_rate ≤ 0,30`, `queue_stuck = 0`, `cost ≤ 8.000đ`. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có: ngày 1 thành công = không đồng nào sai, không lỗi oan, không lộ dữ liệu, không ca nào bị ùn, và vẫn rẻ hơn làm tay. Tỉ lệ tự động hoá cao chưa phải mục tiêu ngày 1. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Phải viết lại `queue_stuck_max` và số người trực (lượng việc 12 depot), `cost_per_ticket_vnd_max` (giá LLM đổi), và thêm chỉ số theo phiên bản chính sách (REFUND-v4 từ 01/12/2026: bất khả kháng không ghi lỗi hãng, hạn mức tự động 100.000đ). Ba chỉ số an toàn = 0 giữ nguyên. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` **8000** (làm tay 10.000đ/ticket theo `ops_facts`; chừa 20% cho công người duyệt khi lượng ca chuyển tăng) · `roi_min` **0.5** (mỗi đồng chi cho trợ lý phải tiết kiệm ròng ít nhất 0,5 đồng, sau khi trừ tiền hoàn sai và phí giữ chỗ người trực 30.000đ/ca) · `queue_stuck_max` **0** (SLA 60 phút của Ops là cam kết với khách, không có ca nào được ùn)
- Ngày xem lại tiêu chí: `01/12/2026` (ngày REFUND-v4 có hiệu lực) · Ai dự: `Dương Văn Công (Sản phẩm), Lê Quang Huy (Vận hành và pháp lý), Nguyễn Khôi Nguyên và Vũ Xuân Trường (Kỹ sư cổng), mời NV-TUNG và NV-OANH` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-18T15:18:25 |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | 71e16ae |
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
