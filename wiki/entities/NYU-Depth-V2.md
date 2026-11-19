---
type: entity
tags: [dataset, indoor]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation, 2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation, 2022_Can-Language-Understand-Depth, 2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language, 2026_CLIP-Can-Understand-Depth]
updated: 2026-11-19
---

# NYU Depth V2

- 類型：室內 RGB-D 資料集
- 影像大小 480×640，深度範圍 1×10⁻³～10 m（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §4）
- 常用切分：依 Lee et al.（Big to Small）的切分，24,231 張訓練、654 張測試（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §4）
- 常用指標：δ<1.25、Abs Rel、log10、RMSE（[[Depth-Metrics]]）

## 各論文結果（Abs Rel ↓）
| 論文 | Abs Rel | δ<1.25 | RMSE | 出處 |
|---|---|---|---|---|
| [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation\|WorDepth]] | 0.088 | 0.932 | 0.317 | Table 1 |
| [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.]]（1-shot） | 0.347 | 0.428 | 1.049 | Table 1 |
| [[2026_CLIP-Can-Understand-Depth\|CLIP2Depth]] | 0.100 | 0.900 | 0.379 | Table 3 |
| [[CLIPMDE]]（learned-7） | 0.319 | 0.465 | 0.970 | [[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]] Table 3 |
| [[DepthCLIP]]（0-shot） | 0.388 | 0.394 | 1.167 | [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]] Table 1；[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]] Table 1 ；[[2022_Can-Language-Understand-Depth]] Table 1 |

## 跨論文差異
- [[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language|CLIPMDE 論文]] 使用 AdaBins 的切分（訓練 24231 張、測試 654 張），訓練時隨機裁切 416 × 544（§4.1.2）。
- **CLIPMDE 的 log10**：WorDepth Table 1 列 0.139，原論文的 log10 為 0.128（0.139 是 RMSL）。
- **資料描述**：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] 寫 24,231 張訓練、654 張測試（§4）；[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation|Hu et al.]] 寫訓練集 36,253 張（249 個場景）、測試 654 張（215 個場景），並裁切為 416 × 512（§4.1）。測試集張數一致。
- [[2022_Can-Language-Understand-Depth|DepthCLIP 論文]]的資料描述與 Hu et al. 相同（訓練 36,253 張、測試 654 張，裁切 416 × 512）（§4.1）。
- **DepthFormer 的數值不同**：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] Table 1 為 δ<1.25 0.923、Abs Rel 0.094、RMSE 0.329；[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation|Hu et al.]] Table 1 與 [[2022_Can-Language-Understand-Depth|DepthCLIP 論文]] Table 1 皆為 0.921、0.096、0.339。
- Few-shot 設定：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation|Hu et al.]] 從 27 個場景類別各取 1 張訓練（§4.2）。

## 相關頁面
[[KITTI]]、[[SUN-RGBD]]
