---
type: paper
tags: [mde, vision-language, prompt-tuning, frozen-clip]
sources: [2026_CLIP-Can-Understand-Depth, 2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# CLIP Can Understand Depth

> 出處：Pattern Recognition, vol. 172, 2026（2025-09 線上刊出）｜作者：Sohee Kim, Jisu Kang, Dunam Kim, Seokju Lee（KENTECH）｜原文：[[raw/2026_CLIP-Can-Understand-Depth/meta.md]]
> 程式碼：論文中未提供｜方法名稱：CLIP2Depth

## 一句話總結

CLIP2Depth 不微調 [[CLIP]]，把 frozen text encoder 的語意 prior 蒸餾成一個非人類語言的可學 embedding「mirror」，以 [[FiLM]] 調變影像特徵並接上輕量的 [[CLIPSeg]] decoder 做 dense depth；Abs Rel 比 [[CLIPMDE|Auty et al.]] 在 NYU Depth v2 降低 68.7%、在 KITTI 降低 75.6%（Abstract, §7）。

## Introduction

### 研究背景
- CLIP 泛化能力強，但在預訓練時表徵不足的領域有明顯限制；為特定任務微調 CLIP 需要大量計算與資料（§1）。
- 與只用視覺特徵的 MDE 不同，調整 CLIP 可以把語意 prior 與跨模態知識帶進深度預測，可能在分布轉移或資料有限時更穩健（§1）。
- 作者的核心問題：CLIP 能否適應自然語言監督不足的領域？具體而言——CLIP 能理解深度嗎（§1）？

### 現有方法的問題
- 先前 frozen-CLIP 方法（§2.1）：
  - [[DepthCLIP]]（Zhang et al.）：以描述距離的語意 token 對應 depth bin，zero-shot。
  - [[CLIPMDE|Auty et al.]]：可學的距離 token 加上固定的人類語言前綴。
  - [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation|Hu et al.]]：可學的前綴 prompt 加上固定的距離 token，few-shot。
  - 共同限制：都用預先定義的 bin 值把影像–文字相似度轉成深度，或依賴自然語言 token 引導可學部分。
- 近期方法改為微調 CLIP 或加入大量參數（§2.1）：
  - CaBins 部分解凍 CLIP；CaBins 與 [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] 以額外的神經模組加入大量可學參數。
  - HoCLIP 微調整個 CLIP backbone，並加入 multi-scale attention decoder 等模組。
- CLIP 無法穩定地把影像 patch 與描述距離的自然語言 prompt 對上（Abstract, §3.1）。

### 動機與貢獻
- 不微調 CLIP、也不加大型模組，只用一個非人類語言的可學 token 調整 CLIP 的視覺–語言對齊（§2.1）。
- 貢獻（§1）：
  1. 證明 CLIP 不需微調、只用既有 prior 就能有效做 dense MDE。
  2. 單一 query 向量即可抽取單一種逐像素特徵，不需要人工設計的 prompt 集合或 token binning。
  3. 在 [[NYU-Depth-V2]] 與 [[KITTI]] 勝過所有先前 CLIP-based 方法，並與 task-specific 視覺模型競爭，同時保留 CLIP 的 task-agnostic 特性。

## Method

### 整體架構（Fig. 2）
- 元件（Fig. 2, Table 1）：
  - **CLIP Text Model**（frozen）：Prompt Encoder，12 層 transformer、寬 512。
  - **CLIP Image Model**（frozen）：Visual Encoder，ViT-B/16，12 層、寬 768。
  - **Dense Predictor**（沿用 CLIPSeg，可訓練）：3 個 transformer block（寬 64）、2 個 FiLM、3 個 projection、deconvolution。
- 流程（Fig. 2, Algorithm 1–2）：
  1. Mirror Embeddings 取代人類語言 prompt，送入 frozen 的 Prompt Encoder，以 eos-pooling 得到一個 512 維的條件 embedding。
  2. 條件 embedding 經 FiLM Add 與 FiLM Mul，產生加法與乘法調變。
  3. 輸入影像經 frozen 的 Visual Encoder，取第 3、6、9 層的中間特徵（L3、L6、L9）。
  4. 各層特徵經 FiLM 調變（⊗、⊕）後，搭配 skip connection 送入 3 個 Transformer Block。
  5. Deconvolution 上採樣後經 Soft-Plus，輸出 Depth Map。
- Fig. 2 圖示：訓練前距離詞（far、remote、close）在 CLIP embedding 空間中對齊不佳；mirror 訓練後改善對齊。

