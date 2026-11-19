# Learning to Adapt CLIP for Few-Shot Monocular Depth Estimation — Slide Spec

## S1 · Cover
- 標題：Learning to Adapt CLIP for Few-Shot Monocular Depth Estimation
- 內容：
  - 作者：Xueting Hu, Ce Zhang, Yi Zhang, Bowen Hai, Ke Yu, Zhihai He
  - SUSTech · Pengcheng Laboratory｜WACV 2024
  - 一句話：在 DepthCLIP 上，每個場景類別只用 1 張影像訓練 learnable prompt 與依場景切換的 depth codebook
- 圖表：無
- 出處：Abstract, §1
- Wiki：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#一句話總結]]

## S2 · Introduction — 研究背景
- 標題：研究背景：用 CLIP 做 zero-shot 深度估計
- 內容：
  - CLIP 以 4 億組 image-text pair 做 contrastive learning，用 cosine similarity 判斷影像與文字是否配對
  - 傳統 supervised MDE 需要大量標註資料，計算成本高、訓練耗時
  - DepthCLIP（zero-shot）：
    - 影像 patch 與一組深度描述做相似度，再對人工設定的深度值加權求和
    - Prompt：「This object is [Depth CLASS]」
    - [Depth CLASS] 共 7 類：giant、extremely close、close、not in distance、a little remote、far、unseen
- 圖表：無
- 出處：§1, §3.3
- Wiki：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#研究背景]]

## S3 · Introduction — 問題與動機
- 標題：問題：固定的 depth bin 不適合所有場景
- 內容：
  - 現有問題：
    - 不同場景的深度分布不同（如 bathroom vs. bedroom），固定的深度值只在部分場景表現好
    - 為人類設計的 prompt 對模型不一定直觀
  - 動機：few-shot 介於 supervised（成本高）與 zero-shot（泛化有限）之間
  - 貢獻：
    - 在 few-shot 設定下用 vision-language model 做 MDE
    - Learnable prompt ＋ learnable depth codebook
    - 每個場景只用 1 張影像，NYU V2 上 MARE 比先前 SOTA 最多改善 10.6%
- 圖表：無
- 出處：§1, §3.3, Fig. 1
- Wiki：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#現有方法的問題]]、[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#動機與貢獻]]

## S4 · Method — 整體架構
- 標題：整體架構：三個 frozen CLIP encoder ＋ 兩個可學元件
- 內容：
  - 三個 encoder 都來自 CLIP（ResNet-50），全部 frozen
  - 只更新 learnable prompt 與 learnable depth codebook
  - 文字路徑決定每個 patch 屬於哪個深度類別（depth weights）
  - 場景路徑決定這張影像要用哪一組深度值（selected depth bin）
- 圖表：架構圖
  - 節點：Learnable Prompt（[V1…Vn] + class）、Textual Encoder、Text Features、Input Image、Visual Encoder、Image Feature、Softmax、Depth Weights、Scene Encoder（輸入影像用）、Scene Feature、Few-shot Training Images、Scene Encoder（訓練影像用，與前者為同一個 CLIP encoder，圖中畫成兩個方塊）、Class-specific Features、OneHot、Learnable Depth Codebook、Selected Depth Bin、Weighted Sum、Depth Predictions
  - 連線：Learnable Prompt → Textual Encoder → Text Features；Input Image → Visual Encoder → Image Feature；Text Features ⊙ Image Feature → Softmax → Depth Weights → Weighted Sum；Input Image → Scene Encoder（輸入影像用）→ Scene Feature；Few-shot Training Images → Scene Encoder（訓練影像用）→ Class-specific Features；Scene Feature ⊙ Class-specific Features → OneHot；OneHot ＋ Learnable Depth Codebook → Selected Depth Bin → Weighted Sum；Weighted Sum → Depth Predictions
  - 對照：Fig. 2
- 出處：Fig. 2, §3.2
- Wiki：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#整體架構（Fig. 2）]]

## S5 · Method — Learnable prompt
- 標題：Learnable prompt：把人類的句子換成模型的向量
- 內容：
  - DepthCLIP：「This object is」＋ [Depth CLASS]，人工撰寫
  - 本篇：把「This object is」換成可學向量 V = [v1, …, vn]，n 是超參數
  - 輸入形式「[Vector] + [Class]」：K 個深度類別共用 V，各自接上 class token
  - 每個 prompt 經 frozen CLIP text encoder 得到 text feature
  - 以預測深度與 ground truth 的 RMSE 作為 loss 更新 V
- 圖表：無
- 出處：§3.3, Eq. 1–3
- Wiki：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#Learnable prompt（§3.3）]]

## S6 · Method — Depth codebook 與深度預測
- 標題：Learnable depth codebook 與深度預測
- 內容：
  - Depth codebook：每個場景類別一組 depth bin
    - 輸入影像的 scene feature 與各場景特徵算 cosine similarity，取最相似者（one-hot）
    - 選出該場景的 depth bin θ*；NYU V2 為 27 類 × 7 個深度值
  - 深度預測：
    - Patch 特徵與 K 個 text feature 算相似度，softmax 得到 depth weight
    - 深度 = depth weight 對 θ* 加權求和
    - 以 patch 為單位，同一 patch 內像素深度相同
