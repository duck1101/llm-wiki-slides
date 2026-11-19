---
type: concept
tags: [mde, loss]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# Scale-Invariant Loss（SI loss）

## 定義
源自 Eigen et al.（NeurIPS 2014），常用於 supervised MDE，可提升在多樣場景下的訓練穩定性（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §3.3, Eq. 3）：

L_SI(y, y*) = (1/N_e) Σ e(i,j)² − (γ/N_e²) (Σ e(i,j))²，其中 e(i,j) = log y(i,j) − log y*(i,j)

- N_e：像素數；γ：控制 loss 敏感度的係數（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §3.3）。
- 直覺（補充）：第二項抵銷整體的 log 偏移；γ = 1 時對整體 scale 完全不變，γ < 1 時保留部分對 scale 的懲罰。

## 各論文的設定
- [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]]：γ = 0.85，並搭配 KL divergence loss（§4）。

## 相關頁面
[[Scale-Ambiguity]]、[[Depth-Metrics]]
