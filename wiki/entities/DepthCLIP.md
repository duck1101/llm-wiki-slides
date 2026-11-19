---
type: entity
tags: [model, mde, zero-shot, vision-language]
sources: [2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation, 2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation, 2022_Can-Language-Understand-Depth, 2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language, 2026_CLIP-Can-Understand-Depth]
updated: 2026-11-19
---

# DepthCLIP

- 類型：以 [[CLIP]] 做 zero-shot MDE 的方法
- 原始論文：[[2022_Can-Language-Understand-Depth]]（ACM MM 2022）
- 作法：
  - 影像 patch 與一組深度描述的 text feature 計算相似度，再與人工設定的深度值加權求和（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §1）。
  - Prompt 為「This object is [Depth CLASS]」，[Depth CLASS] 共 7 類：giant、extremely close、close、not in distance、a little remote、far、unseen（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §3.3）。
  - 利用 CLIP 的語意 depth response 與 depth projection，做 zero-shot 遷移（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §2）。
- 限制：深度描述對應的深度值固定，難以適應不同場景的深度分布（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §1）。

- 設定：7 個距離詞對應 1.00～3.00 m 的固定深度值，softmax temperature 0.1，CLIP ResNet-50（[[2022_Can-Language-Understand-Depth]], §4.2）。

## 後續延伸
- [[CLIPMDE]]（Auty et al.）：以 learnable depth token 取代人類距離詞，指出人工選詞帶來 human bias（[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]], §1, §3）。
- [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation|Hu et al.（WACV 2024）]]：加入 learnable prompt 與依場景的 depth codebook，做 few-shot 調整。

- [[2026_CLIP-Can-Understand-Depth|CLIP2Depth]]：以非人類語言的 mirror 與輕量 decoder 取代距離詞與 depth bins（[[2026_CLIP-Can-Understand-Depth]], §3）。

## 各論文報告的結果
| 資料集 | δ<1.25 | Abs Rel（MARE） | RMSE | 出處 |
|---|---|---|---|---|
| [[NYU-Depth-V2]] | 0.394 | 0.388 | 1.167 | [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]] Table 1；[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]] Table 1 |
| [[KITTI]] | 0.281 | 0.473 | 12.958 | [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]] Table 2（depth bin 經作者手動調整） |

- 兩篇論文在 NYU V2 的數值一致。
- [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]] 的 Table 5 中 DepthCLIP 的 NYU V2 RMSE 為 1.147，與同篇 Table 1 的 1.167 不同。

## 相關頁面
[[Vision-Language-Model]]、[[Depth-Bins]]、[[Prompt-Tuning]]
