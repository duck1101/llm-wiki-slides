# Learning to Prompt CLIP for Monocular Depth Estimation: Exploring the Limits of Human Language — Slide Spec

## S1 · Cover
- 標題：Learning to Prompt CLIP for Monocular Depth Estimation: Exploring the Limits of Human Language
- 內容：
  - 作者：Dylan Auty, Krystian Mikolajczyk
  - Imperial College London｜ICCV Workshops 2023
  - 一句話：把 DepthCLIP 的人類距離詞換成可學的 depth token，CLIP 完全 frozen，只學幾千個參數就大幅提升
- 圖表：無
- 出處：Abstract, §1, §5
- Wiki：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#一句話總結]]

## S2 · Introduction — 研究背景
- 標題：研究背景：DepthCLIP 用人類語言描述深度
- 內容：
  - MDE 是 poorly-posed 問題：同一張影像可能來自無數 3D 場景
  - CLIP 以 4 億張附說明的影像訓練，學到大量世界知識
  - DepthCLIP：每個 depth bin 對應一句「This object is [near/far/…]」，依相似度加權 bin 中心
- 圖表：無
- 出處：§1
- Wiki：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#研究背景]]

## S3 · Introduction — 問題與貢獻
- 標題：問題：人類語言可能不是向 CLIP 描述深度的好方法
- 內容：
  - 現有問題：
    - Human bias：用哪個詞是人選的，而且 prompt 本身就是文字
    - CLIP 的訓練說明很少談深度，它對深度的理解可能是隱性的
    - 人類語言是離散的，bin 一多描述就冗長，bin 數受限
  - 貢獻：
    - 以 learnable prompt token 取代人類距離詞
    - 系統性實驗 prompt 模板、bin 數與分布
    - 分析學到的 token，理解 CLIP 如何理解深度
- 圖表：無
- 出處：§1
- Wiki：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#現有方法的問題]]、[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#動機與貢獻]]

## S4 · Method — 整體架構
- 標題：整體架構：DepthCLIP ＋ 修改過的 text encoder
- 內容：
  - 流程與 DepthCLIP 相同，只把 text encoder 換成可插入 learnable token 的版本
  - 預訓練 CLIP 完全 frozen，只訓練 learnable token
  - 輸出刻意保持低解析度，避免專門的 decoder 混淆對 CLIP 能力的判斷
- 圖表：架構圖
  - 節點：N depth prompts「This object appears to be {depth_tkn_n}」、Modified CLIP Text Encoder、txt_f（C × N）、Input Image、CLIP Img Encoder（frozen）、img_f（經 view / permute 攤平成 HW/32 個 patch）、Inner product、prompt logits、N fixed depth centres [c0, …, cn]、⊗、Reshape, bilinear resize、Depth map
  - 連線：N depth prompts → Modified CLIP Text Encoder → txt_f → Inner product；Input Image → CLIP Img Encoder → img_f → Inner product；Inner product → prompt logits → ⊗；N fixed depth centres → ⊗；⊗ → Reshape, bilinear resize → Depth map
  - 對照：Fig. 1
- 出處：Fig. 1, §3
- Wiki：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#整體架構（Fig. 1）]]

## S5 · Method — Learnable depth token
- 標題：Learnable depth token：替換掉 prompt 裡的距離詞
- 內容：
  - CLIP 原本把每個詞查表成 frozen 的 512 維 token
  - 修改 tokenizer：特殊詞 {depth_tkn_n} 換成可學參數，其餘仍 frozen
  - 沿用 CoOp 的作法；以平均 0、標準差 0.02 的常態分布初始化
  - 可再加入所有 bin 共用的 learnable context token {p_i}
- 圖表：表格（Table 1 節錄）
  - 欄：名稱、模板
  - Baseline｜This object appears to be {depth_tkn}.
  - 1o1d｜{p_0} object {p_1} {depth_tkn}.
  - 4o4d｜{p_0} {p_1} {p_2} {p_3} object {p_4} {p_5} {p_6} {p_7} {depth_tkn}.
- 出處：§3.1, §3.3, Fig. 2, Table 1
- Wiki：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#Learnable depth token（§3.1, Fig. 2）]]