- 圖表：無
- 出處：§3.4–3.5, §4.2, Eq. 4–12
- Wiki：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#Learnable depth codebook（§3.4）]]、[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#Depth prediction（§3.5）]]

## S7 · Experimental Results — NYU Depth V2
- 標題：NYU Depth V2：明顯優於 DepthCLIP，但仍遠落後 supervised
- 內容：
  - 設定：27 個場景類別各 1 張影像訓練、200 epochs、單張 RTX 3090
  - 相對 DepthCLIP 所有指標都改善；MARE 0.388 → 0.347
  - 可與 fully-supervised 的 Make3D 相比，RMSE 1.049 vs. 1.214
  - 與 DepthFormer 等現代 supervised 方法差距仍大
- 圖表：表格（Table 1 節錄）
  - 欄：Method、Supervision、δ<1.25 ↑、MARE ↓、RMSE ↓
  - Make3D｜full｜0.447｜0.349｜1.214
  - DepthFormer｜full｜0.921｜0.096｜0.339
  - Lower Bound｜—｜0.140｜1.327｜2.934
  - DepthCLIP｜0-shot｜0.394｜0.388｜1.167
  - Ours｜1-shot｜0.428｜0.347｜1.049（強調）
- 出處：Table 1, §4.2, §4.4
- Wiki：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#設定（§4.1–4.3）]]、[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#NYU Depth V2（Table 1）]]

## S8 · Experimental Results — KITTI 與效率
- 標題：KITTI 與訓練成本
- 內容：
  - KITTI：仍大幅優於 DepthCLIP，但絕對誤差高（RMSE 12.290）
  - DepthCLIP 的 depth bin 由作者手動調整；本方法的 depth bin 可學
  - 效率：只更新 8K 參數、27 張影像訓練 70 分鐘
- 圖表：兩個表格
  - Table 2 節錄（KITTI），欄：Method、δ<1.25、MARE、RMSE
    - DepthFormer｜0.975｜0.052｜2.143
    - DepthCLIP｜0.281｜0.473｜12.958
    - Ours｜0.312｜0.384｜12.290（強調）
  - Table 5（NYU V2），欄：Method、Time、Params.、RMSE
    - DORN｜> 30 h｜51M｜0.509
    - DepthCLIP｜0｜0｜1.147
    - Ours｜70 min｜8K｜1.049（強調）
- 出處：Table 2, Table 5, §4.4, §4.6
- Wiki：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#KITTI（Table 2）]]、[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#效率比較（Table 5）]]

## S9 · Experimental Results — Ablation
- 標題：Ablation：兩個元件都有貢獻
- 內容：
  - Learnable prompt 明顯提升表現
  - Depth codebook（依場景）取代單一 depth bin：除 δ<1.25 外所有指標改善
  - Patch size 32 × 32 最好（ResNet-50 CLIP 的特徵為輸入的 1/32）
  - 注意：原文 Table 3–4 的 RMSE / AELS 欄位疑似對調，此處依數值意義標示
  - 定性（Fig. 3）：紅框區域比 DepthCLIP 更準
- 圖表：兩個表格
  - Table 3 節錄，欄：Method、δ<1.25、MARE、RMSE
    - Baseline（DepthCLIP）｜0.394｜0.388｜1.167
    - + Learnable Prompt｜0.429｜0.386｜1.076
    - + Prompt + Depth Bin｜0.433｜0.378｜1.066
    - + Prompt + Depth Codebook｜0.428｜0.347｜1.049（強調）
  - Table 4 節錄，欄：Patch size、δ<1.25、MARE、RMSE
    - 8 × 8｜0.336｜0.379｜1.300
    - 16 × 16｜0.354｜0.514｜1.229
    - 32 × 32｜0.428｜0.347｜1.049（強調）
- 出處：Table 3, Table 4, Fig. 3, §4.5–4.6
- Wiki：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#Ablation（Table 3–4）]]、[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#定性結果（Fig. 3）]]

## S10 · Conclusions — 結論與限制
- 標題：結論與限制
- 內容：
  - 結論：
    - 以 few-shot 調整 CLIP，在訓練成本與泛化之間取得平衡
    - 依場景指派 depth bin，並用 learnable prompt 把文字轉成模型易懂的向量
  - 限制（補充，論文未明列）：
    - 與 supervised 差距大：δ<1.25 0.428 vs. DepthFormer 0.921
    - 以 patch 為單位預測，深度圖解析度粗
    - 需要事先定義場景類別並準備每類影像
  - 提醒：論文中有數處表格欄位、公式與數值前後不一致，引用時請對照 Wiki
- 圖表：左右兩欄（結論 / 限制）
- 出處：§5, Table 1, §3.5
- Wiki：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#結論（§5）]]、[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#限制（補充）]]、[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation#論文內的不一致]]
