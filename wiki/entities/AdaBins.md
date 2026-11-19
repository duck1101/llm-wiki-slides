---
type: entity
tags: [model, mde, supervised]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# AdaBins

- 論文：Bhat et al., "AdaBins: Depth Estimation Using Adaptive Bins", CVPR 2021（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], ref. [2]）
- 作法：以 transformer block 把深度範圍切成 adaptive bins（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §2）
- Backbone：EffNet-B5 + ViT-mini（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], Table 1）

## 作為比較對象的結果
| 資料集 | Abs Rel | δ<1.25 | RMSE | 出處 |
|---|---|---|---|---|
| [[NYU-Depth-V2]] | 0.103 | 0.903 | 0.364 | [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], Table 1 |
| [[KITTI]] | 0.058 | 0.964 | 2.360 | [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], Table 2 |
| [[SUN-RGBD]]（zero-shot） | 0.159 | 0.771 | 0.476 | [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], Table 4 |

- [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] 以 AdaBins 作為定性比較的 baseline（Fig. 3–4）。

## 相關頁面
[[Swin-Transformer]]、[[Depth-Metrics]]
