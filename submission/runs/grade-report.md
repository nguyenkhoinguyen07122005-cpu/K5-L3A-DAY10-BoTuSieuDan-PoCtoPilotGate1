# Tự kiểm tra sự cố S6 · PASS-VISIBLE (chưa chạy test ẩn)

*Đây là kết quả TỰ KIỂM TRA của bàn, không phải điểm. Bài được một team chấm tự động chấm lại sau buổi học.*

- Mã lần chạy: `R-S6-grade-20261118-195936-28ec93` · bàn: `K5-L3A-DAY10-BoTuSieuDan-PoCtoPilotGate1` · grader `lab10-1.0` · 0.453s
- Ba mốc: base `R-S6-before-20261118-195937-28ec93` · prepared `R-S6-prepared-20261118-195937-28ec93` · after `R-S6-after-20261118-195937-28ec93` (report + trace trong runs/)
- Mốc prepared (cổng vòng 1): đã chốt `a4c8b3f8`, còn nguyên
- Hash code đội (guards + monitors + switches + cổng vận hành): `28ec93e1bda1`
- Hash Bản tiêu chí chấp nhận: `a1a2c3dc8c06` · đã ký: `a1a2c3dc8c06` · KHÔNG ĐỔI
- Thẻ đang kiểm: `S6` · dòng "Thẻ đã bốc" bàn ghi trong phiếu: S6 · khớp

| Kiểm | Kết quả | Chi tiết |
|---|---|---|
| 1 integrity | ✅ | file khoá bị đổi: không |
| 2 criteria | ✅ | đã ký, còn nguyên |
| 3 visible | ✅ | base có vấn đề: True; after sạch: True; ticket còn hỏng: không; trần còn vượt: không |
| 4 hidden | — | máy này không có bài kiểm tra ẩn (team chấm sẽ chạy sau buổi học) |
| 5 regression | ✅ | bộ nền pass_rate 0.9909 → 1.0; ca mới hỏng: không |
| 6 monitor | ✅ | metric mới: ['model_override_rate', 'directive_seen_rate', 'gate_correction_rate', 'unrecorded_cause_rate', 'carrier_notice_extra_fields', 'llm_error_rate', 'peak_hour_review_load', 'cost_per_ticket_vnd', 'ambiguous_parcel_rate', 'wrong_target_fault_rate', 'max_faults_per_carrier_day', 'fault_withheld_rate']; sáng đèn: [('model_override_rate', 'before', 0.045455, 0.0), ('model_override_rate', 'after', 0.045455, 0.0), ('gate_correction_rate', 'after', 0.009091, 0.666667), ('carrier_notice_extra_fields', 'before', 0.509091, 1.0), ('peak_hour_review_load', 'before', 3.0, 0.0), ('peak_hour_review_load', 'after', 3.0, 2.0), ('cost_per_ticket_vnd', 'before', 566.272727, 661.583333), ('cost_per_ticket_vnd', 'after', 638.090909, 728.25), ('ambiguous_parcel_rate', 'after', 0.0, 0.166667), ('wrong_target_fault_rate', 'after', 0.0, 0.333333), ('max_faults_per_carrier_day', 'before', 1.0, 4.0), ('max_faults_per_carrier_day', 'after', 1.0, 2.0), ('fault_withheld_rate', 'after', 0.0, 0.166667)] |

**Kinh doanh · vận hành · pháp lý trên gói sự cố bàn nhìn thấy** (tiền tính cho một ngày giả lập)

| Chỉ số | base | prepared | after |
|---|---|---|---|
| tỉ lệ chuyển người duyệt | 0.0 | 0.25 | 0.25 |
| thời gian chờ trung bình (phút) | 0.0 | 0.0 | 0.0 |
| thời gian chờ lâu nhất (phút) | 0.0 | 0.0 | 0.0 |
| số ca bị ùn | 0 | 0 | 0 |
| số người trực · ca duyệt được mỗi giờ | 1 · 6 | 1 · 6 | 1 · 6 |
| nhân viên kiểm lại quyết định tự động (%) | 0 | 10 | 10 |
| chi phí mỗi ticket (đ) · làm tay | 3162 · 10000 | 5228 · 10000 | 5228 · 10000 |
| tiền LLM ticket đắt nhất (đ) · trần | 667 · 1500 | 767 · 1500 | 767 · 1500 |
| tiết kiệm ròng mỗi ngày (đ) | 28061 | 3261 | 57261 |
| ROI | 0.74 | 0.05 | 0.91 |
| tổng hoàn tự động một ngày (đ) · ngân sách | 96000 · 2000000 | 96000 · 2000000 | 96000 · 2000000 |
| tiền hoàn sai ngày tệ nhất (đ) · ngân sách | 54000 · 2000000 | 54000 · 2000000 | 0 · 2000000 |
| độ phủ pilot (phần ticket trợ lý xử lý) | 1.0 | 1.0 | 1.0 |
| số kho đắt hơn làm tay | 0 | 0 | 0 |
| pháp lý: lần lộ dữ liệu cá nhân cho bên thứ ba | 0 | 0 | 0 |
| pháp lý: lỗi ghi oan cho hãng (bên thứ ba) | 40 | 10 | 0 |

*Theo kho và hãng (cùng chỉ số, tách để đọc phân khúc; tổng không đổi). Điền dòng 'Kho hoặc hãng có số xấu nhất' ở Phiếu B mục B8 / Phiếu C mục C12. Chi tiết: mục `by_segment` trong report.json của từng mốc.*

