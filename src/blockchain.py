"""
迷你区块链 + 挖矿

一条完整的区块链，每个区块通过工作量证明挖出来。
包含：
- 交易池
- 挖矿奖励
- 链验证
- 难度调整
"""
import hashlib
import time
import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float
    fee: float = 0.0
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "fee": self.fee,
            "timestamp": self.timestamp,
        }


@dataclass
class Block:
    index: int
    prev_hash: str
    timestamp: float
    transactions: list[Transaction]
    nonce: int
    difficulty: int
    hash: str = ""

    def compute_hash(self) -> str:
        """计算区块哈希"""
        data = json.dumps(
            {
                "index": self.index,
                "prev_hash": self.prev_hash,
                "timestamp": self.timestamp,
                "transactions": [t.to_dict() for t in self.transactions],
                "nonce": self.nonce,
            },
            sort_keys=True,
        )
        return hashlib.sha256(data.encode()).hexdigest()

    def mine(self, max_nonce: int = 10_000_000) -> bool:
        """挖这个区块"""
        target = "0" * self.difficulty
        for nonce in range(max_nonce):
            self.nonce = nonce
            self.hash = self.compute_hash()
            if self.hash.startswith(target):
                return True
        return False


class Blockchain:
    """
    一条迷你区块链

    和真正的比特币的区别：
    - 难度用前导零简化了（比特币用 target 值比较）
    - 没有 UTXO 模型（用账户余额简化）
    - 没有 P2P 网络
    - 只有一个节点
    但核心逻辑（挖矿 + 链验证 + 难度调整）是一样的
    """

    def __init__(self, difficulty: int = 4):
        self.chain: list[Block] = []
        self.pending_tx: list[Transaction] = []
        self.difficulty = difficulty
        self.mining_reward = 50.0  # 区块奖励（模拟早期比特币）
        self.difficulty_adjust_interval = 5  # 每5个块调整难度
        self.target_block_time = 3.0  # 目标出块时间（秒）
        self._create_genesis()

    def _create_genesis(self):
        """创世区块"""
        genesis = Block(
            index=0,
            prev_hash="0" * 64,
            timestamp=time.time(),
            transactions=[],
            nonce=0,
            difficulty=self.difficulty,
        )
        genesis.mine(max_nonce=5_000_000)
        self.chain.append(genesis)

    def add_transaction(self, tx: Transaction):
        """添加交易到内存池"""
        self.pending_tx.append(tx)
        print(f"📝 交易入池: {tx.sender} → {tx.receiver} {tx.amount} 币")

    def create_coinbase_tx(self, miner_address: str) -> Transaction:
        """创建区块奖励交易（coinbase）"""
        total_fee = sum(tx.fee for tx in self.pending_tx)
        return Transaction(
            sender="COINBASE",
            receiver=miner_address,
            amount=self.mining_reward + total_fee,
            fee=0.0,
        )

    def mine_block(self, miner_address: str, max_tx: int = 5) -> Optional[Block]:
        """
        矿工打包区块

        1. 从交易池选交易（按手续费排序）
        2. 加上 coinbase 交易（奖励自己）
        3. 挖矿（找 nonce）
        4. 链接到链上
        """
        if not self.pending_tx:
            print("⚠️  交易池空的，没有交易可打包")
            return None

        prev = self.chain[-1]

        # 选交易（手续费高的优先）
        txs = sorted(self.pending_tx, key=lambda t: t.fee, reverse=True)[:max_tx]

        # 加上 coinbase
        coinbase = self.create_coinbase_tx(miner_address)
        txs.insert(0, coinbase)

        block = Block(
            index=prev.index + 1,
            prev_hash=prev.hash,
            timestamp=time.time(),
            transactions=txs,
            nonce=0,
            difficulty=self.difficulty,
        )

        print(f"\n⛏️  矿工 {miner_address} 开始挖区块 #{block.index}")
        print(f"   交易数: {len(txs)} | 难度: {self.difficulty} 个前导零")
        start = time.time()

        if block.mine(max_nonce=50_000_000):
            elapsed = time.time() - start
            self.chain.append(block)

            # 从交易池移除已打包的交易
            tx_ids = {t.timestamp for t in block.transactions if t.sender != "COINBASE"}
            self.pending_tx = [t for t in self.pending_tx if t.timestamp not in tx_ids]

            print(f"   🎉 挖到了！nonce={block.nonce}")
            print(f"   ⏱️  耗时 {elapsed:.1f}s | 哈希: {block.hash[:24]}...")
            print(f"   💰 奖励: {coinbase.amount} 币 → {miner_address}")

            # 难度调整
            self._adjust_difficulty()
            return block
        else:
            print("   ❌ 没挖到")
            return None

    def _adjust_difficulty(self):
        """每 N 个区块调整难度"""
        if len(self.chain) % self.difficulty_adjust_interval != 0:
            return

        recent = self.chain[-self.difficulty_adjust_interval :]
        total_time = recent[-1].timestamp - recent[0].timestamp
        avg_time = total_time / self.difficulty_adjust_interval

        old_diff = self.difficulty
        if avg_time < self.target_block_time:
            self.difficulty += 1
            print(f"   📈 难度上调: {old_diff} → {self.difficulty} (出块太快了)")
        elif avg_time > self.target_block_time * 2:
            self.difficulty = max(1, self.difficulty - 1)
            print(f"   📉 难度下调: {old_diff} → {self.difficulty} (出块太慢了)")

    def is_valid(self) -> bool:
        """验证整条链是否有效"""
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # 检查哈希
            if curr.hash != curr.compute_hash():
                print(f"❌ 区块{curr.index}哈希不匹配")
                return False

            # 检查链接
            if curr.prev_hash != prev.hash:
                print(f"❌ 区块{curr.index}前驱哈希断裂")
                return False

            # 检查工作量证明
            target = "0" * curr.difficulty
            if not curr.hash.startswith(target):
                print(f"❌ 区块{curr.index}工作量证明无效")
                return False

        return True

    def get_balance(self, address: str) -> float:
        """计算某个地址的余额"""
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.receiver == address:
                    balance += tx.amount
        return balance


