# Index

MDE 論文 Wiki 的內容目錄。每頁一行：連結 — 一句話摘要。

## Papers
- [[2022_Can-Language-Understand-Depth]] — DepthCLIP：不訓練，以距離詞 prompt 與影像 patch 相似度加權固定 depth bins，首個 CLIP zero-shot MDE（ACM MM 2022）
- [[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]] — CLIPMDE：以 learnable depth token 取代人類距離詞，發現 CLIP 的深度概念難以用語言表達（ICCVW 2023）
- [[2026_CLIP-Can-Understand-Depth]] — CLIP2Depth：不微調 CLIP，以非人類語言的 mirror 經 FiLM 調變影像特徵、接輕量 decoder 做 dense depth（Pattern Recognition 2026）
- [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]] — WorDepth：以 text-VAE 把 caption 建模為 variational prior，再由影像 conditional sampler 選出 metric depth（CVPR 2024）
- [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]] — 以 learnable prompt 與依場景的 depth codebook，用每類 1 張影像 few-shot 調整 CLIP 做 MDE（WACV 2024）

## Concepts
- [[Scale-Ambiguity]] — 單張影像無法確定重建 scale 的根本歧義
- [[Language-Prior]] — 以場景文字描述作為深度估計的 prior，與 generic / specific prior 的比較
- [[Variational-Autoencoder]] — VAE、reparameterization trick、KL loss，以及在 MDE 中的用法
- [[Scale-Invariant-Loss]] — Eigen et al. 的 log 空間 scale-invariant 深度 loss
- [[Vision-Language-Model]] — CLIP 等 VLM 及其在 MDE 的應用，語言作為相似度或作為 prior 的兩種用法
- [[Zero-Shot-Transfer]] — 不在目標任務上訓練，直接以預訓練模型完成任務；DepthCLIP 的設定
- [[Few-Shot-Learning]] — 少量標註樣本調整預訓練模型；與 supervised、zero-shot 的成本比較
- [[Prompt-Tuning]] — 從人工 prompt 到可學 soft prompt（CoOp、CoCoOp）及在 MDE 的用法
- [[FiLM]] — 以條件向量產生乘法與加法係數調變特徵；CLIP2Depth 用來注入 mirror query
- [[Depth-Bins]] — 把深度離散成 bins 再加權求和；固定、adaptive 與依場景切換的比較

## Entities

### Datasets
- [[NYU-Depth-V2]] — 室內 RGB-D，654 張測試影像，深度至 10 m
- [[KITTI]] — 室外自駕場景，常用 Eigen split（23,488 / 697 張），深度至 80 m
- [[SUN-RGBD]] — 室內 RGB-D，常用於從 NYUv2 zero-shot 遷移測試

### Metrics
- [[Depth-Metrics]] — Abs Rel、RMSE、log10、RMSElog、δ<1.25ⁱ 的定義與解讀

### Models
- [[CLIP]] — 對比式 vision-language model；WorDepth 用其 text encoder，Hu et al. 用其三個 encoder
- [[Swin-Transformer]] — hierarchical ViT backbone，MDE 常用 Swin-L
- [[AdaBins]] — 以 adaptive bins 切分深度範圍的 supervised MDE 方法（CVPR 2021）
- [[DepthCLIP]] — 以 CLIP 深度描述相似度做 zero-shot MDE 的方法
- [[CLIPSeg]] — CLIP-based 分割模型的輕量 decoder，CLIP2Depth 沿用為深度 decoder
- [[CLIPMDE]] — Auty et al. 的 learnable depth token 方法（WorDepth 稱 CLIPMDE）

## Syntheses
