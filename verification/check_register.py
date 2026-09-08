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

import datetime
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
for k in ("occurred", "recorded", "basis"):
    missing = [e["id"] for e in entries if not e.get(k)]
    check("すべてに %s がある" % k, not missing, ", ".join(missing))

bad_basis = [e["id"] for e in entries if e.get("basis") not in ("同時", "再構成")]
check("basis が「同時」か「再構成」である", not bad_basis, ", ".join(bad_basis))

# ------------------------------------------------ 日付。ここは詐称できない
section("1.5 日付が筋を通っているか")

# recorded は「この登録簿に書いた日」である。自己申告にしておくと、
# あとから遡って書いたものを同時記録に見せかけられる。だから git から取る。
# その id が register.toml に最初に現れたコミットの日付と一致しなければ落とす。
revs = subprocess.check_output(
    ["git", "log", "--reverse", "--format=%H %cs", "--", "register.toml"],
    cwd=ROOT, text=True).strip().split("\n")
first_seen = {}
for line in revs:
    h, day = line.split()
    blob = subprocess.check_output(["git", "show", "%s:register.toml" % h],
                                   cwd=ROOT, text=True)
    for i in re.findall(r'^id = "([A-Z]{2}-\d{3})"', blob, re.M):
        first_seen.setdefault(i, day)

wrong = []
for e in entries:
    seen = first_seen.get(e["id"])
    if seen is None:
        continue          # まだコミットしていない項目。次の commit で見る
    if e.get("recorded") != seen:
        wrong.append("%s: 名乗り %s / git %s" % (e["id"], e.get("recorded"), seen))
check("recorded が git の履歴と合っている", not wrong, "; ".join(wrong))


def as_day(v):
    """2026-08 のような月までの値は、その月の 1 日として扱う。"""
    parts = str(v).split("-")
    while len(parts) < 3:
        parts.append("01")
    return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))


backwards = [e["id"] for e in entries
             if as_day(e["recorded"]) < as_day(e["occurred"])]
check("起きるより前に書いたことになっていない", not backwards, ", ".join(backwards))

# 「同時」を名乗れるのは、書いたのが出来事の翌日までのときだけ。
# 逆向き（再構成を名乗ること）は制限しない。控えめに書く分には止めない。
overclaim = [e["id"] for e in entries if e["basis"] == "同時"
             and (as_day(e["recorded"]) - as_day(e["occurred"])).days > 1]
check("「同時」と名乗れるのは 1 日以内のものだけ", not overclaim, ", ".join(overclaim))

n_recon = sum(1 for e in entries if e["basis"] == "再構成")
check("再構成の件数を数えている", True,
      "%d 件が再構成、%d 件が同時" % (n_recon, len(entries) - n_recon))


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

section("6. 使わないと決めた語")

# 紙面には印字されているが、いま自分が書く文章では使わない。忘れると自然に
# 戻ってくるので、機械で止める。この登録簿に逐語転記は無いので、例外は無い。
FORBIDDEN = ["独立研究者", "Independent Researcher"]
SELF = os.path.join("verification", "check_register.py")
found = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
    for name in filenames:
        if not name.endswith((".md", ".toml", ".py", ".cff", ".yml", ".json")):
            continue
        rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
        if rel == SELF:
            continue
        body = io.open(os.path.join(dirpath, name), encoding="utf-8",
                       errors="replace").read()
        for term in FORBIDDEN:
            if term in body:
                found.append("%s に「%s」" % (rel, term))
check("使わないと決めた語が入っていない", not found, ", ".join(found))

# README は手で書いている。register.toml が増えたとき、ここが真っ先にずれる。
# この登録簿の趣旨からして、名乗る数だけは機械で押さえておく。
readme = io.open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()

m = re.search(r"いま \*\*(\d+) 件\*\*", readme)
check("README が名乗る総件数が実際と合う",
      m is not None and int(m.group(1)) == len(entries),
      ("名乗り %s / 実際 %d" % (m.group(1), len(entries))) if m
      else "名乗っている箇所が見つからない")

LABEL = {"standing": "いま立っている", "open": "未解決",
         "unresolvable": "直せない", "corrected": "直した", "withdrawn": "撤回した"}
wrong = []
for st, label in sorted(LABEL.items()):
    want = len([e for e in entries if e["status"] == st])
    m = re.search(r"\|\s*\*{0,2}" + label + r"\*{0,2}\s*\|\s*(\d+)\s*\|", readme)
    if m is None or int(m.group(1)) != want:
        wrong.append("%s: 名乗り %s / 実際 %d"
                     % (label, m.group(1) if m else "無し", want))
check("README の状態ごとの内訳が実際と合う", not wrong, "; ".join(wrong))


print("\n" + "-" * 58)
if failures:
    print("%d 件が通り、%d 件が通りませんでした。" % (passed, len(failures)))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("%d 件すべて通りました。" % passed)
