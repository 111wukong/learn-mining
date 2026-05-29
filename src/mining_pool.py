"""
矿池模拟

个人挖矿 = 买彩票，可能永远挖不到
矿池 = 大家一起买，中奖了按贡献分

这个脚本模拟：
- 多个矿工连接同一个矿池
- 矿池分配任务（给不同矿工不同的 nonce 范围）
- 谁挖到了，矿池按算力分配奖励
- PPLNS（按最后 N 个 share 分配）和 PPS（按 share 固定支付）
"""
import hashlib
import time
import random
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Miner:
    """矿工"""
    name: str
    hashrate: int  # H/s（哈希每秒）
    shares: int = 0  # 提交的有效 share 数
    earned: float = 0.0  # 累计收益


@dataclass
class Share:
    """矿工提交的 share — 证明自己确实在算"""
    miner: str
    block_template: str
    nonce: int
    hash: str
    difficulty: int  # share 难度（比区块难度低）


class MiningPool:
    """
    矿池

    工作原理：
    1. 矿池构造区块模板（不含 nonce）
    2. 分发给所有矿工
    3. 矿工在自己分配的 nonce 范围内尝试
    4. 找到满足 share 难度的哈希 → 提交 share（证明在工作）
    5. 找到满足区块难度的哈希 → 挖出区块，全池分红
    """

    def __init__(self, name: str, block_difficulty: int = 5, share_difficulty: int = 3):
        self.name = name
        self.block_difficulty = block_difficulty
        self.share_difficulty = share_difficulty
        self.miners: dict[str, Miner] = {}
        self.shares: list[Share] = []
        self.total_blocks_mined = 0
        self.block_reward = 50.0

    def add_miner(self, name: str, hashrate: int):
        self.miners[name] = Miner(name=name, hashrate=hashrate)
        print(f"👷 {name} 加入矿池，算力 {hashrate:,} H/s")

    def simulate_mining_round(self, duration_seconds: float = 10.0):
        """模拟一轮挖矿（真实世界一笔带过的时间步长）"""
        target = "0" * self.block_difficulty
        share_target = "0" * self.share_difficulty
        total_hashes = sum(m.hashrate for m in self.miners.values())
        total_shares = 0

        elapsed = 0.0
        found_block = False

        print(f"\n{'='*60}")
        print(f"⛏️  {self.name} 矿池 — 本轮挖矿（{duration_seconds}秒）")
        print(f"{'='*60}")
        print(f"  矿工数: {len(self.miners)} | 总算力: {total_hashes:,} H/s")
        print(f"  区块难度: {self.block_difficulty} | Share难度: {self.share_difficulty}")
        print()

        # 给每个矿工分配 nonce 起始位置
        nonces = {name: random.randint(0, 1_000_000_000) for name in self.miners}
        step = 0.1  # 每 100ms 一个时间步

        while elapsed < duration_seconds:
            for name, miner in self.miners.items():
                # 这个时间步内算了多少哈希
                hashes_this_step = int(miner.hashrate * step)

                for _ in range(hashes_this_step):
                    nonces[name] += 1
                    h = hashlib.sha256(
                        f"block_template|{name}|{nonces[name]}".encode()
                    ).hexdigest()

                    # 找到 share
                    if h.startswith(share_target):
                        total_shares += 1
                        miner.shares += 1
                        self.shares.append(
                            Share(
                                miner=name,
                                block_template="block_template",
                                nonce=nonces[name],
                                hash=h,
                                difficulty=self.share_difficulty,
                            )
                        )
                        break  # 这个时间步内一个矿工最多一个 share

                    # 找到完整区块
                    if h.startswith(target):
                        self.total_blocks_mined += 1
                        self._distribute_reward(h)
                        found_block = True
                        break

            elapsed += step

        print(f"  📊 本轮统计:")
        print(f"    总算力: {total_hashes:,} H/s")
        print(f"    Share数: {total_shares}")
        for name, miner in self.miners.items():
            print(f"    {name}: {miner.shares} shares, {miner.earned:.2f} 币")
        print(f"    挖到区块: {'🎉 是！' if found_block else '❌ 否'}")

    def _distribute_reward(self, block_hash: str):
        """找到区块，按 share 数分红"""
        total_shares = sum(m.shares for m in self.miners.values())
        if total_shares == 0:
            return

        for miner in self.miners.values():
            share_pct = miner.shares / total_shares
            reward = self.block_reward * share_pct
            miner.earned += reward

        print(f"  🎉 挖到区块！{block_hash[:16]}...")
        print(f"  💰 奖励 {self.block_reward} 币按贡献分配")

    def pool_stats(self):
        """矿池统计"""
        print(f"\n{'='*60}")
        print(f"📊 {self.name} 矿池总览")
        print(f"{'='*60}")
        print(f"  挖出区块: {self.total_blocks_mined}")
        print(f"  总 Shares: {len(self.shares)}")
        total_earned = sum(m.earned for m in self.miners.values())
        print(f"  总发币: {total_earned:.2f}")
        print()
        for miner in sorted(self.miners.values(), key=lambda m: m.earned, reverse=True):
            pct = miner.shares / len(self.shares) * 100 if self.shares else 0
            print(f"  {miner.name:12s} | {miner.hashrate:>8,} H/s | "
                  f"{miner.shares:>4} shares({pct:>5.1f}%) | 收益{miner.earned:>8.2f} 币")


def real_world_context():
    """现实对比 — 为什么你挖不了"""
    print("=" * 60)
    print("🌍 现实对照：为什么你的电脑挖不了")
    print("=" * 60)
    print()

    # 比特币全网算力（2024年真实数据）
    print("  比特币全网算力: ~600,000,000,000,000,000,000 H/s (600 EH/s)")
    print("  你的 MacBook Air: ~100 H/s (Python) / ~10,000 H/s (C/ASIC 软件)")
    print()
    print("  如果全网是一个巨大的矿池，你加入它：")
    print(f"  你的份额 ≈ 0%")
    print()
    print("  比特币实际使用 SHA-256 ASIC 矿机，算力以 TH/s 计")
    print("  一台 Antminer S19 ≈ 110,000,000,000,000 H/s = 你电脑的 10 亿倍")
    print()
    print("  💡 结论：个人电脑挖 BTC 不是慢，是概率为零")


if __name__ == "__main__":
    pool = MiningPool("龙虾矿池🦞", block_difficulty=4, share_difficulty=2)

    pool.add_miner("你的MacBook", 100)
    pool.add_miner("一台游戏本", 500)
    pool.add_miner("RTX4090", 5000)
    pool.add_miner("Antminer S19", 100000)

    pool.simulate_mining_round(duration_seconds=15)
    pool.pool_stats()

    print()
    real_world_context()
