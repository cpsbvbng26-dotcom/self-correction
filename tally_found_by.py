#!/usr/bin/env python3
"""誰が見つけたかを数える。

    python3 tally_found_by.py

登録簿の各項目には `found_by` がある。**誰が、どうやって見つけたか**である。
そこを数えると、この記録が何に支えられているかが出る。

分け方は五つ。**最初に名指しされた者で数える。**「A と B」の形は、
複数の欄に別に数える。

    機械    検査・道具が落とした
    著者    目視、数え直し、問い直し
    利用者  指摘・申し出
    Claude  作業中に気づいた
    外部    Stanford Agentic Reviewer・Grok・ChatGPT

**これは手柄の配分ではない。**どこが弱いかを見るための数である。
"""

import collections
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

KINDS = [
    ('機械', ('機械',)),
    ('著者', ('著者',)),
    ('利用者', ('利用者',)),
    # 「こちら」はこの記録では作業の側、すなわち Claude を指す。
    # **別の欄を立てない。**立てれば同じものが二つに割れる。
    ('Claude', ('Claude', 'こちら')),
    ('外部', ('Stanford Agentic Reviewer', 'Grok', 'ChatGPT', '外部')),
]


def classify(text):
    """その記述に現れる見つけ手を、現れた順に返す。"""
    hits = []
    for name, keys in KINDS:
        pos = min((text.find(k) for k in keys if k in text), default=-1)
        if pos >= 0:
            hits.append((pos, name))
    return [n for _, n in sorted(hits)]


def read():
    src = open(os.path.join(ROOT, 'register.toml'), encoding='utf-8').read()
    ids = re.findall(r'^id\s*=\s*"([^"]+)"', src, re.M)
    found = re.findall(r'^found_by\s*=\s*"([^"]+)"', src, re.M)
    return ids, found


def main():
    ids, found = read()
    first = collections.Counter()
    anywhere = collections.Counter()
    multi = 0
    unknown = []
    for t in found:
        who = classify(t)
        if not who:
            unknown.append(t)
            continue
        first[who[0]] += 1
        for w in set(who):
            anywhere[w] += 1
        if len(set(who)) > 1:
            multi += 1

    print('登録簿の項目            %d 件' % len(ids))
    print('found_by がある項目     %d 件' % len(found))
    print('found_by が無い項目     %d 件' % (len(ids) - len(found)))
    print()
    print('  見つけ手   最初に名指し   どこかに出る')
    print('  --------  ------------  ------------')
    for name, _ in KINDS:
        print('  %-8s  %12d  %12d' % (name, first[name], anywhere[name]))
    print('  %-8s  %12d' % ('分類不能', len(unknown)))
    print()
    print('  二者以上が関わったもの   %d 件' % multi)
    print()

    total = sum(first.values())
    if total:
        m = first['機械']
        print('**機械が最初に見つけたのは %d 件である**（%d 件中、%.1f%%）。'
              % (m, total, 100.0 * m / total))
        print('残る %d 件は、人が見つけている。' % (total - m))
        print()
        print('検査は、見つけた誤りが**戻ってこない**ようにする道具である。')
        print('**最初に見つける道具ではない。**')
    for t in unknown:
        print('  分類できない記述: ' + t, file=sys.stderr)
    return first, anywhere, multi, len(unknown)


if __name__ == '__main__':
    main()
