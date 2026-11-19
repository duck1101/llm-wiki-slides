---
type: paper
tags: [mde, zero-shot, vision-language, depth-bins]
sources: [2022_Can-Language-Understand-Depth, 2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]
updated: 2026-11-19
---

# Can Language Understand Depth?

> 出處：ACM MM 2022｜作者：Renrui Zhang, Ziyao Zeng et al.（Peking University、ShanghaiTech University）｜原文：[[raw/2022_Can-Language-Understand-Depth/meta.md]]
> 程式碼：https://github.com/Adonis-galaxy/DepthCLIP
> 本篇提出的方法即 [[DepthCLIP]]。

## 一句話總結

[[DepthCLIP]] 不需任何訓練，把 [[CLIP]] 的影像 patch 與「This object is [distance class]」的深度描述做相似度，再對固定的 [[Depth-Bins|depth bins]] 加權求和，首次以 CLIP 做 [[Zero-Shot-Transfer|zero-shot]] MDE（Abstract, §1）。

## Introduction

### 研究背景
- CLIP 在 zero/few-shot 影像分類、物體偵測、語意分割等任務表現亮眼，但這些任務只需要從高層次「辨識」視覺訊號（§1）。
- 在偵測中 CLIP 只負責物體層級的分類而非定位；至今沒有工作用 CLIP 處理預測連續數值的量化任務（§2）。
- Supervised MDE 需要稠密深度標註，從頭訓練成本高、標註大型資料集（如 NYUV2）昂貴（§1）。
- Unsupervised MDE 需要額外資料（單眼影片、雙目影像）或 3D prior（§1–2）。

### 現有方法的問題
- CLIP 的對比式預訓練不太可能學到回歸數值的知識，因此無法直接從 CLIP 輸出深度（§1）。
- 先前所有 MDE 方法都需要額外的視覺資料或幾何 prior（§2）。

### 動機與貢獻
- 核心問題：能否利用 CLIP 學到的語意語言知識，同時省下訓練模型與收集資料的成本（§1）？
- 想法：把深度回歸改成距離分類——CLIP 只需理解「the object is close/far」，不需理解「the object is 5 meters away」（§1）。
- 貢獻（§1）：
  1. 提出 DepthCLIP，首個從語意語言知識 zero-shot 遷移到 MDE 的方法。
  2. 在 CLIP 的語意知識與量化深度預測之間建立橋樑。
  3. 在 [[NYU-Depth-V2]] 上超越既有 unsupervised 方法，並接近部分 fully-supervised 模型。

## Method

### 整體架構（Fig. 2）
- 兩個 encoder 都來自預訓練的 CLIP（ResNet-50），完全不訓練（Fig. 2, §4.2）。
- 流程（Fig. 2）：
  1. Prompt「This Object is [CLASS]」的 [CLASS] 依序填入 K 個距離詞（giant、close、…、far、unseen），經 Textual Encoder 得到 K 個 Text Features。
  2. 輸入影像經 Visual Encoder 得到 H × W 的 Image Features。
  3. Text Features 與 Image Features 做 dot product，得到 Similarity Scores（H × W × K）。
  4. SoftMax 得到 Depth Weights（H × W × K）。
  5. Depth Weights 與固定的 Depth Bins（K 個深度值）做 Weighted Sum，得到 Depth Predictions。

### Image encoding 與 text encoding（§3.1–3.2）
- **Image encoding**：影像送入去掉最後 pooling layer 的 visual encoder，得到最後一層的 C 維特徵圖 F_img ∈ R^(HW×C)（Eq. 1）。pooling 前的每個位置保留了周圍的區域語意，因此可以各自被文字回應、得到深度（§3.1）。
- **Text encoding**：以「This object is [distance class]」為 prompt，代入 K 個距離詞，經 CLIP textual encoder 得到 F_text ∈ R^(K×C)（Eq. 2）（§3.2）。
- 兩者計算 cosine similarity，得到 S ∈ R^(K×HW)（Eq. 3）（§3.2）。

