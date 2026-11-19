# WorDepth: Variational Language Prior for Monocular Depth Estimation — Slide Spec

## S1 · Cover
- 標題：WorDepth: Variational Language Prior for Monocular Depth Estimation
- 內容：
  - 作者：Ziyao Zeng, Daniel Wang, Fengyu Yang, Hyoungseob Park, Stefano Soatto, Dong Lao, Alex Wong
  - Yale University · UCLA｜CVPR 2024
  - 一句話：把 text caption 當作 variational prior，先學出「這段描述可能對應哪些 metric-scale 深度圖」，再用影像從中選出最符合的一張
- 圖表：無
- 出處：Abstract, §1
- Wiki：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#一句話總結]]

## S2 · Introduction — 研究背景
- 標題：研究背景：單張影像本來就無法確定 scale
- 內容：
  - 成像是 3D → 2D 的 surjection，無限多個 3D 場景會得到同一張影像，MDE 是 ill-posed
  - 主要歧義是重建的 scale
  - 網路從訓練集學場景分布，但大規模深度資料集稀少，學到的分布未必符合真實世界
  - 核心問題（強調框）：除了訓練集之外，能不能用其他 prior 把學到的場景分布校正到真實世界的統計？
- 圖表：無
- 出處：§1
- Wiki：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#研究背景]]

## S3 · Introduction — 動機與現有問題
- 標題：動機：兩種「有歧義」的模態剛好互補
- 內容：
  - 影像：看得到 layout 與物體形狀，但不知道 scale
  - 文字（例：「A bedroom with a bed and a table」）：物體的典型大小提供 scale 線索，但不知道 layout
  - 現有方法的問題：
    - Generic prior（smoothness、connectivity 等）缺乏特定場景資訊
    - 特定架構設計（如利用相機參數）在假設不成立時會失效
    - VLM-based MDE（DepthCLIP、CLIPMDE、VPD）都是 implicit modeling；本文首次把 language 明確建模為 variational prior
- 圖表：左右對照框（影像 vs. 文字）
- 出處：§1–2, Fig. 1
- Wiki：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#動機]]、[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#現有方法的問題]]

## S4 · Method — 整體架構
- 標題：整體架構：text-VAE ＋ conditional sampler ＋ 共用 depth decoder
- 內容：
  - 文字決定「可能的場景分布」（μ̂, σ̂）
  - 影像決定「從分布中選哪一個」（ε̃ 取代 Gaussian noise）
  - Loss：scale-invariant loss（γ = 0.85）＋ KL divergence（α = β = 1×10⁻³）
- 圖表：架構圖
  - 範圍：Fig. 2 下半部的 conditional sampler 路徑（推論時使用）；上半部 ε ~ N(0, 1) 的 text-VAE 訓練分支在 S6 以文字說明
  - 節點：Caption、Text-VAE（CLIP text encoder + MLP）、μ̂ / σ̂、RGB Image、Conditional Sampler（Swin-L）、ε̃、z̃ = μ̂ + ε̃·σ̂、Depth Decoder、深度圖
  - 連線：Caption → Text-VAE → μ̂ / σ̂ → z̃；μ̂ / σ̂ → Conditional Sampler（detached gradient）；RGB Image → Conditional Sampler → ε̃ → z̃；z̃ → Depth Decoder → 深度圖
  - 對照：Fig. 2
- 出處：Fig. 2, §3.1–3.3, §4
- Wiki：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#整體架構（Fig. 2）]]、[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#Training loss（§3.3）]]

## S5 · Method — 兩個核心模組
- 標題：兩個核心模組
- 內容：
  - Text-VAE：
    - Caption → frozen CLIP text encoder（ResNet-50 版，1024 維）→ 3 層 MLP → μ̂, σ̂（d = 128）
    - Reparameterization：ẑ = μ̂ + ε·σ̂，ε ~ N(0, 1)
    - ẑ 在空間上複製成 d×h×w 後送入 depth decoder
  - Image-based conditional sampler：
    - Swin-L（ImageNet 預訓練）編碼影像，輸出 patch-wise 的 ε̃
    - z̃ = μ̂ + ε̃·σ̂：用影像在文字分布中選出最可能的場景
    - μ̂, σ̂ detach 後也作為輸入；3 個 skip connection 接到 decoder
    - KL loss 讓 ε̃ 不偏離標準 Gaussian
- 圖表：左右兩欄
- 出處：§3.1–3.2, §4
- Wiki：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#Text-VAE（§3.1）]]、[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#Image-based conditional sampler（§3.2）]]

## S6 · Method — 訓練與推論
- 標題：訓練：Alternating optimization
- 內容：
  - 為什麼不分兩階段：先訓練 text-VAE 再訓練 sampler，sampler 常卡在 suboptimal local minimum，且多一個訓練階段
  - 交替訓練：
    - 比例 p：訓練 text-VAE（freeze sampler，ε ~ N(0, 1)）
    - 比例 1 − p：訓練 sampler（freeze text-VAE，用 ε̃）
    - Depth decoder 兩步都更新；p 設為 1%
  - 推論：不再從 Gaussian 取樣，影像 + caption → conditional sampler → 深度圖；另一模式只用 text-VAE 從 caption 生成可能的深度圖
