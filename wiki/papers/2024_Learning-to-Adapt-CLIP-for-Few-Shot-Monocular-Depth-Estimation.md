---
type: paper
tags: [mde, few-shot, vision-language, prompt-tuning, depth-bins]
sources: [2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation, 2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# Learning to Adapt CLIP for Few-Shot Monocular Depth Estimation

> 出處：WACV 2024｜作者：Xueting Hu et al.（SUSTech、Pengcheng Laboratory）｜原文：[[raw/2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation/meta.md]]
> 程式碼：論文中未提供

## 一句話總結

在 [[DepthCLIP]] 的 zero-shot 架構上，每個場景類別只用 1 張影像做 [[Few-Shot-Learning|few-shot]] 訓練，學習 [[Prompt-Tuning|learnable prompt]] 與依場景切換的 learnable depth codebook（[[Depth-Bins]]）（Abstract, §1）。

## Introduction

### 研究背景
- [[CLIP]] 以 4 億組 image-text pair 做 contrastive learning，分別以 image encoder 與 text encoder 取得特徵，再以 cosine similarity 判斷配對（§1）。
- 傳統機器學習與深度學習的 MDE 方法都需要大量資料，且計算成本高、訓練耗時（§1）。
- [[DepthCLIP]] 以 CLIP 做 zero-shot MDE：影像 patch 與一組深度描述計算相似度，再與人工設定的深度值加權求和，得到深度（§1）。
  - 深度描述的 prompt 為「This object is [Depth CLASS]」，[Depth CLASS] 包含 giant、extremely close、close、not in distance、a little remote、far、unseen 共 7 類，各自對應一個人工設定的距離，例如 unseen 可能代表 5 m（§3.3）。

### 現有方法的問題
- 不同場景的影像有不同的深度分布，例如 bathroom 與 bedroom（Fig. 1a）（§1）。
- DepthCLIP 預先固定每個深度描述對應的深度值，在某些場景表現好、在其他場景則不理想，泛化能力有限（§1, Fig. 1b）。
- 為人類理解設計的 prompt（符合英文語法）對模型而言不一定直觀（§3.3）。
- Fully-supervised 方法（如 DepthFormer）需要收集完整標註資料，成本高、擴展性受限（§2）。

### 動機與貢獻
- 目標：在耗時的 supervised 方法與泛化有限的 zero-shot 方法之間取得平衡，設計 few-shot 方法（§1）。
- 視覺面：以整張影像的 scene feature 選擇最適合的 depth bin（depth codebook），以 patch feature 做局部預測（§1）。
- 文字面：以簡單網路把「人看得懂」的文字轉成「模型看得懂」的向量（learnable prompt）（§1）。
- 貢獻（§1）：
  1. 在新的 few-shot 設定下，以 vision-language model 做 MDE。
  2. 針對不同場景深度分布不同的問題，設計 learnable prompt 與 learnable depth codebook。
  3. 每個場景只用 1 張影像訓練，在 [[NYU-Depth-V2]] 上 MARE 比先前 state-of-the-art 最多改善 10.6%，甚至可與部分 fully-supervised 方法比較。

## Method

### 整體架構（Fig. 2）
- 三個 encoder 都來自 CLIP（ResNet-50 backbone）（Fig. 2）：
  - **Text encoder**：直接使用 CLIP 的 text encoder。
  - **Scene encoder**：直接使用 CLIP 的 image encoder，輸出整張影像的 scene feature F_s。
  - **Visual encoder**：CLIP 的 ResNet-50 image encoder 但去掉最後的 pooling layer，輸出 patch 特徵 F_v。
- 只有 learnable prompt 與 depth codebook 會在 few-shot 訓練中更新（Fig. 2 的火焰圖示）（Fig. 2）。
- 流程（§3.2）：
  1. 訓練前：每個場景類別取 1 張影像送入 scene encoder，得到一組 class-specific scene features；所有深度描述送入 text encoder，得到一組 text features。
  2. 輸入影像經 visual encoder 得到 F_v，經 scene encoder 得到 F_s。
  3. F_v 與 text features 計算 cosine similarity，normalize 後得到每個 patch 的 depth weight。
  4. F_s 與 scene features 計算 cosine similarity，找出最相似的場景，以 one-hot 從 depth codebook 選出對應的 depth bin。
  5. Depth weight 與 depth bin 加權求和，得到每個 patch 的深度；同一 patch 內所有像素深度相同。

### Learnable prompt（§3.3）
- 把「This object is」這幾個字換成可學習的向量 V = [v1, …, vn]，n 是超參數，不需與原本的字數相同（§3.3）。
- 輸入文字的形式為「[Vector] + [Class]」：K 個深度類別各自以 token m1, …, mK 表示，與共用的 V 串接成 K 個 prompt（Eq. 1）（§3.3）。
- 每個 prompt 經 CLIP text encoder 得到 text feature F*_t,i（Eq. 2）。
- 以預測深度與 ground truth 的 RMSE 作為 loss 更新 prompt 向量（Eq. 3）。
- 概念見 [[Prompt-Tuning]]（與 CoOp 同類作法）。

### Learnable depth codebook（§3.4）
- Depth codebook Θ 負責把離散的分類結果轉成深度值；每個場景類別在 codebook 中有一個 depth bin（§3.4）。
- 做法（§3.4, Eq. 4–8）：
  1. Few-shot 用的場景影像 S_j 經 scene encoder 得到 class-specific features F*_s,j（j = 1, …, N，N 為場景數）。
  2. 輸入影像 I 經 scene encoder 得到 F_s。
  3. 計算 F_s 與各 F*_s,j 的 cosine similarity，取最大者 j* 為場景類別。
  4. 選出 codebook 第 j* 列作為本張影像的 depth bin θ*。
- Codebook 先給初始值，再以 Eq. 3 的 RMSE loss 更新（§3.4）。
- NYU V2 的設定：codebook 初始大小 27 × 7（27 個場景類別 × 7 個深度描述），7 個描述的初始深度值皆為 1.00、1.50、2.00、2.25、2.50、2.75、3.00（§4.2）。
- 概念見 [[Depth-Bins]]。

### Depth prediction（§3.5）
- 輸入影像經 visual encoder 得到 F_v ∈ R^(H×W×C)，H×W 為 patch 數（Eq. 9）（§3.5）。
- 計算每個 text feature F*_t,i 與 F_v 的 cosine similarity，得到相似度 s^v（Eq. 10）。
- s^v 經 softmax 得到 depth weight d ∈ R^(H×W×K)：每個 patch 在 K 個深度類別上的機率分布（Eq. 11）。
- 最終深度：d̂ = θ* · dᵀ，也就是以 depth weight 對選出的 depth bin 加權求和（Eq. 12）。
- 預測以 patch 為單位，同一 patch 內的像素深度相同（§3.5）。

## Experimental Results

### 設定（§4.1–4.3）
- 資料集（§4.1）：
  - [[NYU-Depth-V2]]：室內，影像 480 × 640，深度 0～10 m；測試集 654 張；裁切為 416 × 512。
  - [[KITTI]]：室外，影像 375 × 1242；採 ASTransformer 的切分，訓練 23,488 張、測試 697 張；裁切為 352 × 704；深度範圍 0～80 m（Table 2）。
- 實作（§4.2）：
  - 以 PyTorch 實作，基於預訓練的 ResNet-50 CLIP；learnable prompt 隨機初始化。
  - 每個場景類別選 1 張影像參與訓練（NYU V2 共 27 張；KITTI 也只用 27 張，見 Table 2 說明）。
  - Learning rate：prompt 0.5、depth codebook 0.01，decay 1 × 10⁻⁵；訓練 200 epochs；單張 RTX 3090。
- 評估指標（§4.3）：MARE、MSRE、AELS、RMSE 與 threshold accuracy δ（[[Depth-Metrics]]）。

### NYU Depth V2（Table 1）

| Method | Pre-training | Supervision | δ<1.25 ↑ | δ<1.25² ↑ | δ<1.25³ ↑ | MARE ↓ | AELS ↓ | RMSE ↓ |
|---|---|---|---|---|---|---|---|---|
| Make3D | – | full | 0.447 | 0.745 | 0.897 | 0.349 | – | 1.214 |
| DepthFormer | – | full | 0.921 | 0.989 | 0.998 | 0.096 | 0.041 | 0.339 |
| LORN | ImageNet-1k | few-shot† | 0.703 | 0.923 | 0.979 | 1.008 | 0.222 | – |
| Lower Bound | – | – | 0.140 | 0.297 | 0.471 | 1.327 | 0.323 | 2.934 |
| [[DepthCLIP]] | CLIP | 0-shot | 0.394 | 0.683 | 0.851 | 0.388 | 0.156 | 1.167 |
| **Ours** | CLIP | 1-shot | **0.428** | **0.732** | **0.898** | **0.347** | **0.140** | **1.049** |

（節錄，完整比較見 Table 1；† LORN 使用 200 張影像與 2,500 張部分影像訓練。）

- Lower Bound：在 0～10 m 內對每個像素隨機預測（Table 1）。
- 相對 DepthCLIP 所有指標都改善；MARE 0.388 → 0.347，約為摘要所說的「最多改善 10.6%」（Abstract, Table 1）。
- 優於 vid2depth、Zhang et al. 等在 KITTI video 上預訓練的 zero-shot 方法（§4.4）。
- 可與 fully-supervised 的 Make3D 相比，部分指標超越：RMSE 1.049 vs. 1.214（§4.4）。
- 與 DepthFormer 等現代 supervised 方法仍有很大差距（Table 1）。
- 與 [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] 不同：DepthFormer 在 NYU V2 的數值，本篇為 δ<1.25 0.921、AbsRel 0.096、RMSE 0.339，WorDepth Table 1 為 0.923、0.094、0.329。

### KITTI（Table 2）

| Method | Supervision | δ<1.25 ↑ | δ<1.25² ↑ | δ<1.25³ ↑ | MARE ↓ | MSRE ↓ | RMSE ↓ | AELS ↓ |
|---|---|---|---|---|---|---|---|---|
| DepthFormer | full | 0.975 | 0.997 | 0.999 | 0.052 | 0.158 | 2.143 | 0.079 |
| [[DepthCLIP]] | 0-shot | 0.281 | 0.531 | 0.696 | 0.473 | 6.007 | 12.958 | 0.680 |
| **Ours** | 1-shot | **0.312** | **0.569** | **0.739** | **0.384** | **4.661** | **12.290** | **0.632** |

（節錄，完整比較見 Table 2。）

- DepthCLIP 的 depth bin 由作者手動調整；本方法的 depth bin 可學習，只需隨機初始化（Table 2 說明）。
- 本方法仍大幅優於 DepthCLIP（§4.4），但絕對誤差仍高（RMSE 12.290 m）。

### 效率比較（Table 5）

| Method | Supervision | Time | Params. | RMSE ↓ |
|---|---|---|---|---|
| DORN | full | > 30 h | 51M | 0.509 |
| [[DepthCLIP]] | 0-shot | 0 | 0 | 1.147 |
| **Ours** | 1-shot | 70 min | 8K | **1.049** |

- 本方法只更新 8K 參數、以 27 張影像訓練 70 分鐘，RMSE 低於 DepthCLIP（§4.6, Table 5）。

### Ablation（Table 3–4）
NYU V2 上的元件分析（Table 3）。欄位標題依原文為「MARE、RMSE、AELS」，但數值與 Table 1 對照後疑似 RMSE 與 AELS 對調（見 [[#論文內的不一致]]），以下以對調後的意義標示：

| Method | δ<1.25 ↑ | MARE ↓ | AELS ↓（原文標 RMSE） | RMSE ↓（原文標 AELS） |
|---|---|---|---|---|
| Baseline（DepthCLIP） | 0.394 | 0.388 | 0.156 | 1.167 |
| + Learnable Prompt | 0.429 | 0.386 | 0.145 | 1.076 |
| + Learnable Prompt + Learnable Depth Bin | 0.433 | 0.378 | 0.143 | 1.066 |
| + Learnable Prompt + Learnable Depth Codebook | 0.428 | 0.347 | 0.140 | 1.049 |

- 「Learnable Depth Bin」：所有場景共用一個 class-independent depth bin；「Depth Codebook」：每個場景各有一個 class-dependent depth bin（Table 3 說明）。
- Learnable prompt 明顯提升表現（§4.6）。
- Depth codebook 取代單一 depth bin 後，除了 δ<1.25 以外所有指標都改善（§4.6）。

Patch size（Table 4，欄位同樣疑似對調）：

| Patch size | δ<1.25 ↑ | MARE ↓ | AELS ↓（原文標 RMSE） | RMSE ↓（原文標 AELS） |
|---|---|---|---|---|
| 8 × 8 | 0.336 | 0.379 | 0.179 | 1.300 |
| 16 × 16 | 0.354 | 0.514 | 0.172 | 1.229 |
| 32 × 32 | 0.428 | 0.347 | 0.140 | 1.049 |

- ResNet-50 CLIP 輸出特徵為輸入大小除以 32，因此自然採用 32；8、16 以 encoder 中間層特徵實驗，32 × 32 最好（§4.6）。

### 定性結果（Fig. 3）
- 在 NYU V2 的三張影像上，本方法的深度預測都比 DepthCLIP 好，特別是紅框區域（§4.5, Fig. 3）。

## Conclusions

### 結論（§5）
- 提出以 few-shot 調整 CLIP 做 MDE 的方法，在訓練成本與泛化能力之間取得平衡。
- 為不同場景指派不同的 depth bin，推論時由模型選擇；並以 learnable prompt 把人類文字轉為模型易理解的向量。
- 每個場景只用 1 張影像訓練，在 NYU V2 與 KITTI 上比先前 state-of-the-art 最多改善 10.6%。

### 限制（補充）
論文沒有獨立的限制段落，以下為依實驗結果的觀察：
- 與現代 fully-supervised 方法仍有很大差距：NYU V2 的 δ<1.25 為 0.428，DepthFormer 為 0.921（Table 1）。
- 以 patch 為單位預測，同一 patch 內深度相同，深度圖解析度粗（§3.5）；patch size 受限於 ResNet-50 的 32 倍下採樣（§4.6）。
- 需要事先定義場景類別，並為每個類別準備訓練影像（§3.4, §4.2）。
- KITTI 上絕對誤差仍高（RMSE 12.290）（Table 2）。

### 論文內的不一致
閱讀時發現以下前後不一致，引用數值時需注意：
- **Table 3、Table 4 欄位疑似對調**：欄位標題為「MARE、RMSE、AELS」，但 Baseline 列的 0.388、0.156、1.167 與 Table 1 中 DepthCLIP 的 MARE、AELS、RMSE 相同，因此 RMSE 與 AELS 的標題疑似對調。
- **Eq. 13–14 公式疑似對調**：MARE（mean absolute relative error）的公式分子有平方，MSRE（mean squared relative error）的公式反而沒有平方。
- **DepthCLIP 的 NYU V2 RMSE**：Table 1 為 1.167，Table 5 為 1.147。
- **Table 2 中的 ASTransformer**：KITTI 的 MARE 0.103 與 AELS 0.374，與 Table 1 中 ASTransformer 在 NYU V2 的 MARE 0.103、RMSE 0.374 相同，疑似誤植。
- **實驗範圍描述**：摘要與結論說在 NYU V2 與 KITTI 都有實驗，貢獻第 3 點只寫 NYU V2。

## 相關頁面
- Concepts：[[Few-Shot-Learning]]、[[Prompt-Tuning]]、[[Depth-Bins]]、[[Vision-Language-Model]]
- Entities：[[DepthCLIP]]、[[CLIP]]、[[NYU-Depth-V2]]、[[KITTI]]、[[Depth-Metrics]]
- Papers：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]]（同樣以 CLIP text encoder 引入語言資訊，但作為 variational prior）
