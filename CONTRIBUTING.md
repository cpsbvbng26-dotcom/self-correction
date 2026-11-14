# 手を入れるときに

Issue も pull request も歓迎する。登録は要らない。

## ここに何があるか

訂正の登録簿である。`register.toml` が正で、[REGISTER.md](REGISTER.md)・
`data/register.csv`・`views/` はそこから生成される。九つのリポジトリ全部から、訂正の記録として参照されている。

```
python3 build.py    # register.toml から REGISTER.md・CSV・絞り込んだ頁を出す
```

## 何を知らせてほしいか

<https://github.com/cpsbvbng26-dotcom/self-correction/issues> に立てる。

1. 記録されていない誤り。どのリポジトリの、何か
2. 記録の誤り。登録簿の項目が、実際と食い違っている場合
3. 参照の切れ（他のリポジトリから指されている番号が、ここに無い場合）
4. このデータを使ったこと。専用の様式（「このデータを使った」）がある

## 項目を消さない

この登録簿の核である。直した項目も、直したと書いて残す。
消すと、何を間違えたかが分からなくなる。

都合の悪い項目だけを落とせないようにするために、器を先に固定してある。
項目数は README とワークフローの仕事の名前が名乗っており、ずれると検査が落ちる。

## REGISTER.md を手で編集しない

生成物である。`data/register.csv` と `views/` も同じ。直すのは `register.toml` のほうで、そのあと `build.py` を回す。

## 変更を出す

```
python3 verification/check_register.py    # 登録簿の形と履歴
python3 verification/check_dataset.py     # データセットとしての形
```

通ってから出す。依存パッケージは要らない。

## 等級を上げない

各項目は、根拠の等級を持っている（`紙面`・`証言`・`未確認` など）。
確かめていないものを確かめたことにする変更は受けられない。
上げるには、誰でも確かめられる根拠が要る。

## 通らない変更

- **項目を消すこと**
- **根拠の等級を、根拠なしに上げること**
- **生成物（`REGISTER.md`・`data/register.csv`・`views/`）への直接の変更**
- **検査の期待値を、通すために変えること**

## 支えの範囲と、これからの見込み

- **維持しているのは著者一人である**（根本卓哉）。組織の後ろ盾は無い
- issue への返答は**数日から一週間**を目安とする。約束ではない
- 範囲。この九つのリポジトリで起きた訂正に限る。他所の誤りは扱わない
- 項目は増え続ける。減ることは無い

## ライセンス

[MIT](LICENSE)。手を入れたぶんも同じ条件で扱われる。

## 突き合わせの受付 / Checked intake

2026-12-01 から、誤りの知らせ（`error-report.yml`）は「突き合わせの受付」で確かめる。
人が嘘をつくこと一般は、仕組みでは止められない。受けるのは、申し立てた人がその場で書けない出どころと突き合わせられる申し立てだけで、通らないものと確かめられないものは自動で退ける。
確かめるのは一つだけである。「書いてあること」の語が、「どこか」の欄に書いた所（このリポジトリのファイル、配っている頁、このリポジトリが写しを持つ DOI の PDF か翻刻）に、そのとおりにあること。空白の違いと文字の幅は見ない。頁や節は確かめず、文書の全体を探す。
あればラベル「quote verified」を付ける。それが誤りかどうかは、人が読んで決める。なければ、ラベル「not verified」と決まった文のコメントを付け、その申し立ては受け付けない。本文を直すか、新しい issue で出し直せば、もう一度確かめる。
突き合わせの受付は、どの issue も閉じず、鍵も掛けない。どの issue も人が読む。言葉の並びでは、法令が受けて扱うことを求める求め（削除・権利・個人の情報・人についての記述・同意の撤回。どの言語でも）を、誤りの知らせと見分けきれないためである（2026-11-15）。
そう読める語を含む issue には、ラベル「needs a person」も付ける。人への目印で、これに頼って何かを決めることはない。
持ち主が開き直したり直したりしたときは、何もしない。
コメントと実行の記録は、決まった語と issue の番号だけを書き、issue に書かれたことを写さない。
道具は `.github/checked-intake/verify.js`、確かめる先は `.github/checked-intake/config.json` にある。

From 2026-12-01, error reports (`error-report.yml`) are checked by the checked intake.
No system can stop a person from lying in general. Only claims that can be checked against a source that the claimant does not write at the moment of claiming are accepted; a claim that fails, or cannot be checked, is turned away automatically.
One thing is checked: that the words under "What it says" occur, as written, at the location under "Where" (a file of this repository, a page that it serves, or the PDF or transcription of a DOI of which it holds a copy). Differences of white space and character width are ignored. The page or section is not checked; the whole document is searched.
If they occur, the label "quote verified" is added, and whether it is an error is decided by a person. If they do not, the label "not verified" and a fixed comment are added, and the claim is not accepted; editing the issue, or opening a new one, runs the check again.
The checked intake never closes or locks an issue; a person reads every one. No list of words can tell every request that the law requires the operator to receive (removal, rights, personal data, statements about a person, the withdrawal of a consent, in any language) from an error report (2026-11-15).
An issue with words that read as such a request also gets the label "needs a person": a signal for the person, never relied on.
When the owner of the repository reopens or edits an issue, nothing is done.
Comments and logs carry only fixed words and the issue number, never what the issue says.
The script is `.github/checked-intake/verify.js`; what it checks against is in `.github/checked-intake/config.json`.
