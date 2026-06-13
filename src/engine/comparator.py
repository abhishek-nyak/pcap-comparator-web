import pandas as pd

def compare_headers(h1, h2):
    all_keys = set(h1.keys()).union(set(h2.keys()))
    comparison = []
    for key in all_keys:
        v1 = h1.get(key, None)
        v2 = h2.get(key, None)
        if v1 == v2:
            status = "✅ Match"
        elif v1 is None:
            status = "❌ Missing in PCAP 1"
        elif v2 is None:
            status = "❌ Missing in PCAP 2"
        else:
            status = "⚠️ Value Mismatch"
        comparison.append({"Header Name": key, "PCAP 1 Value": v1 if v1 is not None else "[Missing]", "PCAP 2 Value": v2 if v2 is not None else "[Missing]", "Status": status})
    return pd.DataFrame(comparison)
