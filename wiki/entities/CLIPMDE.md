---
type: entity
tags: [model, mde, vision-language, prompt-tuning]
sources: [2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language, 2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation, 2026_CLIP-Can-Understand-Depth]
updated: 2026-11-19
---

# CLIPMDE（Auty et al.）

- 類型：以 learnable depth token 改良 [[DepthCLIP]] 的 CLIP-based MDE 方法
- 原始論文：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]]（ICCVW 2023）
- 名稱：WorDepth 稱為 CLIPMDE（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], Table 1）；其他論文多稱「Auty et al.」
- 作法：
  - 把 prompt 中的人類距離詞換成可學的 512 維 depth token，CLIP 完全 frozen（[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]], §3.1）。
  - 7 個 bin 時只有 3584 個可學參數；每多一個 bin 增加 512 個（[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]], §4.2, §4.4）。
  - 輸出為 H/32 × W/32 的低解析度深度圖再雙線性放大（[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]], §3.2）。
- 發現：learned token 大多不對應任何英文詞，CLIP 的深度概念難以用人類語言表達（[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]], §4.5）。

## 各論文報告的結果
| 資料集 | δ<1.25 | Abs Rel | RMSE | 出處 |
|---|---|---|---|---|
| [[NYU-Depth-V2]] | 0.465 | 0.319 | 0.970 | [[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]] Table 3（learned-7）；[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]] Table 1 |
| [[KITTI]] | 0.550 | 0.303 | 6.322 | [[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]] Table 3（learned-7）；[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]] Table 2 |

- 注意：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] Table 1 列 NYUv2 的 log10 為 0.139，實為原論文的 RMSL；原論文的 log10 為 0.128。
- 原論文的最佳設定（256 個 log-uniform bins）更好：NYUv2 Abs 0.298、KITTI Abs 0.238（[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]], Table 7），但其他論文比較時多引用 7-bin 的結果。

- [[2026_CLIP-Can-Understand-Depth|CLIP2Depth]] 以 Auty et al. 為主要比較基準：Abs Rel 在 NYU 降低 68.7%、KITTI 降低 75.6%；時間一致性的錯誤率為 CLIP2Depth 的兩倍以上（[[2026_CLIP-Can-Understand-Depth]], Abstract, §4.4）。

## 相關頁面
[[DepthCLIP]]、[[Prompt-Tuning]]、[[Depth-Bins]]、[[CLIP]]
