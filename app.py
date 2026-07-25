import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Review Extraction Pipeline",
    page_icon="◇",
    layout="wide",
)

# Minimalist Custom CSS (Linear / Notion aesthetic)
st.markdown(
    """
<style>
    /* Minimalist System Typography */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Subtle Headers */
    .main-title {
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 4px;
    }
    
    .sub-title {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 24px;
    }

    /* Minimal Card */
    .minimal-card {
        border: 1px solid rgba(226, 232, 240, 0.15);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        background: rgba(255, 255, 255, 0.02);
    }

    /* Simple Tag */
    .meta-tag {
        display: inline-block;
        background: rgba(148, 163, 184, 0.12);
        color: #cbd5e1;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    /* Clean Sentiment Pills */
    .badge-pos {
        color: #10b981;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-neg {
        color: #ef4444;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-neutral {
        color: #f59e0b;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown('<div class="main-title">Review Extraction Pipeline</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Extract key sentiment, themes, and pros/cons from customer reviews into MongoDB Atlas.</div>', unsafe_allow_html=True)

# Helper function
def fetch_all_reviews():
    try:
        res = requests.get(f"{API_URL}/reviews", timeout=4)
        if res.status_code == 200:
            return res.json().get("reviews", [])
    except Exception:
        pass
    return []

reviews_data = fetch_all_reviews()

# Minimal Sidebar
with st.sidebar:
    st.markdown("### Overview")
    total_reviews = len(reviews_data)
    pos_count = sum(1 for r in reviews_data if r.get("sentiment") == "pos")
    neg_count = sum(1 for r in reviews_data if r.get("sentiment") == "neg")
    neu_count = sum(1 for r in reviews_data if r.get("sentiment") == "neutral")

    st.metric("Total Extracted", total_reviews)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Positive", pos_count)
        st.metric("Neutral", neu_count)
    with col_s2:
        st.metric("Negative", neg_count)
        ratio = f"{int((pos_count/total_reviews)*100)}%" if total_reviews > 0 else "0%"
        st.metric("Positive %", ratio)

    st.markdown("---")
    st.markdown("### API Connection")
    api_online = False
    try:
        res = requests.get(f"{API_URL}/reviews", timeout=2)
        if res.status_code == 200:
            api_online = True
    except Exception:
        pass

    if api_online:
        st.caption("Backend Server: Connected")
    else:
        st.caption("Backend Server: Disconnected")


tab1, tab2 = st.tabs(["Analyze", "Database"])

PRESETS = {
    "Select an example...": "",
    "Sony WH-1000XM5 Review": "I bought the Sony WH-1000XM5 headphones and the noise cancellation is extraordinary! Battery life easily reaches 30 hours. However, the non-foldable design makes them a bit bulky for travel. Review by Nitish.",
    "MacBook Air M2 Review": "I've been using the MacBook Air M2 for a few weeks now for coding. The M2 chip performance is blazing fast, battery life easily lasts 14 hours, and the fanless build is completely silent! My only regret is getting the 8GB RAM base model. Review by Rahul Chaudhary.",
    "Doorbell Camera Review": "The installation was simple enough and 4K daytime video is sharp. However, night vision is blurry and motion detection triggers whenever a car passes. Review by Marcus.",
}

# --- TAB 1: ANALYZE ---
with tab1:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("##### Input Review")
        selected_preset = st.selectbox("Sample reviews:", list(PRESETS.keys()), label_visibility="collapsed")
        default_text = PRESETS[selected_preset] if selected_preset else ""

        review_input = st.text_area(
            "Review text",
            value=default_text,
            height=220,
            placeholder="Paste text here...",
            label_visibility="collapsed",
        )

        analyze_btn = st.button("Analyze Review", type="primary", use_container_width=True)

    with col_right:
        st.markdown("##### Extracted Insights")
        
        if analyze_btn:
            if not review_input.strip():
                st.warning("Please enter review text.")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        res = requests.post(f"{API_URL}/analyze", json={"text": review_input}, timeout=15)
                        if res.status_code == 200:
                            data = res.json()
                            
                            sentiment = (data.get("sentiment") or "neutral").lower()
                            sentiment_label = (
                                "Positive" if sentiment == "pos"
                                else "Negative" if sentiment == "neg"
                                else "Neutral"
                            )
                            
                            c1, c2 = st.columns(2)
                            c1.metric("Reviewer", data.get("name") or "Anonymous")
                            c2.metric("Sentiment", sentiment_label)

                            st.markdown("**Summary**")
                            st.write(data.get("summary") or "No summary.")

                            themes = data.get("key_themes") or []
                            if themes:
                                st.markdown("**Themes**")
                                tags = " ".join([f'<span class="meta-tag">{t}</span>' for t in themes])
                                st.markdown(tags, unsafe_allow_html=True)

                            st.markdown("---")
                            col_p, col_c = st.columns(2)
                            with col_p:
                                st.markdown("**Pros**")
                                pros = data.get("pros") or []
                                if pros:
                                    for p in pros:
                                        st.write(f"• {p}")
                                else:
                                    st.caption("None reported")

                            with col_c:
                                st.markdown("**Cons**")
                                cons = data.get("cons") or []
                                if cons:
                                    for c in cons:
                                        st.write(f"• {c}")
                                else:
                                    st.caption("None reported")

                        else:
                            st.error(f"API Error: {res.json().get('detail')}")
                    except Exception as e:
                        st.error(f"Failed to connect to server: {e}")
        else:
            st.caption("Enter review text on the left and click 'Analyze Review'.")

# --- TAB 2: DATABASE ---
with tab2:
    col_f1, col_f2 = st.columns([3, 1])
    with col_f1:
        search_query = st.text_input("Search", placeholder="Search by text or reviewer name...", label_visibility="collapsed")
    with col_f2:
        sentiment_filter = st.selectbox("Sentiment Filter", ["All", "Positive", "Negative", "Neutral"], label_visibility="collapsed")

    try:
        res = requests.get(f"{API_URL}/reviews", timeout=5)
        if res.status_code == 200:
            docs = res.json().get("reviews", [])
            
            if sentiment_filter == "Positive":
                docs = [d for d in docs if d.get("sentiment") == "pos"]
            elif sentiment_filter == "Negative":
                docs = [d for d in docs if d.get("sentiment") == "neg"]
            elif sentiment_filter == "Neutral":
                docs = [d for d in docs if d.get("sentiment") == "neutral"]

            if search_query.strip():
                q = search_query.lower()
                docs = [
                    d for d in docs
                    if q in (d.get("summary") or "").lower()
                    or q in (d.get("name") or "").lower()
                    or q in (d.get("raw_text") or "").lower()
                ]

            st.caption(f"{len(docs)} record(s)")

            if not docs:
                st.info("No records found.")
            else:
                for doc in docs:
                    s = doc.get("sentiment")
                    badge = (
                        '<span class="badge-pos">POS</span>' if s == "pos"
                        else '<span class="badge-neg">NEG</span>' if s == "neg"
                        else '<span class="badge-neutral">NEU</span>'
                    )
                    reviewer = doc.get("name") or "Anonymous"
                    summary = doc.get("summary") or ""
                    
                    with st.expander(f"{reviewer} — {summary[:75]}..."):
                        st.markdown(f"**Sentiment**: {badge}", unsafe_allow_html=True)
                        st.markdown(f"**Summary**: {summary}")
                        
                        themes = doc.get("key_themes") or []
                        if themes:
                            tags = " ".join([f'<span class="meta-tag">{t}</span>' for t in themes])
                            st.markdown(f"**Themes**: {tags}", unsafe_allow_html=True)
                            
                        cp, cc = st.columns(2)
                        with cp:
                            st.markdown("**Pros**")
                            for p in doc.get("pros") or []:
                                st.write(f"• {p}")
                        with cc:
                            st.markdown("**Cons**")
                            for c in doc.get("cons") or []:
                                st.write(f"• {c}")

                        st.caption(f"ID: {doc.get('_id')}")
    except Exception as e:
        st.error(f"Error loading database: {e}")