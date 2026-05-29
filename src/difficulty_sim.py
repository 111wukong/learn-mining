"""
难度调整机制

比特币每 2016 个区块调整一次难度，目标出块时间 10 分钟。

这个脚本模拟：
- 算力增加 → 出块变快 → 难度上调
- 算力减少 → 出块变慢 → 难度下调
- 难度和出块时间的动态平衡
"""
import random
import statistics
from typing import Optional


class NetworkSimulator:
    """比特币网络难度调整模拟"""

    def __init__(self, initial_hashrate: float, target_block_time: float = 10.0):
        self.hashrate = initial_hashrate  # H/s
        self.target_block_time = target_block_time  # 秒
        self.current_difficulty = 1.0
        self.block_count = 0
        self.blocks_since_adjust = 0
        self.adjust_interval = 2016  # 比特币每 2016 个块调整

        # 统计
        self.block_times: list[float] = []
        self.difficulty_history: list[float] = []

    def mine_one_block(self) -> float:
        """
        模拟挖一个区块
        返回挖出它用了多少秒

        预期时间 = difficulty / hashrate * 2^32
        实际时间加入随机性（因为挖矿本身就是随机的）
        """
        expected = (self.current_difficulty * 2**32) / self.hashrate
        # 指数分布模拟实际挖矿时间
        actual = random.expovariate(1.0 / expected) if expected > 0 else 0
        return actual

    def adjust_difficulty(self):
        """每 adjust_interval 个区块调整难度"""
        if len(self.block_times) < self.adjust_interval:
            return

        recent = self.block_times[-self.adjust_interval :]
        actual_avg = statistics.mean(recent)
        ratio = actual_avg / (self.target_block_time * 60)  # 转为秒
        self.current_difficulty *= self.target_block_time * 60 / actual_avg
        self.current_difficulty = max(0.001, self.current_difficulty)

        self.difficulty_history.append(self.current_difficulty)

    def run(self, total_blocks: int = 10_000, hashrate_changes: Optional[dict] = None):
        """
        运行模拟

        hashrate_changes: {区块数: 新算力} 在指定区块数改变算力
        """
        if hashrate_changes is None:
            hashrate_changes = {}

        for i in range(total_blocks):
            # 检查算力变化
            if i in hashrate_changes:
                old = self.hashrate
                self.hashrate = hashrate_changes[i]
                print(f"  ⚡ 区块 #{i}: 算力变化 {old:,.0f} → {self.hashrate:,.0f} H/s")

            # 挖一个块
            time_taken = self.mine_one_block()
            self.block_times.append(time_taken)
            self.blocks_since_adjust += 1
            self.block_count += 1

            # 调整难度
            if self.blocks_since_adjust >= self.adjust_interval:
                self.adjust_difficulty()
                self.blocks_since_adjust = 0


def demo_difficulty_adjustment():
    print("=" * 60)
    print("📐 难度调整机制")
    print("=" * 60)
    print()

    print("""
    核心公式：新难度 = 旧难度 × (目标出块时间 / 实际平均出块时间)

    如果出块比目标快 → 难度增加
    如果出块比目标慢 → 难度降低

    每 2016 个区块调整一次（约 2 周）
    """)

    # 场景1：算力暴涨
    print("\n📈 场景1：大量矿工加入，算力暴涨 10 倍")
    print("-" * 60)
    sim = NetworkSimulator(initial_hashrate=1_000_000_000)
    sim.adjust_interval = 500  # 缩小区块间隔加快演示
    sim.run(5000, {2000: 10_000_000_000})
    print(f"  初始难度: {sim.difficulty_history[0]:.2f}")
    print(f"  最终难度: {sim.difficulty_history[-1]:.2f}")
    print(f"  难度涨了 {sim.difficulty_history[-1]/sim.difficulty_history[0]:.1f} 倍")
    print(f"  说明：算力涨 10 倍，难度也跟涨 10 倍，维持出块稳定")


def demo_hashrate_vs_probability():
    print("\n\n📊 场景2：你的电脑 vs 全网")
    print("-" * 60)

    your_hashrate = 10_000  # 你的电脑，10 KH/s（已经高估了）
    network_hashrate = 600_000_000_000_000_000_000  # 600 EH/s

    probability = your_hashrate / network_hashrate
    blocks_per_day = 144  # 每天约 144 个区块
    expected_per_year = probability * blocks_per_day * 365

    print(f"  你的算力: {your_hashrate:,} H/s")
    print(f"  全网算力: {network_hashrate:,} H/s ({network_hashrate/1e18:.0f} EH/s)")
    print(f"  你的份额: {probability:.2e}")
    print(f"  预期每年挖到: {expected_per_year:.10f} 个区块")
    print(f"  也就是大约 {1/expected_per_year:,.0f} 年才能挖到一个")
    print()
    print(f"  💀 宇宙的年龄才 138 亿年，你需要等 {1/expected_per_year:,.0f} 年")


def demo_difficulty_history():
    print("\n\n📉 难度历史（真实比特币数据）")
    print("-" * 60)
    print("""
    比特币难度从创世到现在：

    2009年: 难度 1（Satoshi 一个人用 CPU 挖）
    2010年: 难度 ~100（GPU 挖矿兴起）
    2013年: 难度 ~500,000（ASIC 矿机出现）
    2017年: 难度 ~1,000,000,000,000
    2024年: 难度 ~70,000,000,000,000

    难度增长了 70 万亿倍！

    这就是为什么：
    2009年 → 你的笔记本能挖 50 BTC/天
    2024年 → 你的笔记本永远挖不到
    """)


if __name__ == "__main__":
    demo_difficulty_adjustment()
    demo_hashrate_vs_probability()
    demo_difficulty_history()
