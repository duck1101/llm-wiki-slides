---
type: concept
tags: [conditioning, architecture]
sources: [2026_CLIP-Can-Understand-Depth]
updated: 2026-11-19
---

# FiLM（Feature-wise Linear Modulation）

## 定義
- 以一個條件向量產生逐通道的乘法與加法係數，調變另一路特徵（補充）。
- CLIP2Depth 的 dense predictor 中有兩個 FiLM（FiLM Add、FiLM Mul），把文字端的條件 embedding（512 維）投影到 decoder 寬度（64 維）（[[2026_CLIP-Can-Understand-Depth]], Table 1, Fig. 2）。

## 在 MDE 論文中的用法
| 論文 | 條件來源 | 被調變的特徵 | 出處 |
|---|---|---|---|
| [[2026_CLIP-Can-Understand-Depth\|CLIP2Depth]] | mirror 經 frozen CLIP text encoder 得到的單一 query | CLIP image encoder 第 3、6、9 層特徵 | §3.2, Fig. 2 |

## 與相似度作法的比較
- [[DepthCLIP]]、[[CLIPMDE]] 等方法以多個 prompt 與影像 patch 的相似度加權 depth bins。
- CLIP2Depth 以單一 query 經 FiLM 調變影像特徵；在相同設定下各項指標都較好（Abs Rel 0.0768 vs. 0.0802）（[[2026_CLIP-Can-Understand-Depth]], Table 8）。

## 相關頁面
[[CLIPSeg]]、[[Prompt-Tuning]]
