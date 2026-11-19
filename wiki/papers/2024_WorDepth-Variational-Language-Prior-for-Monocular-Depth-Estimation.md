---
type: paper
tags: [mde, supervised, language-prior, vae, vision-language]
sources: [2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# WorDepth: Variational Language Prior for Monocular Depth Estimation

> 出處：CVPR 2024｜作者：Ziyao Zeng et al.（Yale、UCLA）｜原文：[[raw/2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation/meta.md]]
> 程式碼：https://github.com/Adonis-galaxy/WorDepth

## 一句話總結

把影像的 text caption 當成 variational prior：用 text-VAE 學出「這段描述可能對應哪些 metric-scale 深度圖」的分布，再用影像（conditional sampler）從分布中選出最符合的那一張（Abstract, §1）。

## Introduction

### 研究背景
- 成像是 3D → 2D 的 surjection，無限多個 3D 場景可對應到同一張影像，因此 monocular depth estimation 是 ill-posed，主要歧義是 [[Scale-Ambiguity|scale]]（§1）。
- 深度估計因此需要 induction：網路在訓練集上學到的場景分布決定預測；但大規模深度資料集稀少，學到的分布不一定符合真實世界統計（§1）。

### 動機
- 核心問題：除了訓練集，能否用其他 prior 校正學到的場景分布（§1）？
- 文字描述同樣 ill-posed：「A bedroom with a bed and a table」對應無限多種 layout，但場景的 scale 與其中物體的典型大小密切相關（§1–2, Fig. 1）。
- 兩種模態的歧義互補（§1）：
  - 影像：看得到 layout 與物體形狀，但缺 scale。
  - 文字：提供 scale（與粗略形狀）的強 prior，但缺 layout。

### 現有方法的問題
- Generic prior（local smoothness、connectivity、object orientation 等）適用範圍廣，但缺乏針對特定場景的資訊，例如物體大小（§1）。
- 特定的架構設計（例如利用相機參數）在假設不成立時會失效（§1–2）。
- 只靠視覺線索推得語意很困難，原因是 scale ambiguity 與有標註資料集規模有限（§2）。
- 既有 VAE 類方法多以影像取得分布的 mean，與 WorDepth 根本不同；且都沒有使用 language prior（§2）。
- 既有使用 [[Vision-Language-Model|vision-language model]] 的 MDE 方法（DepthCLIP、CLIPMDE、VPD 等）都是 implicit modeling（§2）。

### 貢獻（§1）
1. 提出 variational framework，利用兩種有歧義的模態的互補性做 MDE，稱為 WorDepth。
2. 提出 image-based conditional sampler，將 language 建模為 conditional prior。
3. 在 [[NYU-Depth-V2]] 與 [[KITTI]] 達到 state-of-the-art。
4. 作者所知第一個把 language 當作 MDE 的 variational prior 的工作。

## Method

### 問題設定
- 輸入 RGB 影像 x 與描述它的 text caption t，輸出 dense depth map y；訓練資料為 {影像, caption, ground-truth depth} 三元組（§3）。
- Caption 由 image captioner ExpansionNet v2 自動產生（§1, §4）；作者不限制 caption 來源，人工撰寫亦可（§1）。

### 整體架構（Fig. 2）
三個元件：**text-VAE**、**image-based conditional sampler**、兩者共用的 **depth decoder**。

### Text-VAE（§3.1）
- Caption → frozen [[CLIP]] text encoder（ResNet-50 版，特徵 1024 維）→ 3 層 MLP（512、256、128）→ 輸出 latent 分布的 μ̂、σ̂ ∈ R^d，d = 128（§3.1, §4）。
- CLIP text encoder 全程 frozen，不更新（§3.1）。
- 以 ε ~ N(0, 1) 與 reparameterization trick 取樣：ẑ = μ̂ + ε·σ̂（§3.1）；概念見 [[Variational-Autoencoder]]。
- ẑ 沿水平、垂直方向複製成 d × h × w 的 latent，送入 depth decoder 得到深度圖 ŷ（§3.1）。
- Loss：L_VAE = L_SI + α·L_KL（Eq. 1）。

### Image-based conditional sampler（§3.2）
- 目的：text-VAE 只給出「描述相符的可能場景分布」，需要依影像選出最可能的那一個（§3.2）。
- 以 [[Swin-Transformer|Swin-L]]（ImageNet 預訓練）編碼影像，預測 patch-wise 的 ε̃ ∈ R^(d×h×w)，取代 Gaussian noise（§3.2, §4）。
- 輸入另外包含 μ̂、σ̂（已 detach，視為輸入）（§3.2）。
- z̃ = μ̂ + ε̃·σ̂，再經 depth decoder 得到 ỹ（§3.2）。
- Encoder 以 3 個 skip connection 接到 decoder；訓練 text-VAE 那一步時 skip connection 填 0（§3.2, §4）。
- Loss：L_CS = L_SI + β·L_KL（Eq. 2），KL 項讓 ε̃ 不偏離標準 Gaussian，並提升訓練穩定性（§3.2）。

### Training loss（§3.3）
- [[Scale-Invariant-Loss]]（Eq. 3，源自 Eigen et al.），γ = 0.85（§4）。
- KL divergence（Eq. 4），α = β = 1×10⁻³（§4）。

### Alternating optimization（§3.4）
- 先訓練 text-VAE 收斂再訓練 sampler 的兩階段作法，常讓 sampler 卡在 suboptimal local minimum，且多一個訓練階段（§3.4）。
- 改採交替訓練：以比例 p 訓練 text-VAE（freeze sampler），以 1−p 訓練 sampler（freeze text-VAE）；depth decoder 兩步都更新（§3.4, Fig. 2）。
- p 設為 1%（§4）。

### 推論（§3.4）
- 不再從 Gaussian 取樣，直接走 conditional sampler 路徑：影像 + caption → 深度圖。
- 另一模式：捨棄 sampler，只用 text-VAE 從 caption 產生可能的深度圖。

### 其他訓練設定（§4）
- Adam（無 weight decay），learning rate 以 cosine scheduler 從 3×10⁻⁵ 降到 1×10⁻⁵，訓練 50 epochs。
- Data augmentation：random gamma、brightness、color intensity、horizontal flip（50%）、rotation（±2.5°）。

## Experimental Results

### 設定（§4）
- 資料集：
  - [[NYU-Depth-V2]]（室內）：24,231 張訓練、654 張測試，深度範圍 1×10⁻³～10 m。
  - [[KITTI]] Eigen split（室外）：23,488 張訓練、697 張測試，清除無有效 ground truth 後剩 652 張；深度範圍 1×10⁻³～80 m。
  - [[SUN-RGBD]]：只用於 zero-shot 測試。
- 評估指標：Abs Rel、RMSE、log10、RMSElog、threshold accuracy δ（[[Depth-Metrics]]）。
- Baseline：直接訓練 Swin-L image encoder + depth decoder，不使用 language prior（Table 1–2）。

### NYU Depth V2（Table 1）

| Method | Backbone | δ<1.25 ↑ | δ<1.25² ↑ | δ<1.25³ ↑ | Abs Rel ↓ | log10 ↓ | RMSE ↓ |
|---|---|---|---|---|---|---|---|
| [[AdaBins]] | EffNet-B5 + ViT-mini | 0.903 | 0.984 | 0.997 | 0.103 | 0.044 | 0.364 |
| NeWCRFs | Swin-L | 0.922 | 0.992 | 0.998 | 0.095 | 0.041 | 0.331 |
| DepthFormer | Swin-L | 0.923 | 0.989 | 0.997 | 0.094 | 0.040 | 0.329 |
| Baseline | Swin-L | 0.910 | 0.990 | 0.998 | 0.098 | 0.043 | 0.351 |
| **WorDepth** | Swin-L | **0.932** | **0.992** | **0.998** | **0.088** | **0.038** | **0.317** |
| % Improvement | – | +2.42% | +0.02% | +0.00% | −10.20% | −11.63% | −9.69% |

- 所有指標都優於 baseline 與既有方法（§4）。
- δ<1.25 提升最明顯：既有方法常能預測正確的形狀（點的 ordinal 關係），但 scale 偏離；WorDepth 憑場景中物體推得更好的 scale（§4）。

### KITTI Eigen split（Table 2）

| Method | Backbone | δ<1.25 ↑ | δ<1.25² ↑ | δ<1.25³ ↑ | Abs Rel ↓ | RMSElog ↓ | RMSE ↓ |
|---|---|---|---|---|---|---|---|
| [[AdaBins]] | EffNet-B5+ViT-mini | 0.964 | 0.995 | 0.999 | 0.058 | 0.089 | 2.360 |
| NeWCRFs | Swin-L | 0.974 | 0.997 | 0.999 | 0.052 | 0.079 | 2.129 |
| DepthFormer | Swin-L | 0.975 | 0.997 | 0.999 | 0.052 | 0.079 | 2.143 |
| Baseline | Swin-L | 0.969 | 0.996 | 0.999 | 0.054 | 0.085 | 2.343 |
| **WorDepth** | Swin-L | **0.979** | **0.998** | **0.999** | **0.049** | **0.074** | **2.039** |
| % Improvement | – | +1.03% | +0.20% | +0.00% | −9.26% | −12.94% | −12.97% |

- 同樣達到 state-of-the-art，但 δ<1.25 的相對提升不如 NYUv2 明顯（§4）。
- 作者解釋：室外同一類物體的大小、形狀差異大，例如「car」可能是 sedan、coupe 或 hatchback；caption 模糊時，明確依賴它反而可能出錯，但以影像為條件能部分化解（§4）。

### Ablation：alternating ratio p（Table 3，NYU Depth V2）

| p | δ<1.25 ↑ | Abs Rel ↓ | RMSE ↓ |
|---|---|---|---|
| 0% | 0.929 | 0.091 | 0.323 |
| **1%** | **0.932** | **0.088** | **0.317** |
| 10% | 0.930 | 0.090 | 0.322 |
| 50% | 0.763 | 0.163 | 0.527 |
| 90% | 0.642 | 0.211 | 0.687 |
| 100% | 0.590 | 0.225 | 0.746 |

（完整欄位見 Table 3，此處節錄三項指標。）

- p 越低，模型越 deterministic；p 越高，text-VAE 學到更好的 variational prior、能產生多樣的 prior depth，但 sampler 更新次數變少，在固定訓練長度下收斂慢、預測較模糊（§4）。
- p > 10% 表現明顯下降；p = 100%（完全不看影像）仍有合理結果，代表 caption 本身帶有與 ground truth 相符的統計資訊（§4）。
- p = 0%（text 與 image 一起直接映射到深度，沒有 variational prior）表現下降，說明 prior 的作用（§4）。

### Zero-shot generalization（Table 4）
在 NYU Depth V2 訓練，不 fine-tune 直接測 [[SUN-RGBD]]：

| Method | δ<1.25 ↑ | Abs Rel ↓ | RMSE ↓ |
|---|---|---|---|
| [[AdaBins]] | 0.771 | 0.159 | 0.476 |
| DepthFormer | 0.815 | 0.137 | 0.408 |
| Baseline | 0.803 | 0.141 | 0.427 |
| **WorDepth** | **0.833** | **0.123** | **0.376** |

（完整欄位見 Table 4，此處節錄三項指標。）

- 作者認為不同場景之間，語言描述的 domain gap 比影像小，因此 language prior 有較好的遷移性（§4）。

### 定性結果（Fig. 3–4）
- 與 [[AdaBins]] 相比，error map 整體變暗（誤差降低），代表 scale 更準確（Fig. 3–4）。
- Caption 有提到的物體改善最明顯：NYUv2 的 chairs、window、shower curtain、man、desks；KITTI 的 wall、trees、building（Fig. 3–4, §4）。
- 作者觀察：即使「a wall」本身很模糊，caption（不論人寫或模型產生）傾向只在物體大小或距離落在某範圍時才提到它，因此隱含的 scale 資訊比表面多（§4）。

## Conclusions

### 結論（§5）
- Language 可以把學到的場景分布校正到真實世界的統計，有助於處理 MDE 與 structure-from-motion 長期存在的 [[Scale-Ambiguity|scale ambiguity]]。
- 首個利用兩種有歧義的模態互補、做 3D 重建的方法；把 language 的 layout 歧義透過 variational 方法轉為優勢，將預測 ground 到 metric scale。
- 為目前只能預測 relative / scaleless depth 的方法提供延伸到 metric scale 的方向。

### 限制（§5）
- [[Language-Prior|Language prior]] 介於 generic 與 specific regularizer 之間，正則化程度由 caption 的具體程度決定：
  - 模糊的 caption 幾乎不提供物體形狀或大小資訊，幫助有限。
  - 具體但錯誤的 caption 可能讓預測出錯。
- 依賴 image captioner 的品質，會受其錯誤影響。
- 容易被惡意使用者以刻意選擇的 caption 操控預測。

## 相關頁面
- Concepts：[[Scale-Ambiguity]]、[[Language-Prior]]、[[Variational-Autoencoder]]、[[Scale-Invariant-Loss]]、[[Vision-Language-Model]]
- Entities：[[NYU-Depth-V2]]、[[KITTI]]、[[SUN-RGBD]]、[[Depth-Metrics]]、[[CLIP]]、[[Swin-Transformer]]、[[AdaBins]]
