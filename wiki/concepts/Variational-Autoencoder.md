---
type: concept
tags: [generative-model, vae]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# Variational Autoencoder（VAE）

## 定義
- Encoder 輸出 latent 分布的 mean μ 與 standard deviation σ，再從分布取樣、由 decoder 重建輸出（補充）。
- **Reparameterization trick**：從 ε ~ N(0, 1) 取樣，令 z = μ + ε·σ，使取樣過程可微分（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §3.1）。
- **KL divergence loss**：把預測的分布拉向標準 Gaussian，作為 regularizer（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], Eq. 4, §3.3）：
  L_KL(μ, σ) = −log(σ) + (σ² + μ²)/2 − 1/2

## 在 MDE 中的用法
- 既有 VAE 類方法多以「影像」取得分布的 mean，建模深度的不確定性（例如 CodeSLAM、VDN）（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §2）。
- [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] 改以「文字」取得 μ、σ（text-VAE），再以影像預測的 ε̃ 取代 Gaussian noise 來選擇樣本：z̃ = μ̂ + ε̃·σ̂（§3.1–3.2）。

## 相關頁面
[[Language-Prior]]