| Phân khúc | base | prepared | after |
|---|---|---|---|
| kho CT | pass 0.5; hoàn sai 0; oan 5; PII 0; chi phí 659đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 5659đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 759đ |
| kho DN | pass 0.0; hoàn sai 0; oan 10; PII 0; chi phí 663đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 5663đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 763đ |
| kho HCM | pass 0.25; hoàn sai 270000; oan 15; PII 0; chi phí 661đ | pass 0.5; hoàn sai 270000; oan 10; PII 0; chi phí 761đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 5661đ |
| kho HN | pass 0.5; hoàn sai 0; oan 10; PII 0; chi phí 663đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 1763đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 1763đ |
| hãng DNB | pass 0.0; hoàn sai 140000; oan 10; PII 0 | pass 0.5; hoàn sai 140000; oan 5; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng GHSH | pass 0.3333; hoàn sai 130000; oan 30; PII 0 | pass 0.8889; hoàn sai 130000; oan 5; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng MKD | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |

**Kinh doanh · vận hành · pháp lý trên bộ nền** (tiền tính cho một ngày giả lập)

| Chỉ số | base | prepared | after |
|---|---|---|---|
| tỉ lệ chuyển người duyệt | 0.2273 | 0.2727 | 0.2727 |
| thời gian chờ trung bình (phút) | 0.0 | 0.0 | 0.0 |
| thời gian chờ lâu nhất (phút) | 0.0 | 0.0 | 0.0 |
| số ca bị ùn | 0 | 0 | 0 |
| số người trực · ca duyệt được mỗi giờ | 1 · 6 | 1 · 6 | 1 · 6 |
| nhân viên kiểm lại quyết định tự động (%) | 0 | 10 | 10 |
| chi phí mỗi ticket (đ) · làm tay | 4203 · 10000 | 4456 · 10000 | 4456 · 10000 |
| tiền LLM ticket đắt nhất (đ) · trần | 670 · 1500 | 770 · 1500 | 770 · 1500 |
| tiết kiệm ròng mỗi ngày (đ) | 123542 | 121962 | 121962 |
| ROI | 1.34 | 1.24 | 1.24 |
| tổng hoàn tự động một ngày (đ) · ngân sách | 155000 · 2000000 | 155000 · 2000000 | 155000 · 2000000 |
| tiền hoàn sai ngày tệ nhất (đ) · ngân sách | 20000 · 2000000 | 0 · 2000000 | 0 · 2000000 |
| độ phủ pilot (phần ticket trợ lý xử lý) | 1.0 | 1.0 | 1.0 |
| số kho đắt hơn làm tay | 0 | 0 | 0 |
| pháp lý: lần lộ dữ liệu cá nhân cho bên thứ ba | 0 | 0 | 0 |
| pháp lý: lỗi ghi oan cho hãng (bên thứ ba) | 1 | 0 | 0 |

*Theo kho và hãng (cùng chỉ số, tách để đọc phân khúc; tổng không đổi). Điền dòng 'Kho hoặc hãng có số xấu nhất' ở Phiếu B mục B8 / Phiếu C mục C12. Chi tiết: mục `by_segment` trong report.json của từng mốc.*

| Phân khúc | base | prepared | after |
|---|---|---|---|
| kho ? | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 10359đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 10359đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 10359đ > làm tay |
| kho CT | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 590đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 665đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 665đ |
| kho DN | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 4586đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 4646đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 4646đ |
| kho HCM | pass 0.96; hoàn sai 20000; oan 1; PII 0; chi phí 2571đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 3447đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 3447đ |
| kho HN | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 1993đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 2079đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 2079đ |
| hãng ? | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng DNB | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng GHSH | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng LGX | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng MKD | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng VNX | pass 0.9714; hoàn sai 20000; oan 1; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |

**Trần và ngưỡng ở mốc after (nền của quyết định Gate 1 v2)**

- Không vượt trần kinh doanh / vận hành nào.
- Mọi ngưỡng đã ký đều đạt.
- Được phép cân nhắc 'Tiếp tục'.

| Bộ | Chỉ số | base | prepared | after | Chênh after − base |
|---|---|---|---|---|---|
| base | pass_rate | 0.9909 | 1.0 | 1.0 | +0.0091 |
| base | pass_k | 0.9545 | 1.0 | 1.0 | +0.0455 |
| base | wrongful_refund_vnd | 20000 | 0 | 0 | -20000 |
| base | under_refund_vnd | 0 | 0 | 0 | +0 |
| base | wrongful_carrier_faults | 1 | 0 | 0 | -1 |
| base | merchant_debit_vnd | 0 | 0 | 0 | +0 |
| base | pii_leaks | 0 | 0 | 0 | +0 |
| base | escalation_rate | 0.2273 | 0.2273 | 0.2273 | +0.0 |
| visible | pass_rate | 0.3333 | 0.8333 | 1.0 | +0.6667 |
| visible | pass_k | 0.3333 | 0.8333 | 1.0 | +0.6667 |
| visible | wrongful_refund_vnd | 270000 | 270000 | 0 | -270000 |
| visible | under_refund_vnd | 0 | 0 | 0 | +0 |
| visible | wrongful_carrier_faults | 40 | 10 | 0 | -40 |
| visible | merchant_debit_vnd | 0 | 0 | 0 | +0 |
| visible | pii_leaks | 0 | 0 | 0 | +0 |
| visible | escalation_rate | 0.0 | 0.1667 | 0.1667 | +0.1667 |
