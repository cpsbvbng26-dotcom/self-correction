# 登録簿：`GW` の項目（1 件）

このファイルは `register.toml` からの生成物です。手で編集しません。
（`python3 build.py` で作り直す）

`id` が `GW` で始まる項目を集めた頁です。`register.toml` で置かれている節は、黄金比の窓の予想を解いた稿 1 です。

[目次](README.md)・[全件](../REGISTER.md)

## 直せない（1 件）

### GW-001 —— 次元の公式の出所を、Allaart・Kong が挙げたものとは別の Raith の論文にしていました

- **どこ** —— Resolution of the Golden-Window Conjecture and Related Results on β-Transformations with a Hole and on the Trinity-Infinity Series II Game（Figshare）の Corollary 7.2 の証明と、文献の [17]
- **DOI** —— [10.6084/m9.figshare.35050300](https://doi.org/10.6084/m9.figshare.35050300)
- **述べていたこと** —— The dimension formula dim_H K_β(t) = h(K̃_β(t))/log β for all β > 1 is [AKgen, Lemma 6.2], stated there as deducible from Raith [17] (not read). [17] P. Raith, Hausdorff dimension for piecewise monotonic maps, Studia Math. (1989)
- **何が問題か** —— Allaart・Kong（arXiv 2411.03516v3）は、Lemma 6.2 の直前で can be deduced from Raith [26] と書いています。その [26] は、P. Raith, Continuity of the Hausdorff dimension for invariant subsets of interval maps, Acta Math. Univ. Comenian. (N.S.) 63 (1994) です。稿は、これとは別の 1989 年の論文を挙げていました。稿はどちらの論文も読んでいません。読んでいないものを、読んだ側の文献の番号と取り違えて写しました
- **どうしたか** —— 結論は変わりません。次元の公式は Allaart・Kong の Lemma 6.2 から引いており、Raith の論文はどちらも読んでいません。正しい出所は Raith 1994 です。golden-window-resolution の continuity/REFEREE.md と、continuity/ の稿の文献の節に書きました
- **なぜ直せないか** —— Figshare で公開した PDF は凍結しており、直しません
- **見つけたのは** —— Claude（2026-11-19 に、二つ目の稿を査読したとき）
- **証拠** —— <https://github.com/cpsbvbng26-dotcom/golden-window-resolution/blob/main/continuity/REFEREE.md>
- **起きた** —— 2026-11-18
- **書いた** —— 2026-11-19
- **記録の性質** —— 同時
- **誰が確かめられるか** —— 紙面
