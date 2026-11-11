#!/usr/bin/env python3
"""register.csv を読んで数える例。標準ライブラリだけで動く。

    python3 data/example.py
"""

import collections
import csv
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "register.csv")
with open(path, encoding="utf-8", newline="") as fh:
    rows = list(csv.DictReader(fh))

print("全件", len(rows))
for status, n in collections.Counter(r["status"] for r in rows).most_common():
    print(status, n)
print("証言しか根拠が無い", sum(r["verifiable"] == "証言" for r in rows))
print("検査が誤って通した", sum(r["passed_check"] != "" for r in rows))
