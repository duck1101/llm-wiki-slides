# WorDepth: Variational Language Prior for Monocular Depth Estimation — Outline

> 補建說明：本篇在 workflow v2 之前完成，大綱內容為第 1 輪由使用者確認的版本（直接通過），於 v2 補建成檔並對應 paper 頁段落。

一句話總結：把 text caption 當作 variational prior，先用 text-VAE 學出描述可能對應的 metric depth 分布，再用影像從分布中選出最符合的深度圖。→ 段落：一句話總結

## Cover（1 張）
- 標題、作者、CVPR 2024、一句話總結

## Introduction（2 張）
- 背景：單張影像重建 3D 是 ill-posed，主要歧義是 scale；訓練集學到的分布未必符合真實世界（§1）→ 段落：研究背景
- 動機：影像有 layout 缺 scale、文字有 scale 線索缺 layout，兩種歧義互補（§1–2, Fig. 1）→ 段落：動機
- 現有問題：generic prior 缺乏場景資訊、特定架構設計假設不成立時失效、VLM-based 方法皆為 implicit modeling（§1–2）→ 段落：現有方法的問題

## Method（3 張）
- 整體架構：text-VAE、conditional sampler、共用 depth decoder；loss 為 scale-invariant loss 加 KL divergence（Fig. 2, §3.3）→ 段落：整體架構（Fig. 2）、Training loss（§3.3）
- 兩個核心模組：text-VAE（frozen CLIP + MLP → μ̂、σ̂）、conditional sampler（Swin-L → ε̃，z̃ = μ̂ + ε̃·σ̂）（§3.1–3.2）→ 段落：Text-VAE（§3.1）、Image-based conditional sampler（§3.2）
- 訓練與推論：alternating optimization（p = 1%）與推論方式（§3.4）→ 段落：Alternating optimization（§3.4）、推論（§3.4）

## Experimental Results（3 張）
- NYU Depth V2：Table 1 節錄，δ<1.25 提升最明顯的原因 → 段落：NYU Depth V2（Table 1）
- KITTI 與 zero-shot：Table 2、Table 4 節錄，室外增益較小的原因 → 段落：KITTI Eigen split（Table 2）、Zero-shot generalization（Table 4）
- Ablation 與定性：Table 3 的 p 影響、caption 提到的物體改善最明顯 → 段落：Ablation：alternating ratio p（Table 3，NYU Depth V2）、定性結果（Fig. 3–4）

## Conclusions（1 張）
- 結論與限制（§5）→ 段落：結論（§5）、限制（§5）

## 預計張數
1 + 2 + 3 + 3 + 1 = 10 張

## 預計頁面
- papers：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]]
- concepts：[[Scale-Ambiguity]]、[[Language-Prior]]、[[Variational-Autoencoder]]、[[Scale-Invariant-Loss]]、[[Vision-Language-Model]]
- entities：[[NYU-Depth-V2]]、[[KITTI]]、[[SUN-RGBD]]、[[Depth-Metrics]]、[[CLIP]]、[[Swin-Transformer]]、[[AdaBins]]