### Mirror：non-human language prompt（§3.1）
- 先前實驗（DepthCLIP）顯示 CLIP 無法穩定地把影像與深度相關 prompt 對上；微調 CLIP 又缺乏深度–文字訓練資料、成本高（§3.1）。
- 作法：凍結 CLIP text encoder，把其語意 prior 蒸餾進一個可學的 embedding 矩陣「mirror」（§3.1）。
- 與 DepthCLIP、Auty et al.、Hu et al. 的三點差異（§3.1）：
  1. Mirror 是非人類語言的 embedding 矩陣，完全不用 CLIP 的自然語言 token embedding。
  2. 不論由幾個 embedding 組成，mirror 都只被編碼成一個 query 向量。
  3. 與較大的模組一起訓練時，mirror 仍保有捕捉場景語意物體的角色。
- (s, d) 的 mirror 經 frozen text encoder 只產生一個 (1, d) query；先前方法則產生 s 個 query，再把 s 個 embedding（或相似度）彙整成一個深度值（§3.1）。
- 作者主張單一 query（如「How far is this location from the camera?」）就足以做深度估計；並認為此設計可避免彙整多個 embedding 造成的過度平滑，但未提供實證比較（§3.1）。
- 實作：M ∈ R^(64×512)，即 64 個 512 維可學向量，前後接上 CLIP 的 BOS、EOS token（§3.2）；以平均 0.0、標準差 0.02 的常態分布初始化（§3.2）。

### Minimal decoder 與訓練（§3.2, §4.1）
- CLIP image encoder 的 patch embedding 失去了時空資訊，難以準確捕捉深度，因此加入 deconvolutional decoder 做 dense prediction（§3.2）。
- 不從頭設計 decoder，而是沿用最輕量且經驗證的 [[CLIPSeg]] decoder，避免模型過度依賴 decoder（§3.2）。
- 輸入影像 resize 成 352 × 352，切成 16 × 16 的 patch，共 484 個 patch embedding（ViT-B/16）（§3.2）。
- 凍結 CLIP encoder 與 FiLM 內的兩個 feed-forward network；其餘 decoder 與 mirror 一起訓練（§3.2）。
- Loss：AdaBins 的 modified scale-invariant loss，λ = 0.85、α = 10（[[Scale-Invariant-Loss]]）（§3.2）。
- 訓練（§4.1）：25 epochs、batch size 32、AdamW（weight decay 0.01）、cosine annealing、初始 learning rate 0.003；單張 RTX 3090。
- 資料（§4.1.1, Table 2）：
  - NYU Depth v2：24,231 張訓練、654 張測試；訓練用 Eigen crop 後 resize 成 352 × 352，評估時直接 resize 不裁切。
  - KITTI：Eigen split，23,157 張訓練、696 張測試；Garg crop 後 resize 成 352 × 352。
  - SUN RGB-D：只用官方測試集 5,050 張，做 zero-shot 評估。
- 公平性說明：本篇用較大的 CLIP ViT-B/16 並多一個可學 decoder，而先前方法用 CLIP ResNet-50；作者認為只要 CLIP encoder 保持 frozen，比較即屬合理，並把微調 CLIP 的 CaBins、HoCLIP 另列（§4.2）。

## Experimental Results

### NYU Depth V2（Table 3）

| Model | Abs Rel ↓ | RMSE ↓ | log10 ↓ | δ1 ↑ |
|---|---|---|---|---|
| DepthFormer | 0.096 | 0.339 | 0.041 | 0.921 |
| ZoeDepth | 0.077 | 0.277 | 0.033 | 0.953 |
| DepthAnything v2 | 0.056 | 0.206 | 0.024 | 0.984 |
| [[DepthCLIP]] | 0.388 | 1.167 | 0.156 | 0.394 |
| [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.]] | 0.347 | 1.049 | 0.140 | 0.428 |
| [[CLIPMDE\|Auty et al.]] | 0.319 | 0.970 | 0.128 | 0.465 |
| **CLIP2Depth** | **0.100** | **0.379** | **0.042** | **0.900** |
| HoCLIP（微調 CLIP） | 0.214 | 0.702 | 0.085 | 0.668 |

（節錄，完整比較見 Table 3。）

- 作者稱這是第一個不微調任何 CLIP 元件、卻能與 vision-only 模型相當的 vision-language 深度方法（§4.2）。
- 仍落後 ZoeDepth（BeiT-L）與 DepthAnything v2（ViT-L）等大型 vision-only 模型（§4.2）。

