# Learning to Prompt CLIP for Monocular Depth Estimation: Exploring the Limits of Human Language — Outline

一句話總結：把 DepthCLIP prompt 中的人類距離詞換成可學的 depth token，CLIP 完全 frozen、只學幾千個參數就大幅提升表現，且學到的 token 大多不對應任何英文詞——CLIP 的「深度」概念難以用人類語言表達。→ 段落：一句話總結

## Cover（1 張）
- 標題、作者、ICCVW 2023、一句話總結

## Introduction（2 張）
- 背景：DepthCLIP 以距離詞 prompt 做 zero-shot MDE，每個 prompt 對應一個 depth bin（§1）→ 段落：研究背景
- 問題：人工選詞帶來 human bias；CLIP 對深度的理解可能是隱性的、無法用文字表達；人類語言是離散的，bin 數一多描述就變得冗長（§1）→ 段落：現有方法的問題
- 貢獻：learnable prompt token 取代人類語言；系統性實驗 prompt 模板、bin 數與分布；分析學到的 token（§1）→ 段落：動機與貢獻

## Method（3 張）
- 整體架構：與 DepthCLIP 相同，只換成修改過的 CLIP text encoder；CLIP 全部 frozen；輸出刻意保持低解析度（Fig. 1, §3）→ 段落：整體架構（Fig. 1）
- Learnable depth token：tokenizer 把特殊詞替換成可學的 512 維向量，以 N(0, 0.02) 初始化；模板含可學 context token（1o1d、1o2d、4o4d）（§3.1, §3.3, Fig. 2, Table 1）→ 段落：Learnable depth token（§3.1, Fig. 2）
- 輸出與訓練：inner product 正規化成 bin logits，乘上固定 bin 中心後加總，再雙線性上採樣；以 SILog loss 在完整訓練集上訓練 25 epochs（§3.2, §4.1）→ 段落：輸出與訓練（§3.2, §4.1）

## Experimental Results（3 張）
- Learned vs. human-language tokens（Table 3）：learned-7 在 NYUv2 Abs 0.319（depth-7 為 1.014）、KITTI 0.303（2.353）；KITTI 上 random token 勝過所有人類詞，NYUv2 上 colour-7 勝過 size-7 → 段落：Learned vs. human-language tokens（Table 3）
- Context token 與 bin 數（Table 4–5, Table 7）：context token 對人類詞幫助大、對 learned token 幫助小；bin 數越多越好（256 bins：NYUv2 Abs 0.298、KITTI 0.238）→ 段落：Context tokens（Table 4–5）、Bin 數量與分布（Table 6–7）
- Token 解讀（Table 8）：7 個 learned token 中只有 2 個最接近 close、distant，其餘最接近彼此 → 段落：Learned token 的解讀（Table 8）

## Conclusions（1 張）
- 結論：learned token 用少量參數大幅提升；CLIP 的深度概念難以用人類語言簡潔表達（§5）→ 段落：結論與未來方向（§5）
- 限制（補充）：仍為 patch 級低解析度輸出；需在完整訓練集上訓練；固定 bin 中心 → 段落：限制（補充）
- 不一致與跨論文差異：WorDepth 引用本篇 NYUv2 的 log10 為 0.139，實為本篇的 RMSL（log10 為 0.128）→ 段落：論文內的不一致與跨論文差異

## 預計張數
1 + 2 + 3 + 3 + 1 = 10 張

## 預計頁面
- papers：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]]
- entities（新增）：[[CLIPMDE]]
- concepts（更新）：[[Prompt-Tuning]]、[[Depth-Bins]]、[[Vision-Language-Model]]
- entities（更新）：[[DepthCLIP]]、[[CLIP]]、[[NYU-Depth-V2]]、[[KITTI]]
