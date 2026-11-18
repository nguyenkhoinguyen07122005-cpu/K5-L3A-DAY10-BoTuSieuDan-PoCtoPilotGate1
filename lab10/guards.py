"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

===================================================================================================================
CỔNG CỦA BÀN BoTuSieuDan · VÒNG 1 (cổng phòng ngừa, viết trước khi biết sự cố)

Nguyên tắc chung: chữ khách viết và chữ model suy ra KHÔNG BAO GIỜ quyết số tiền hay lỗi của hãng. Mọi lệnh ghi được
đối chiếu lại với NGUỒN SỰ THẬT (đơn hàng, tracking, chính sách đang hiệu lực theo ngày, bảng phê duyệt, sổ cái) ngay
trước khi ghi. Không có quy tắc nào dựa vào mã ticket hay câu chữ cụ thể.

  G0  pre_guard · ghim chính sách theo NGÀY HIỆU LỰC (effective_from..effective_to chứa hôm nay), không theo cờ
      `index_active` của chỉ mục (cờ đó là bản sao, có thể lệch khi đổi phiên bản chính sách).
      ← HAZOP issue_refund/INVALID (sai phiên bản chính sách) · pre-mortem kỹ thuật #2
  G1  write_gate · issue_refund: số tiền = quyền lợi tính lại từ DB (độ trễ theo tracking của đúng kiện khách hỏi,
      nguyên nhân ghi trong tracking, chính sách theo ngày). Khác thì sửa về đúng số; quyền lợi 0 thì chặn lệnh ghi.
      Người trả luôn là LogiX trừ khi có phê duyệt. Trừ phần đơn đã được hoàn trước đó (sổ cái là nguồn sự thật,
      không tin cờ `refund_status` của batch đêm); không ghi hai lần cho cùng ticket (chống ghi lặp khi LLM lỗi 429).
      ← B2 (T-002@55, model tin số ngày khách khai) · HAZOP issue_refund/WRONG, PERTURBED · pre-mortem kỹ thuật #1
  G2  write_gate · issue_refund: khoản vượt hạn mức tự động của chính sách phải có phê duyệt HỢP LỆ của CHÍNH
      ticket này (đúng ticket, đúng đơn, còn hạn, trạng thái valid, đủ hạn mức, người duyệt đúng người đứng tên).
      Không có thì chuyển người TRƯỚC khi ghi. Thêm trần Ops/Finance: tổng hoàn tự động cho một khách trong ngày.
      (Trần "từ lỗi thứ 3 của cùng một hãng trong ngày" ở vòng 1 nằm trong lệnh hoàn; vòng 2 chuyển sang G6.)
      ← HAZOP issue_refund/INVALID (phê duyệt của đơn khác, hết hạn) · pre-mortem kinh doanh
  G3  write_gate · file_carrier_fault: chỉ ghi lỗi khi tracking ghi rõ nguyên nhân thuộc `fault_causes` của chính sách
      đang hiệu lực và trễ thật ≥ ngưỡng; ghi đúng kiện / đúng hãng / đúng số ngày theo DB.
      ← pre-mortem pháp lý (hãng nhỏ bị ghi lỗi oan, bị phạt / đình chỉ) · HAZOP file_carrier_fault/INCOMPLETE
  G4  write_gate · notify_carrier: chỉ gửi cho hãng đúng các trường chính sách cho phép (`carrier_notice_fields`);
      bỏ chữ khách tự gõ và thông tin người nhận quà. send_reply: số tiền báo khách = số thật trong sổ cái.
      ← pre-mortem pháp lý (lộ dữ liệu cá nhân cho bên thứ ba) · HAZOP notify_carrier/PERTURBED
===================================================================================================================
VÒNG 2 · THẺ S6 · "Tài xế bị trừ thưởng vì kiện của hãng khác" (cổng thêm sau khi biết sự cố; cổng vòng 1 giữ nguyên)

