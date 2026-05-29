#!/usr/bin/env python3
"""
デジタル単語帳

【単語の追加・切り替え方法】
  words/ フォルダに CSV ファイルを置くだけで自動で認識されます。
  例: words/unit7.csv, words/midterm.csv など

【CSV ファイルのフォーマット】
  1行目（ヘッダー）: english,kana,japanese
  2行目以降（単語）: run out of ~,ラン アウト オブ,不足する
"""
import csv
import random
import sys
from pathlib import Path

WORDS_DIR = Path(__file__).parent / "words"


# ─────────────────────────────────────────────────────────
#  CSV 読み込み・セット検出
# ─────────────────────────────────────────────────────────

def detect_sets() -> dict[str, Path]:
    """words/ 内の CSV を検出してファイル名→パスの辞書を返す"""
    if not WORDS_DIR.exists():
        print(f"\n  エラー: words/ フォルダが見つかりません。")
        print(f"  場所: {WORDS_DIR}")
        sys.exit(1)

    found = {p.stem: p for p in sorted(WORDS_DIR.glob("*.csv"))}
    if not found:
        print(f"\n  エラー: words/ フォルダに CSV ファイルがありません。")
        sys.exit(1)
    return found


def load_csv(name: str, path: Path) -> list[dict]:
    """CSV 1ファイルを読み込んで単語リストを返す"""
    words = []
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            words.append({
                "set":  name,
                "en":   row["english"].strip(),
                "kana": row["kana"].strip(),
                "ja":   row["japanese"].strip(),
                "pos":  row.get("pos", "").strip(),
            })
    return words


def word_count(path: Path) -> int:
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f) - 1  # ヘッダー行を除く


# ─────────────────────────────────────────────────────────
#  設定メニュー
# ─────────────────────────────────────────────────────────

def select_sets(sets: dict[str, Path]) -> list[dict]:
    """出題セットを選択（複数選択・全選択対応）"""
    names = list(sets.keys())

    print("\n  出題するセットを選んでね:")
    for i, name in enumerate(names, 1):
        print(f"    {i}. {name}（{word_count(sets[name])}語）")
    if len(names) > 1:
        print(f"    a. すべて（合計 {sum(word_count(p) for p in sets.values())}語）")
    print()
    print("  複数選ぶときはカンマ区切り（例: 1,2）")

    while True:
        raw = input("  選択: ").strip().lower()

        if raw == "a" and len(names) > 1:
            selected = names
            break

        parts = [p.strip() for p in raw.split(",")]
        try:
            indices = [int(p) - 1 for p in parts]
            if parts and all(0 <= idx < len(names) for idx in indices):
                selected = [names[idx] for idx in indices]
                break
        except ValueError:
            pass
        print(f"  1〜{len(names)} の番号か a を入力してね。")

    pool = []
    for name in selected:
        pool.extend(load_csv(name, sets[name]))
    return pool


def select_direction() -> str:
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

def quiz(pool: list[dict], direction: str):
    deck = pool[:]
    random.shuffle(deck)
    total      = len(deck)
    correct    = 0
    wrong_list = []

    for i, word in enumerate(deck, 1):
        print(f"\n  {'─' * 43}")
        print(f"  【 {i} / {total} 】  {word['set']}")
        print(f"  {'─' * 43}")

        if direction == "3":
            d = random.choice(["en_to_ja", "ja_to_en"])
        else:
            d = "en_to_ja" if direction == "1" else "ja_to_en"

        pos_str = f"  [{word['pos']}]" if word.get("pos") else ""
        if d == "en_to_ja":
            print(f"\n  ❓  {word['en']}{pos_str}")
            print(f"      読み: {word['kana']}")
            input("\n  Enter で答えを確認... ")
            print(f"\n  ✅  {word['ja']}")
        else:
            print(f"\n  ❓  {word['ja']}{pos_str}")
            input("\n  Enter で答えを確認... ")
            print(f"\n  ✅  {word['en']}")
            print(f"      読み: {word['kana']}")

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

    if wrong_list:
        print(f"\n  【要復習リスト】")
        for w in wrong_list:
            pos_tag = f" [{w['pos']}]" if w.get("pos") else ""
            print(f"  ・{w['en']}（{w['kana']}）→ {w['ja']}{pos_tag}")


# ─────────────────────────────────────────────────────────
#  メイン
# ─────────────────────────────────────────────────────────

def main():
    print("\n  ╔═══════════════════════════════════════════╗")
    print("  ║         デジタル単語帳                    ║")
    print("  ╚═══════════════════════════════════════════╝")

    while True:
        sets      = detect_sets()
        pool      = select_sets(sets)
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
