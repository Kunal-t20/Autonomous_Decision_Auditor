import streamlit as st
import requests
from typing import Dict, Any

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Autonomous Decision Auditor", page_icon="", layout="wide")

st.title("Autonomous Decision Auditor")
st.markdown("Evaluate the logical strength of a reasoning paragraph, check against custom policies, and interact with the Human-in-the-loop fallback.")

st.sidebar.header("Settings")
api_base_url = st.sidebar.text_input("Backend API URL", API_URL)


with st.form("audit_form"):
    st.subheader("Submit Audit Request")
    reasoning = st.text_area("Reasoning Paragraph", height=120, placeholder="e.g. We should deploy to production today because the build passed.")
    evidence_text = st.text_area("Evidence List (one per line)", height=100, placeholder="Build 403 passed successfully.")
    policies_text = st.text_area("Custom Policies (one per line)", height=100, placeholder="No Friday deployments allowed unless hotfix.")
    
    submitted = st.form_submit_button("Run Audit")
    
if submitted:
    if not reasoning.strip():
        st.error("Reasoning paragraph is required.")
    else:
        # Pre-process inputs
        evidence = [e.strip() for e in evidence_text.split('\n') if e.strip()]
        policies = [p.strip() for p in policies_text.split('\n') if p.strip()]
        
        payload = {
            "reasoning": reasoning,
            "evidence": evidence,
            "policies": policies
        }
        
        with st.spinner("Analyzing rules, extracting claims, mapping evidence..."):
            try:
                response = requests.post(f"{api_base_url}/audit", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.session_state['last_audit_result'] = result
                else:
                    st.error(f"API Error ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

# Display Result
if 'last_audit_result' in st.session_state:
    st.markdown("---")
    res = st.session_state['last_audit_result']
    verdict = res.get("verdict", "UNKNOWN")
    conf = res.get("confidence", 0.0)
    explanation = res.get("explanation", {})
    breakdown = res.get("breakdown", {})
    audit_id = res.get("audit_id")
    
    col1, col2 = st.columns(2)
    with col1:
        if verdict == "ACCEPT":
            st.success(f"Verdict: **{verdict}**")
        elif verdict == "REJECT":
            st.error(f"Verdict: **{verdict}**")
        elif verdict == "ESCALATE":
            st.warning(f"Verdict: **{verdict}** ⚠️ Review Needed")
        else:
            st.metric(label="Verdict", value=verdict)
            
    with col2:
        st.metric(label="Confidence Score", value=f"{conf:.0%}")
        
    st.subheader("Explanation")
    if isinstance(explanation, dict):
        # Flatten explanation dictionary if it exists
        summary = explanation.get("summary", "")
        if summary:
            st.info(summary)
        else:
            st.json(explanation)
    else:
         st.write(explanation)

    with st.expander("Detailed Breakdown"):
        st.json(breakdown)

    if verdict == "ESCALATE":
        st.markdown("### ⚠️ Human-in-the-Loop Required")
        with st.form("resolve_form"):
            st.write(f"Audit `#{audit_id}` requires human resolution. Please review the breakdown above and decide the final verdict.")
            final_v = st.radio("Final Verdict", ("ACCEPT", "REJECT"))
            reviewer_notes = st.text_area("Reviewer Notes", placeholder="Reasoning for overriding or resolving this decision.")
            resolve_submitted = st.form_submit_button("Submit Resolution")
            
            if resolve_submitted:
                res_payload = {
                    "final_verdict": final_v,
                    "reviewer_notes": reviewer_notes
                }
                try:
                    resolve_resp = requests.post(f"{api_base_url}/audit/{audit_id}/resolve", json=res_payload)
                    if resolve_resp.status_code == 200:
                        st.success(f"Audit {audit_id} resolved to {final_v} successfully!")
                        # Update session to hide form gracefully
                        st.session_state['last_audit_result']['verdict'] = final_v
                        st.rerun()
                    else:
                        st.error(f"Failed to resolve: {resolve_resp.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