Nguyên nhân gốc (không dừng ở nhánh đầu): hệ thống hình dung "một đơn = một số ngày trễ = một hãng", còn thực tế vận hành
là MỖI KIỆN có hãng, tài xế, ngày giao riêng. Khi ticket không nói rõ kiện nào, `helpers.ticket_parcel` âm thầm chọn kiện
trễ nhất rồi cổng vòng 1 coi lựa chọn đó là đúng. Hai hãng cùng trễ thì hãng bị ghi lỗi là hãng may rủi, và tài xế của
kiện đó bị trừ thưởng. Cổng vòng 1 sửa được "ghi nhầm kiện đúng hẹn" nhưng KHÔNG sửa được "không biết kiện nào".

  G5  write_gate · issue_refund (và file_carrier_fault): xác định ĐÚNG MỘT kiện mà ticket nói tới.
      - ticket có `parcel_id` mà kiện đó không thuộc đơn  → chuyển người (đầu vào không khớp thực tế).
      - ticket không có `parcel_id`, đơn có ≥ 2 kiện và ≥ 2 kiện trễ tới ngưỡng tính phí → CHUYỂN NGƯỜI TRƯỚC khi
        ghi khoản hoàn: không hoàn, không ghi lỗi hãng, không báo hãng. Không được đoán.
      - còn lại (ticket nói rõ kiện, hoặc chỉ có đúng một kiện trễ) → như vòng 1.
      ← HAZOP S6 file_carrier_fault/INCOMPLETE (thiếu kiện) và WRONG (chọn kiện theo "trễ nhất")
  G6  write_gate · file_carrier_fault: trần số lỗi tự động của một hãng trong ngày (`ops_limits`: 2) áp NGAY TẠI lệnh ghi
      lỗi. Vòng 1 chặn ở lệnh hoàn tiền (chuyển cả ticket cho người); vòng 2 tách hai việc: khách vẫn được hoàn tự
      động đúng chính sách, còn lỗi từ lần thứ 3 của hãng trong ngày bị GIỮ (không ghi, không báo hãng) chờ người duyệt.
      Rẻ hơn (không tốn một ca duyệt cho mỗi ticket) và đúng bản chất: khách không có lỗi, chỉ việc đổ lỗi cho hãng cần người.
      ← S6 "ghi một lèo mấy lỗi liền"
===================================================================================================================
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict

APPROVER_OF_RECORD = "NV-HANH"          # data/world.json → staff: trưởng ca CSKH, người duyệt vượt hạn mức


# ----------------------------------------------------------------------------------------------- tra cứu nguồn sự thật
def _policy(ctx):
    """Chính sách có hiệu lực theo NGÀY (nguồn sự thật), không theo cờ chỉ mục."""
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _target(ctx, order, policy):
    """G5 · kiện mà ticket nói tới: (parcel, None) nếu xác định được ĐÚNG MỘT kiện, (None, lý do) nếu phải để người xem.
    Không đoán theo "kiện trễ nhất" như helpers.ticket_parcel khi đơn có nhiều kiện cùng trễ."""
    parcels = order["parcels"]
    pid = ctx.ticket.get("parcel_id")
    if pid:
        hit = next((p for p in parcels if p["parcel_id"] == pid), None)
        if hit is None:
            return None, f"ticket ghi kiện {pid} không thuộc đơn {order['order_id']}"
        return hit, None
    if len(parcels) == 1:
        return parcels[0], None
    floor = int(policy["late"]["min_days_fee"])
    late = [p for p in parcels if H.db_delay_days(p, ctx.as_of) >= floor]
    if len(late) >= 2:
        who = ", ".join(f"{p['parcel_id']}/{p['carrier_id']}" for p in late)
        return None, f"đơn có {len(late)} kiện cùng trễ ({who}) mà ticket không nói rõ kiện nào"
    return (late[0] if late else max(parcels, key=lambda p: H.db_delay_days(p, ctx.as_of))), None


def _facts(ctx, order_id):
    """(order, parcel, delay_db, cause_recorded, policy, why_unclear) cho ticket đang xử lý, hoặc None nếu thiếu dữ liệu.
    `why_unclear` khác None = không xác định được kiện (parcel là None, delay là 0)."""
    order = ctx.tools.lookup_order(order_id)
    policy = _policy(ctx)
    if order is None or policy is None or not order.get("parcels"):
        return None
    parcel, why = _target(ctx, order, policy)
    if parcel is None:
        return order, None, 0, None, policy, why
    delay = H.db_delay_days(parcel, ctx.as_of)
    return order, parcel, delay, parcel.get("delay_cause"), policy, None


def _entitlement(ctx, order, parcel, delay, cause, policy):
    if delay > 0 and cause is None:     # trễ mà tracking không ghi nguyên nhân: không tự tính, để người xem
        return None
    return H.entitlement_vnd(policy, order, delay, cause)


def _approval_ok(ctx, appr, order_id, amount):
    return bool(appr) and appr.get("ticket_id") == ctx.ticket.get("ticket_id") and appr.get("order_id") == order_id \
        and appr.get("status") == "valid" and str(appr.get("expires_at", "")) >= ctx.as_of \
        and int(appr.get("max_vnd") or 0) >= amount \
        and appr.get("approver_id") == ((ctx.gates or {}).get("operations", {}).get("approver_id") or APPROVER_OF_RECORD)