def demo():
    print("=" * 60)
    print("🔗 迷你区块链 + 挖矿演示")
    print("=" * 60)

    chain = Blockchain(difficulty=3)

    chain.add_transaction(Transaction("Alice", "Bob", 10, fee=0.1))
    chain.add_transaction(Transaction("Bob", "Charlie", 5, fee=0.05))
    chain.add_transaction(Transaction("Charlie", "Alice", 3, fee=0.02))

    chain.mine_block("Miner_1")

    chain.add_transaction(Transaction("Alice", "Charlie", 2, fee=0.01))
    chain.mine_block("Miner_1")

    chain.add_transaction(Transaction("Bob", "Alice", 8, fee=0.08))
    chain.mine_block("Miner_2")

    chain.add_transaction(Transaction("Charlie", "Bob", 1, fee=0.01))
    chain.mine_block("Miner_2")

    chain.add_transaction(Transaction("Alice", "Bob", 15, fee=0.2))
    chain.mine_block("Miner_1")

    print()
    print("=" * 60)
    print("📊 链状态")
    print("=" * 60)
    print(f"  区块数: {len(chain.chain)}")
    print(f"  当前难度: {chain.difficulty}")
    print(f"  待处理交易: {len(chain.pending_tx)}")
    print(f"  链有效性: {'✅ 有效' if chain.is_valid() else '❌ 无效'}")
    print()
    print("  🏦 余额:")
    for addr in ["Miner_1", "Miner_2", "Alice", "Bob", "Charlie"]:
        print(f"    {addr}: {chain.get_balance(addr)} 币")


if __name__ == "__main__":
    demo()