### KITTI（Table 4）

| Model | Abs Rel ↓ | Sq Rel ↓ | RMSE ↓ | δ1 ↑ |
|---|---|---|---|---|
| DepthFormer | 0.052 | 0.158 | 2.143 | 0.975 |
| DepthAnything v2 | 0.045 | – | 1.861 | 0.983 |
| [[DepthCLIP]] | 0.473 | 6.007 | 12.958 | 0.281 |
| [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.]] | 0.384 | 4.661 | 12.290 | 0.312 |
| [[CLIPMDE\|Auty et al.]] | 0.303 | – | 6.322 | 0.550 |
| **CLIP2Depth** | **0.074** | **0.303** | **2.948** | **0.938** |
| HoCLIP（微調 CLIP） | 0.107 | 0.539 | 3.835 | 0.879 |

（節錄，完整比較見 Table 4。）

- 先前 CLIP-based 方法在 KITTI 都明顯比 NYU 差；CLIP2Depth 同樣如此但差距大幅縮小，作者據此認為改善來自深度理解的修正，而非參數或 decoder（§4.2）。
- 相對 Auty et al. 的 Abs Rel 降幅：NYU (0.319 → 0.100) 為 68.7%，KITTI (0.303 → 0.074) 為 75.6%（Abstract, §7）。

### 參數量與計算量（Table 5）

| Model | Learnable Params | GFLOPs |
|---|---|---|
| DORN | 110,300k | 775.05 |
| ZoeDepth | 345,000k | 538.60 |
| DepthAnything v2 | 335,300k | 1121.58 |
| [[DepthCLIP]] | 0 | 48.76 |
| [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation\|Hu et al.]] | 8k | – |
| [[CLIPMDE\|Auty et al.]] | 3k | 107.36 |
| **CLIP2Depth** | **1,095k** | **89.60** |
| HoCLIP | 295,000k | 944 |

（節錄。GFLOPs 以 ptflops 量測 KITTI 評估解析度的單次前向。）

- 可學參數比 CLIP-based 前作多，但表現一致更好；比微調整個 CLIP 的 HoCLIP 少約 300 倍（§4.2, Fig. 4）。

### Zero-shot generalization（Table 6）
在 NYU Depth v2 訓練，直接測 [[SUN-RGBD]]：

| Model | Abs Rel ↓ | RMSE ↓ | log10 ↓ | δ1 ↑ |
|---|---|---|---|---|
| [[AdaBins]] | 0.159 | 0.476 | 0.068 | 0.771 |
| ZoeDepth | 0.119 | 0.346 | 0.052 | 0.864 |
| [[CLIPMDE\|Auty et al.]] | 0.446 | 0.950 | 0.146 | 0.380 |
| HoCLIP | 0.401 | 0.850 | 0.135 | 0.402 |
| **CLIP2Depth** | 0.431 | 0.535 | 0.096 | 0.627 |

（節錄；Auty et al. 的數值取自 HoCLIP 論文。）

- 在 CLIP-based 方法中，CLIP2Depth 除 Abs Rel 外各項最佳；但仍落後 ZoeDepth、NeWCRFs 等 vision-only 模型（Table 6, §4.3）。

### 一致性分析（Fig. 7–8）
- **時間一致性**：以 KITTI 影片的相鄰幀重投影計算不一致程度；CLIP2Depth 錯誤率遠低於 DepthCLIP 與 Auty et al.，DepthCLIP 的錯誤常高於隨機上界，Auty et al. 的錯誤仍超過本方法兩倍（§4.4, Fig. 7）。
- **空間連續性**：在 KITTI 物體偵測資料中，比較 car、cyclist、pedestrian 的 bounding box 高度與中位深度；CLIP2Depth 與 ground truth 分布最吻合，DepthCLIP 的預測侷限在有限範圍（§4.4, Fig. 8）。

### Ablation（Table 7–9）
全部在 KITTI 上進行（§4.5）：

| 實驗 | 變體 | Abs Rel ↓ | RMSE ↓ | δ1 ↑ |
|---|---|---|---|---|
| Mirror 狀態（Table 7） | Randomized（訓練後把 mirror 隨機化） | 0.0961 | 3.6415 | 0.8906 |
| Mirror 狀態（Table 7） | **Converged** | **0.0739** | **2.9480** | **0.9379** |
| Mirror 狀態（Table 7） | Disrupted（每步重新隨機化） | 0.0742 | 2.9970 | 0.9372 |
| 調變方式（Table 8） | Auty et al. 的相似度作法 | 0.0802 | 3.1390 | 0.9239 |
| 調變方式（Table 8） | **CLIP2Depth（FiLM）** | **0.0768** | **3.1267** | **0.9287** |
| 預訓練（Table 9） | Randomized（從頭訓練） | 0.077 | 3.127 | 0.929 |
| 預訓練（Table 9） | **CLIPSeg 預訓練** | **0.074** | **2.948** | **0.938** |