def _valid_approval(ctx, order_id, amount):
    for a in ctx.tools.lookup_approvals(ticket_id=ctx.ticket.get("ticket_id")):
        if _approval_ok(ctx, a, order_id, amount):
            return a
    return None


# --------------------------------------------------------------------------------------------------------- G0
def pre_guard(ctx):
    policy = _policy(ctx)
    if policy is None:                                   # không có chính sách nào hiệu lực hôm nay: không tự quyết
        ctx.log("no_effective_policy", as_of=ctx.as_of)
        return Verdict.escalate("không có chính sách hoàn tiền nào hiệu lực ở ngày hôm nay")
    active = next((p for p in ctx.tools.lookup_policies() if p.get("index_active")), None)
    if active is None or active["policy_id"] != policy["policy_id"]:
        ctx.log("policy_index_drift", index_active=(active or {}).get("policy_id"), effective=policy["policy_id"])
    return Verdict.allow(policy_id=policy["policy_id"])


# ---------------------------------------------------------------------------------------------------- G1–G4
def write_gate(ctx, action):
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify(ctx, action)
    if tool == "send_reply":
        return _gate_reply(ctx, action)
    return Verdict.allow()


def _gate_refund(ctx, action):
    oid, tid = action.get("order_id"), action.get("ticket_id")
    f = _facts(ctx, oid)
    if f is None:
        return Verdict.escalate("thiếu đơn / tracking / chính sách để đối chiếu số tiền")
    order, parcel, delay, cause, policy, unclear = f
    asked = int(action.get("amount_vnd") or 0)

    # G5 · không xác định được đúng một kiện thì DỪNG TRƯỚC khi ghi khoản hoàn (không hoàn, không ghi lỗi, không báo hãng)
    if unclear:
        ctx.log("ambiguous_parcel", order_id=oid, ticket_parcel=ctx.ticket.get("parcel_id"), reason=unclear)
        return Verdict.escalate(f"{unclear}: chuyển người hỏi lại khách")

    # G1a · không ghi hai lần cho cùng ticket (ghi lặp khi "không chắc đã ghi")
    if ctx.tools.ledger_rows(ticket_id=tid):
        ctx.log("duplicate_refund_blocked", ticket_id=tid, asked=asked)
        return Verdict.deny("ticket này đã có dòng hoàn trong sổ cái: không ghi lần hai")

    # G1b · quyền lợi tính lại từ DB, trừ phần đơn đã được hoàn (sổ cái, không tin cờ batch đêm)
    ent = _entitlement(ctx, order, parcel, delay, cause, policy)
    if ent is None:
        ctx.log("cause_missing", order_id=oid, parcel_id=parcel["parcel_id"], db_delay=delay)
        return Verdict.escalate("trễ nhưng tracking không ghi nguyên nhân: chuyển người xác minh")
    already = sum(int(r["amount_vnd"]) for r in ctx.tools.ledger_rows(order_id=oid))
    due = max(0, ent - already)
    if due <= 0:
        ctx.log("refund_not_due", order_id=oid, asked=asked, entitlement=ent, already_refunded=already,
                db_delay=delay, cause=cause, policy_id=policy["policy_id"])
        return Verdict.deny(f"theo DB không còn khoản nào phải hoàn (quyền lợi {ent}đ, đã hoàn {already}đ)")

    changes = {}
    if asked != due:
        changes["amount_vnd"] = due
    if action.get("payer", "LOGIX") != "LOGIX":              # chữ trong ticket / ghi chú không được đổi người trả tiền
        changes["payer"] = "LOGIX"

    # G2 · phê duyệt và các trần Ops/Finance
    lim = ctx.tools.ops_limits()
    appr_id = action.get("approval_id")
    if due > int(policy["auto_limit_vnd"]):
        ok = appr_id and _approval_ok(ctx, next(iter(ctx.tools.lookup_approvals(approval_id=appr_id)), None), oid, due)
        if not ok:
            good = _valid_approval(ctx, oid, due)
            if good is None:
                ctx.log("approval_missing_or_invalid", order_id=oid, amount=due, approval_id=appr_id)
                return Verdict.escalate("vượt hạn mức tự động, chưa có phê duyệt hợp lệ của chính ticket này")
            changes["approval_id"] = good["approval_id"]
    else:
        if appr_id and not _approval_ok(ctx, next(iter(ctx.tools.lookup_approvals(approval_id=appr_id)), None), oid, due):
            changes["approval_id"] = None                     # không gắn phê duyệt không hợp lệ vào dòng sổ cái
        cust_cap = lim.get("max_auto_refund_per_customer_per_day_vnd")
        cust_today = sum(int(r["amount_vnd"]) for r in ctx.tools.ledger_rows(customer_id=order["customer_id"])
                         if not r.get("approval_id"))          # tính cả dòng cũ trong sổ: thà chuyển người sớm hơn
        if cust_cap is not None and cust_today + due > cust_cap:
            ctx.log("customer_daily_cap", customer_id=order["customer_id"], today=cust_today, asked=due, cap=cust_cap)
            return Verdict.escalate("vượt trần hoàn tự động cho một khách trong ngày: chuyển người duyệt")

    # Vòng 2 (S6): trần lỗi hãng KHÔNG còn chặn khoản hoàn cho khách. Khách không có lỗi gì khi hãng đã chạm trần,
    # nên khoản hoàn vẫn tự động; phần "ghi lỗi cho hãng" mới bị giữ lại cho người xem (xem G6 trong _gate_fault).

    if changes:
        ctx.log("refund_corrected", order_id=oid, asked=asked, due=due, db_delay=delay, cause=cause,
                policy_id=policy["policy_id"], changes=sorted(changes))
        return Verdict.modify("đối chiếu lại với DB: số tiền / người trả / phê duyệt theo nguồn sự thật", **changes)
    return Verdict.allow()


