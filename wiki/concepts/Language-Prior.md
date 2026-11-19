---
type: concept
tags: [mde, prior, vision-language]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# Language Prior（語言先驗）

## 定義
- 以描述場景的文字作為深度估計的 prior。文字與語意、物體形狀（與功能）密切相關，可提供場景 scale 的線索（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §1–2）。
- 文字本身也有歧義：同一段描述對應無限多種 layout 與物體形狀，但場景 scale 與其中物體的典型大小相關（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §1, Fig. 1）。

## 與其他 prior 的比較（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §1, §5）
| Prior 類型 | 例子 | 優點 | 缺點 |
|---|---|---|---|
| Generic prior | local smoothness、connectivity、object orientation | 適用多數場景，通常不太造成傷害 | 缺乏特定場景資訊，增益小 |
| Specific prior | 針對相機參數的架構設計、物體形狀集合 | 增益可能較大 | 假設不成立時會失效，應用受限 |
| Language prior | 「A bedroom with a bed and a table」 | 介於兩者之間：對場景具體，但不假設相機或形狀 | 正則化程度由 caption 的具體程度決定 |

## 建模方式
- Implicit：DepthCLIP、CLIPMDE、VPD 等透過 [[Vision-Language-Model]] 的特徵隱式使用語言（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §2）。
- Explicit / variational：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] 以 text-VAE 把 caption 編碼成 latent 分布（[[Variational-Autoencoder]]），再由影像選擇（§3）。

## 已知風險（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §5）
- 模糊的 caption 幾乎沒有幫助；具體但錯誤的 caption 會誤導預測。
- 依賴 captioner 品質；可能被惡意 caption 操控。

## 相關頁面
[[Scale-Ambiguity]]、[[Vision-Language-Model]]、[[CLIP]]
