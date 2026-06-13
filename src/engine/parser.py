import pyshark
import streamlit as st

def extract_http_streams(pcap_path):
    streams = []
    try:
        cap = pyshark.FileCapture(pcap_path, display_filter='http')
        for idx, pkt in enumerate(cap):
            if 'HTTP' in pkt:
                http_layer = pkt.http
                is_request = hasattr(http_layer, 'request_method')
                method = getattr(http_layer, 'request_method', 'RESPONSE')
                uri = getattr(http_layer, 'request_uri', '')
                status_code = getattr(http_layer, 'response_code', '')
                host = getattr(http_layer, 'host', 'Unknown-Host')
                
                endpoint = f"{method} {host}{uri}" if is_request else f"HTTP RESPONSE ({status_code})"
                
                headers = {}
                for field in http_layer.field_names:
                    if field.startswith('request_') or field.startswith('response_') or field in ['chat', 'content_length']:
                        continue
                    val = getattr(http_layer, field, None)
                    if val:
                        headers[field.lower()] = str(val)
                
                streams.append({"id": idx + 1, "endpoint": endpoint, "type": "Request" if is_request else "Response", "headers": headers})
        cap.close()
    except Exception as e:
        st.error(f"Error parsing PCAP file: {e}")
    return streams
