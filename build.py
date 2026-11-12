#!/usr/bin/env python3
"""register.toml から、人が読む版と表計算の版を組み立てる。

    python3 build.py

作るもの（どれも生成物。手で編集しない）
  REGISTER.md             全件を状態ごとに
  data/register.csv       全件を一行ずつ。表計算ですぐ開ける
  views/README.md         絞り込んだ頁の目次
  views/status-*.md       状態ごとの頁
  views/kind-*.md         種類（id の頭の二文字）ごとの頁

**人が読む版を手で書かない。**手で書くと、登録簿のほうと必ずずれる。
ずれたときに気づく手立てが無ければ、記録としての意味が無くなる。
"""

import csv
import io
import os
import re
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))

LABEL = {
    "standing": ("いま立っている", "この主張は取り下げていません。反証の手順を添えてあります"),
    "corrected": ("直した", "誤りが見つかり、直したもの。元の記述は消していません"),
    "withdrawn": ("撤回した", "取り下げたもの。元の記述は消していません"),
    "unresolvable": ("直せない", "凍結された成果物の側に誤りがあります。もう直せません"),
    "open": ("未解決", "まだ判断がついていません"),
}
ORDER = ["standing", "open", "unresolvable", "corrected", "withdrawn"]

FIELDS = [
    ("where", "どこ"),
    ("doi", "DOI"),
    ("claimed", "述べていたこと"),
    ("support", "支え"),
    ("counter", "何が弱めているか"),
    ("problem", "何が問題か"),
    ("correction", "どうしたか"),
    ("why_unresolvable", "なぜ直せないか"),
    ("why_open", "なぜ未解決か"),
    ("refute", "どうすれば覆るか"),
    ("found_by", "見つけたのは"),
    ("passed_check", "誤って通した検査"),
    ("evidence", "証拠"),
    ("occurred", "起きた"),
    ("recorded", "書いた"),
    ("basis", "記録の性質"),
    ("verifiable", "誰が確かめられるか"),
]


# CSV の列。順は固定する。データ辞書（data/README.md）と datapackage.json が
# この順を名乗り、verification/check_dataset.py が突き合わせる。
CSV_COLUMNS = ["id", "status", "title"] + [k for k, _ in FIELDS]

GENERATED = "このファイルは `register.toml` からの生成物です。手で編集しません。"


def load(path=None):
    with open(path or os.path.join(HERE, "register.toml"), "rb") as fh:
        return tomllib.load(fh)


def render_entry(e):
    out = ["### %s —— %s" % (e["id"], e["title"]), ""]
    for key, label in FIELDS:
        if key in e:
            v = e[key]
            if key == "doi":
                v = "[%s](https://doi.org/%s)" % (v, v)
            elif key == "evidence" and str(v).startswith("http"):
                v = "<%s>" % v
            out.append("- **%s** —— %s" % (label, v))
    out.append("")
    return out


def render(reg):
    out = ["# 訂正の登録簿",
           "",
           GENERATED,
           "（`python3 build.py` で作り直す）",
           "",
           "公開したあとで誤りが見つかったもの、撤回したもの、果たされなかった約束を、",
           "一件ずつ、消さずに記録する登録簿です。",
           "",
           "`id` は永久に消しません。過去のどの版にあった `id` も、いまの版に無ければ",
           "`verification/check_register.py` が落とします。都合の悪い記録は、消せない",
           "作りにしてあります。",
           ""]
    entries = reg["entry"]
    counts = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    out += ["| 状態 | 件数 | 意味 |", "| --- | --- | --- |"]
    for st in ORDER:
        if st in counts:
            name, meaning = LABEL[st]
            out.append("| **%s** | %d | %s |" % (name, counts[st], meaning))
    out += ["| | **%d** | |" % len(entries), ""]

    for st in ORDER:
        group = [e for e in entries if e["status"] == st]
        if not group:
            continue
        name, meaning = LABEL[st]
        out += ["---", "", "## %s（%d 件）" % (name, len(group)), "", meaning + "。", ""]
        for e in group:
            out += render_entry(e)
    out += ["---", "",
            "所有者: %s（ORCID: [%s](https://orcid.org/%s)）"
            % (reg["owner"], reg["orcid"], reg["orcid"]), ""]
    return "\n".join(out)


def render_csv(reg):
    """全件を一行ずつ。欄の無い項目は空にする。UTF-8、BOM なし、改行は LF。"""
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(CSV_COLUMNS)
    for e in reg["entry"]:
        w.writerow([str(e.get(k, "")) for k in CSV_COLUMNS])
    return buf.getvalue()


# ---------------------------------------------------------------- 絞り込み
#
# 種類は id の頭の二文字で分ける。意味は手で書かない。register.toml の節の見出しの
# うち、その二文字の項目が置かれている節を、件数とともに写す。手で書けば、項目が
# 増えた日にずれる。一つの頭の二文字が、いくつもの節にまたがることがある。

