---
type: entity
tags: [model, vision-language, foundation-model]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation, 2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation, 2022_Can-Language-Understand-Depth, 2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language, 2026_CLIP-Can-Understand-Depth]
updated: 2026-11-19
---

# CLIP

- 類型：[[Vision-Language-Model]]，以 text-image pair 做 contrastive learning，提供 vision 與 text 共享的 latent space（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §2, §3.1）
- 原始論文：Radford et al., 2021（補充）
- 預訓練資料：4 億組 image-text pair（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §1, §3.1）

## 在 MDE 論文中的用法
| 論文 | 用法 | 出處 |
|---|---|---|
| [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation\|WorDepth]] | ResNet-50 版 text encoder（輸出 1024 維特徵），全程 frozen，作為 text-VAE 的前端 | §3.1, §4 |
| [[DepthCLIP]] | ResNet-50 版 image 與 text encoder，image encoder 去掉 pooling 取 patch 特徵；完全不訓練 | [[2022_Can-Language-Understand-Depth]], §3.1, §4.2 |
| [[DepthCLIP]]（WorDepth 的描述） | 利用 CLIP 的語意 depth response 做 zero-shot MDE | [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §2 |
| [[CLIPMDE]] | ResNet-50 版，image 與 text encoder 皆 frozen，只學 prompt 中的 depth token；作者認為 ResNet 版比 ViT 版更能抽出空間特徵 | [[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]], §3, §4.1 |
| [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.]] | ResNet-50 版的 text encoder、scene encoder（image encoder）與去掉 pooling 的 visual encoder，全部 frozen，只學 prompt 與 depth codebook | §3.2, Fig. 2 |

- [[2026_CLIP-Can-Understand-Depth|CLIP2Depth]] 改用 ViT-B/16 版：image 與 text encoder 皆 frozen，取 image encoder 第 3、6、9 層特徵（[[2026_CLIP-Can-Understand-Depth]], §3.2, Table 1）。

## 相關頁面
[[Vision-Language-Model]]、[[Language-Prior]]
