# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
import os

import requests

url = os.getenv("OBLIVION_URL", "http://127.0.0.1:8080")
r = requests.get(url + "/health", timeout=10)
r.raise_for_status()
print(r.json())
