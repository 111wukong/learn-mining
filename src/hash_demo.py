"""
哈希基础 — 挖矿的数学基石

SHA-256: 无论输入多大，输出固定 256 位（64 字符十六进制）
"""
import hashlib
import time


def sha256(text: str) -> str:
    """对文本进行 SHA-256 哈希"""
    return hashlib.sha256(text.encode()).hexdigest()


def demo_avalanche_effect():
    """雪崩效应：微小改动，输出巨变"""
    print("=" * 60)
    print("🔬 雪崩效应：输入差一个字符，输出完全不同")
    print("=" * 60)

    h1 = sha256("hello world")
    h2 = sha256("hello worlD")

    print(f'  "hello world"  → {h1}')
    print(f'  "hello worlD"  → {h2}')
    print()

    same = sum(a == b for a, b in zip(h1, h2))
    print(f"  256 位中只有 {same} 位相同（{same/64*100:.1f}%），几乎完全变了！")


def demo_preimage_resistance():
    """原像抗性：无法从哈希反推原文"""
    print("=" * 60)
    print("🔐 原像抗性：已知哈希，无法反推输入")
    print("=" * 60)

    secret = "my_secret_12345"
    h = sha256(secret)
    print(f'  "my_secret_12345" → {h}')
    print(f"  给你这个哈希，你能反推出原文吗？不能。唯一办法是暴力猜。")


def demo_leading_zeros():
    """前导零：挖矿的核心概念"""
    print("=" * 60)
    print("🎯 前导零：'挖矿'就是找满足前导零条件的哈希")
    print("=" * 60)

    data = "block:1"
    nonce = 0
    target_zeros = 4

    start = time.time()
    while True:
        guess = sha256(f"{data}|{nonce}")
        if guess.startswith("0" * target_zeros):
            break
        nonce += 1

    elapsed = time.time() - start
    print(f"  目标：哈希前 {target_zeros} 位都是 0")
    print(f"  尝试 {nonce:,} 次后找到：{hash}")
    print(f"  耗时 {elapsed:.2f} 秒")
    print()
    print(f"  💡 难度 = 16^{target_zeros} = {16**target_zeros:,} 种可能")
    print(f"  平均需要尝试 {16**target_zeros // 2:,} 次")


def demo_pow_failure():
    """演示不同难度下找哈希的速度"""
    print("=" * 60)
    print("📊 难度 vs 时间（在你的电脑上实测）")
    print("=" * 60)

    for zeros in [2, 3, 4, 5, 6]:
        start = time.time()
        nonce = 0
        while True:
            guess = sha256(f"benchmark|{nonce}")
            if guess.startswith("0" * zeros):
                break
            nonce += 1
        elapsed = time.time() - start
        hash_rate = nonce / elapsed if elapsed > 0 else 0
        print(f"  前导 {zeros} 个零 → {nonce:>10,} 次尝试 → {elapsed:>8.3f}s → 算力约 {hash_rate:,.0f} H/s")


if __name__ == "__main__":
    demo_avalanche_effect()
    print()
    demo_preimage_resistance()
    print()
    demo_leading_zeros()
    print()
    demo_pow_failure()
