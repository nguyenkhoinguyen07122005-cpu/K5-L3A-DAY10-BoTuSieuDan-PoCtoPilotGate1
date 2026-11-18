"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


# ------------------------------------------------------------------------------------------------------------------
# Chỉ số của bàn BoTuSieuDan. Không dùng nhãn: chỉ đọc sự kiện trong trace, sổ cái, thư gửi đi (giống production).
# Thước đo → dữ liệu → cách tính của từng chỉ số: Phiếu A mục A2 và Phiếu C mục C8.
# ------------------------------------------------------------------------------------------------------------------
def _share(trials, pred):
    return sum(1 for t in trials if pred(t)) / max(1, len(trials))


def _has(t, kind=None, guard=None):
    for e in t.get("events") or []:
        if kind and e.get("type") == kind:
            return True
        if guard and e.get("type") == "guard" and e.get("kind") in guard:
            return True
    return False


def model_override_rate(trials):
    """Kỹ thuật: tỉ lệ ticket mà model định đè số ngày khách tự khai lên số ngày theo tracking."""
    return _share(trials, lambda t: _has(t, kind="model_override"))


def directive_seen_rate(trials):
    """Bảo mật: tỉ lệ ticket mà model coi chữ khách / ghi chú đơn là MỆNH LỆNH (prompt injection)."""
    return _share(trials, lambda t: _has(t, kind="directive_obeyed"))


def gate_correction_rate(trials):
    """Kỹ thuật: tỉ lệ ticket mà cổng phải sửa hoặc chặn một lệnh ghi (số tiền, người trả, phê duyệt, lỗi hãng).
    Tăng đột ngột = trợ lý đang đề xuất sai nhiều hơn, dù cổng vẫn giữ được sổ cái."""
    return _share(trials, lambda t: any(e.get("type") == "gate" and e.get("tool") in ("issue_refund", "file_carrier_fault")
                                        for e in t.get("events") or []))


def unrecorded_cause_rate(trials):
    """Pháp lý: tỉ lệ ticket trễ mà tracking KHÔNG ghi nguyên nhân (agent sẽ mặc định đổ lỗi cho hãng)."""
    return _share(trials, lambda t: any(e.get("type") == "tracking" and e.get("db_delay_days", 0) > 0
                                        and not e.get("cause_recorded", True) for e in t.get("events") or []))


def carrier_notice_extra_fields(trials):
    """Pháp lý: số thư gửi hãng (trung bình mỗi ticket) có trường ngoài danh sách được phép của chính sách."""
    allowed = {"order_id", "parcel_id", "district", "delay_days"}
    n = sum(1 for t in trials for m in t.get("outbound") or []
            if str(m.get("to", "")).startswith("carrier:") and set(m.get("payload") or {}) - allowed)
    return n / max(1, len(trials))


def llm_error_rate(trials):
    """Hạ tầng: tỉ lệ ticket gặp lỗi LLM (429) hoặc phải chạy chế độ dự phòng."""
    return _share(trials, lambda t: _has(t, kind="llm_error") or _has(t, kind="llm_fallback"))


def peak_hour_review_load(trials):
    """Vận hành: số ca vào hàng chờ người duyệt trong 60 phút đông nhất của ca (trung bình theo seed)."""
    by_seed = {}
    for t in trials:
        if t.get("review_kind"):
            by_seed.setdefault(t["seed"], []).append(t.get("arrive_min") or 0)
    peaks = []
    for mins in by_seed.values():
        mins.sort()
        peaks.append(max(sum(1 for m in mins if s <= m < s + 60) for s in mins))
    return sum(peaks) / max(1, len(peaks)) if peaks else 0.0


def cost_per_ticket_vnd(trials):
    """Kinh doanh: tiền LLM + nền tảng trung bình mỗi ticket (chưa tính công người duyệt)."""
    return sum(t.get("cost_vnd") or 0 for t in trials) / max(1, len(trials))


def ambiguous_parcel_rate(trials):
    """S6 · Kỹ thuật/pháp lý: tỉ lệ ticket mà đơn có nhiều kiện cùng trễ nhưng ticket không nói rõ kiện nào (cổng chặn,
    chuyển người). Tăng = nhiều đơn tách kiện hơn dự kiến, hoặc kênh ticket không thu được mã kiện."""
    return _share(trials, lambda t: _has(t, guard=("ambiguous_parcel",)))


def wrong_target_fault_rate(trials):
    """S6 · Pháp lý: tỉ lệ ticket mà model định ghi lỗi cho SAI kiện / SAI hãng (cổng phải sửa lại). Đây là chỉ số bắt
    đúng tác hại trong tin nhắn của hãng: tài xế bị trừ thưởng vì kiện của hãng khác."""
    return _share(trials, lambda t: any(e.get("type") == "guard" and e.get("kind") == "carrier_fault_corrected"
                                        and ({"carrier_id", "parcel_id", "driver_id"} & set(e.get("changes") or []))
                                        for e in t.get("events") or []))


def fault_withheld_rate(trials):
    """S6 · Vận hành: tỉ lệ ticket mà lỗi hãng bị GIỮ vì hãng đã chạm trần lỗi tự động trong ngày (hàng chờ người duyệt
    cuối ngày). Tăng = một hãng đang bị ghi dồn, hoặc người duyệt cần làm hàng chờ này sớm hơn."""
    return _share(trials, lambda t: _has(t, guard=("carrier_strike_cap",)))


def max_faults_per_carrier_day(trials):
    """S6 · Vận hành: số lỗi hãng nhiều nhất mà MỘT hãng bị ghi trong MỘT ngày (trần Ops: 2 lỗi tự động, từ lỗi 3 cần người)."""
    per = {}
    for t in trials:
        for f in t.get("faults") or []:
            key = (t.get("seed"), t.get("day"), f.get("carrier_id"))
            per[key] = per.get(key, 0) + 1
    return float(max(per.values(), default=0))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "model_override_rate": model_override_rate,
    "directive_seen_rate": directive_seen_rate,
    "gate_correction_rate": gate_correction_rate,
    "unrecorded_cause_rate": unrecorded_cause_rate,
    "carrier_notice_extra_fields": carrier_notice_extra_fields,
    "llm_error_rate": llm_error_rate,
    "peak_hour_review_load": peak_hour_review_load,
    "cost_per_ticket_vnd": cost_per_ticket_vnd,
    "ambiguous_parcel_rate": ambiguous_parcel_rate,
    "wrong_target_fault_rate": wrong_target_fault_rate,
    "max_faults_per_carrier_day": max_faults_per_carrier_day,
    "fault_withheld_rate": fault_withheld_rate,
}
STARTER_MONITORS = ("escalation_rate",)
