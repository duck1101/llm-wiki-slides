---
type: concept
tags: [mde, depth-representation]
sources: [2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation, 2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation, 2022_Can-Language-Understand-Depth, 2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]
updated: 2026-11-19
---

# Depth Bins

## 定義
- 把連續的深度範圍離散成一組代表深度值（bins），模型預測每個像素或 patch 在各 bin 上的權重，再加權求和得到深度（補充）。
- 在 CLIP-based MDE 中，每個深度描述（如 close、far）對應一個 bin 的深度值（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §3.3–3.5）。

## 各論文的作法
| 論文 | Bin 怎麼決定 | 是否依場景改變 | 出處 |
|---|---|---|---|
| [[AdaBins]] | 以 transformer block 把深度範圍切成 adaptive bins | 依輸入影像調整 | [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §2 |
| [[CLIPMDE]] | 固定的 bin 中心，平均或 log-uniform 分布；learned token 解除 bin 數限制，最多試到 256 個 | 否；但 KITTI 上 log-uniform 較好、bin 越多越好（[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]], Table 6–7） |
| [[DepthCLIP]] | 人工設定：7 個距離詞對應 1.00～3.00 m（[[2022_Can-Language-Understand-Depth]], §4.2） | 否，所有場景共用；但 ablation 顯示依場景換劃分可大幅改善（[[2022_Can-Language-Understand-Depth]], Table 2） | [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §1 |
| [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.]] | Learnable depth codebook：每個場景類別一個可學的 depth bin，以 scene feature 選擇 | 是，依場景類別切換 | §3.4 |

## 為什麼要依場景改變
- 不同場景的深度分布不同（例如 bathroom 與 bedroom），固定的 bin 在某些場景表現好、其他場景則不理想（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], §1, Fig. 1）。
- Ablation：單一可學 depth bin（class-independent）→ 換成依場景的 depth codebook，除 δ<1.25 外所有指標改善，MARE 0.378 → 0.347（[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]], Table 3）。

## 相關頁面
[[DepthCLIP]]、[[AdaBins]]、[[Depth-Metrics]]
