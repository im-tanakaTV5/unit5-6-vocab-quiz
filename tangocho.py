#!/usr/bin/env python3
"""
デジタル単語帳 - Unit 5 & 6
ランダム出題・カタカナ読み付き答え合わせアプリ
"""
import random
import sys

# ─────────────────────────────────────────────────────────
#  単語データ（Unit 5・Unit 6）
# ─────────────────────────────────────────────────────────
WORDS = [
    # ── Unit 5 ──────────────────────────────────────────
    {"unit": 5, "en": "run out of ~",          "kana": "ラン アウト オブ",          "ja": "不足する、なくなる、足りなくなる"},
    {"unit": 5, "en": "date back to ~",        "kana": "デイト バック トゥ",        "ja": "〜にさかのぼる、〜の時代から続く"},
    {"unit": 5, "en": "trace",                 "kana": "トレイス",                  "ja": "（起源・歴史などを）たどる、さかのぼって調べる"},
    {"unit": 5, "en": "wild",                  "kana": "ワイルド",                  "ja": "野生の、荒れた"},
    {"unit": 5, "en": "commonly",              "kana": "コモンリー",                "ja": "一般に、普通に"},
    {"unit": 5, "en": "ancestor",              "kana": "アンセスター",              "ja": "祖先、先祖"},
    {"unit": 5, "en": "domestic",              "kana": "ドメスティック",            "ja": "家庭の、国内の、（動物が）飼いならされた"},
    {"unit": 5, "en": "temporary",             "kana": "テンポラリー",              "ja": "一時的な、仮の"},
    {"unit": 5, "en": "a period of time",      "kana": "ア ピリオド オブ タイム",   "ja": "一定の期間"},
    {"unit": 5, "en": "permanent",             "kana": "パーマネント",              "ja": "永続的な、永久の"},
    {"unit": 5, "en": "disturb",               "kana": "ディスターブ",              "ja": "乱す、不安にさせる"},
    {"unit": 5, "en": "even",                  "kana": "イーブン",                  "ja": "〜でさえ／平らな、均等な"},
    {"unit": 5, "en": "be responsible for ~",  "kana": "ビー レスポンシブル フォー","ja": "〜に対して責任がある、〜の原因である"},
    {"unit": 5, "en": "fault",                 "kana": "フォールト",                "ja": "過失、欠点、責任"},
    {"unit": 5, "en": "run a restaurant",      "kana": "ラン ア レストラン",        "ja": "レストランを経営する"},
    {"unit": 5, "en": "shipping",              "kana": "シッピング",                "ja": "輸送、出荷、海運"},
    {"unit": 5, "en": "blame ~ for ...",       "kana": "ブレイム フォー",           "ja": "〜のことで…を非難する、…の責任を〜のせいにする"},
    {"unit": 5, "en": "shortage",              "kana": "ショーテージ",              "ja": "不足、欠乏"},
    {"unit": 5, "en": "ascribe ~ to ...",      "kana": "アスクライブ トゥ",         "ja": "〜を…のせいにする、〜の原因を…とみなす"},
    # ── Unit 6 ──────────────────────────────────────────
    {"unit": 6, "en": "exclude",               "kana": "エクスクルード",            "ja": "〜を除外する、締め出す"},
    {"unit": 6, "en": "release",               "kana": "リリース",                  "ja": "〜を解放する、公開する／釈放"},
    {"unit": 6, "en": "opponent",              "kana": "オポーネント",              "ja": "反対者、対戦相手"},
    {"unit": 6, "en": "disagree",              "kana": "ディスアグリー",            "ja": "同意しない、意見が合わない"},
    {"unit": 6, "en": "punishment",            "kana": "パニッシュメント",          "ja": "罰、刑罰"},
    {"unit": 6, "en": "confidence",            "kana": "コンフィデンス",            "ja": "自信、信頼"},
    {"unit": 6, "en": "abolish",               "kana": "アボリッシュ",              "ja": "〜を廃止する"},
    {"unit": 6, "en": "declare",               "kana": "デクレア",                  "ja": "〜を宣言する、表明する"},
    {"unit": 6, "en": "position",              "kana": "ポジション",                "ja": "立場、位置、職"},
    {"unit": 6, "en": "matter",                "kana": "マター",                    "ja": "問題、事柄／重要である"},
    {"unit": 6, "en": "worldwide",             "kana": "ワールドワイド",            "ja": "世界中の、世界的に"},
]

