# 登録簿を絞り込んだ頁

このファイルは `register.toml` からの生成物です。手で編集しません。
（`python3 build.py` で作り直す）

[REGISTER.md](../REGISTER.md) の全件を、状態ごとと種類ごとに分けた頁です。
どの頁も静的な Markdown で、絞り込みにスクリプトを使いません。

## 状態ごと

| 状態 | 件数 | 頁 |
| --- | --- | --- |
| いま立っている | 13 | [standing](status-standing.md) |
| 未解決 | 7 | [open](status-open.md) |
| 直せない | 28 | [unresolvable](status-unresolvable.md) |
| 直した | 50 | [corrected](status-corrected.md) |
| 撤回した | 6 | [withdrawn](status-withdrawn.md) |

## 種類ごと

種類は `id` の頭の二文字です。
その二文字の項目が `register.toml` のどの節に置かれているかを、節ごとの件数とともに写しています。

| 種類 | 置かれている節 | 件数 | 頁 |
| --- | --- | --- | --- |
| `TI` | 三篇そのもの 7、道具そのもの 5 | 12 | [TI](kind-TI.md) |
| `WD` | 撤回したもの 4 | 4 | [WD](kind-WD.md) |
| `SC` | 自分の訂正のほうの誤り 5、哲学の三篇 1、道具そのもの 26、外部からの評価 13 | 45 | [SC](kind-SC.md) |
| `ST` | 自分の訂正のほうの誤り 1、道具そのもの 1、いま立っているもの 3 | 5 | [ST](kind-ST.md) |
| `WS` | サイトの記述 3、外部からの評価 1 | 4 | [WS](kind-WS.md) |
| `PH` | 哲学の三篇 8、道具そのもの 5、外部からの評価 1 | 14 | [PH](kind-PH.md) |
| `NG` | 史料ノート 4 | 4 | [NG](kind-NG.md) |
| `MR` | 機械を介した再発見の論文 3 | 3 | [MR](kind-MR.md) |
| `TL` | 道具そのもの 2 | 2 | [TL](kind-TL.md) |
| `EX` | 道具そのもの 2、外部からの評価 8 | 10 | [EX](kind-EX.md) |
| `BK` | 一般向けの書籍 1 | 1 | [BK](kind-BK.md) |
