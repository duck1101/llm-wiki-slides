---
type: concept
tags: [mde, fundamentals]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# Scale Ambiguity（尺度歧義）

## 定義
- 成像是 3D 場景到 2D 影像的 surjection，無限多個 3D 場景可對應到同一張影像；因此從單張影像估計 3D 結構是 ill-posed，主要歧義之一就是重建的 scale（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §1）。
- 直覺例子（補充）：一張照片中的房間，可能是真實房間，也可能是縮小比例的模型，單看影像無法區分。

## 影響
- 既有方法常能預測正確的形狀（點之間的 ordinal 關係），但 scale 偏離，導致 δ<1.25 等指標偏低（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §4）。
- 許多方法因此只能做 relative / scaleless depth（[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]], §5）。

## 各論文的處理方式
- [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]]：以 text caption 中物體的典型大小作為 scale 的 prior（[[Language-Prior]]），讓預測 ground 到 metric scale（§1, §5）。

## 相關頁面
[[Language-Prior]]、[[Scale-Invariant-Loss]]、[[Depth-Metrics]]
