---
type: paper
tags: [mde, vision-language, prompt-tuning, depth-bins]
sources: [2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language, 2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation, 2026_CLIP-Can-Understand-Depth]
updated: 2026-11-19
---

# Learning to Prompt CLIP for Monocular Depth Estimation: Exploring the Limits of Human Language

> 出處：ICCV Workshops 2023｜作者：Dylan Auty, Krystian Mikolajczyk（Imperial College London）｜原文：[[raw/2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language/meta.md]]
> 程式碼：https://github.com/DylanAuty/PromptLearningCLIP-MDE
> 其他論文稱本篇方法為 [[CLIPMDE]]（WorDepth）或「Auty et al.」（Hu et al.、CLIP2Depth）。

## 一句話總結

把 [[DepthCLIP]] prompt 中的人類距離詞換成可學的 depth token，[[CLIP]] 完全 frozen、只學幾千個參數就大幅提升表現；而學到的 token 大多不對應任何英文詞，表示 CLIP 的「深度」概念難以用人類語言簡潔表達（Abstract, §1, §5）。

## Introduction

### 研究背景
- MDE 是 poorly-posed 問題：同一張 2D 影像可能來自無數 3D 場景，需要場景脈絡與先驗知識（§1）。
- CLIP 以 4 億張附文字說明的影像訓練，學到大量關於世界的一般知識，可用於分類、captioning、VQA 等 low/zero-shot 任務（§1）。
- DepthCLIP 把 MDE 改寫成 image patch 對 depth bin 的 zero-shot 序數分類：每個 bin 對應一句「This object is [near/far/…]」的 prompt，依相似度加權 bin 中心得到連續深度（§1）。

### 現有方法的問題
- **Human bias**：每個深度刻度用哪個詞是人工選的，而且 prompt 本身就是文字（§1）。
- CLIP 的訓練資料是一般影像說明，很少討論深度；它對深度的理解可能是隱性的，無法明確用文字表達（§1）。
- **Bin 數受限**：人類語言是離散的，序數刻度越細，描述就越冗長彆扭，因此能用的 bin 數有限（§1）。

### 動機與貢獻
- 以不受人類語言束縛的 learnable prompt token 取代人工選擇的距離詞，並分析學到的 embedding，理解 CLIP 如何理解深度（§1）。
- 貢獻（§1）：
  1. 首次以 learnable prompt token 讓 CLIP 做 MDE，去除人類語言造成的 bias。
  2. 大量實驗尋找最佳 prompt 策略：depth-bin prompt 數量、learnable context token、bin 分布。
  3. 分析學到的 prompt，提供「人類語言不足以精確向 CLIP 表達深度」的證據。

## Method

### 整體架構（Fig. 1）
- 流程與 DepthCLIP 相同，只把 CLIP text encoder 換成可插入 learnable token 的版本（Fig. 1, §3）。
- 流程（Fig. 1）：
  1. N 個 depth prompt（每個 bin 一個）：「This object appears to be {depth_tkn_n}」→ Modified CLIP Text Encoder → 文字特徵 txt_f（C × N）。
  2. 輸入影像 → frozen CLIP Img Encoder → 影像特徵 img_f（C × H/32 × W/32），攤平成 HW/32 個 patch。
  3. img_f 與 txt_f 做 inner product → prompt logits。
  4. prompt logits 乘上 N 個固定的 depth 中心 [c0, …, cn] 並加總。
  5. Reshape 後以 bilinear resize 放大到輸入解析度，得到深度圖。
- 預訓練 CLIP 完全 frozen，只訓練 learnable token（Fig. 1）。
- 輸出刻意保持低解析度：目的是測試 CLIP 本身的理解極限，避免專門訓練的 decoder 混淆結論（Fig. 1）。

### Learnable depth token（§3.1, Fig. 2）
- CLIP 原本把 prompt 中的每個詞查表成 frozen 的 512 維 token，再送入 transformer（§3.1）。
- 本篇修改 tokenizer：prompt 中的特殊詞（如 depth_tkn_n）被替換成可學參數（nn.Parameter）；CLIP 的 token embedding 與 transformer 仍 frozen（§3.1, Fig. 2）。
- 作法沿用 CoOp 的技巧（[[Prompt-Tuning]]）；learned token 以平均 0、標準差 0.02 的常態分布初始化（§3.1）。
- Prompt 模板（Table 1, §3.3）：

| 名稱 | 模板 |
|---|---|
| Baseline | 「This object appears to be {depth_tkn}.」 |
| 1o1d | 「{p_0} object {p_1} {depth_tkn}.」 |
| 1o2d | 「{p_0} object {p_1} {p_2} {depth_tkn}.」 |
| 4o4d | 「{p_0} {p_1} {p_2} {p_3} object {p_4} {p_5} {p_6} {p_7} {depth_tkn}.」 |

