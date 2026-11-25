# 登録簿：`GW` の項目（4 件）

このファイルは `register.toml` からの生成物です。手で編集しません。
（`python3 build.py` で作り直す）

`id` が `GW` で始まる項目を集めた頁です。`register.toml` で置かれている節は、黄金比の窓の予想を解いた稿 4 です。

[目次](README.md)・[全件](../REGISTER.md)

## 直せない（4 件）

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

### GW-002 —— Theorem D のあとの一文が、一般の r の窓を、Proposition 5.3 と表 1 とは違う形で書いていました

- **どこ** —— Resolution of the Golden-Window Conjecture and Related Results on β-Transformations with a Hole and on the Trinity-Infinity Series II Game（Figshare）の 4.4 節、Theorem D のあとの段落の最後の一文
- **DOI** —— [10.6084/m9.figshare.35050300](https://doi.org/10.6084/m9.figshare.35050300)
- **述べていたこと** —— With general r, the window is (δ_3(r), (1 + r)/3), non-empty iff r ≠ 2.
- **何が問題か** —— δ_3(r) = (√(1+4r) − 1)/2 は、r > 2 で 1 を超えます。r = 3 では 1.3028 です。割引因子は (0, 1) の中にあるので、r > 2 では窓に入る割引因子がありません。r = 2 では δ_3 = 1 です。稿の Proposition 5.3 も、k = 2 の辺で窓が開くのを k > r、すなわち r < 2 のときに限っています。上端も食い違っています。Proposition 5.3 は上端を U_2(r) = max(1/2, (1+r)/3) とし、表 1 は r = 1/4 の窓を (0.2071, 0.5000) と載せています。この一文の式では (0.2071, 0.4167) になります。Figshare に置いた数表 windows_three_players.csv の格子探索も、r = 1/4 と r = 1/2 の上端を 0.4991 としています。この一文が成り立つのは 1/2 ≤ r < 2 のときだけです
- **どうしたか** —— 窓は (δ_3(r), max(1/2, (1+r)/3)) で、空でないのは 0 < r < 2 のときです。稿の Proposition 5.3 と表 1 は、この形で書いています。Theorem D の三つの恒等式と、二つの閾値が δ_3(r) で一致することは変わりません。golden-window-resolution には正誤表が無いので、ここに書きます
- **なぜ直せないか** —— Figshare で公開した PDF は凍結しており、直しません
- **見つけたのは** —— Claude（2026-11-25 に、公開した稿の主張を自前の計算と稿の表・数表で突き合わせ直したとき）
- **証拠** —— <https://github.com/cpsbvbng26-dotcom/golden-window-resolution/blob/main/paper/golden-window-resolution.pdf>
- **起きた** —— 2026-11-18
- **書いた** —— 2026-11-25
- **記録の性質** —— 再構成
- **誰が確かめられるか** —— 紙面

### GW-003 —— Remark 8.5 が、六つ目の族の分解が崩れる理由を λ < 0 としていましたが、崩れるのは λ > 1 のときです

- **どこ** —— Resolution of the Golden-Window Conjecture …（Figshare）の 8.2 節、Remark 8.5
- **DOI** —— [10.6084/m9.figshare.35050300](https://doi.org/10.6084/m9.figshare.35050300)
- **述べていたこと** —— For δ > 1/√2 the decomposition used for the sixth family fails (λ < 0)
- **何が問題か** —— 分解の係数は、Theorem 8.4 の証明で λ = (2δ − 1)/(2δe) と定めてあります。e は 1 − δ です。1/2 < δ < 1 では分子も分母も正なので、λ は正です。λ ≤ 1 は 2δ² ≤ 1 と同じで、δ ≤ 1/√2 のときに限ります。δ > 1/√2 で崩れるのは λ ≤ 1 のほうで、1 − λ が負になります。δ = 0.7072 では λ = 1.0006、δ = 0.71 では λ = 1.0199 です。証明は λ ∈ [0, 1] iff δ ≤ 1/√2 と正しく書いており、注意の括弧だけが向きを取り違えていました
- **どうしたか** —— 結論は変わりません。δ > 1/√2 で、六つ目の族の分解は崩れます。理由は λ > 1、すなわち 1 − λ < 0 です。golden-window-resolution には正誤表が無いので、ここに書きます
- **なぜ直せないか** —— Figshare で公開した PDF は凍結しており、直しません
- **見つけたのは** —— Claude（2026-11-25 に、公開した稿の主張を自前の計算と稿の表・数表で突き合わせ直したとき）
- **証拠** —— <https://github.com/cpsbvbng26-dotcom/golden-window-resolution/blob/main/paper/golden-window-resolution.pdf>
- **起きた** —— 2026-11-18
- **書いた** —— 2026-11-25
- **記録の性質** —— 再構成
- **誰が確かめられるか** —— 紙面

### GW-004 —— Allaart・Kong の Theorem 1.4 を仮定を落として引き、文献の [22] に題を書いていませんでした

- **どこ** —— Resolution of the Golden-Window Conjecture …（Figshare）の 4.3 節の最後の段落と、文献の [5]・[22]
- **DOI** —— [10.6084/m9.figshare.35050300](https://doi.org/10.6084/m9.figshare.35050300)
- **述べていたこと** —— for the hole at 0 and fixed β the plateaus are identified in [5, Theorem 1.4]. ／ [22] D. Abreu, D. Pearce, E. Stacchetti, Econometrica (1990). DOI 10.2307/2938299.
- **何が問題か** —— Allaart・Kong（arXiv 2304.06892v3）の Theorem 1.4 は、Assume α(β) is eventually periodic で始まります。平坦部を特定しているのは、α(β) が最終的に周期的になる β についてだけです。稿は、この仮定を書かずに、固定した β 一般のこととして引いていました。稿の文献の節は、この論文を Section 1 と Lemmas 2.1–2.2 まで読んだとしており、Theorem 1.4 は Section 1 にあります。あわせて、文献の [22] には題がありません。DOI 10.2307/2938299 の記録の題は Toward a Theory of Discounted Repeated Games with Imperfect Monitoring で、Econometrica の 58 巻 5 号です
- **どうしたか** —— Theorem C の証明は、同じ論文の Lemma 2.1 を使っており、Theorem 1.4 には依っていません。Theorem 1.4 は、固定した β での類例として挙げたものです。正しくは「α(β) が最終的に周期的な β について、平坦部は [5, Theorem 1.4] で特定されている」です。[22] は D. Abreu, D. Pearce, E. Stacchetti, Toward a Theory of Discounted Repeated Games with Imperfect Monitoring, Econometrica 58(5) (1990) です。golden-window-resolution には正誤表が無いので、ここに書きます
- **なぜ直せないか** —— Figshare で公開した PDF は凍結しており、直しません
- **見つけたのは** —— Claude（2026-11-25 に、公開した稿の引用を、引いた論文の本文と DOI の記録で突き合わせ直したとき）
- **証拠** —— <https://github.com/cpsbvbng26-dotcom/golden-window-resolution/blob/main/paper/golden-window-resolution.pdf>
- **起きた** —— 2026-11-18
- **書いた** —— 2026-11-25
- **記録の性質** —— 再構成
- **誰が確かめられるか** —— 紙面