### Depth projection（§3.3）
- 以 temperature softmax 把相似度轉成線性組合權重 W（Eq. 4）；temperature 設為 0.1（§3.3, §4.2）。
- 以 W 對 depth bins d 加權求和得到每個位置的深度 D_pred（Eq. 5）；同一 patch 內所有像素深度相同（§3.3）。
- 主實驗設定（§4.2）：
  - 7 個距離詞：giant、extremely close、close、not in distance、a little remote、far、unseen。
  - 對應深度值：1.00、1.50、2.00、2.25、2.50、2.75、3.00（公尺）。
  - 選擇理由：這樣的語意與深度 bin 數量能適當涵蓋室內深度範圍。

## Experimental Results

### 設定（§4.1–4.3）
- [[NYU-Depth-V2]]：Microsoft Kinect 拍攝的 464 個室內場景，影像 480 × 640，深度 0～10 m；訓練集 36,253 張（249 個場景）、測試集 654 張（215 個場景）；裁切為 416 × 512（§4.1）。
- 以 PyTorch 實作，image 與 textual encoder 皆為 CLIP 預訓練的 ResNet-50（§4.2）。
- 指標：rel、rmse、log10、threshold accuracy δ（§4.3, [[Depth-Metrics]]）。

### NYU Depth V2（Table 1）

| Method | Pre-training | Supervision | δ<1.25 ↑ | rel ↓ | log10 ↓ | rmse ↓ |
|---|---|---|---|---|---|---|
| Make3D | – | depth | 0.447 | 0.349 | – | 1.214 |
| DORN | – | depth | 0.828 | 0.115 | 0.051 | 0.509 |
| DepthFormer | – | depth | 0.921 | 0.096 | 0.041 | 0.339 |
| Lower Bound | – | – | 0.140 | 1.327 | 0.323 | 2.934 |
| vid2depth | KITTI video | 0-shot | 0.268 | 0.572 | – | 1.637 |
| Zhang et al. | KITTI video | 0-shot | 0.350 | 0.513 | 0.529 | 1.457 |
| **DepthCLIP** | CLIP | 0-shot | **0.394** | **0.388** | **0.156** | **1.167** |

（節錄，完整比較見 Table 1。）

- Lower Bound：在 0～10 m 內對每個像素隨機預測（§4.4）。
- 與 fully-supervised 方法仍有差距，但大幅超越 lower bound，也超越在 KITTI 影片上預訓練的 zero-shot 方法（§4.4）。
- 接近 fully-supervised 的 Make3D，rmse 甚至較低（§4.4）。
- 本篇 DepthFormer 的數值（0.921、0.096、0.339）與 [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation|Hu et al.]] Table 1 相同，與 [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] Table 1（0.923、0.094、0.329）不同。

### Class-dependent depth bin（Table 2）
- 不同場景的深度分布不同（Fig. 3）；CLIP 能抓到同一張影像內的相對遠近，但不同場景中距離不同的 patch 可能被對應到同一個語意概念，因此同一個距離詞應依場景對應到不同深度值（§4.5）。
- 因時間限制，主實驗所有場景共用同一組 bin；以 ablation 檢驗依場景切換 bin 的效果（§4.5）。

Bin 劃分（公尺）：

| 劃分 | 深度值 |
|---|---|
| Original | 1.00, 1.50, 2.00, 2.25, 2.50, 2.75, 3.00 |
| Class-dependent 3 | 1.00, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50 |
| Class-dependent 4 | 2.00, 2.50, 3.00, 3.25, 3.50, 3.75, 4.00 |

（節錄，Table 2 共有 Original 與 4 種 class-dependent 劃分。）