- **Mirror**：mirror 只有約 30k 參數，可能被模型忽略；但 Converged 模型在 mirror 被隨機化後明顯變差，表示確實依賴 mirror。Fig. 9 顯示 mirror 隨機化後，人、車、窗等需語意判斷的物體邊界失準（§4.5.1, Fig. 9）。
- **調變方式**：兩者都用 64 個 token／mirror embedding、都不使用 CLIPSeg 預訓練；以單一 query 經 FiLM 調變，各項指標都優於多個 prompt 相似度彙整（§4.5.2, Table 8）。
- **預訓練**：沿用在 PhraseCut 上預訓練的 CLIPSeg 權重優於從頭訓練，作者認為語意分割知識可協助修正 vision-language 模型的對齊偏差（§4.5.3, Table 9）。

## Conclusions

### 結論（§7）
- CLIP 不需微調、也不需人工調整 subword embedding，就能有效適應 MDE。
- CLIP2Depth 把 frozen text encoder 的語意 prior 蒸餾進精簡的非人類語言 prompt，表現接近先前的 SOTA 方法。
- Mirror 的 ablation 顯示它在語意線索關鍵的區域捕捉物體深度；方法同時改善時間與空間一致性，且不修改 CLIP backbone。

### 限制（§5）
- 雖有明顯進步，仍未達 CLIP 在語意分割、生成模型等其他應用的 SOTA 水準；幾何推理的本質差異使 CLIP prior 難以完全發揮。
- Mirror 的效果可能高度依賴場景中語意豐富的內容；在幾何結構為主、語意線索稀少的環境，泛化可能受限。
- 以非人類語言 embedding 取代自然語言 prompt，可能犧牲 CLIP 的 open-vocabulary 推理能力。

### 論文內的不一致與跨論文差異
- **Table 6 的文字描述**：§4.3 說 CLIP2Depth「除 Abs Rel 外各項最佳」，但 Table 6 中 ZoeDepth 的 RMSE（0.346）、log10（0.052）、δ1（0.864）都優於 CLIP2Depth（0.535、0.096、0.627）；此說法只在 CLIP-based 方法之間成立（補充：依 Table 6 比對）。
- **KITTI 表的 log10 欄**：Table 4 的 log10 欄中，DORN 0.120、DepthFormer 0.079、NeWCRFs 0.079 與 [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] Table 2 的 RMSElog 數值相同，疑似把 RMSElog 混入 log10 欄（補充：由兩篇論文表格比對）。
- **ZoeDepth 參數量**：§4.2 文字寫 346M，Table 5 為 345,000k。
- **CaBins 的 NYU RMSE**：Table 3 列為 0.041，低於所有方法（含 DepthAnything v2 的 0.206），與其 Abs Rel 0.120 不相稱，疑似誤植（補充）。
- **NeWCRFs 的 NYU RMSE**：本篇 Table 3 為 0.334，WorDepth Table 1 為 0.331。
- **與 WorDepth 的 SUN RGB-D 結果**：本篇文中提到 WorDepth，但 Table 6 未列入；WorDepth 自己報告的 SUN RGB-D 結果為 Abs Rel 0.123、RMSE 0.376、δ1 0.833（WorDepth Table 4），兩篇的評估流程（如 resize 方式）可能不同，不宜直接比較（補充）。
- **CLIPMDE 的 log10**：本篇 Table 3 列 Auty et al. 的 NYU log10 為 0.128，與原論文一致；WorDepth 列的 0.139 實為 RMSL。

## 相關頁面
- Concepts：[[FiLM]]、[[Prompt-Tuning]]、[[Vision-Language-Model]]、[[Scale-Invariant-Loss]]
- Entities：[[CLIPSeg]]、[[CLIP]]、[[CLIPMDE]]、[[DepthCLIP]]、[[NYU-Depth-V2]]、[[KITTI]]、[[SUN-RGBD]]、[[AdaBins]]
- Papers：[[2022_Can-Language-Understand-Depth]]、[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]]、[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]]、[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]]
