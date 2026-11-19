---
type: entity
tags: [model, backbone, transformer]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# Swin Transformer

- 類型：hierarchical vision transformer backbone，以 shifted window 計算 self-attention（補充）
- MDE 中常用 **Swin-L**（large 版），NeWCRFs、DepthFormer 等方法皆採用（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], Table 1–2）

## 在 MDE 論文中的用法
| 論文 | 用法 | 出處 |
|---|---|---|
| [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation\|WorDepth]] | Swin-L（ImageNet 預訓練）作為 image-based conditional sampler 的 encoder；選用原因是利用其 token 的 locality 做 patch-wise 取樣 | §3.2, §4 |

## 相關頁面
[[AdaBins]]
