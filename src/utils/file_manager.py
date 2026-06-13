import tempfile
import os
from contextlib import contextmanager

@contextmanager
def manage_temp_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pcap") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    try:
        # Give the path back to the app to use
        yield tmp_path
    finally:
        # This ALWAYS runs afterwards to clean up the hard drive
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
