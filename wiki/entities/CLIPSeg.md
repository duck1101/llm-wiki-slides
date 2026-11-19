---
type: entity
tags: [model, segmentation, vision-language, decoder]
sources: [2026_CLIP-Can-Understand-Depth]
updated: 2026-11-19
---

# CLIPSeg

- 類型：以文字或影像 prompt 做影像分割的 CLIP-based 模型（Lüddecke & Ecker）（[[2026_CLIP-Can-Understand-Depth]], ref. [2]）
- 結構：frozen CLIP（ViT-B/16）加上輕量的 dense predictor：3 個 transformer block、FiLM、projection、deconvolution（[[2026_CLIP-Can-Understand-Depth]], Table 1）
- 預訓練資料：PhraseCut（[[2026_CLIP-Can-Understand-Depth]], §4.5.3）

## 在 MDE 論文中的用法
| 論文 | 用法 | 出處 |
|---|---|---|
| [[2026_CLIP-Can-Understand-Depth\|CLIP2Depth]] | 沿用預訓練的 CLIPSeg decoder，以 mirror 為條件微調成深度預測；選用原因是它是最輕量且經驗證的 decoder | §3.2 |

- 以 CLIPSeg 預訓練權重初始化優於從頭訓練：KITTI Abs Rel 0.074 vs. 0.077（[[2026_CLIP-Can-Understand-Depth]], Table 9）。

## 相關頁面
[[FiLM]]、[[CLIP]]
