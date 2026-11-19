---
type: entity
tags: [dataset, indoor, zero-shot]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation, 2026_CLIP-Can-Understand-Depth]
updated: 2026-11-19
---

# SUN RGB-D

- 類型：室內 RGB-D 資料集
- 常見用途：在 [[NYU-Depth-V2]] 訓練後，不 fine-tune 直接測試，評估 zero-shot generalization（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §4）

## 各論文結果（train on NYUv2, zero-shot）
| 論文 | Abs Rel | δ<1.25 | RMSE | 出處 |
|---|---|---|---|---|
| [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation\|WorDepth]] | 0.123 | 0.833 | 0.376 | Table 4 |
| [[2026_CLIP-Can-Understand-Depth\|CLIP2Depth]] | 0.431 | 0.627 | 0.535 | Table 6 |

- [[2026_CLIP-Can-Understand-Depth|CLIP2Depth]] 只用官方測試集 5,050 張；影像 730 × 530、47 類室內場景（§4.1.1）。WorDepth 的結果未列在 CLIP2Depth 的比較表中，兩篇評估流程可能不同（補充）。

## 相關頁面
[[NYU-Depth-V2]]
