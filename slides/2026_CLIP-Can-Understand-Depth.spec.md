# CLIP Can Understand Depth — Slide Spec

## S1 · Cover
- 標題：CLIP Can Understand Depth
- 內容：
  - 作者：Sohee Kim, Jisu Kang, Dunam Kim, Seokju Lee
  - KENTECH｜Pattern Recognition 2026
  - 一句話：CLIP2Depth 不微調 CLIP，用非人類語言的可學 embedding「mirror」加上輕量 decoder 做 dense depth
- 圖表：無
- 出處：Abstract, §7
- Wiki：[[2026_CLIP-Can-Understand-Depth#一句話總結]]

## S2 · Introduction — 研究背景
- 標題：研究背景：CLIP 能理解深度嗎？
- 內容：
  - CLIP 泛化能力強，但在預訓練時表徵不足的領域（如深度）有明顯限制
  - 為特定任務微調 CLIP 需要大量計算與資料
  - 調整 CLIP 可把語意 prior 帶進深度預測，可能在分布轉移或資料少時更穩健
  - 核心問題：不微調的情況下，CLIP 能理解深度嗎？
- 圖表：無
- 出處：§1
- Wiki：[[2026_CLIP-Can-Understand-Depth#研究背景]]

## S3 · Introduction — 現有問題與貢獻
- 標題：現有方法：不是依賴 bins 與人類語言，就是微調 CLIP
- 內容：
  - Frozen-CLIP 方法（DepthCLIP、Auty et al.、Hu et al.）：靠預設 bin 值或人類語言 token
  - CaBins、WorDepth、HoCLIP：部分或全部微調 CLIP，或加入大量參數
  - 貢獻：
    - 不微調 CLIP 即可做 dense depth
    - 單一 query 向量即可，不需 prompt 集合與 binning
    - 在 NYU、KITTI 勝過所有 CLIP-based 方法，並與視覺模型競爭
- 圖表：無
- 出處：§1, §2.1
- Wiki：[[2026_CLIP-Can-Understand-Depth#現有方法的問題]]、[[2026_CLIP-Can-Understand-Depth#動機與貢獻]]

## S4 · Method — 整體架構
- 標題：整體架構：mirror 經 FiLM 調變 frozen CLIP 的影像特徵
- 內容：
  - CLIP 的 text 與 image encoder 全部 frozen
  - 只訓練 mirror 與 dense predictor（沿用 CLIPSeg）
  - Mirror 經 text encoder 只產生一個 query，透過 FiLM 加法與乘法調變影像特徵
- 圖表：架構圖
  - 節點：Mirror Embeddings、Prompt Encoder（CLIP Text Model，frozen）、FiLM Add、FiLM Mul、Input Image、Visual Encoder（CLIP Image Model，frozen）、L3 / L6 / L9 中間層特徵、⊗ ⊕ 調變、Transformer Block × 3、Deconvolution、Soft-Plus、Depth Map
  - 連線：Mirror Embeddings → Prompt Encoder → FiLM Add、FiLM Mul → ⊗ ⊕ 調變；Input Image → Visual Encoder → L3 / L6 / L9 → ⊗ ⊕ 調變 → Transformer Block × 3（含 skip connection）→ Deconvolution → Soft-Plus → Depth Map
  - 對照：Fig. 2
- 出處：Fig. 2, Table 1, §3
- Wiki：[[2026_CLIP-Can-Understand-Depth#整體架構（Fig. 2）]]

## S5 · Method — Mirror
- 標題：Mirror：非人類語言的 prompt
- 內容：
  - 64 個 512 維可學向量，完全不用 CLIP 的自然語言 token embedding
  - 前後接 BOS、EOS 送入 frozen text encoder，只得到一個 query
  - 先前方法：s 個 prompt → s 個相似度 → 加權 bins；本篇：1 個 query → FiLM 調變
  - 作者的直覺：一個「How far is this location from the camera?」式的 query 就夠了
- 圖表：無
- 出處：§3.1–3.2
- Wiki：[[2026_CLIP-Can-Understand-Depth#Mirror：non-human language prompt（§3.1）]]

## S6 · Method — Decoder 與訓練
- 標題：輕量 decoder 與訓練設定
- 內容：
  - Patch embedding 失去時空資訊，因此加入 deconvolutional decoder
  - 沿用預訓練 CLIPSeg decoder，避免模型過度依賴 decoder
  - ViT-B/16、輸入 352 × 352、484 個 patch；FiLM 內的 FFN 也 frozen
  - Scale-invariant loss（λ = 0.85、α = 10）；25 epochs、AdamW、單張 RTX 3090
  - 注意：先前方法用 CLIP ResNet-50，本篇 backbone 較大且多一個 decoder
- 圖表：無
- 出處：§3.2, §4.1, §4.2
- Wiki：[[2026_CLIP-Can-Understand-Depth#Minimal decoder 與訓練（§3.2, §4.1）]]

## S7 · Experimental Results — NYU 與 KITTI
- 標題：NYU 與 KITTI：大幅領先 frozen-CLIP 方法
- 內容：
  - Abs Rel 相對 Auty et al.：NYU 降低 68.7%、KITTI 降低 75.6%
  - 先前 CLIP 方法在 KITTI 都明顯較差，本篇的差距大幅縮小
  - 仍落後 DepthAnything v2 等大型 vision-only 模型
- 圖表：兩個表格
  - Table 3 節錄（NYU），欄：Model、Abs Rel、RMSE、δ1
    - DepthAnything v2｜0.056｜0.206｜0.984
    - DepthCLIP｜0.388｜1.167｜0.394
    - Auty et al.｜0.319｜0.970｜0.465
    - CLIP2Depth｜0.100｜0.379｜0.900（強調）
  - Table 4 節錄（KITTI），欄：Model、Abs Rel、RMSE、δ1
    - DepthAnything v2｜0.045｜1.861｜0.983
    - DepthCLIP｜0.473｜12.958｜0.281
    - Auty et al.｜0.303｜6.322｜0.550
    - CLIP2Depth｜0.074｜2.948｜0.938（強調）
- 出處：Table 3, Table 4, §4.2
- Wiki：[[2026_CLIP-Can-Understand-Depth#NYU Depth V2（Table 3）]]、[[2026_CLIP-Can-Understand-Depth#KITTI（Table 4）]]

## S8 · Experimental Results — 參數量與 zero-shot
- 標題：參數少很多；zero-shot 在 CLIP 方法中最好
- 內容：
  - 1,095k 可學參數，比微調整個 CLIP 的 HoCLIP 少約 300 倍
  - SUN RGB-D zero-shot：CLIP-based 方法中除 Abs Rel 外各項最佳
  - 仍落後 ZoeDepth 等大型 vision-only 模型
- 圖表：兩個表格
  - Table 5 節錄（KITTI），欄：Model、Learnable Params、GFLOPs
    - ZoeDepth｜345,000k｜538.60
    - HoCLIP｜295,000k｜944
    - Auty et al.｜3k｜107.36
    - CLIP2Depth｜1,095k｜89.60（強調）
  - Table 6 節錄（NYU → SUN RGB-D），欄：Model、Abs Rel、RMSE、δ1
    - ZoeDepth｜0.119｜0.346｜0.864
    - Auty et al.｜0.446｜0.950｜0.380
    - HoCLIP｜0.401｜0.850｜0.402
    - CLIP2Depth｜0.431｜0.535｜0.627（強調）
- 出處：Table 5, Table 6, §4.2–4.3
- Wiki：[[2026_CLIP-Can-Understand-Depth#參數量與計算量（Table 5）]]、[[2026_CLIP-Can-Understand-Depth#Zero-shot generalization（Table 6）]]

## S9 · Experimental Results — Ablation 與一致性
- 標題：Mirror 真的有用；時間與空間一致性也較好
- 內容：
  - 訓練後把 mirror 隨機化，表現明顯下降：模型確實依賴 mirror
  - FiLM 單一 query 優於 Auty et al. 的多 prompt 相似度作法
  - CLIPSeg 預訓練優於從頭訓練
  - 時間一致性：錯誤率遠低於 DepthCLIP 與 Auty et al.
  - 空間連續性：物體高度與深度的關係最接近 ground truth
- 圖表：表格（Table 7–9 節錄，KITTI）
  - 欄：實驗、變體、Abs Rel、RMSE、δ1
  - Mirror｜Randomized｜0.0961｜3.6415｜0.8906
  - Mirror｜Converged｜0.0739｜2.9480｜0.9379（強調）
  - 調變｜Auty et al. 作法｜0.0802｜3.1390｜0.9239
  - 調變｜FiLM｜0.0768｜3.1267｜0.9287（強調）
  - 預訓練｜從頭訓練｜0.077｜3.127｜0.929
  - 預訓練｜CLIPSeg｜0.074｜2.948｜0.938（強調）
- 出處：Table 7–9, Fig. 7–9, §4.4–4.5
- Wiki：[[2026_CLIP-Can-Understand-Depth#Ablation（Table 7–9）]]、[[2026_CLIP-Can-Understand-Depth#一致性分析（Fig. 7–8）]]

## S10 · Conclusions — 結論與限制
- 標題：結論與限制
- 內容：
  - 結論：
    - 不微調 CLIP，就能修正它對深度的理解
    - 改善時間與空間一致性，且不修改 CLIP backbone
  - 限制：
    - 仍未達 CLIP 在分割、生成等任務的 SOTA 水準
    - Mirror 依賴場景語意，語意稀少的場景可能泛化差
    - 非人類語言 prompt 可能犧牲 open-vocabulary 能力
  - 提醒：Table 6 文字宣稱的「最佳」只在 CLIP-based 方法之間成立，詳見 Wiki
- 圖表：左右兩欄（結論 / 限制）
- 出處：§5, §7, Table 6
- Wiki：[[2026_CLIP-Can-Understand-Depth#結論（§7）]]、[[2026_CLIP-Can-Understand-Depth#限制（§5）]]、[[2026_CLIP-Can-Understand-Depth#論文內的不一致與跨論文差異]]