- {p_i} 為 learnable context token，所有 bin 的 prompt 共用；只有 {depth_tkn} 隨 bin 改變（Table 1, §3.3）。

### 輸出與訓練（§3.2, §4.1）
- 影像經去掉最後 pooling 的 CLIP image encoder，得到 patch 特徵；RN50 的通道數 C 為 1024（§3.2）。
- 影像與文字特徵做 inner product 並正規化，得到 N × H/32 × W/32 的 depth-bin logits；乘上預先固定的 N 個 bin 中心（公尺）並沿 N 加總，得到 1 × H/32 × W/32 的低解析度深度圖，再雙線性上採樣（§3.2）。
- 訓練（§4.1）：
  - Loss：Scale-Invariant Log loss（SILog）的變體（Eq. 1），參見 [[Scale-Invariant-Loss]]。
  - 25 epochs、batch size 16、AdamW、learning rate 0.000357、OneCycleLR；超參數沿用 [[AdaBins]]。
  - 所有實驗使用 CLIP ResNet-50（作者引用多篇研究，認為 ResNet 版比 ViT 版更能抽出空間相關特徵）。
- 資料（§4.1.2）：
  - [[NYU-Depth-V2]]：24231 張訓練、654 張測試；訓練隨機裁切 416 × 544，以 Eigen crop 評估。
  - [[KITTI]]：23157 張訓練、696 張測試；訓練隨機裁切 352 × 704。
  - 切分直接取自 AdaBins 的官方實作。
- 評估使用 test-time augmentation：原圖與水平翻轉的預測取平均（§4.1.3）。

## Experimental Results

### Learned vs. human-language tokens（Table 3）
- 設定：7 個 bin 平均分布於資料集範圍（NYUv2 [0.001, 10.0] m、KITTI [0.001, 80.0] m），使用 Baseline 模板（§4.2）。
- 比較的 7 點人類語言刻度（Table 2）：
  - **depth-7**：very close、close、slightly close、neither close nor distant、slightly distant、distant、very distant。
  - **size-7**：very small … very large（透過透視與深度相關）。
  - **colour-7**：very red … very green（與深度無關的對照組）。
- 另有兩個隨機對照：random-7（固定的隨機向量）、rand-txt-7（從 CLIP 字彙隨機選詞）（§4.2）。

| Depth tokens | Dataset | Abs ↓ | RMS ↓ | δ1 ↑ |
|---|---|---|---|---|
| colour-7 | NYUv2 | 1.381 | 3.010 | 0.131 |
| size-7 | NYUv2 | 2.130 | 4.431 | 0.048 |
| depth-7 | NYUv2 | 1.014 | 2.413 | 0.227 |
| random-7 | NYUv2 | 1.593 | 3.308 | 0.081 |
| rand-txt-7 | NYUv2 | 1.335 | 2.875 | 0.129 |
| **learned-7** | NYUv2 | **0.319** | **0.970** | **0.465** |
| colour-7 | KITTI | 2.177 | 23.470 | 0.077 |
| size-7 | KITTI | 3.363 | 33.978 | 0.048 |
| depth-7 | KITTI | 2.353 | 25.518 | 0.094 |
| random-7 | KITTI | 1.664 | 19.279 | 0.119 |
| rand-txt-7 | KITTI | 2.887 | 29.553 | 0.046 |
| **learned-7** | KITTI | **0.303** | **6.322** | **0.550** |

（節錄，完整欄位見 Table 3。learned-7 的其餘指標：NYUv2 RMSL 0.139、log10 0.128、δ2 0.776、δ3 0.922；KITTI RMSL 0.119、log10 0.112、δ2 0.830、δ3 0.938。）

- 每個 prompt 只用一個 learned token（共 512 × 7 = 3584 個參數）就讓表現提升 1.5～5.5 倍（§4.2）。
- 與深度相關的人類詞不一定最好：KITTI 上 random-7 勝過所有人類詞；NYUv2 上 colour-7 勝過 size-7（§4.2）。
- 作者推測原因是人類語言普遍不適合描述隱性而複雜的深度概念（§4.2）。

### Context tokens（Table 4–5）
- 在人類詞 depth-7 上加入 learnable context token {p_i}，表現大幅提升，且 context token 越多越好（Table 4, §4.3）：

| 模板 | Dataset | Abs ↓ | RMS ↓ | δ1 ↑ |
|---|---|---|---|---|
| Baseline（depth-7） | NYUv2 | 1.014 | 2.413 | 0.227 |
| 4o4d（depth-7） | NYUv2 | 0.318 | 0.965 | 0.466 |
| Baseline（depth-7） | KITTI | 2.353 | 25.518 | 0.094 |
| 4o4d（depth-7） | KITTI | 0.309 | 6.334 | 0.541 |