def _gate_fault(ctx, action):
    oid = action.get("order_id")
    f = _facts(ctx, oid)
    if f is None:
        return Verdict.deny("thiếu đơn / tracking / chính sách: không ghi lỗi cho hãng")
    order, parcel, delay, cause, policy, unclear = f
    if unclear:                                              # G5 · lớp thứ hai: không bao giờ ghi lỗi khi chưa rõ kiện
        return Verdict.deny(f"{unclear}: không ghi lỗi cho hãng nào")
    if not ctx.tools.ledger_rows(ticket_id=action.get("ticket_id")):
        return Verdict.deny("chưa có khoản hoàn hợp lệ cho ticket này: không ghi lỗi hãng")
    if not H.carrier_at_fault(policy, parcel, delay):
        ctx.log("carrier_fault_blocked", parcel_id=parcel["parcel_id"], carrier_id=parcel["carrier_id"],
                db_delay=delay, recorded_cause=cause, policy_id=policy["policy_id"])
        return Verdict.deny(f"tracking không cho thấy lỗi hãng (trễ {delay} ngày, nguyên nhân {cause})")
    cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")   # G6 · trần lỗi tự động của một hãng trong ngày
    strikes = len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"]))
    if cap is not None and strikes >= cap:
        ctx.log("carrier_strike_cap", carrier_id=parcel["carrier_id"], strikes_today=strikes, cap=cap, at="file_carrier_fault")
        return Verdict.deny(f"hãng {parcel['carrier_id']} đã có {strikes} lỗi tự động trong ngày: lỗi này cần người xem")
    want = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
            "driver_id": parcel.get("driver_id"), "delay_days": delay}
    changes = {k: v for k, v in want.items() if action.get(k) != v}
    if changes:
        ctx.log("carrier_fault_corrected", changes=sorted(changes))
        return Verdict.modify("ghi lỗi đúng kiện, đúng hãng, đúng số ngày theo tracking", **changes)
    return Verdict.allow()


def _gate_notify(ctx, action):
    policy = _policy(ctx)
    allowed = (policy or {}).get("carrier_notice_fields") or ["order_id", "parcel_id", "district", "delay_days"]
    payload = action.get("payload") or {}
    keep = {k: v for k, v in payload.items() if k in allowed}
    if not ctx.tools.fault_rows(ticket_id=action.get("ticket_id"), carrier_id=action.get("carrier_id")):
        return Verdict.deny("không có lỗi hãng hợp lệ đã ghi cho ticket này: không báo hãng")
    if keep != payload:
        ctx.log("carrier_notice_trimmed", dropped=sorted(set(payload) - set(keep)))
        return Verdict.modify("chỉ gửi hãng các trường chính sách cho phép", payload=keep)
    return Verdict.allow()


def _gate_reply(ctx, action):
    paid = sum(int(r["amount_vnd"]) for r in ctx.tools.ledger_rows(ticket_id=action.get("ticket_id")))
    if int(action.get("amount_vnd") or 0) != paid:
        ctx.log("reply_amount_fixed", said=action.get("amount_vnd"), ledger=paid)
        return Verdict.modify("số tiền báo khách phải bằng số trong sổ cái", amount_vnd=paid)
    return Verdict.allow()