def kinds(path=None):
    """{頭の二文字: [(節の見出し, 件数), ...]} を、register.toml に現れる順で返す。"""
    text = io.open(path or os.path.join(HERE, "register.toml"), encoding="utf-8").read()
    section, found = "", {}
    for line in text.splitlines():
        m = re.match(r"^# =+ (.+)$", line)
        if m:
            section = m.group(1).strip()
            continue
        m = re.match(r'^id = "([A-Z]{2})-\d{3}"', line)
        if m:
            secs = found.setdefault(m.group(1), {})
            secs[section] = secs.get(section, 0) + 1
    return {k: list(v.items()) for k, v in found.items()}


def sections_text(secs):
    return "、".join("%s %d" % (name, n) for name, n in secs)


def view_name(axis, key):
    return "%s-%s.md" % (axis, key)


def render_views(reg, kind_sections):
    """{ファイル名: 中身}。views/ の下に置く。"""
    entries = reg["entry"]
    files = {}
    by_status = [(st, [e for e in entries if e["status"] == st]) for st in ORDER]
    by_status = [(st, g) for st, g in by_status if g]
    by_kind = [(k, [e for e in entries if e["id"][:2] == k]) for k in kind_sections]

    index = ["# 登録簿を絞り込んだ頁", "", GENERATED,
             "（`python3 build.py` で作り直す）", "",
             "[REGISTER.md](../REGISTER.md) の全件を、状態ごとと種類ごとに分けた頁です。",
             "どの頁も静的な Markdown で、絞り込みにスクリプトを使いません。", "",
             "## 状態ごと", "",
             "| 状態 | 件数 | 頁 |", "| --- | --- | --- |"]
    for st, group in by_status:
        name, _ = LABEL[st]
        index.append("| %s | %d | [%s](%s) |" % (name, len(group), st, view_name("status", st)))
    index += ["", "## 種類ごと", "",
              "種類は `id` の頭の二文字です。",
              "その二文字の項目が `register.toml` のどの節に置かれているかを、節ごとの件数とともに写しています。",
              "", "| 種類 | 置かれている節 | 件数 | 頁 |", "| --- | --- | --- | --- |"]
    for k, group in by_kind:
        index.append("| `%s` | %s | %d | [%s](%s) |"
                     % (k, sections_text(kind_sections[k]), len(group), k, view_name("kind", k)))
    index.append("")
    files["README.md"] = "\n".join(index)

    for st, group in by_status:
        name, meaning = LABEL[st]
        out = ["# 登録簿：%s（%d 件）" % (name, len(group)), "", GENERATED,
               "（`python3 build.py` で作り直す）", "",
               "状態が「%s」の項目を集めた頁です。%s。" % (name, meaning), "",
               "[目次](README.md)・[全件](../REGISTER.md)", ""]
        for e in group:
            out += render_entry(e)
        files[view_name("status", st)] = "\n".join(out)

    for k, group in by_kind:
        out = ["# 登録簿：`%s` の項目（%d 件）" % (k, len(group)), "", GENERATED,
               "（`python3 build.py` で作り直す）", "",
               "`id` が `%s` で始まる項目を集めた頁です。`register.toml` で置かれている節は、%s です。"
               % (k, sections_text(kind_sections[k])), "",
               "[目次](README.md)・[全件](../REGISTER.md)", ""]
        for st in ORDER:
            sub = [e for e in group if e["status"] == st]
            if not sub:
                continue
            out += ["## %s（%d 件）" % (LABEL[st][0], len(sub)), ""]
            for e in sub:
                out += render_entry(e)
        files[view_name("kind", k)] = "\n".join(out)
    return files


def outputs(reg=None):
    """{リポジトリからの相対パス: 中身}。build.py が書くものの全部。"""
    reg = reg or load()
    out = {"REGISTER.md": render(reg), os.path.join("data", "register.csv"): render_csv(reg)}
    for name, text in render_views(reg, kinds()).items():
        out[os.path.join("views", name)] = text
    return out


def write(rel, text):
    path = os.path.join(HERE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    before = io.open(path, encoding="utf-8", newline="").read() if os.path.exists(path) else None
    if before != text:
        io.open(path, "w", encoding="utf-8", newline="").write(text)
    return before == text


if __name__ == "__main__":
    reg = load()
    files = outputs(reg)
    same = {rel: write(rel, text) for rel, text in sorted(files.items())}
    # 状態や種類が無くなったときの頁を残さない。
    vdir = os.path.join(HERE, "views")
    for name in sorted(os.listdir(vdir)):
        if os.path.join("views", name) not in files:
            os.remove(os.path.join(vdir, name))
            print("views/%s  消しました" % name)
    print("REGISTER.md  %d 件  %s"
          % (len(reg["entry"]), "変更なし" if same["REGISTER.md"] else "書き直しました"))
    rest = [r for r in same if r != "REGISTER.md"]
    print("ほか %d ファイル  %s" % (len(rest), "変更なし" if all(same[r] for r in rest)
                                   else "書き直しました"))
