---
type: concept
tags: [learning-setting, few-shot]
sources: [2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# Few-Shot Learning

## 定義
- 只用少量有標註的樣本調整預訓練模型，以適應下游任務（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §1）。
- 在 MDE 中的定位：介於 fully-supervised（需要大量標註、訓練耗時）與 zero-shot（不需訓練，但泛化有限）之間（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §1）。

## 在 MDE 論文中的用法
| 論文 | 設定 | 訓練資料量 | 更新的參數 | 出處 |
|---|---|---|---|---|
| [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.（WACV 2024）]] | 1-shot：每個場景類別 1 張影像 | NYU V2 27 張 | learnable prompt + depth codebook，共 8K 參數 | §4.2, Table 5 |

## 與其他設定的比較（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], Table 5）
| 設定 | 例子 | 訓練時間 | 參數量 | NYU V2 RMSE |
|---|---|---|---|---|
| Fully-supervised | DORN | > 30 h | 51M | 0.509 |
| Zero-shot | [[DepthCLIP]] | 0 | 0 | 1.147 |
| Few-shot | [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.]] | 70 min | 8K | 1.049 |

（DepthCLIP 的 RMSE 在同一篇論文 Table 1 為 1.167，見 [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#論文內的不一致]]。）

## 相關頁面
[[Prompt-Tuning]]、[[DepthCLIP]]
