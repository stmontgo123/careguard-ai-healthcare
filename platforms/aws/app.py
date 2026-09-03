from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from src.models import AccessContext
from src.orchestrator import investigate_claim


st.set_page_config(page_title="ClaimGuard AI - AWS", page_icon="🛡️", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background: #f4f8fc; color: #0b2341; }
    .cg-hero { background: linear-gradient(135deg,#071f3d,#0b5fc6); padding: 2rem 2.2rem;
      border-radius: 18px; color: white; margin-bottom: 1.2rem; }
    .cg-hero h1 { margin: 0; font-size: 2.55rem; }
    .cg-badge { display:inline-block; margin-top:.8rem; padding:.35rem .7rem; border-radius:999px;
      color:#064e3b; background:#dff7eb; font-weight:700; }
    .cg-callout { border-left: 6px solid #16866b; background:white; padding:1rem 1.2rem;
      border-radius:10px; box-shadow:0 3px 16px rgba(11,35,65,.08); }
    </style>
    <div class="cg-hero">
      <div style="letter-spacing:.12em;font-weight:700;opacity:.8">CAREGUARD AI</div>
      <h1>ClaimGuard - AWS Edition</h1>
      <div>Resolve a denied claim without widening the PHI boundary.</div>
      <span class="cg-badge">SYNTHETIC DATA ONLY - NO REAL PHI/ePHI</span>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Authorized session")
    st.text_input("User", "claims-demo-01", disabled=True)
    st.text_input("Role", "CLAIMS_SPECIALIST", disabled=True)
    st.text_input("Purpose", "PAYMENT", disabled=True)
    st.text_input("Assigned case", "CASE-2026-0917", disabled=True)
    st.caption("Authorization and minimum-necessary filtering occur before model context.")

ctx = AccessContext(
    user_id="claims-demo-01",
    role="CLAIMS_SPECIALIST",
    purpose="PAYMENT",
    member_id="MEM-2048",
    case_id="CASE-2026-0917",
    assigned_case_ids=("CASE-2026-0917",),
)

if "claim_result" not in st.session_state:
    st.session_state.claim_result = None
if "audit" not in st.session_state:
    st.session_state.audit = []

top_left, top_right = st.columns([1, 1])
with top_left:
    st.subheader("Synthetic denial")
    st.markdown("**Claim:** CLM-784291  \n**Denied:** CO-197  \n**Submitted CPT:** 73722")
with top_right:
    st.subheader("Known authorization")
    st.markdown("**Prior auth:** PA-55219  \n**EHR order CPT:** 73721  \n**Coverage:** active")

if st.button("Investigate denied claim", type="primary", use_container_width=True):
    st.session_state.audit = []
    st.session_state.claim_result = investigate_claim(
        ctx,
        "CASE-2026-0917",
        audit_sink=st.session_state.audit.append,
    )

result = st.session_state.claim_result
if result:
    st.markdown("### Evidence-grounded resolution")
    st.markdown(f"<div class='cg-callout'>{result['recommendation']}</div>", unsafe_allow_html=True)
    st.info(
        f"Proposed action {result['action']['action_id']} is {result['action']['status']}. "
        "A human reviewer must decide."
    )
    a, b = st.columns(2)
    if a.button("Approve corrected-claim preparation", use_container_width=True):
        result["action"]["status"] = "APPROVED"
        st.success("Approved for preparation only. No claim was submitted by the AI.")
    if b.button("Reject and route to UM", use_container_width=True):
        result["action"]["status"] = "REJECTED"
        st.warning("Rejected. Route to Utilization Management for review.")

    with st.expander("Authorized evidence and policy"):
        st.json({"evidence": result["evidence"], "policies": result["policies"]})
    with st.expander("Audit trail"):
        st.json([event.to_dict() for event in st.session_state.audit])
