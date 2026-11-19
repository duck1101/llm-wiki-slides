---
type: concept
tags: [vision-language, prompt]
sources: [2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation, 2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation, 2022_Can-Language-Understand-Depth, 2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language, 2026_CLIP-Can-Understand-Depth]
updated: 2026-11-19
---

# Prompt Tuning

## 定義
- 把預訓練模型調整到下游任務的方法，特別適用於訓練資料很少或沒有的情況（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §2）。
- 演進（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §2）：
  - 起初在語言模型中，以文字指令或範例作為輸入的一部分。
  - 之後把任務轉成「cloze」填空形式，但找最佳模板很耗時。
  - 近期改為在連續空間中學習 soft prompt。

## 用於 vision-language model
- **CoOp**：以一組可學習的向量最佳化 prompt context，可共用或依類別設定（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §2）。
- **CoCoOp**：在 CoOp 之上，依每張影像生成條件向量，改善對未見類別的泛化（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §2）。

## 在 MDE 論文中的用法
| 論文 | 作法 | 出處 |
|---|---|---|
| [[DepthCLIP]] | 人工 prompt「This object is [Depth CLASS]」，不學習；換用其他距離詞組合差異不大（[[2022_Can-Language-Understand-Depth]], Table 3） | [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §3.3 |
| [[CLIPMDE]] | 把距離詞換成 learnable depth token（可再加共用的 learnable context token）；KITTI 上隨機 token 勝過所有人類詞 | [[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]], §3.1, Table 3 |
| [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.]] | 把「This object is」換成可學向量 V，輸入為「[Vector] + [Class]」，以 RMSE loss 更新；加入後表現明顯提升 | §3.3, Table 3 |

## 從 learnable token 到非人類語言 query
- [[2026_CLIP-Can-Understand-Depth|CLIP2Depth]] 的 mirror：64 個 512 維可學向量完全取代自然語言 token，經 frozen text encoder 只產生一個 query，以 [[FiLM]] 調變影像特徵，不再需要 depth bins（[[2026_CLIP-Can-Understand-Depth]], §3.1）。

## 相關頁面
[[Vision-Language-Model]]、[[CLIP]]、[[Few-Shot-Learning]]