## S6 · Method — 輸出與訓練
- 標題：輸出與訓練
- 內容：
  - Inner product 正規化成 N 個 bin 的 logits，乘上固定 bin 中心後加總
  - 得到 H/32 × W/32 的深度圖，再雙線性上採樣
  - Loss：SILog 變體；25 epochs、AdamW，超參數沿用 AdaBins
  - 資料：NYUv2 24231 / 654 張、KITTI 23157 / 696 張（完整訓練集）
  - CLIP ResNet-50；評估時對原圖與翻轉圖的預測取平均
- 圖表：無
- 出處：§3.2, §4.1
- Wiki：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#輸出與訓練（§3.2, §4.1）]]

## S7 · Experimental Results — Learned vs. 人類語言
- 標題：Learned token 大勝人類語言，連隨機 token 都可能贏過人類詞
- 內容：
  - 7 個平均分布的 bin，比較人類詞刻度與 learned token
  - learned-7 只有 3584 個參數，表現提升 1.5～5.5 倍
  - KITTI 上 random-7 勝過所有人類詞；NYUv2 上 colour-7 勝過 size-7
- 圖表：表格（Table 3 節錄）
  - 欄：Tokens、Dataset、Abs ↓、RMS ↓、δ1 ↑
  - depth-7｜NYUv2｜1.014｜2.413｜0.227
  - colour-7｜NYUv2｜1.381｜3.010｜0.131
  - learned-7｜NYUv2｜0.319｜0.970｜0.465（強調）
  - depth-7｜KITTI｜2.353｜25.518｜0.094
  - random-7｜KITTI｜1.664｜19.279｜0.119
  - learned-7｜KITTI｜0.303｜6.322｜0.550（強調）
- 出處：Table 2, Table 3, §4.2
- Wiki：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#Learned vs. human-language tokens（Table 3）]]

## S8 · Experimental Results — Context token 與 bin 數
- 標題：Context token 救人類詞；bin 越多越好
- 內容：
  - 人類詞 depth-7 加上 4o4d context token：NYUv2 Abs 1.014 → 0.318
  - Context token 加在 learned token 上只小幅改善，多數效益來自 depth token
  - Learned token 解除 bin 數限制：KITTI 用 log-uniform 分布較好
- 圖表：表格（Table 7 節錄，log-uniform bins）
  - 欄：Bins、Dataset、Abs ↓、RMS ↓、δ1 ↑
  - 7｜NYUv2｜0.312｜0.991｜0.449
  - 256｜NYUv2｜0.298｜0.933｜0.485（強調）
  - 7｜KITTI｜0.265｜6.933｜0.580
  - 256｜KITTI｜0.238｜5.756｜0.652（強調）
- 出處：Table 4–7, §4.3–4.4
- Wiki：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#Context tokens（Table 4–5）]]、[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#Bin 數量與分布（Table 6–7）]]

## S9 · Experimental Results — Learned token 的解讀
- 標題：學到的 token 幾乎不對應任何英文詞
- 內容：
  - 方法：把 CLIP 字彙約 4 萬個 token 代入 prompt，找每個 learned token 的最近鄰
  - 7 個 token 中只有 token 1 最接近「close」、token 6 最接近「distant」
  - 其餘 token 的最近鄰都是其他 learned token，且依遠近排成一條路徑
  - Bin 數增加持續提升表現 → 其他 token 也帶有無法用語言表達的深度資訊
- 圖表：無
- 出處：Table 8, §4.5
- Wiki：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#Learned token 的解讀（Table 8）]]

## S10 · Conclusions — 結論與限制
- 標題：結論與限制
- 內容：
  - 結論：
    - 只學幾千個參數，就比人類詞與隨機 token 大幅提升
    - CLIP 的深度概念無法用人類語言簡潔表達；其他抽象概念可能也是如此
  - 限制（補充，論文未明列）：
    - 輸出為 H/32 × W/32 低解析度
    - 仍需在完整訓練集上訓練，並非 zero/few-shot
    - Bin 中心固定，不依影像調整
  - 提醒：WorDepth 引用本篇 NYUv2 的 log10 為 0.139，實為 RMSL（log10 為 0.128）
- 圖表：左右兩欄（結論 / 限制）
- 出處：§5, §3.2, §4.1
- Wiki：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#結論與未來方向（§5）]]、[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#限制（補充）]]、[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language#論文內的不一致與跨論文差異]]
