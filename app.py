import streamlit as st
from src.engine.parser import extract_http_streams
from src.engine.comparator import compare_headers
from src.utils.file_manager import manage_temp_file

st.set_page_config(page_title="HTTP PCAP Header Comparator", layout="wide")

st.title("🌐 HTTP PCAP Stream & Header Comparator")
st.markdown("Upload two PCAP files to perform an order-agnostic HTTP header comparison.")

col1, col2 = st.columns(2)
with col1:
    pcap1_file = st.file_uploader("Upload PCAP 1", type=['pcap', 'pcapng'], key="pcap1")
with col2:
    pcap2_file = st.file_uploader("Upload PCAP 2", type=['pcap', 'pcapng'], key="pcap2")

if pcap1_file and pcap2_file:
    if st.button("🚀 Run Comparison", use_container_width=True):
        with st.spinner("Processing files and matching HTTP streams..."):
            
            # Using our custom context manager to safely handle files!
            with manage_temp_file(pcap1_file) as tmp1_path, manage_temp_file(pcap2_file) as tmp2_path:
                streams1 = extract_http_streams(tmp1_path)
                streams2 = extract_http_streams(tmp2_path)

            st.success("Analysis complete!")
            
            tab1, tab2 = st.tabs(["🔍 Detailed Side-by-Side Diff", "⚙️ Raw JSON Data"])
            with tab1:
                max_len = max(len(streams1), len(streams2))
                for i in range(max_len):
                    s1 = streams1[i] if i < len(streams1) else None
                    s2 = streams2[i] if i < len(streams2) else None
                    ep1 = s1['endpoint'] if s1 else "Missing"
                    ep2 = s2['endpoint'] if s2 else "Missing"
                    status_indicator = "🟢 Aligned Pairs" if (s1 and s2 and s1['endpoint'] == s2['endpoint']) else "🔴 Flow Mismatch"
                    
                    with st.expander(f"Stream Pair #{i+1} — {status_indicator}"):
                        cols = st.columns(2)
                        cols[0].markdown(f"**PCAP 1 Endpoint:** `{ep1}`")
                        cols[1].markdown(f"**PCAP 2 Endpoint:** `{ep2}`")
                        if s1 and s2:
                            diff_df = compare_headers(s1['headers'], s2['headers'])
                            def style_status(row):
                                if "✅" in row["Status"]: return ['background-color: #d4edda; color: #155724'] * len(row)
                                elif "⚠️" in row["Status"]: return ['background-color: #fff3cd; color: #856404'] * len(row)
                                else: return ['background-color: #f8d7da; color: #721c24'] * len(row)
                            st.dataframe(diff_df.style.apply(style_status, axis=1), use_container_width=True, hide_index=True)
            with tab2:
                c1, c2 = st.columns(2)
                with c1: st.json(streams1)
                with c2: st.json(streams2)
else:
    st.info("💡 Please upload both PCAP files to begin.")