- 圖表：無
- 出處：§3.4, §4, Fig. 2
- Wiki：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#Alternating optimization（§3.4）]]、[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#推論（§3.4）]]

## S7 · Experimental Results — NYU Depth V2
- 標題：NYU Depth V2（室內）：全部指標最佳
- 內容：
  - 測試集 654 張；Baseline = 同樣 Swin-L + decoder，但不使用 language prior
  - δ<1.25 提升最明顯：既有方法形狀正確但 scale 偏離，WorDepth 用物體大小推得更好的 scale
- 圖表：表格（Table 1 節錄）
  - 欄：Method、Backbone、δ<1.25 ↑、Abs Rel ↓、log10 ↓、RMSE ↓
  - AdaBins｜EffNet-B5 + ViT-mini｜0.903｜0.103｜0.044｜0.364
  - NeWCRFs｜Swin-L｜0.922｜0.095｜0.041｜0.331
  - DepthFormer｜Swin-L｜0.923｜0.094｜0.040｜0.329
  - Baseline｜Swin-L｜0.910｜0.098｜0.043｜0.351
  - WorDepth｜Swin-L｜0.932｜0.088｜0.038｜0.317（強調）
  - 相對 Baseline｜—｜+2.42%｜−10.20%｜−11.63%｜−9.69%
- 出處：Table 1, §4
- Wiki：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#NYU Depth V2（Table 1）]]

## S8 · Experimental Results — KITTI 與 Zero-shot
- 標題：KITTI（室外）與 Zero-shot 遷移
- 內容：
  - KITTI：δ<1.25 增益不如室內明顯；室外同一類物體大小差異大，例如「car」可能是 sedan、coupe 或 hatchback
  - Zero-shot（NYUv2 訓練 → SUN-RGBD 測試，不 fine-tune）：作者認為語言描述跨場景的 domain gap 比影像小
- 圖表：兩個表格
  - Table 2 節錄，欄：Method、δ<1.25、Abs Rel、RMSE
    - DepthFormer｜0.975｜0.052｜2.143
    - Baseline｜0.969｜0.054｜2.343
    - WorDepth｜0.979｜0.049｜2.039（強調）
  - Table 4 節錄，欄：Method、δ<1.25、Abs Rel、RMSE
    - AdaBins｜0.771｜0.159｜0.476
    - DepthFormer｜0.815｜0.137｜0.408
    - Baseline｜0.803｜0.141｜0.427
    - WorDepth｜0.833｜0.123｜0.376（強調）
- 出處：Table 2, Table 4, §4
- Wiki：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#KITTI Eigen split（Table 2）]]、[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#Zero-shot generalization（Table 4）]]

## S9 · Experimental Results — Ablation 與定性結果
- 標題：Ablation：alternating ratio p 與定性觀察
- 內容：
  - p = 0%：沒有 variational prior，表現下降
  - p > 10%：sampler 更新太少，表現明顯下降
  - p = 100%：完全不看影像，仍有合理結果
  - 定性（對比 AdaBins）：error map 整體變暗 → scale 更準
  - Caption 提到的物體改善最明顯：chairs、window、shower curtain（NYUv2）；wall、trees、building（KITTI）
  - 「a wall」看似模糊，但 caption 傾向只在大小或距離落在某範圍時才提到它 → 隱含 scale 資訊
- 圖表：表格（Table 3 節錄，NYUv2）
  - 欄：p、δ<1.25、Abs Rel、RMSE
  - 0%｜0.929｜0.091｜0.323
  - 1%｜0.932｜0.088｜0.317（強調）
  - 10%｜0.930｜0.090｜0.322
  - 50%｜0.763｜0.163｜0.527
  - 90%｜0.642｜0.211｜0.687
  - 100%｜0.590｜0.225｜0.746
- 出處：Table 3, Fig. 3–4, §4
- Wiki：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#Ablation：alternating ratio p（Table 3，NYU Depth V2）]]、[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#定性結果（Fig. 3–4）]]

## S10 · Conclusions — 結論與限制
- 標題：結論與限制
- 內容：
  - 結論：
    - Language 可以把學到的場景分布校正到真實世界的 metric scale，緩解 scale ambiguity
    - 首個利用兩種有歧義模態互補的 3D 重建方法：把文字的 layout 歧義透過 variational 建模轉為優勢
    - 為只能預測 relative / scaleless depth 的方法提供延伸到 metric scale 的方向
  - 限制：
    - 模糊的 caption：幾乎不提供大小或形狀資訊，幫助有限
    - 具體但錯誤的 caption：可能誤導預測
    - 依賴 image captioner 的品質
    - 可能被惡意 caption 操控預測
- 圖表：左右兩欄（結論 / 限制）
- 出處：§5
- Wiki：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#結論（§5）]]、[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation#限制（§5）]]
