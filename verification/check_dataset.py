#!/usr/bin/env python3
"""登録簿を、データセットとして検査する。

    python3 verification/check_dataset.py

check_register.py は登録簿の形と履歴を見る。ここは、登録簿を外へ配る形のほうを見る。

  1. 種類と状態の札が、README・CITATION.cff・.zenodo.json で食い違っていない
  2. data/register.csv が register.toml から作り直したものと一致する
  3. views/ の頁が作り直したものと一致し、README と目次から辿れる
  4. データ辞書（data/README.md）の列が、CSV の列と同じ順で並ぶ
  5. datapackage.json の列・型・制約が、実際の値に合う
  6. 引用の文字列が、名乗る箇所の数だけ一字一句同じ
  7. 使い方の例が、データ辞書の写しと同じで、走らせた結果が件数と合う
  8. 使ったことを知らせる issue の様式があり、連絡先を求めていない
  9. README が名乗る検査の数が、実際に走らせた数と合う

check_register.py の項目の数はサイトにも写してあるので、そちらには足さない。
ここに足したものは、ここで数える。

標準ライブラリのみ。
"""

import csv
import datetime
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import build  # noqa: E402

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


def read(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return None
    return io.open(path, encoding="utf-8", newline="").read()


reg = build.load()
entries = reg["entry"]
readme = read("README.md") or ""
cff = read("CITATION.cff") or ""
zen = json.loads(read(".zenodo.json") or "{}")

# ------------------------------------------------------------ 札
section("1. 種類と状態の札")

LABEL_LINE = "種類：データセット　状態：運営中"
lines = readme.splitlines()
first = next((l for l in lines[1:] if l.strip()), "")
check("README の題のすぐ下に、種類と状態の札がある",
      lines[:1] == ["# self-correction"] and first == LABEL_LINE, first)
check("CITATION.cff の type が dataset で、札の「データセット」と合う",
      re.search(r"^type: dataset$", cff, re.M) is not None)
check(".zenodo.json の upload_type が dataset で、札と合う",
      zen.get("upload_type") == "dataset", str(zen.get("upload_type")))

# ------------------------------------------------------------ CSV
section("2. CSV")

csv_text = read(os.path.join("data", "register.csv"))
check("data/register.csv が register.toml から作り直したものと一致する",
      csv_text == build.render_csv(reg),
      "" if csv_text == build.render_csv(reg) else "python3 build.py を走らせる")
rows = list(csv.DictReader(io.StringIO(csv_text or "")))
header = next(csv.reader(io.StringIO(csv_text or "")), [])
check("CSV の列が build.CSV_COLUMNS と同じ順で並ぶ", header == build.CSV_COLUMNS,
      "%d 列" % len(header))
check("CSV の行数が登録簿の件数と合う", len(rows) == len(entries),
      "%d 行 / %d 件" % (len(rows), len(entries)))
known = {k for e in entries for k in e}
check("登録簿のどの欄も、CSV の列に入っている", known <= set(header),
      ", ".join(sorted(known - set(header))))

# ------------------------------------------------------------ 絞り込み
section("3. 絞り込んだ頁")

want = {rel: text for rel, text in build.outputs(reg).items()
        if rel.startswith("views" + os.sep)}
vdir = os.path.join(ROOT, "views")
have = {os.path.join("views", n) for n in os.listdir(vdir)} if os.path.isdir(vdir) else set()
check("views/ にあるファイルが、作るべきものと過不足なく同じ", have == set(want),
      "余り %s / 足りない %s" % (sorted(have - set(want)), sorted(set(want) - have)))
stale = [rel for rel, text in sorted(want.items()) if read(rel) != text]
check("views/ の頁が、register.toml から作り直したものと一致する", not stale,
      ", ".join(stale) or "%d 頁" % len(want))
index = want.get(os.path.join("views", "README.md"), "")
pages = [os.path.basename(r) for r in want if not r.endswith("README.md")]
unlinked = [p for p in pages if "](%s)" % p not in index]
check("目次が、絞り込んだ頁のすべてにつながる", not unlinked, ", ".join(unlinked))
n_by_status = sum(1 for st in build.ORDER if any(e["status"] == st for e in entries))
in_view = sum(len(re.findall(r"^### [A-Z]{2}-\d{3} ", want[r], re.M))
              for r in want if os.path.basename(r).startswith("status-"))
check("状態ごとの頁を合わせると、全件がちょうど一度ずつ現れる", in_view == len(entries),
      "%d / %d 件" % (in_view, len(entries)))
in_kind = sum(len(re.findall(r"^### [A-Z]{2}-\d{3} ", want[r], re.M))
              for r in want if os.path.basename(r).startswith("kind-"))
check("種類ごとの頁を合わせると、全件がちょうど一度ずつ現れる", in_kind == len(entries),
      "%d / %d 件" % (in_kind, len(entries)))

KANJI = "〇一二三四五六七八九十"
status_links = re.findall(r"\]\(views/(status-[a-z]+\.md)\)", readme)
check("README が状態ごとの頁を、すべてつないでいる",
      sorted(status_links) == sorted(p for p in pages if p.startswith("status-")),
      ", ".join(status_links))
m = re.search(r"状態ごとの頁は\s*\n?.*?\n?の(.)つです", readme, re.S)
check("README が名乗る状態ごとの頁の数が、実際の数と合う",
      m is not None and m.group(1) == KANJI[n_by_status],
      ("名乗り %s / 実際 %s" % (m.group(1), KANJI[n_by_status])) if m else "名乗りが無い")
check("README が絞り込んだ頁の目次につないでいる", "](views/README.md)" in readme)

# ------------------------------------------------------------ データ辞書
section("4. データ辞書")

dic = read(os.path.join("data", "README.md")) or ""
m = re.search(r"^## 列の定義\n(.*?)(?=^## )", dic, re.S | re.M)
dic_cols = re.findall(r"^\| `([a-z_]+)` \|", m.group(1), re.M) if m else []
check("データ辞書の列が、CSV の列と同じ順で並ぶ", dic_cols == header,
      "辞書 %d 列 / CSV %d 列" % (len(dic_cols), len(header)))
m = re.search(r"^## `status` について\n(.*?)(?=^## )", dic, re.S | re.M)
dic_status = re.findall(r"^\| `([a-z]+)` \|", m.group(1), re.M) if m else []
check("データ辞書の状態が、build.py の五つと同じ", sorted(dic_status) == sorted(build.LABEL),
      ", ".join(dic_status))
check("README がデータ辞書につないでいる", "](data/README.md)" in readme)

# ------------------------------------------------------------ datapackage.json
section("5. datapackage.json")

try:
    pkg = json.loads(read(os.path.join("data", "datapackage.json")) or "")
except ValueError as exc:
    pkg = {}
    print("  （datapackage.json が読めませんでした: %s）" % exc)
res = (pkg.get("resources") or [{}])[0]
fields = res.get("schema", {}).get("fields", [])
names = [f.get("name") for f in fields]
check("datapackage.json の資源が data/register.csv を指す",
      res.get("path") == "register.csv" and csv_text is not None, str(res.get("path")))
check("datapackage.json の列が、CSV の列と同じ順で並ぶ", names == header,
      "%d 列 / %d 列" % (len(names), len(header)))
check("datapackage.json の題が CITATION.cff と .zenodo.json の題と同じ",
      pkg.get("title") and ('title: "%s"' % pkg.get("title")) in cff
      and zen.get("title") == pkg.get("title"))
check("datapackage.json のライセンスが CITATION.cff と同じ（MIT）",
      [l.get("name") for l in pkg.get("licenses", [])] == ["MIT"]
      and re.search(r"^license: MIT$", cff, re.M) is not None)
check("datapackage.json の主キーが id", res.get("schema", {}).get("primaryKey") == "id")

bad = []
for f in fields:
    n, c = f.get("name"), f.get("constraints", {})
    vals = [r.get(n, "") for r in rows]
    filled = [v for v in vals if v != ""]
    if c.get("required") and len(filled) != len(vals):
        bad.append("%s: 空欄 %d" % (n, len(vals) - len(filled)))
    if c.get("unique") and len(set(filled)) != len(filled):
        bad.append("%s: 重複" % n)
    if "pattern" in c:
        miss = [v for v in filled if not re.fullmatch(c["pattern"], v)]
        if miss:
            bad.append("%s: 形が合わない %s" % (n, miss[:3]))
    if "enum" in c and not set(filled) <= set(c["enum"]):
        bad.append("%s: 表に無い値 %s" % (n, sorted(set(filled) - set(c["enum"]))))
    if f.get("type") == "date":
        for v in filled:
            try:
                datetime.date.fromisoformat(v)
            except ValueError:
                bad.append("%s: 日付でない %s" % (n, v))
check("datapackage.json の制約を、CSV の全行が満たす", not bad, "; ".join(bad))

enums = {f["name"]: f.get("constraints", {}).get("enum") for f in fields}
check("status の値の表が、build.py の五つと同じ",
      sorted(enums.get("status") or []) == sorted(build.LABEL))
check("basis と verifiable の値の表が、check_register.py の決めと同じ",
      enums.get("basis") == ["同時", "再構成"] and enums.get("verifiable") == ["紙面", "証言"])

# ------------------------------------------------------------ 引用の文字列
section("6. 引用の文字列")

CITATION = pkg.get("citation", "")
check("引用の文字列が、題と、すべての版の DOI を含む",
      bool(CITATION) and ("「%s」" % pkg.get("title")) in CITATION
      and CITATION.endswith("https://doi.org/10.5281/zenodo.24033596"), CITATION)
PLACES = (("README.md", readme), ("data/README.md", dic))
for label, text in PLACES:
    block = re.search(r"^```\n(根本卓哉「self-correction.*?)\n```$", text, re.M)
    check("%s の引用の文字列が datapackage.json と一字一句同じ" % label,
          block is not None and block.group(1) == CITATION,
          block.group(1) if block else "囲みが見つからない")
places = 1 + len(PLACES)
said = []
for label, text in PLACES:
    prose = "\n".join(l for l in text.splitlines() if not l.startswith("#"))
    said += ["%s: %s箇所" % (label, k) for k in re.findall(r"([一二三四五六七八九])箇所", prose)]
check("散文が名乗る引用の文字列の箇所の数が、確かめている数（%s箇所）と合う" % KANJI[places],
      bool(said) and all(s.endswith(KANJI[places] + "箇所") for s in said),
      " / ".join(said) or "名乗りが無い")

# ------------------------------------------------------------ 使い方の例
section("7. 使い方の例")

example = read(os.path.join("data", "example.py")) or ""
m = re.search(r"^## 使い方の例\n.*?^```python\n(.*?)^```$", dic, re.S | re.M)
check("データ辞書の例が data/example.py と一字一句同じ", m is not None and m.group(1) == example)
try:
    out = subprocess.run([sys.executable, os.path.join(ROOT, "data", "example.py")],
                         capture_output=True, text=True, timeout=60)
    ran = out.returncode == 0
    got = out.stdout.splitlines()
except Exception as exc:                                    # noqa: BLE001
    ran, got = False, [str(exc)]
check("data/example.py が走る", ran, (out.stderr.strip()[-200:] if not ran else ""))
want_lines = {"全件 %d" % len(entries),
              "証言しか根拠が無い %d" % sum(e["verifiable"] == "証言" for e in entries)}
for st in build.LABEL:
    n = sum(e["status"] == st for e in entries)
    if n:
        want_lines.add("%s %d" % (st, n))
check("data/example.py の出力が、register.toml の件数と合う", set(got) == want_lines,
      " / ".join(got))

# ------------------------------------------------------------ 使ったことの知らせ
section("8. 使ったことを知らせる窓口")

tmpl = read(os.path.join(".github", "ISSUE_TEMPLATE", "used-this-data.yml"))
check("「このデータを使った」の issue の様式がある",
      tmpl is not None and "name: このデータを使った" in tmpl)
check("その様式が連絡先を求めていない",
      tmpl is not None and not re.search(r"(?i)e-?mail|メール|電話|住所", tmpl))
check("README がその様式につないでいる", "template=used-this-data.yml" in readme)

# ------------------------------------------------------------ 検査の結果
section("9. README が名乗る検査の数")

try:
    out = subprocess.run([sys.executable, os.path.join(HERE, "check_register.py")],
                         capture_output=True, text=True, timeout=600, cwd=ROOT)
    m = re.search(r"(\d+) 件すべて通りました。", out.stdout)
    n_register = int(m.group(1)) if m else None
except Exception:                                           # noqa: BLE001
    n_register = None
m = re.search(r"^\| `verification/check_register\.py` \| (\d+) \| すべて通る \|$", readme, re.M)
check("README の表の check_register.py の数が、走らせた数と合う",
      m is not None and n_register is not None and int(m.group(1)) == n_register,
      "名乗り %s / 実際 %s" % (m.group(1) if m else "無い", n_register))

# 最後の一つ。この検査自身の数は、この項目を含めて数える。
total = passed + len(failures) + 1
m = re.search(r"^\| `verification/check_dataset\.py` \| (\d+) \| すべて通る \|$", readme, re.M)
check("README の表の check_dataset.py の数が、実際の数と合う",
      m is not None and int(m.group(1)) == total,
      "名乗り %s / 実際 %d" % (m.group(1) if m else "無い", total))

print("\n" + "-" * 58)
if failures:
    print("%d 件が通り、%d 件が通りませんでした。" % (passed, len(failures)))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("%d 件すべて通りました。" % passed)
