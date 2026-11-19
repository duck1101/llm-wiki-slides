---
type: concept
tags: [vision-language, foundation-model]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation, 2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation, 2022_Can-Language-Understand-Depth, 2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language, 2026_CLIP-Can-Understand-Depth]
updated: 2026-11-19
---

# Vision-Language Model（VLM）

## 定義
- 建立視覺與語言輸入之間連結的模型，例如 [[CLIP]] 以 text-image pair 做 contrastive learning（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §2）。

## 在 MDE 中的應用（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §2）
| 方法 | 作法 |
|---|---|
| [[DepthCLIP]]（[[2022_Can-Language-Understand-Depth\|Zhang et al.]]） | 利用 CLIP 的語意 depth response 與 depth projection，做 zero-shot MDE |
| [[CLIPMDE]]（[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language\|Auty et al.]]） | 以連續的 learnable token 取代離散的人類語言 prompt |
| VPD | 利用預訓練 text-to-image diffusion model 的 embedding |
| TADP | 用 AI 產生的 caption 加強 diffusion-based 模型中 text 與 image 的對應 |
| [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.（WACV 2024）]] | 在 DepthCLIP 上加入 learnable prompt 與依場景的 depth codebook，做 few-shot 調整（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §3） |

- 上述方法都是 implicit modeling；[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] 則明確把 language 建模為 prior（[[Language-Prior]]）（§2）。
- 數值比較：DepthCLIP（zero-shot）在 [[NYU-Depth-V2]] 的 Abs Rel 為 0.388、CLIPMDE 為 0.319，遠落後 supervised 方法（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], Table 1）。

## 語言資訊的三種用法
- **以單一 query 調變影像特徵**：[[2026_CLIP-Can-Understand-Depth|CLIP2Depth]] 把非人類語言的 mirror 經 text encoder 變成一個 query，以 [[FiLM]] 調變 CLIP 影像特徵，再接 decoder（[[2026_CLIP-Can-Understand-Depth]], §3）。
- **以相似度直接預測深度**：[[DepthCLIP]] 與 [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation|Hu et al.]] 以 patch 特徵與深度描述的 text feature 做 cosine similarity，再對 [[Depth-Bins|depth bins]] 加權求和（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §3.5）。
- **作為 prior**：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] 以描述場景的 caption 經 text-VAE 建模為 variational prior，影像再從中選擇（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §3）。

## 相關頁面
[[CLIP]]、[[Language-Prior]]、[[DepthCLIP]]、[[Prompt-Tuning]]
