#!/usr/bin/env python3
"""register.toml から REGISTER.md を組み立てる。

    python3 build.py

**人が読む版を手で書かない。**手で書くと、登録簿のほうと必ずずれる。
ずれたときに気づく手立てが無ければ、記録としての意味が無くなる。
"""

import io
import os
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))

LABEL = {
    "standing": ("いま立っている", "この主張は取り下げていない。反証の手順を添えてある"),
    "corrected": ("直した", "誤りが見つかり、直したもの。元の記述は消していない"),
    "withdrawn": ("撤回した", "取り下げたもの。元の記述は消していない"),
    "unresolvable": ("直せない", "凍結された成果物の側に誤りがある。もう直せない"),
    "open": ("未解決", "まだ判断がついていない"),
}
ORDER = ["standing", "open", "unresolvable", "corrected", "withdrawn"]

FIELDS = [
    ("where", "どこ"),
    ("doi", "DOI"),
    ("claimed", "述べていたこと"),
    ("support", "支え"),
    ("problem", "何が問題か"),
    ("correction", "どうしたか"),
    ("why_unresolvable", "なぜ直せないか"),
    ("why_open", "なぜ未解決か"),
    ("refute", "どうすれば覆るか"),
    ("found_by", "見つけたのは"),
    ("evidence", "証拠"),
    ("occurred", "起きた"),
    ("recorded", "書いた"),
    ("basis", "記録の性質"),
]


def load(path=None):
    with open(path or os.path.join(HERE, "register.toml"), "rb") as fh:
        return tomllib.load(fh)


def render(reg):
    out = ["# 訂正の登録簿",
           "",
           "**このファイルは `register.toml` から生成しています。手で編集しないでください。**",
           "（`python3 build.py` で作り直します）",
           "",
           "公開したあとで誤りが見つかったもの、撤回したもの、果たされなかった約束を、",
           "**一件ずつ、消さずに**記録しています。",
           "",
           "`id` は永久に消しません。過去のどの版にあった `id` も、いまの版に無ければ",
           "`verification/check_register.py` が落とします。**都合の悪い記録は、消せない",
           "作りにしてあります。**",
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
            out += ["### %s —— %s" % (e["id"], e["title"]), ""]
            for key, label in FIELDS:
                if key in e:
                    v = e[key]
                    if key == "doi":
                        v = "[%s](https://doi.org/%s)" % (v, v)
                    elif key == "evidence" and str(v).startswith("http"):
                        v = "<%s>" % v
                    out.append("- **%s** —— %s" % (label, v))
            out.append("")
    out += ["---", "",
            "所有者: %s（ORCID: [%s](https://orcid.org/%s)）"
            % (reg["owner"], reg["orcid"], reg["orcid"]), ""]
    return "\n".join(out)


if __name__ == "__main__":
    reg = load()
    text = render(reg)
    path = os.path.join(HERE, "REGISTER.md")
    before = io.open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if before != text:
        io.open(path, "w", encoding="utf-8").write(text)
    print("REGISTER.md  %d 件  %s"
          % (len(reg["entry"]), "変更なし" if before == text else "書き直しました"))
