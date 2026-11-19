# Can Language Understand Depth? — Slide Spec

## S1 · Cover
- 標題：Can Language Understand Depth?
- 內容：
  - 作者：Renrui Zhang, Ziyao Zeng, Ziyu Guo, Yafeng Li
  - Peking University · ShanghaiTech University｜ACM MM 2022
  - 一句話：DepthCLIP 不需訓練，用距離詞 prompt 與影像 patch 的相似度，對固定 depth bins 加權求和
- 圖表：無
- 出處：Abstract, §1
- Wiki：[[2022_Can-Language-Understand-Depth#一句話總結]]

## S2 · Introduction — 研究背景
- 標題：研究背景：CLIP 很會「辨識」，但還沒用在「量化」任務
- 內容：
  - CLIP 在 zero/few-shot 分類、偵測、分割表現亮眼，但只需要高層次辨識能力
  - 沒有工作用 CLIP 處理預測連續數值的任務
  - Supervised MDE：需要稠密深度標註，訓練與標註成本高
  - Unsupervised MDE：需要單眼影片、雙目影像或 3D prior
- 圖表：無
- 出處：§1–2
- Wiki：[[2022_Can-Language-Understand-Depth#研究背景]]

## S3 · Introduction — 問題與想法
- 標題：關鍵想法：把深度回歸改成距離分類
- 內容：
  - 問題：CLIP 的對比式預訓練學不到回歸數值，無法直接輸出深度
  - 想法：CLIP 只需理解「the object is close/far」，不需理解「the object is 5 meters away」
  - 貢獻：
    - 首個從語言知識 zero-shot 遷移到 MDE 的方法 DepthCLIP
    - 在 NYU Depth V2 超越 unsupervised 方法，接近部分 fully-supervised 模型
- 圖表：無
- 出處：§1
- Wiki：[[2022_Can-Language-Understand-Depth#現有方法的問題]]、[[2022_Can-Language-Understand-Depth#動機與貢獻]]

## S4 · Method — 整體架構
- 標題：整體架構：兩個 frozen CLIP encoder，不訓練任何參數
- 內容：
  - Text Encoder 與 Visual Encoder 皆為預訓練 CLIP（ResNet-50）
  - 文字路徑：K 個距離詞各自組成 prompt
  - 影像路徑：每個 patch 得到一個特徵
  - 相似度經 softmax 成為權重，對固定深度值加權求和
- 圖表：架構圖
  - 節點：Prompt「This Object is [CLASS]」（giant、close、…、far、unseen）、Textual Encoder、Text Features（K）、Input 2D RGB Image、Visual Encoder、Image Features（H × W）、Dot Product、Similarity Scores、SoftMax、Depth Weights、Depth Bins（Fixed depth values）、Weighted Sum、Depth Predictions
  - 連線：Prompt → Textual Encoder → Text Features；Input 2D RGB Image → Visual Encoder → Image Features；Text Features ⊙ Image Features（Dot Product）→ Similarity Scores → SoftMax → Depth Weights → Weighted Sum；Depth Bins → Weighted Sum；Weighted Sum → Depth Predictions
  - 對照：Fig. 2
- 出處：Fig. 2, §3, §4.2
- Wiki：[[2022_Can-Language-Understand-Depth#整體架構（Fig. 2）]]

## S5 · Method — Image 與 text encoding
- 標題：Image 與 text encoding：patch 特徵 × 距離詞特徵
- 內容：
  - Image：去掉最後 pooling 的 visual encoder，每個位置保留周圍的區域語意
  - Text：「This object is [distance class]」代入 K 個距離詞，經 textual encoder 得到 K 個特徵
  - 兩者計算 cosine similarity，得到每個 patch 對每個距離詞的分數
- 圖表：無
- 出處：§3.1–3.2, Eq. 1–3
- Wiki：[[2022_Can-Language-Understand-Depth#Image encoding 與 text encoding（§3.1–3.2）]]

## S6 · Method — Depth projection
- 標題：Depth projection：從距離詞到公尺
- 內容：
  - Temperature softmax（0.1）把相似度轉成權重
  - 權重對 depth bins 加權求和，得到每個 patch 的深度；同一 patch 內像素深度相同
  - 7 個距離詞：giant、extremely close、close、not in distance、a little remote、far、unseen
  - 對應深度值：1.00、1.50、2.00、2.25、2.50、2.75、3.00 m
- 圖表：無
- 出處：§3.3, §4.2, Eq. 4–5
- Wiki：[[2022_Can-Language-Understand-Depth#Depth projection（§3.3）]]

## S7 · Experimental Results — NYU Depth V2
- 標題：NYU Depth V2：不訓練也能接近早期 supervised 方法
- 內容：
  - 測試 654 張，裁切 416 × 512
  - 大幅超越 lower bound，也超越在 KITTI 影片上預訓練的 zero-shot 方法
  - 接近 fully-supervised 的 Make3D，rmse 1.167 vs. 1.214
- 圖表：表格（Table 1 節錄）
  - 欄：Method、Supervision、δ<1.25 ↑、rel ↓、rmse ↓
  - Make3D｜depth｜0.447｜0.349｜1.214
  - DepthFormer｜depth｜0.921｜0.096｜0.339
  - Lower Bound｜—｜0.140｜1.327｜2.934
  - Zhang et al.（KITTI video）｜0-shot｜0.350｜0.513｜1.457
  - DepthCLIP｜0-shot｜0.394｜0.388｜1.167（強調）
- 出處：Table 1, §4.1, §4.4
- Wiki：[[2022_Can-Language-Understand-Depth#設定（§4.1–4.3）]]、[[2022_Can-Language-Understand-Depth#NYU Depth V2（Table 1）]]

## S8 · Experimental Results — Class-dependent depth bin
- 標題：依場景換 depth bin，效果差很多
- 內容：
  - 不同場景深度分布不同（Fig. 3），同一個距離詞應對應不同深度值
  - Bathroom 換成 Class-dependent 3 劃分：rel 0.549 → 0.373
  - 不同場景的最佳劃分不同
  - 作者提出：先用 CLIP 做場景分類，再選對應的 bin（補充：後由 Hu et al. 實現）
- 圖表：表格（Table 2 節錄）
  - 欄：場景、劃分、δ<1.25、rel、rmse
  - Bathroom｜Original｜0.333｜0.549｜0.922
  - Bathroom｜Class-dependent 3｜0.425｜0.373｜0.745（強調）
  - Classroom｜Original｜0.308｜0.372｜1.826
  - Classroom｜Class-dependent 4｜0.276｜0.461｜1.544
- 出處：Table 2, Fig. 3, §4.5
- Wiki：[[2022_Can-Language-Understand-Depth#Class-dependent depth bin（Table 2）]]

## S9 · Experimental Results — Prompt design 與語意回應
- 標題：換距離詞影響不大；近與遠的 patch 回應不同
- 內容：
  - 不同距離詞組合差異不大，遠不如 bin 劃分敏感
  - 原因：giant 與 extremely close 等詞語意相近，同一 patch 會同時回應
  - 13 × 17 的特徵圖上，近處與遠處 patch 對距離詞的回應明顯不同（Fig. 4）
- 圖表：表格（Table 3 節錄）
  - 欄：Prompt、δ<1.25、rel、rmse
  - Original｜0.394｜0.388｜1.167（強調）
  - Prompt 1｜0.341｜0.379｜1.274
  - Prompt 2｜0.377｜0.385｜1.196
  - Prompt 3｜0.380｜0.375｜1.196
- 出處：Table 3, Fig. 4, §4.6–4.7
- Wiki：[[2022_Can-Language-Understand-Depth#Prompt design（Table 3）]]、[[2022_Can-Language-Understand-Depth#Semantic bin responses（Fig. 4）]]

## S10 · Conclusions — 結論與限制
- 標題：結論與限制
- 內容：
  - 結論：
    - 以 CLIP 做 zero-shot MDE，不需訓練與深度標註
    - 開啟「語言知識 → 量化視覺任務」的研究方向
  - 限制：
    - 需要人工調整 depth bin，所有場景共用時表現差
    - CLIP 偏重分類用的局部細節，牆、天花板、地板等大區域回應弱
  - 提醒：論文文字與表格有數處不一致（如 rmse 1.186 vs. 1.167），引用時請對照 Wiki
- 圖表：左右兩欄（結論 / 限制）
- 出處：§5, §6, §4.4, Table 1
- Wiki：[[2022_Can-Language-Understand-Depth#結論（§6）]]、[[2022_Can-Language-Understand-Depth#限制（§5）]]、[[2022_Can-Language-Understand-Depth#論文內的不一致]]
