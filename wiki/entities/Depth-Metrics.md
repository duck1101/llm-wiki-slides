---
type: entity
tags: [metric, evaluation]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation, 2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# Depth Metrics（深度估計評估指標）

MDE 常用的評估指標（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §4）。論文正文未列公式（放在 Supp. Mat.），以下公式為補充。

| 指標 | 方向 | 定義（補充） | 直覺 |
|---|---|---|---|
| Abs Rel | ↓ | mean( \|y − y*\| / y* ) | 平均相對誤差 |
| RMSE | ↓ | sqrt( mean( (y − y*)² ) ) | 以公尺計的誤差，對大誤差敏感 |
| log10 | ↓ | mean( \|log10 y − log10 y*\| ) | log 空間的絕對誤差 |
| RMSElog | ↓ | sqrt( mean( (log y − log y*)² ) ) | log 空間的 RMSE |
| δ < 1.25ⁱ | ↑ | max(y/y*, y*/y) < 1.25ⁱ 的像素比例，i = 1, 2, 3 | 預測落在 ground truth 一定倍數內的比例 |

## 不同論文的指標名稱
| 本頁名稱 | [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.]] 的名稱 |
|---|---|
| Abs Rel | MARE（mean absolute relative error） |
| Sq Rel（補充） | MSRE（mean squared relative error） |
| log10 | AELS（absolute error in log space） |
| RMSE | RMSE |

- 注意：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation|Hu et al.]] 的 Eq. 13–14 中，MARE 的分子有平方、MSRE 沒有，與名稱相反，疑似公式對調（§4.3）。

## 解讀
- δ<1.25 對 scale 偏差敏感：形狀正確但 scale 偏離時，δ<1.25 會偏低（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §4）。
- 慣例（補充）：[[NYU-Depth-V2]] 多報 log10，[[KITTI]] 多報 RMSElog。

## 相關頁面
[[Scale-Ambiguity]]、[[Scale-Invariant-Loss]]