# ─────────────────────────────────────────────────────────
#  設定メニュー
# ─────────────────────────────────────────────────────────
def select_unit():
    print("\n  出題範囲を選んでね:")
    print("    1. Unit 5 のみ（19語）")
    print("    2. Unit 6 のみ（11語）")
    print("    3. Unit 5 + 6（全30語）")
    while True:
        c = input("  選択 [1/2/3]: ").strip()
        if c == "1":
            return [w for w in WORDS if w["unit"] == 5]
        if c == "2":
            return [w for w in WORDS if w["unit"] == 6]
        if c == "3":
            return WORDS[:]
        print("  1〜3 で入力してね。")

def select_direction():
    print("\n  出題方向を選んでね:")
    print("    1. 英語 → 日本語")
    print("    2. 日本語 → 英語")
    print("    3. ランダム（どちらも出る）")
    while True:
        c = input("  選択 [1/2/3]: ").strip()
        if c in ("1", "2", "3"):
            return c
        print("  1〜3 で入力してね。")

# ─────────────────────────────────────────────────────────
#  クイズ本体
# ─────────────────────────────────────────────────────────
def quiz(pool, direction):
    deck = pool[:]
    random.shuffle(deck)
    total   = len(deck)
    correct = 0
    wrong_list = []

    for i, word in enumerate(deck, 1):
        print(f"\n  {'─' * 43}")
        print(f"  【 {i} / {total} 】  Unit {word['unit']}")
        print(f"  {'─' * 43}")

        # 出題方向を決定
        if direction == "3":
            d = random.choice(["en_to_ja", "ja_to_en"])
        else:
            d = "en_to_ja" if direction == "1" else "ja_to_en"

        # 問題表示
        if d == "en_to_ja":
            print(f"\n  ❓  {word['en']}")
            print(f"      読み: {word['kana']}")
            input("\n  Enter で答えを確認... ")
            print(f"\n  ✅  {word['ja']}")
        else:
            print(f"\n  ❓  {word['ja']}")
            input("\n  Enter で答えを確認... ")
            print(f"\n  ✅  {word['en']}")
            print(f"      読み: {word['kana']}")

        # 自己採点
        while True:
            mark = input("\n  正解した？  [o = ○正解 / x = ✗不正解]: ").strip().lower()
            if mark in ("o", "○", "0"):
                correct += 1
                print("  ○ 正解！")
                break
            if mark in ("x", "✗", "×"):
                print("  ✗ 残念！次は覚えよう！")
                wrong_list.append(word)
                break
            print("  o か x で入力してね。")

    # ── 結果 ────────────────────────────────────────────
    pct = correct / total * 100
    print(f"\n  {'═' * 43}")
    print(f"  結果: {correct} / {total} 問正解！  （{pct:.0f}%）")
    if pct == 100:
        print("  🎉 満点！完璧だよ！")
    elif pct >= 80:
        print("  👏 よくできました！もう少しで完璧！")
    elif pct >= 60:
        print("  💪 半分以上正解！引き続き頑張ろう！")
    else:
        print("  📖 もう一度チャレンジしてみよう！")
    print(f"  {'═' * 43}")

    # 間違えた単語の一覧
    if wrong_list:
        print(f"\n  【要復習リスト】")
        for w in wrong_list:
            print(f"  ・{w['en']}（{w['kana']}）→ {w['ja']}")

# ─────────────────────────────────────────────────────────
#  メイン
# ─────────────────────────────────────────────────────────
def main():
    print("\n  ╔═══════════════════════════════════════════╗")
    print("  ║     デジタル単語帳  Unit 5 & 6           ║")
    print("  ╚═══════════════════════════════════════════╝")

    while True:
        pool      = select_unit()
        direction = select_direction()
        quiz(pool, direction)

        print("\n  もう一度やる？ [y = もう一度 / n = 終了]: ", end="")
        if input().strip().lower() != "y":
            print("\n  お疲れ様！また勉強しようね！👋\n")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  終了します。またね！👋\n")
        sys.exit(0)