| 場景 | 劃分 | δ<1.25 ↑ | rel ↓ | rmse ↓ |
|---|---|---|---|---|
| Bathroom | Original | 0.333 | 0.549 | 0.922 |
| Bathroom | Class-dependent 3 | 0.425 | 0.373 | 0.745 |
| Classroom | Original | 0.308 | 0.372 | 1.826 |
| Classroom | Class-dependent 4 | 0.276 | 0.461 | 1.544 |
| All | Original | 0.394 | 0.388 | 1.167 |

- 依場景選擇劃分可明顯改善；不同場景的最佳劃分不同（§4.5）。
- 作者提出未來方向：學習依場景的 bin 劃分，並用 CLIP 做 zero-shot 場景分類來選擇對應的 bin（§4.5）。此方向後來由 [[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation|Hu et al.]] 的 learnable depth codebook 實現（補充）。

### Prompt design（Table 3）

| Prompt | 距離詞 | δ<1.25 ↑ | rel ↓ | rmse ↓ |
|---|---|---|---|---|
| Original | giant, extremely close, close, not in distance, a little remote, far, unseen | 0.394 | 0.388 | 1.167 |
| Prompt 1 | extremely close, close, middle, a little far, far, quite far, unseen | 0.341 | 0.379 | 1.274 |
| Prompt 2 | extremely close, very close, close, a little close, a little far, far, unseen | 0.377 | 0.385 | 1.196 |
| Prompt 3 | giant, close, a little close, not in distance, a bit remote, far, unseen | 0.380 | 0.375 | 1.196 |

- 不同 prompt 之間差距不大，遠不如 bin 劃分敏感；原因是不同距離詞語意相近（如 giant 與 extremely close），同一個 patch 會同時回應兩者（§4.6）。
- 作者認為方法對人工 prompt 設計具穩健性（§4.6）。

### Semantic bin responses（Fig. 4）
- 最後的特徵圖為 13 × 17，每個 patch 各自得到深度預測（§4.7）。
- 近處與遠處 patch 對距離詞的回應有明顯差異，這是 DepthCLIP 有效的基礎（§4.7, Fig. 4）。
- 預測深度圖略為模糊，較注重細節物體（如水龍頭、浴缸）（§4.8, Fig. 5）。

## Conclusions

### 結論（§6）
- 提出 DepthCLIP，以 CLIP 做 zero-shot MDE，不需要訓練，也不需要深度標註資料。
- 希望啟發「把語意視覺語言知識連到量化視覺任務」的研究。

### 限制（§5）
- 需要人工調整 depth bin；不同場景共用同一組 bin 時表現差。作者建議先用 CLIP 做 zero-shot 場景分類，再選擇依場景的 depth bin。
- CLIP 的 visual encoder 以類似分類的任務預訓練，偏重有助於分類的局部細節；缺乏分類特徵的大區域（牆、天花板、地板）語意深度回應弱。作者建議以分割或偵測等區域性任務預訓練 vision-language model。

### 論文內的不一致
- **rmse 數值**：§4.4 文字寫 DepthCLIP 的 rmse 為 1.186，Table 1 為 1.167。
- **圖表編號**：§4.5 寫「Shown as Table 3, images from different classes possess different depth distribution」，但不同場景深度分布的說明在 Fig. 3。
- **Fig. 4 的設定**：Fig. 4 的距離詞（a little close、a bit remote）與深度值（含 4.00 m）與主實驗設定不同，較接近 Prompt 3 與 Class-dependent 1。
- **Table 2 / Table 3 的「最佳」**：All classes 的 Class-dependent 3 rel 為 0.353，優於 Original 的 0.388，但 gain 列標示為「-」；Table 3 中三種替代 prompt 的 rel 也都低於 Original，文字卻說 Original 表現最好（δ 與 rmse 確實最好）。

## 相關頁面
- Concepts：[[Zero-Shot-Transfer]]、[[Depth-Bins]]、[[Prompt-Tuning]]、[[Vision-Language-Model]]
- Entities：[[DepthCLIP]]、[[CLIP]]、[[NYU-Depth-V2]]、[[Depth-Metrics]]
- Papers：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]]（延伸為 few-shot）、[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]]
