import streamlit as st
import pandas as pd
import urllib.parse
from engine import extract_website_context, generate_cold_email

st.set_page_config(
    page_title="ColdCraft Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern Custom Styling (Clean, dark-mode desktop workspace aesthetic)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Top navigation badge */
    .top-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        background: rgba(34, 197, 94, 0.1);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.25);
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }

    /* Simulated Email Client Preview */
    .email-preview-container {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }

    .email-window-bar {
        background: #1e293b;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid #334155;
    }

    .dot {
        width: 11px;
        height: 11px;
        border-radius: 50%;
        display: inline-block;
    }
    .dot-red { background: #ef4444; }
    .dot-yellow { background: #eab308; }
    .dot-green { background: #22c55e; }

    .email-header-meta {
        padding: 14px 20px;
        background: #131d31;
        border-bottom: 1px solid #1e293b;
        font-size: 0.88rem;
        color: #94a3b8;
    }

    .email-header-meta span {
        color: #f1f5f9;
        font-weight: 600;
    }

    .email-body-content {
        padding: 24px;
        background: #0b1120;
        color: #e2e8f0;
        font-size: 0.96rem;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    /* Clean inputs & buttons */
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        border-radius: 8px !important;
        border: 1px solid #2d3748 !important;
        background-color: #0d1117 !important;
        color: #f8fafc !important;
        font-size: 0.92rem !important;
    }

    div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px #6366f1 !important;
    }

    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.25rem !important;
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.45) !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Header Bar with Engine Status
col_title, col_status = st.columns([3, 2])
with col_title:
    st.markdown('<div class="top-badge">🟢 ColdCraft Engine Online</div>', unsafe_allow_html=True)
    st.title("ColdCraft Studio")
    st.caption("Precision B2B outreach generated on local open-weight models. ₹0 API fees • 100% On-Device Privacy.")

with col_status:
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        model_choice = st.selectbox("Model", ["qwen2.5:3b", "llama3.2:1b"], index=0, label_visibility="collapsed")
    with c2:
        outreach_tone = st.selectbox(
            "Tone",
            ["Professional & Consultative", "Direct & Punchy", "Warm & Relatable", "Challenger / Provocative"],
            index=0,
            label_visibility="collapsed"
        )

st.markdown("<hr style='border: none; border-top: 1px solid #1f2937; margin: 1.5rem 0 2rem 0;' />", unsafe_allow_html=True)

# Main Studio Workflow (Two-Column Layout)
col_setup, col_preview = st.columns([5, 6], gap="large")

with col_setup:
    st.markdown("### 1. Campaign Inputs")
    
    with st.container():
        sender_pitch = st.text_area(
            "Your Value Proposition",
            value="We deliver targeted technical modules and self-paced cloud labs that help engineering colleges bridge the curriculum-industry gap.",
            help="Describe what you solve and the core outcome for the prospect.",
            height=95
        )

    st.markdown("### 2. Target Profile")
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        lead_name = st.text_input("Decision Maker / Contact", value="Dean of Academic Affairs")
    with row1_c2:
        company_name = st.text_input("Target Organization", value="NIT Manipur")

    website_url = st.text_input(
        "Prospect Website", 
        value="https://nitmanipur.ac.in/", 
        placeholder="https://example.com"
    )

    with st.expander("⚡ Refine Delivery Strategy", expanded=False):
        c_goal, c_len = st.columns(2)
        with c_goal:
            email_goal = st.selectbox(
                "Campaign Objective",
                ["Academic Partnership", "Direct B2B Sale", "Consulting / Contract", "Feedback Call"],
                index=0
            )
        with c_len:
            email_length = st.select_slider(
                "Target Length",
                options=["Punchy (<80 words)", "Balanced (~110 words)", "Detailed (~150 words)"],
                value="Balanced (~110 words)"
            )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    generate_btn = st.button("Synthesize Outreach Draft", use_container_width=True)

with col_preview:
    st.markdown("### 3. Live Client Preview")

    if generate_btn:
        if not website_url.strip():
            st.warning("Please provide a valid website address to gather contextual intelligence.")
        else:
            with st.status("Analyzing company footprint with ColdCraft locally...", expanded=False) as status:
                st.write("🌐 Scraping landing page text and metadata...")
                site_intel = extract_website_context(website_url)
                st.write(f"🧠 Synthesizing custom draft with {model_choice}...")
                
                try:
                    res = generate_cold_email(
                        prospect_name=lead_name,
                        company_name=company_name,
                        site_context=site_intel,
                        sender_pitch=sender_pitch,
                        goal=email_goal if 'email_goal' in locals() else "Academic Partnership",
                        tone=outreach_tone,
                        length_pref=email_length if 'email_length' in locals() else "Balanced (~110 words)",
                        model=model_choice
                    )
                    status.update(label="ColdCraft draft ready for dispatch!", state="complete")
                    
                    # Store in session state for instant interaction
                    st.session_state['latest_res'] = res
                    st.session_state['latest_intel'] = site_intel
                    st.session_state['meta'] = {
                        "name": lead_name,
                        "company": company_name,
                        "url": website_url
                    }
                except Exception as ex:
                    status.update(label="Generation failed", state="error")
                    st.error(f"Inference error: {str(ex)}")

    if 'latest_res' in st.session_state:
        res = st.session_state['latest_res']
        meta = st.session_state['meta']
        
        # Subject picker
        subject_options = res.get("subject_lines", ["Quick note"])
        selected_subject = st.selectbox("Select Subject Line", subject_options, index=0)
        
        # Interactive Email Client UI Box
        raw_body = res.get("email_body", "").strip()
        
        st.markdown(f"""
        <div class="email-preview-container">
            <div class="email-window-bar">
                <span class="dot dot-red"></span>
                <span class="dot dot-yellow"></span>
                <span class="dot dot-green"></span>
                <span style="font-size: 0.8rem; color: #64748b; margin-left: 10px;">ColdCraft Composer • Draft</span>
            </div>
            <div class="email-header-meta">
                <div><b>To:</b> {meta['name']} &lt;{meta['company'].lower().replace(' ', '')}@domain&gt;</div>
                <div style="margin-top: 4px;"><b>Subject:</b> <span>{selected_subject}</span></div>
            </div>
            <div class="email-body-content">{raw_body}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        # Action Toolbar (Mailto link & CSV export)
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            mailto_url = f"mailto:?subject={urllib.parse.quote(selected_subject)}&body={urllib.parse.quote(raw_body)}"
            st.markdown(
                f'<a href="{mailto_url}" target="_blank" style="display: block; text-align: center; background: #1e293b; color: #f8fafc; padding: 0.6rem; border-radius: 8px; text-decoration: none; font-weight: 600; border: 1px solid #334155;">📬 Open in Email Client</a>',
                unsafe_allow_html=True
            )
        with btn_c2:
            row_data = {
                "Contact": meta['name'],
                "Company": meta['company'],
                "Website": meta['url'],
                "Subject": selected_subject,
                "Email Body": raw_body,
                "Call to Action": res.get("call_to_action", "")
            }
            csv_payload = pd.DataFrame([row_data]).to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Lead (.CSV)",
                data=csv_payload,
                file_name=f"coldcraft_lead_{meta['company'].lower().replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with st.expander("🔍 Scraped Context & Icebreaker Hook", expanded=False):
            st.markdown(f"**Identified Hook:**\n> {res.get('icebreaker', 'N/A')}")
            st.text_area("Sanitized Web Intel", st.session_state.get('latest_intel', ''), height=130, disabled=True)

    else:
        st.markdown("""
        <div style="background: #0f172a; border: 2px dashed #1e293b; border-radius: 12px; padding: 3rem 1.5rem; text-align: center; color: #64748b;">
            <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">⚡</div>
            <div style="font-weight: 600; color: #94a3b8; font-size: 1.05rem;">ColdCraft Canvas Ready</div>
            <div style="font-size: 0.88rem; max-width: 320px; margin: 0.4rem auto 0 auto;">
                Provide the prospect's details and pitch on the left to watch ColdCraft draft a tailored email here in real time.
            </div>
        </div>
        """, unsafe_allow_html=True)