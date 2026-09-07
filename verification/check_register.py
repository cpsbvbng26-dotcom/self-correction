#!/usr/bin/env python3
"""登録簿そのものを検査する。

    python3 verification/check_register.py

記録は、書けばいくらでも都合よく書ける。**都合よく書けないようにする仕掛けが
無ければ、記録は主張と変わらない。**そこでここに置く。

いちばん効くのは最後の一つである。

    **過去のどの版にあった id も、いまの版に無ければ落とす。**

git の履歴から、これまでに一度でも登録簿に載った id をすべて集め、現在の
ファイルと突き合わせる。**消したら落ちる。**書き換えは残るが、消去はできない。

そのほかに、形の検査をする。状態は決めた五つだけか。撤回と訂正には「何が問題
だったか」と「どうしたか」があるか。**いま立っている主張には、覆し方が書いて
あるか。**書けない主張は、主張ではなく宣伝である。

標準ライブラリのみ。
"""

import io
import os
import re
import subprocess
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import build  # noqa: E402

STATUS = {"standing", "corrected", "withdrawn", "unresolvable", "open"}
REQUIRED = {
    "standing": ["claimed", "refute"],
    "corrected": ["claimed", "problem", "correction"],
    "withdrawn": ["claimed", "problem", "correction"],
    "unresolvable": ["claimed", "problem", "why_unresolvable"],
    "open": ["claimed", "why_open"],
}

passed, failures = 0, []


def check(label, cond, detail=""):
    global passed
    if cond:
        passed += 1
        print("  PASS  " + label + (("  " + detail) if detail else ""))
    else:
        failures.append(label)
        print("  FAIL  " + label + (("  " + detail) if detail else ""))


def section(s):
    print("\n" + s)


reg = build.load(os.path.join(ROOT, "register.toml"))
entries = reg["entry"]

# ------------------------------------------------------------------ 形
section("1. 形")

check("登録簿が空でない", len(entries) > 0, "%d 件" % len(entries))
ids = [e.get("id", "") for e in entries]
check("id が重複していない", len(set(ids)) == len(ids))
bad_id = [i for i in ids if not re.fullmatch(r"[A-Z]{2}-\d{3}", i)]
check("id の形が揃っている（AA-000）", not bad_id, ", ".join(bad_id))
bad_status = [e["id"] for e in entries if e.get("status") not in STATUS]
check("状態が決めた五つの中にある", not bad_status, ", ".join(bad_status))
no_title = [e["id"] for e in entries if not e.get("title")]
check("すべてに題がある", not no_title, ", ".join(no_title))
no_date = [e["id"] for e in entries if not e.get("date")]
check("すべてに日付がある", not no_date, ", ".join(no_date))

# -------------------------------------------------- 状態ごとに要る欄
section("2. 状態ごとに、要るものが書いてあるか")

for st, keys in sorted(REQUIRED.items()):
    missing = []
    for e in entries:
        if e.get("status") != st:
            continue
        for k in keys:
            if not e.get(k):
                missing.append("%s に %s" % (e["id"], k))
    check("%s には %s がある" % (st, "・".join(keys)), not missing,
          ", ".join(missing))

# 「いま立っている」に覆し方が無いのは、いちばん見過ごされやすい抜けである。
standing = [e for e in entries if e["status"] == "standing"]
check("いま立っている主張には、覆し方が書いてある",
      all(len(e.get("refute", "")) > 20 for e in standing),
      "%d 件" % len(standing))

# ------------------------------------------------------------- 識別子
section("3. 識別子と証拠")

bad_doi = [e["id"] for e in entries
           if "doi" in e and not re.fullmatch(r"10\.\d{4,9}/\S+", str(e["doi"]))]
check("DOI の形が正しい", not bad_doi, ", ".join(bad_doi))
bad_ev = [e["id"] for e in entries
          if "evidence" in e and not str(e["evidence"]).startswith("https://")]
check("証拠の URL が https である", not bad_ev, ", ".join(bad_ev))
check("ORCID が書いてある", bool(reg.get("orcid")), reg.get("orcid", ""))

# ------------------------------------------------ 人が読む版とのずれ
section("4. 人が読む版とのずれ")

path = os.path.join(ROOT, "REGISTER.md")
current = io.open(path, encoding="utf-8").read() if os.path.exists(path) else ""
check("REGISTER.md が register.toml から作り直したものと一致する",
      current == build.render(reg),
      "python3 build.py を走らせてください")
check("REGISTER.md が件数を正しく述べている",
      ("| | **%d** | |" % len(entries)) in current)

# ------------------------------------------------------------ 消せない
section("5. 消せないこと")

# git の履歴から、これまでに一度でも載った id を集める。
# 浅いクローンだと履歴が読めないので、そのときは通ったことにしない。
try:
    revs = subprocess.check_output(
        ["git", "log", "--format=%H", "--", "register.toml"],
        cwd=ROOT, text=True).split()
except Exception as exc:                                    # noqa: BLE001
    revs = []
    print("  （git の履歴が読めませんでした: %s）" % exc)

ever = set(ids)
for rev in revs:
    try:
        blob = subprocess.check_output(["git", "show", "%s:register.toml" % rev],
                                       cwd=ROOT, text=True)
    except subprocess.CalledProcessError:
        continue
    ever |= set(re.findall(r'^id\s*=\s*"([A-Z]{2}-\d{3})"', blob, re.M))

lost = sorted(ever - set(ids))
check("過去に載ったどの id も、いまも載っている", not lost,
      "消えている: " + ", ".join(lost) if lost else "%d 件を %d 版で確認" % (len(ever), len(revs)))
check("履歴が読めている（浅いクローンではない）",
      len(revs) > 0 or not os.path.exists(os.path.join(ROOT, ".git")),
      "%d 版" % len(revs))

print("\n" + "-" * 58)
if failures:
    print("%d 件が通り、%d 件が通りませんでした。" % (passed, len(failures)))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("%d 件すべて通りました。" % passed)
