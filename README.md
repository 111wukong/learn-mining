# ⛏️ Learn Mining — 从零理解加密货币挖矿

> 一套 Jupyter Notebook 教程，从 SHA-256 讲到 51% 攻击，从区块结构讲到矿池协议。
> 纯技术学习项目，不讲炒币，只讲原理。

## 🎓 课程架构（8 课）

| # | Notebook | 内容 |
|---|----------|------|
| 01 | `01_hash_crypto.ipynb` | SHA-256、RIPEMD-160、Base58Check、ECDSA、雪崩效应 |
| 02 | `02_proof_of_work.ipynb` | nBits 编码、难度计算、Poisson 过程、Nonce 空间 |
| 03 | `03_block_merkle.ipynb` | 80 字节区块头、Merkle Tree、Merkle Proof、链结构 |
| 04 | `04_mining_sim.ipynb` | 完整矿工模拟器、亲手挖一个区块 |
| 05 | `05_mining_pool.ipynb` | Stratum 协议、Share 机制、PPS/PPLNS 分红 |
| 06 | `06_difficulty.ipynb` | 每 2016 块难度调整算法、±4x 限制、历史趋势 |
| 07 | `07_economics_attacks.ipynb` | 盈亏模型、51% 攻击模拟、自私挖矿、MEV |
| 08 | `08_real_data.ipynb` | 硬件进化史、算力分布、能源争议、比特币的未来 |

### 学习路线

```
密码学基础 → 工作量证明 → 区块结构 → 挖矿模拟
      ↓
  矿池协议 → 难度调整 → 经济学&攻击 → 真实数据
```

## 🚀 快速开始

```bash
git clone https://github.com/111wukong/learn-mining.git
cd learn-mining
pip install jupyter matplotlib numpy
jupyter notebook
```

然后在浏览器中按顺序打开 `notebooks/01_hash_crypto.ipynb` 开始。

## 🔧 技术栈

- **Python 3** — 全部纯 Python，无外部区块链依赖
- **Jupyter Notebook** — 交互式教学
- **matplotlib + numpy** — 可视化和数据分析

## 📖 核心概念速览

| 概念 | 一句话 |
|------|--------|
| **哈希** | 任意数据 → 固定长度指纹，单向不可逆 |
| **工作量证明** | 故意制造计算成本，证明付出 |
| **挖矿** | 暴力试 nonce 找满足前导零的哈希 |
| **难度** | 哈希小于某个值才算数，全网每 2016 块自动调整 |
| **矿池** | 矿工抱团平滑收益 |
| **Merkle Tree** | 用 O(log n) 空间证明交易在区块中 |
| **51% 攻击** | 控制过半算力可双花，但 BTC 上经济不可行 |

## ⚠️ 免责声明

本项目仅用于**教育目的**。不构成投资建议，不建议也不鼓励加密货币交易或挖矿。

## 📚 推荐阅读

- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf) — 中本聪原文，只有 9 页
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook) — O'Reilly 免费开源书
- [3Blue1Brown - But how does bitcoin actually work?](https://youtu.be/bBC-nXj3Ng4)
- [Mempool.space](https://mempool.space/) — 实时区块链浏览器
- [Learn Me A Bitcoin](https://learnmeabitcoin.com/) — 交互式学习
