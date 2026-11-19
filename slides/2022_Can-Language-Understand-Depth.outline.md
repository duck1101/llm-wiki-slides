# Can Language Understand Depth? — Outline

一句話總結：DepthCLIP 不需任何訓練，把 CLIP 的影像 patch 與「This object is [distance class]」的深度描述做相似度，再對固定的 depth bins 加權求和，首次以 CLIP 做 zero-shot MDE。→ 段落：一句話總結

## Cover（1 張）
- 標題、作者、ACM MM 2022、一句話總結

## Introduction（2 張）
- 背景：CLIP 在分類、偵測、分割等任務 zero-shot 表現好，但都只用到「辨識」能力；supervised MDE 需要大量標註、unsupervised 需要影片或 3D prior（§1–2）→ 段落：研究背景
- 問題：CLIP 預訓練不會學到回歸連續數值的能力，無法直接輸出深度（§1–2）→ 段落：現有方法的問題
- 想法與貢獻：把深度回歸改成距離分類，CLIP 只需理解「物體很近／很遠」而非「物體在 5 公尺外」；首個 zero-shot 的語言→深度遷移（§1）→ 段落：動機與貢獻

## Method（3 張）
- 整體架構：Text Encoder 與 Visual Encoder 皆為 frozen CLIP ResNet-50，無任何訓練（Fig. 2, §3, §4.2）→ 段落：整體架構（Fig. 2）
- Image / Text encoding：去掉 pooling 的 visual encoder 得到 patch 特徵；7 個距離詞填入 prompt 得到 text 特徵；兩者 cosine similarity（§3.1–3.2, Eq. 1–3）→ 段落：Image encoding 與 text encoding（§3.1–3.2）
- Depth projection：temperature softmax（0.1）得到權重，對 7 個固定深度值 1.00～3.00 m 加權求和；同一 patch 深度相同（§3.3, §4.2, Eq. 4–5）→ 段落：Depth projection（§3.3）

## Experimental Results（3 張）
- 設定：NYU Depth V2，測試 654 張、裁切 416 × 512（§4.1–4.3）→ 段落：設定（§4.1–4.3）
- NYU Depth V2（Table 1）：δ<1.25 0.394、rel 0.388、rmse 1.167；超越在 KITTI 影片上預訓練的 zero-shot 方法，接近 Make3D → 段落：NYU Depth V2（Table 1）
- Class-dependent depth bin（Table 2）：依場景換 bin 劃分可大幅改善（bathroom 最佳劃分 rel 0.549 → 0.373），不同場景最佳劃分不同 → 段落：Class-dependent depth bin（Table 2）
- Prompt design（Table 3）：不同距離詞組合的差異不大，比 bin 劃分不敏感 → 段落：Prompt design（Table 3）
- Semantic bin responses（Fig. 4）：近與遠的 patch 對距離詞的回應明顯不同 → 段落：Semantic bin responses（Fig. 4）

## Conclusions（1 張）
- 結論：以 CLIP 做 zero-shot MDE，不需訓練與深度標註（§6）→ 段落：結論（§6）
- 限制：需要人工調整 depth bin；CLIP visual encoder 偏重分類用的局部細節，牆、天花板、地板等大區域回應弱（§5）→ 段落：限制（§5）
- 論文內的不一致 → 段落：論文內的不一致
  - §4.4 文字寫 rmse 1.186，Table 1 為 1.167
  - §4.5 寫「Shown as Table 3」說明不同場景深度分布不同，實際應為 Fig. 3
  - Fig. 4 的距離詞與深度值（a little close、a bit remote、4.00 m 等）與主實驗設定不同

## 預計張數
1 + 2 + 3 + 3 + 1 = 10 張

## 預計頁面
- papers：[[2022_Can-Language-Understand-Depth]]
- concepts（新增）：[[Zero-Shot-Transfer]]
- concepts（更新）：[[Depth-Bins]]、[[Prompt-Tuning]]、[[Vision-Language-Model]]
- entities（更新）：[[DepthCLIP]]、[[CLIP]]、[[NYU-Depth-V2]]
- 跨論文對照：Table 1 的 DepthFormer（0.921、0.096、0.339）與 Hu et al. 相同、與 WorDepth 不同；DepthCLIP 數值與 Hu et al.、WorDepth 一致