- Context token 在各 bin 之間共用，並不提供區分 bin 的資訊，卻仍有幫助，與 CoOp 在分類上的發現一致（§4.3）。
- 同時學 context token 與 depth token（ls4o4d + learned-7）：NYUv2 只小幅改善（Abs 0.317、RMS 0.955），KITTI 與只學 depth token 差不多（Abs 0.307、RMS 6.209），表示多數效益來自 learned depth token（Table 5, §4.3）。

### Bin 數量與分布（Table 6–7）
- Learned token 解除了 bin 數的限制；深度分布通常是長尾，因此比較 linear 與 log-uniform 分布（§4.4）。
- Log-uniform 在 KITTI（[0.001, 80] m）明顯較好；NYUv2 範圍只有 10 m，log-uniform 的 bin 擠在範圍前端，優勢不明顯（Table 6, §4.4）。
- Bin 數越多越好（log-uniform、learned token）（Table 7）：

| Bins | Dataset | Abs ↓ | RMS ↓ | δ1 ↑ |
|---|---|---|---|---|
| 7 | NYUv2 | 0.312 | 0.991 | 0.449 |
| 20 | NYUv2 | 0.308 | 0.968 | 0.466 |
| 256 | NYUv2 | **0.298** | **0.933** | **0.485** |
| 7 | KITTI | 0.265 | 6.933 | 0.580 |
| 20 | KITTI | 0.265 | 6.153 | 0.606 |
| 256 | KITTI | **0.238** | **5.756** | **0.652** |

- 每多一個 bin 增加 512 個可學參數（§4.4）。

### Learned token 的解讀（Table 8）
- 方法：把 CLIP 字彙中約 4 萬個 token 代入「This object appears to be {token}.」，在 CLIP embedding 空間找每個 learned depth token 的最近鄰（§4.5）。
- 發現（Table 8, §4.5）：
  - 7 個 learned token（NYUv2、平均分布；token 0 約對應 0.714 m、token 6 約 9.29 m）中，只有 token 1 最接近「close」、token 6 最接近「distant」。
  - 其餘 token 的最近鄰都是其他 learned token，而且數值大的 token 靠近數值大的 token，彷彿在 latent space 中排成一條代表遠近的路徑。
  - 若只有兩個 token 有意義、其他無關，增加 bin 數應無幫助；但 bin 數增加確實持續提升表現，表示其他 token 也帶有無法用語言表達的深度資訊。

## Conclusions

### 結論與未來方向（§5）
- Learnable token 只用幾千個參數，就比幾何相關的人類詞與隨機 token 大幅提升 CLIP 的 MDE 表現。
- 學到的 token 在 CLIP embedding 中與深度相關的人類 prompt 不相似，表示深度概念無法用人類語言簡潔表達。
- 意涵：以人工選擇的 prompt 存取 CLIP 的知識可能不是最佳；其他抽象概念或許也需要非語言的 learnable token。
- 未來方向：進一步研究 CLIP embedding 空間，把複雜幾何概念轉成 CLIP 能理解的 token，並把 CLIP 特徵解讀成人類可讀的形式。

### 限制（補充）
論文沒有獨立的限制段落，以下為依方法設計與實驗的觀察：
- 輸出為 H/32 × W/32 的低解析度深度圖再雙線性放大，細節有限（§3.2, Fig. 1）。
- 雖然只學幾千個參數，但仍在完整訓練集（NYUv2 24231 張、KITTI 23157 張）上訓練，並非 zero/few-shot（§4.1.2）。
- Bin 中心在實驗開始時就固定，不像 [[AdaBins]] 依影像調整（§3.2, §4.4）。

### 論文內的不一致與跨論文差異
- **WorDepth 引用的 log10 有誤**：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] Table 1 列 CLIPMDE 在 NYUv2 的 log10 為 0.139，但本篇 Table 3 中 0.139 是 RMSL，log10 為 0.128。[[2026_CLIP-Can-Understand-Depth|CLIP2Depth]] Table 3 列的 log10 0.128 與本篇一致（補充：由兩篇論文的表格比對）。
- **SILog 的形式**：Eq. 1 根號內第二項為「+ 0.15/K² (Σ g_i)²」；Eigen et al. 與 AdaBins 常見的寫法是減去 λ 倍的平方和項（補充），本篇未說明差異。
- **KITTI 測試張數**：本篇為 696 張；WorDepth 為 697 張（清除後 652 張）、Hu et al. 為 697 張。

## 相關頁面
- Concepts：[[Prompt-Tuning]]、[[Depth-Bins]]、[[Vision-Language-Model]]、[[Scale-Invariant-Loss]]
- Entities：[[CLIPMDE]]、[[DepthCLIP]]、[[CLIP]]、[[NYU-Depth-V2]]、[[KITTI]]、[[AdaBins]]
- Papers：[[2022_Can-Language-Understand-Depth]]（前作）、[[2026_CLIP-Can-Understand-Depth]]（後續）
