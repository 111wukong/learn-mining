"""
工作量证明（Proof of Work）— 挖矿的核心算法

矿工做的事情：
1. 拿到区块数据（交易列表 + 前一区块哈希）
2. 暴力尝试不同的 nonce（从 0 一直加）
3. 对「区块头 + nonce」做哈希
4. 看结果有没有足够的前导零
5. 没有就 nonce++，继续试
6. 找到了就广播：我挖到了！

这就叫「工作」— 烧算力，无法作弊，无法跳过。
"""
import hashlib
import time
import struct
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BlockHeader:
    """模拟比特币区块头结构"""
    version: int = 1
    prev_hash: str = ""       # 前一区块哈希
    merkle_root: str = ""     # 交易默克尔根
    timestamp: int = 0        # 时间戳
    bits: int = 0             # 难度目标（压缩格式）
    nonce: int = 0            # 随机数，矿工不断改这个


def double_sha256(data: bytes) -> str:
    """比特币实际使用的是双重 SHA-256"""
    return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()


def bits_to_target(bits: int) -> int:
    """
    把压缩格式的 bits 转成难度目标值
    模拟比特币的难度编码
    bits = 0x1d00ffff → 目标值 0x00000000FFFF...
    """
    exponent = bits >> 24
    coefficient = bits & 0x00ffffff
    return coefficient << (8 * (exponent - 3))


def header_to_bytes(header: BlockHeader) -> bytes:
    """把区块头序列化为字节，用于哈希计算"""
    return struct.pack(
        "<I", header.version
    ) + bytes.fromhex(header.prev_hash) + bytes.fromhex(header.merkle_root) + struct.pack(
        "<I", header.timestamp
    ) + struct.pack("<I", header.bits) + struct.pack("<I", header.nonce)


def validate_pow(header: BlockHeader) -> bool:
    """验证一个区块的工作量证明是否有效"""
    target = bits_to_target(header.bits)
    block_hash = int(double_sha256(header_to_bytes(header)), 16)
    return block_hash < target


def mine_block(header: BlockHeader, max_nonce: int = 10_000_000) -> Optional[BlockHeader]:
    """
    模拟挖矿过程 — 暴力搜索 nonce

    说实话这就是个 for 循环 + 判断，但你写过的那些保险数据
    处理脚本比这复杂多了😏
    """
    target = bits_to_target(header.bits)
    target_hex = hex(target)[2:].zfill(64)

    print(f"⛏️  开始挖矿...")
    print(f"   区块哈希目标: < {target_hex[:16]}...")
    print(f"   搜索空间: 0 ~ {max_nonce:,}")
    print()

    start = time.time()
    hashes_done = 0
    last_report = start

    for nonce in range(max_nonce):
        header.nonce = nonce
        block_hash_bytes = hashlib.sha256(
            hashlib.sha256(header_to_bytes(header)).digest()
        ).digest()
        block_hash_int = int.from_bytes(block_hash_bytes, "big")
        hashes_done += 1

        # 每秒报告一次进度
        now = time.time()
        if now - last_report >= 1:
            elapsed = now - start
            hps = hashes_done / elapsed if elapsed > 0 else 0
            print(f"  进度: {nonce:>10,} nonce | 算力: {hps:>8,.0f} H/s | "
                  f"耗时: {elapsed:>6.1f}s", end="\r")
            last_report = now

        if block_hash_int < target:
            elapsed = time.time() - start
            print(f"\n\n🎉 找到有效 nonce: {nonce}")
            print(f"   区块哈希: {block_hash_bytes.hex()}")
            print(f"   尝试次数: {hashes_done:,}")
            print(f"   耗时: {elapsed:.1f} 秒")
            print(f"   实际算力: {hashes_done / elapsed:,.0f} H/s")
            return header

    print(f"\n❌ 没找到，超过 {max_nonce:,} 次尝试")
    return None


def simulate_mining():
    """完整演示"""
    import random

    # 模拟一些交易数据
    transactions = [
        f"tx_{i}: {random.randint(1, 100)} coins" for i in range(4)
    ]

    # 构造默克尔根（简化：直接把交易拼起来哈希）
    tx_data = "|".join(transactions)
    merkle_root = hashlib.sha256(tx_data.encode()).hexdigest()

    # 区块头
    header = BlockHeader(
        version=1,
        prev_hash="0" * 64,
        merkle_root=merkle_root,
        timestamp=int(time.time()),
        bits=0x1f00ffff,  # 这个难度对于 Python 来说很快能找到
        nonce=0,
    )

    print("=" * 60)
    print("⛏️  Proof of Work 挖矿模拟")
    print("=" * 60)
    print(f"  前一区块: {header.prev_hash[:16]}...")
    print(f"  默克尔根: {header.merkle_root[:16]}...")
    print(f"  交易数量: {len(transactions)}")
    print()

    result = mine_block(header, max_nonce=50_000_000)

    if result:
        print(f"\n✅ 验证结果: {'通过' if validate_pow(result) else '失败'}")

    return result


def explain_difficulty():
    """直观解释难度和工作量"""
    print("=" * 60)
    print("📖 难度直观理解")
    print("=" * 60)
    print()

    for bits, name in [
        (0x1d00ffff, "比特币创世区块难度"),
        (0x1f00ffff, "极简演示难度"),
        (0x1e00ffff, "容易难度"),
    ]:
        target = bits_to_target(bits)
        # 已 target 出现的概率 = target / 2^256
        prob = target / (2**256)
        avg_tries = int((2**256) / target)
        print(f"  {name}: 概率≈ {prob:.2e}")
        print(f"     平均需要 {avg_tries:,} 次哈希才能找到")
        print()


if __name__ == "__main__":
    simulate_mining()
    print()
    explain_difficulty()
