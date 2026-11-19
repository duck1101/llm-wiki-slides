---
type: entity
tags: [dataset, outdoor, driving]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation, 2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation, 2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language, 2026_CLIP-Can-Understand-Depth]
updated: 2026-11-19
---

# KITTI

- 類型：室外自駕場景資料集（Geiger et al., CVPR 2012）
- 影像大小 352×1216，深度範圍 1×10⁻³～80 m（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §4）
- 常用切分：**Eigen split**，23,488 張訓練、697 張測試；清除無有效 ground truth 的樣本後剩 652 張（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §4）
- 常用指標：δ<1.25、Abs Rel、RMSElog、RMSE（[[Depth-Metrics]]）

## 各論文結果
| 論文 | Abs Rel | δ<1.25 | RMSE | 出處 |
|---|---|---|---|---|
| [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation\|WorDepth]] | 0.049 | 0.979 | 2.039 | Table 2 |
| [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.]]（1-shot） | 0.384 | 0.312 | 12.290 | Table 2 |
| [[2026_CLIP-Can-Understand-Depth\|CLIP2Depth]] | 0.074 | 0.938 | 2.948 | Table 4 |
| [[CLIPMDE]]（learned-7） | 0.303 | 0.550 | 6.322 | [[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]] Table 3 |
| [[DepthCLIP]]（0-shot） | 0.473 | 0.281 | 12.958 | [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]] Table 2 |

## 備註
- 室外同一類物體（例如 car）的大小、形狀差異大，language prior 在 KITTI 的 δ<1.25 增益小於 NYUv2（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §4）。

- [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation|Hu et al.]] 採用 ASTransformer 的切分：訓練 23,488 張、測試 697 張，影像裁切為 352 × 704，深度範圍 0～80 m（§4.1, Table 2）。

- [[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language|CLIPMDE 論文]] 使用 23157 張訓練、696 張測試，切分取自 AdaBins（§4.1.2）。

- **log10 與 RMSElog 混用**：[[2026_CLIP-Can-Understand-Depth|CLIP2Depth]] Table 4 的 log10 欄中，DORN、DepthFormer、NeWCRFs 的數值與 WorDepth Table 2 的 RMSElog 相同（補充）。

## 相關頁面
[[NYU-Depth-V2]]
