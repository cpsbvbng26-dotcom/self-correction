# データ辞書

`register.csv` は、登録簿の全件を一件一行に並べたものです。
正は `register.toml` で、`register.csv` は `python3 build.py` が作る生成物です。手で編集しません。
CSV は表計算ソフト向けで、UTF-8（BOM なし）、区切りはカンマ、改行は LF です。
`datapackage.json` が、同じ列の型と制約を機械が読める形で述べています。

## 列の定義

| 列 | 内容 |
| --- | --- |
| `id` | 識別子。`AA-000` の形。頭の二文字が種類を表す。永久に消さない |
| `status` | 状態。五つのどれか。下記参照 |
| `title` | 題 |
| `where` | 誤りや主張がどこにあったか。成果物・ファイル・節の名 |
| `doi` | 対象の DOI。対象が DOI を持たないときは空欄 |
| `claimed` | 述べていたこと。全件にある |
| `support` | 主張の支え |
| `counter` | 何が主張を弱めているか。`standing` の項目にだけ置く |
| `problem` | 何が問題か |
| `correction` | どうしたか |
| `why_unresolvable` | なぜ直せないか。`unresolvable` には必須 |
| `why_open` | なぜ未解決か。`open` には必須 |
| `refute` | どうすれば覆るか。`standing` には必須 |
| `found_by` | 誰が見つけたか |
| `evidence` | 証拠の URL。`https://` で始まる |
| `occurred` | 出来事が起きた時点。`2025-10` のように月までのものと、日までのものがある |
| `recorded` | この登録簿に書いた日。`YYYY-MM-DD`。git の履歴と一致する |
| `basis` | `同時` か `再構成` か |
| `verifiable` | `紙面` か `証言` か |

欄の無い項目は、空欄にしています。空欄は「その欄を書いていない」を意味します。「該当しない」と「書き落とした」を、CSV の上では区別しません。

## `status` について

| 値 | 意味 |
| --- | --- |
| `standing` | いまも立っている主張。覆し方（`refute`）を必ず持つ |
| `open` | まだ判断がついていない。`why_open` を必ず持つ |
| `unresolvable` | 直せない。凍結された成果物の側に誤りがある。`why_unresolvable` を必ず持つ |
| `corrected` | 誤りが見つかり、直した |
| `withdrawn` | 取り下げた。元の記述は消していない |

## `basis` と `verifiable` について

| 列 | 値 | 意味 |
| --- | --- | --- |
| `basis` | `同時` | 出来事の時点で記録した。`recorded − occurred` が 1 日以内 |
| `basis` | `再構成` | あとから書き起こした |
| `verifiable` | `紙面` | 凍結された PDF・git の履歴・走らせられるコードから、誰でも確かめられる |
| `verifiable` | `証言` | 著者の言葉以外に根拠が無い |

## 使い方の例

標準ライブラリだけで動きます。全件と、状態ごとの件数と、証言しか根拠の無い件数を数えます。

```python
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
```

この例は [`example.py`](example.py) と一字一句同じです。`verification/check_dataset.py` が、二つが同じであることと、走らせた結果が `register.toml` の件数と合うことを確かめます。

## 確かめ方

```
python3 verification/check_register.py
python3 verification/check_dataset.py
```

一つ目は登録簿の形と履歴を見ます。二つ目は、CSV が `register.toml` から作り直したものと一致するか、この表の列が CSV の列と同じ順で並ぶか、`datapackage.json` の列・型・制約が実際の値に合うかを見ます。

## 記録していないもの

項目の重さ（重大度）は列にしていません。各リポジトリの正誤表が重大度を持ちますが、登録簿の側では揃えていません。

## 引用

```
根本卓哉「self-correction: 一人の研究者による、自分の公開した主張の訂正の全記録」Zenodo、2026年、https://doi.org/10.5281/zenodo.24033596
```

同じ文字列が、リポジトリの README と `datapackage.json` の `citation` にもあります。`verification/check_dataset.py` が三箇所の一致を確かめています。経緯は [リポジトリの README](../README.md#引用) にあります。
