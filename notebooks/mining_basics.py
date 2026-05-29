"""
交互式挖矿教程 — 从零到理解

一步一步带你理解挖矿，每步都有代码演示。
适合 Python 初学者。
"""
import hashlib
import time
import random


def step1_what_is_hash():
    """第1步：什么是哈希"""
    print("=" * 60)
    print("📖 第1步：哈希函数 — 数据的指纹")
    print("=" * 60)
    print()
    print("哈希是一个单向函数：输入 → 固定长度输出")
    print("同样的输入永远产生同样的输出")
    print("改了输入的一个比特，输出就完全不同")
    print()

    # 手把手演法
    data = "hello bitcoin"
    h = hashlib.sha256(data.encode()).hexdigest()
    print(f'  SHA-256("{data}") = {h}')

    data2 = "hello Bitcoin"
    h2 = hashlib.sha256(data2.encode()).hexdigest()
    print(f'  SHA-256("{data2}") = {h2}')
    print(f'  只改了一个字母，结果完全不同！')

    input("\n按回车继续...")


def step2_what_is_mining():
    """第2步：挖矿到底是什么"""
    print("\n" + "=" * 60)
    print("📖 第2步：挖矿 = 暴力猜 nonce")
    print("=" * 60)
    print()
    print("矿工做的事情：")
    print("  1. 拿到区块数据")
    print("  2. nonce 从 0 开始一直加")
    print("  3. 对「区块 + nonce」做哈希")
    print("  4. 如果哈希前 N 位是 0 → 挖到了！")
    print("  5. 如果不是 → nonce++，回到步骤 3")
    print()
    print("这就是'工作' — 你说你干了活，哈希为证，无法伪造。")

    # 演示
    target_zeros = 3
    nonce = 0
    block = "block_data_xyz"
    start = time.time()

    while True:
        guess = hashlib.sha256(f"{block}|{nonce}".encode()).hexdigest()
        if guess.startswith("0" * target_zeros):
            break
        nonce += 1

    print(f"\n  🎯 演示：前{target_zeros}个零")
    print(f"  试了 {nonce} 次才找到 nonce={nonce}")
    print(f"  哈希: {guess}")
    print(f"  耗时: {time.time()-start:.3f}秒")
    print()
    print("  💡 每多一个前导零，难度×16。4个零 ≈ 65,536次。6个零 ≈ 16,777,216次。")

    input("\n按回车继续...")


def step3_proof_of_work():
    """第3步：工作量证明的意义"""
    print("\n" + "=" * 60)
    print("📖 第3步：为什么需要工作？")
    print("=" * 60)
    print()
    print("工作量证明解决了三个问题：")
    print()
    print("  1. 防女巫攻击：创建身份需要成本（算力），无法批量伪造")
    print("  2. 共识机制：最长链 = 最多工作量 = 大家公认的真相")
    print("  3. 不可逆：改了历史区块就要重算它之后的所有区块")
    print()
    print("简单说：用数学（而不是信任）保证没人能作弊。")

    input("\n按回车继续...")


def step4_block_reward():
    """第4步：区块奖励"""
    print("\n" + "=" * 60)
    print("📖 第4步：矿工为啥要挖 — 区块奖励")
    print("=" * 60)
    print()
    print("两个收入来源：")
    print("  1. 区块奖励（Block Subsidy）：系统白送的币")
    print("  2. 交易手续费（Transaction Fees）：用户付的")
    print()
    print("比特币区块奖励每 21 万个块（约4年）减半：")
    print("  2009: 50 BTC/块")
    print("  2012: 25 BTC/块")
    print("  2016: 12.5 BTC/块")
    print("  2020: 6.25 BTC/块")
    print("  2024: 3.125 BTC/块")
    print("  ...")
    print("  2140年: 趋近于零，矿工只靠手续费")
    print()
    print("这就是 2100 万总量上限的来源。")

    input("\n按回车继续...")


def step5_mining_pool():
    """第5步：矿池"""
    print("\n" + "=" * 60)
    print("📖 第5步：矿池 — 打工人团结起来")
    print("=" * 60)
    print()
    print("问题：个人挖矿跟买彩票一样，可能一辈子挖不到")
    print("解法：矿工组团，挖到按贡献分")
    print()
    print("矿池工作流程：")
    print("  1. 矿池服务器组好区块模板")
    print("  2. 发给所有矿工：'你的 nonce 范围是 X~Y'")
    print("  3. 矿工在自己范围内试")
    print("  4. 找到低难度哈希 → 提交 share（证明在工作）")
    print("  5. 找到高难度哈希 → 挖到区块，按 share 数分红")
    print()
    print("分配方式：")
    print("  PPS: 每个 share 固定收益，稳但少")
    print("  PPLNS: 挖到块时按最后 N 个 share 分，波动大")
    print("  FPPS: PPS + 交易手续费分成")

    input("\n按回车继续...")


def step6_energy_debate():
    """第6步：能源争议"""
    print("\n" + "=" * 60)
    print("📖 第6步：能源争议")
    print("=" * 60)
    print()
    print("比特币每年耗电 ≈ 阿根廷全国用电量")
    print()
    print("反对者说：浪费电，破坏环境")
    print("支持者说：")
    print("  - 消耗的多是弃电（水电过剩、天然气伴生）")
    print("  - 激励可再生能源建设")
    print("  - 银行系统 + 黄金开采也耗能")
    print("  - 换来的是一条无需信任的全球支付网络")
    print()
    print("这个问题没有标准答案，两边的数据都能找到。")

    input("\n按回车继续...")


def step7_final_quiz():
    """第7步：小测验"""
    print("\n" + "=" * 60)
    print("📝 小测验")
    print("=" * 60)

    questions = [
        {
            "q": "挖矿本质上是在做什么？",
            "a": "暴力尝试 nonce，找到满足前导零条件的哈希",
        },
        {
            "q": "为什么不能伪造挖矿结果？",
            "a": "因为哈希无法逆推，只能靠暴力计算，他人可轻易验证",
        },
        {
            "q": "你的 MacBook Air 能挖比特币吗？",
            "a": "技术上能，但概率约等于零。全网算力是你的 10^16 倍",
        },
        {
            "q": "矿池是什么？",
            "a": "矿工组团挖矿，按贡献分红，平滑收益",
        },
    ]

    for i, q in enumerate(questions, 1):
        print(f"\n  {i}. {q['q']}")
        input("  你的答案（按回车看答案）: ")
        print(f"  👉 {q['a']}")

    print(f"\n{'='*60}")
    print("🎓 恭喜！你已经理解了挖矿的基本原理。")
    print()
    print("接下来可以跑其他模块：")
    print("  python src/pow_miner.py     — 亲手挖一个区块")
    print("  python src/blockchain.py    — 跑一条完整区块链")
    print("  python src/mining_pool.py   — 矿池分红模拟")
    print("  python src/difficulty_sim.py — 难度调整机制")


if __name__ == "__main__":
    print("🦞 欢迎来到龙虾挖矿学院！")
    print()
    step1_what_is_hash()
    step2_what_is_mining()
    step3_proof_of_work()
    step4_block_reward()
    step5_mining_pool()
    step6_energy_debate()
    step7_final_quiz()
