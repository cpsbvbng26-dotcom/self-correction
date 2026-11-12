# 登録簿：`MR` の項目（3 件）

このファイルは `register.toml` からの生成物です。手で編集しません。
（`python3 build.py` で作り直す）

`id` が `MR` で始まる項目を集めた頁です。`register.toml` で置かれている節は、機械を介した再発見の論文 3 です。

[目次](README.md)・[全件](../REGISTER.md)

## 直せない（3 件）

### MR-001 —— 到達が独立でなかったと断定していますが、本文は確かめられないと述べています

- **どこ** —— Machine-mediated Rediscovery（SSRN、Sophaxis 2026.0002）の要旨・第4節・第7節
- **DOI** —— [10.2139/ssrn.7537983](https://doi.org/10.2139/ssrn.7537983)
- **述べていたこと** —— the case is neither a Mertonian multiple nor a rediscovery in the usual sense, because the arrival was neither independent nor human（要旨）／ this arrival was not independent in the relevant sense: the construction came from a model trained on text that may well include that literature（第4節）
- **何が問題か** —— 第7節は、it cannot be established which parts of the first preprint were generated, which were edited, and whether the model's output drew on the Friedkin–Johnsen literature と書いています。記録が支えるのは、独立だったと確かめられない、までです。独立ではなかった、はそれより強い主張です。第4節の根拠も may well include で、可能性の形です。要旨と第4節は、その可能性を断定の形に書いています。もう一つの根拠（人が結果に到達したのではなく、受け取った）は、この食い違いと関係なく立ちます
- **なぜ直せないか** —— SSRN で公開した PDF で、直せません。Sophaxis の写し（data/pdf/2026.0002v1.pdf）も、取り寄せたまま変えません。この論文には正誤表がないので、ここに記録します
- **見つけたのは** —— Academia Co-scientist（言語モデルの研究補助）の出力。2026-11-12 に利用者から受け取り、Claude が紙面と照合しました
- **証拠** —— <https://github.com/cpsbvbng26-dotcom/sophaxis/blob/main/data/pdf/2026.0002v1.pdf>
- **起きた** —— 2026-09-30
- **書いた** —— 2026-11-12
- **記録の性質** —— 再構成
- **誰が確かめられるか** —— 紙面

### MR-002 —— 一つの事例から、優先権の確認がすべて正当化の文脈へ移ると一般化しています

- **どこ** —— Machine-mediated Rediscovery の要旨・第3節・第8節
- **DOI** —— [10.2139/ssrn.7537983](https://doi.org/10.2139/ssrn.7537983)
- **述べていたこと** —— The whole burden of establishing that the result is not already known moves into the context of justification.（第3節）／ the check for priority, which used to be shared between the two contexts, now falls entirely on justification（第8節）
- **何が問題か** —— 事例は一つで、比べる群がありません。第7節自身が For these reasons the paper does not generalise と書いています。第3節と第8節は、その一般化をしています。人が独りで発見した場合にも、先行研究の確認が抜けることはありえます。機械が生成したことがこの抜けの原因だとは、示されていません。事例そのものも、すべて、を弱めます。第3節は the model supplied a pointer to the literature that the user did not follow と書いています。発見の文脈の側に、文献への手がかりが届いていました。言えるのは、この事例では確認が正当化の側で行われなかった、までです
- **なぜ直せないか** —— SSRN で公開した PDF で、直せません。Sophaxis の写し（data/pdf/2026.0002v1.pdf）も、取り寄せたまま変えません。この論文には正誤表がないので、ここに記録します
- **見つけたのは** —— Academia Co-scientist（言語モデルの研究補助）の出力。2026-11-12 に利用者から受け取り、Claude が紙面と照合しました
- **証拠** —— <https://github.com/cpsbvbng26-dotcom/sophaxis/blob/main/data/pdf/2026.0002v1.pdf>
- **起きた** —— 2026-09-30
- **書いた** —— 2026-11-12
- **記録の性質** —— 再構成
- **誰が確かめられるか** —— 紙面

### MR-003 —— 実装でしか見えなかったとした取り違えが、紙面だけを読んだ査読にも見えていました

- **どこ** —— Machine-mediated Rediscovery の要旨・第2.2節・第6節
- **DOI** —— [10.2139/ssrn.7537983](https://doi.org/10.2139/ssrn.7537983)
- **述べていたこと** —— Stage 7 exposed an error that could not have been seen on paper.（第2.2節）／ The confusion between norm and spectral radius could not have been found on paper at all（第6節）／ implementation, not reflection, exposed the error that mattered（要旨）
- **何が問題か** —— 比べたもののない反実仮想です。著者自身の記録に反例があります。EX-007 では、Stanford Agentic Reviewer が PDF だけを渡されて (DP)³ = (a₁a₂a₃)I を導き、Series II の縮小率が漸近率としてはゆるいことを示しました（trinity-infinity の ERRATA の N9）。ノルムとスペクトル半径の取り違えのうち、速さの側は紙面から見えていました。その記録は 2026-09-08 で、この論文の公開（2026-09-30）より前です。trinity-infinity の README も、この取り違えを、同じ講義が試験で問うところと書いています。立っているのは狭いほうの主張です。論文の仮定（巡回置換の Q と [0,1) の係数）のもとでは、収束するかどうかの判定は変わりません
- **なぜ直せないか** —— SSRN で公開した PDF で、直せません。Sophaxis の写し（data/pdf/2026.0002v1.pdf）も、取り寄せたまま変えません。この論文には正誤表がないので、ここに記録します
- **見つけたのは** —— Academia Co-scientist（言語モデルの研究補助）の出力。2026-11-12 に利用者から受け取り、Claude が紙面と照合しました
- **証拠** —— <https://github.com/cpsbvbng26-dotcom/sophaxis/blob/main/data/pdf/2026.0002v1.pdf>
- **起きた** —— 2026-09-30
- **書いた** —— 2026-11-12
- **記録の性質** —— 再構成
- **誰が確かめられるか** —— 紙面
