# CLIP Can Understand Depth — Outline

一句話總結：CLIP2Depth 不微調 CLIP，把 frozen text encoder 的語意 prior 蒸餾成一個非人類語言的可學 embedding「mirror」，以 FiLM 調變影像特徵並接上輕量 decoder 做 dense depth；比先前 CLIP-based 方法大幅進步（Abs Rel 比 Auty et al. 降低 68.7%／75.6%）。→ 段落：一句話總結

## Cover（1 張）
- 標題、作者、Pattern Recognition 2026、一句話總結

## Introduction（2 張）
- 背景：CLIP 在預訓練中沒學好的領域（如深度）表現有限；微調 CLIP 成本高（§1–2）→ 段落：研究背景
- 問題：DepthCLIP、Auty et al.、Hu et al. 都依賴預設 bin 值把相似度轉成深度，或依賴人類語言 token；CaBins、WorDepth、HoCLIP 則微調 CLIP 或加入大量參數（§2.1）→ 段落：現有方法的問題
- 貢獻：不微調 CLIP 即可做 dense depth；單一 query 向量即可，不需 prompt 集合與 binning；在 NYU、KITTI 勝過所有 frozen-CLIP 方法（§1）→ 段落：動機與貢獻

## Method（3 張）
- 整體架構：Mirror → frozen CLIP text encoder → FiLM 調變 frozen CLIP image encoder 的中間層特徵 → CLIPSeg dense predictor → Soft-Plus → 深度圖（Fig. 2, Table 1）→ 段落：整體架構（Fig. 2）
- Mirror：64 × 512 的可學 embedding，取代人類語言 token；經 text encoder 後只得到一個 query 向量，以 FiLM 調變影像特徵而非計算多個相似度（§3.1）→ 段落：Mirror：non-human language prompt（§3.1）
- Decoder 與訓練：沿用預訓練的 CLIPSeg decoder（ViT-B/16、352 × 352）；只訓練 mirror 與 decoder（共 1.1M 參數）；scale-invariant loss（§3.2, §4.1）→ 段落：Minimal decoder 與訓練（§3.2, §4.1）

## Experimental Results（3 張）
- NYU 與 KITTI（Table 3–4）：NYU Abs Rel 0.100、KITTI 0.074，大幅領先 frozen-CLIP 方法，接近部分 vision-only 方法 → 段落：NYU Depth V2（Table 3）、KITTI（Table 4）
- 參數量與 zero-shot（Table 5–6）：1,095k 參數 vs. ZoeDepth 345,000k；SUN RGB-D zero-shot 在 CLIP-based 方法中最好 → 段落：參數量與計算量（Table 5）、Zero-shot generalization（Table 6）
- Ablation 與一致性（Table 7–9, Fig. 7–9）：mirror 被隨機化後表現下降；FiLM 優於 Auty et al. 的相似度作法；CLIPSeg 預訓練有幫助；時間與空間一致性較佳 → 段落：Ablation（Table 7–9）、一致性分析（Fig. 7–8）

## Conclusions（1 張）
- 結論：frozen CLIP 的深度理解可以被修正，不需微調（§7）→ 段落：結論（§7）
- 限制：仍未達 CLIP 在其他任務的 SOTA 水準；mirror 依賴場景語意，幾何為主、語意稀少的場景可能泛化差；非人類語言 prompt 可能犧牲 open-vocabulary 能力（§5）→ 段落：限制（§5）
- 不一致與跨論文差異：Table 6 文字宣稱除 Abs Rel 外全部最佳，但 ZoeDepth 全部更好；KITTI 表的 log10 欄混入 RMSElog 數值；ZoeDepth 參數 346M（文字）vs. 345,000k（表）→ 段落：論文內的不一致與跨論文差異

## 預計張數
1 + 2 + 3 + 3 + 1 = 10 張

## 預計頁面
- papers：[[2026_CLIP-Can-Understand-Depth]]
- concepts（新增）：[[FiLM]]
- entities（新增）：[[CLIPSeg]]
- concepts（更新）：[[Prompt-Tuning]]、[[Vision-Language-Model]]
- entities（更新）：[[CLIP]]、[[CLIPMDE]]、[[DepthCLIP]]、[[NYU-Depth-V2]]、[[KITTI]]、[[SUN-RGBD]]
- 補回：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]] 的 log10 跨論文佐證與「後續」連結
