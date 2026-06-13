# 🌐 PCAP Comparator Web App: Project Documentation

## 1. Technology Stack
* **Frontend UI:** `Streamlit`
* **Network Parsing Engine:** `PyShark` (TShark wrapper)
* **Data Manipulation:** `Pandas`
* **Concurrency:** `asyncio`

## 2. Project Architecture
* `app.py`: Main Streamlit UI and application entry point
* `src/engine/parser.py`: Extracts and normalizes HTTP streams
* `src/engine/comparator.py`: Performs order-agnostic dictionary comparisons
* `src/utils/file_manager.py`: Handles temporary file creation and auto-deletion

## 3. How to Start the App (Local Setup)
1. Clone the repo.
2. Activate virtual environment: `source venv/Scripts/activate`
3. Run the Streamlit server: `streamlit run app.py`

## 4. Current Feature Set
* Order-Agnostic Comparison (Keys normalized to lowercase)
* Visual Diffing (Color-coded mismatch highlighting)
* Safe memory management (Auto-cleanup of temp PCAPs)

## 5. Scope for Improvement (Future Roadmap)
* **Phase 1 (AI):** Integrate LLMs to explain *why* a mismatch occurred.
* **Phase 2 (Workflow):** Build a browser extension to send PCAPs directly from firewall dashboards.
* **Phase 3 (Deep Inspection):** Add TCP reassembly and TLS decryption using uploaded `keylog.txt` files.
* **Phase 4 (Reporting):** Add PDF/CSV export functionality for security audits.
