# Learning to Adapt CLIP for Few-Shot Monocular Depth Estimation — Outline

一句話總結：在 DepthCLIP 的 zero-shot 架構上，每個場景類別只用 1 張影像做 few-shot 訓練，學習 learnable prompt 與依場景切換的 learnable depth codebook。→ 段落：一句話總結

## Cover（1 張）
- 標題、作者、WACV 2024、一句話總結

## Introduction（2 張）
- 背景：CLIP 以 4 億組 image-text pair 做 contrastive learning；傳統 supervised MDE 需要大量標註資料、訓練耗時（§1）→ 段落：研究背景
- DepthCLIP：把影像 patch 與「This object is [Depth CLASS]」的深度描述做相似度，再對人工設定的 depth bin 加權求和，達成 zero-shot MDE（§1, §3.3）→ 段落：研究背景
- 問題：不同場景的深度分布不同（Fig. 1a），固定的 depth bin 與人工 prompt 難以泛化（§1）→ 段落：現有方法的問題
- 動機：few-shot 介於 supervised（成本高）與 zero-shot（泛化差）之間；貢獻為 learnable prompt、learnable depth codebook、NYU V2 上 MARE 最多改善 10.6%（§1）→ 段落：動機與貢獻

## Method（3 張）
- 整體架構：text encoder、scene encoder、visual encoder 皆來自 CLIP ResNet-50；只更新 prompt 與 codebook（Fig. 2, §3.2）→ 段落：整體架構（Fig. 2）
- Learnable prompt：把「This object is」換成可學的向量 V，輸入為「[Vector] + [Class]」，以 RMSE loss 更新（§3.3, Eq. 1–3）→ 段落：Learnable prompt（§3.3）
- Learnable depth codebook：scene encoder 找出最相似的場景類別（one-hot），選出該類別專屬的 depth bin；NYU V2 為 27 類 × 7 個深度值（§3.4, §4.2, Eq. 4–8）→ 段落：Learnable depth codebook（§3.4）
- Depth prediction：patch 特徵與 K 個文字特徵的 cosine similarity 經 softmax 得到 depth weight，與選出的 depth bin 加權求和；同一 patch 內像素深度相同（§3.5, Eq. 9–12）→ 段落：Depth prediction（§3.5）

## Experimental Results（3 張）
- 設定：NYU V2、KITTI；每個場景類別 1 張訓練影像（NYU V2 共 27 張）；200 epochs；單張 RTX 3090（§4.1–4.2）→ 段落：設定（§4.1–4.3）
- NYU V2（Table 1 節錄）：MARE 0.388 → 0.347、RMSE 1.167 → 1.049（相對 DepthCLIP）；仍遠低於 fully-supervised（如 DepthFormer δ<1.25 0.921）→ 段落：NYU Depth V2（Table 1）
- KITTI（Table 2 節錄）：MARE 0.473 → 0.384，仍優於 DepthCLIP → 段落：KITTI（Table 2）
- 效率（Table 5）：只更新 8K 參數、訓練 70 分鐘 vs. DORN 51M 參數、> 30 小時 → 段落：效率比較（Table 5）
- Ablation（Table 3–4）：learnable prompt 與 depth codebook 都有貢獻；patch size 32 × 32 最好 → 段落：Ablation（Table 3–4）
- 定性結果：Fig. 3 紅框區域比 DepthCLIP 更準 → 段落：定性結果（Fig. 3）

## Conclusions（1 張）
- 結論：few-shot 調整 CLIP 在訓練成本與泛化之間取得平衡（§5）→ 段落：結論（§5）
- 限制：論文沒有獨立的限制段落，以下為依表格觀察的補充：與 supervised 方法仍有很大差距；以 patch 為單位預測，深度圖解析度粗；需要事先定義場景類別 → 段落：限制（補充）
- 論文內的不一致（建議放在 Wiki、簡報只簡短提醒）→ 段落：論文內的不一致
  - Table 3、Table 4 的欄位標題 RMSE / AELS 疑似對調（數值與 Table 1 的 AELS / RMSE 對應）
  - Eq. 13–14 的 MARE / MSRE 公式疑似對調（MARE 的分子有平方）
  - DepthCLIP 在 NYU V2 的 RMSE：Table 1 為 1.167，Table 5 為 1.147
  - Table 2 中 ASTransformer 的 KITTI 數值（0.103、0.374）與 Table 1 的 NYU 數值相同，疑似誤植
  - 摘要說在 NYU V2 與 KITTI 都有實驗，但貢獻第 3 點只寫 NYU V2

## 預計張數
1 + 2 + 3 + 3 + 1 = 10 張

## 預計頁面
- papers：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]]
- concepts（新增）：[[Few-Shot-Learning]]、[[Prompt-Tuning]]、[[Depth-Bins]]
- concepts（更新）：[[Vision-Language-Model]]
- entities（新增）：[[DepthCLIP]]
- entities（更新）：[[CLIP]]、[[NYU-Depth-V2]]、[[KITTI]]、[[Depth-Metrics]]
- 跨論文差異（寫入時標註）：DepthFormer 在 NYU V2 的數值，本篇 Table 1（δ<1.25 0.921、AbsRel 0.096、RMSE 0.339）與 [[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation|WorDepth]] Table 1（0.923、0.094、0.329）不同
