---
type: concept
tags: [learning-setting, zero-shot]
sources: [2022_Can-Language-Understand-Depth, 2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# Zero-Shot Transfer

## 定義
- 不在目標任務上做任何訓練，直接用預訓練模型完成新任務（[[2022_Can-Language-Understand-Depth]], §1）。
- CLIP 原本的 zero-shot 分類：為每個類別組成「A photo of [class]」的 prompt，取與影像特徵相似度最高者為預測（[[2022_Can-Language-Understand-Depth]], §2）。

## 在 MDE 中的用法
- [[DepthCLIP]]：把深度回歸改成距離分類，以距離詞 prompt 與影像 patch 的相似度加權固定 depth bins，完全不訓練（[[2022_Can-Language-Understand-Depth]], §1, §3）。
- 優點：不需要訓練與深度標註（[[2022_Can-Language-Understand-Depth]], §6）。
- 缺點：固定的 depth bins 與人工 prompt 難以泛化到不同場景（[[2022_Can-Language-Understand-Depth]], §5；[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §1）。

## 與其他設定的比較
見 [[Few-Shot-Learning]]（訓練成本、參數量與準確度的取捨）。

## 相關頁面
[[Few-Shot-Learning]]、[[DepthCLIP]]、[[Vision-Language-Model]]
