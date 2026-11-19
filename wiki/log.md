# Log

## [2026-11-19] schema | 建立 Wiki
- 建立 AGENTS.md、目錄結構、index.md、log.md

## [2026-11-19] ingest | WorDepth: Variational Language Prior for Monocular Depth Estimation
- 來源：使用者提供 PDF（CVF Open Access 正式版，CVPR 2024）→ `raw/2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation/`
- 大綱確認：直接通過（四章節、約 10 張投影片）
- 新增頁面：
  - papers：[[2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation]]
  - concepts：[[Scale-Ambiguity]]、[[Language-Prior]]、[[Variational-Autoencoder]]、[[Scale-Invariant-Loss]]、[[Vision-Language-Model]]
  - entities：[[NYU-Depth-V2]]、[[KITTI]]、[[SUN-RGBD]]、[[Depth-Metrics]]、[[CLIP]]、[[Swin-Transformer]]、[[AdaBins]]
- 更新頁面：[[index]]
- 產出：`slides/2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation.html`（10 張）
- 檢查結果：
  - 數值核對：Wiki 與簡報中的所有數值皆能在論文原文中找到，無不一致。
  - Wikilink：無斷連結、無孤兒頁。
  - 大綱外新增：寫 paper 頁時多建了 [[Vision-Language-Model]]（整理 DepthCLIP / CLIPMDE / VPD 的比較），原大綱未列。
  - 缺少原文依據：[[Depth-Metrics]] 的公式在論文 Supp. Mat.，正文未列，已標註「補充」。
  - 簡報 Method 架構圖錯誤：初版把 ε̃ 直接接到 depth decoder，漏掉「ε̃ 與 μ̂、σ̂ 合成 z̃」這一步，與 Fig. 2 不符 → 改為 μ̂,σ̂ 與 ε̃ 匯入 z̃，再經 decoder 輸出深度圖。
  - 簡報版面：1366×768 下第 5、7、9 張內容溢出 → 調小字級與間距後重測，無溢出。

## [2026-11-19] schema | Ingest 改為 workflow v1
- 流程改為 graph：1 抽取 → 2 寫入 Wiki → 3 從 Wiki 產生大綱 → 4 逐頁 spec → 5 渲染 HTML → 6 記錄；檢查 A～E，B、D 需使用者確認
- 新增 `tools/check.py`（extract / wiki / spec / html）、`paper.txt`、`slides/<...>.spec.md`；log 改為逐檢查記錄

## [2026-11-19] ingest | WorDepth: Variational Language Prior for Monocular Depth Estimation（workflow v1 重跑）
- 新增頁面：無（節點 2 沿用前一輪產生的 13 頁 Wiki，重新執行檢查 C）
- 新增檔案：`raw/2024_WorDepth-.../paper.txt`、`slides/2024_WorDepth-....spec.md`
- 產出：`slides/2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation.html`（10 張，覆蓋前一輪版本）

| 節點 | 檢查 | 結果 | 問題 | 退回 |
|---|---|---|---|---|
| 1 抽取 | A | 通過 | — | — |
| 2 Wiki | C | 通過 | — | — |
| 3 大綱 | B | 通過 | — | — |
| 3 大綱 | 使用者確認 | 通過 | — | — |
| 4 spec | D | 通過 | — | — |
| 4 spec | 使用者確認 | 通過 | — | — |
| 5 HTML | E（文字比對） | 通過 | — | — |
| 5 HTML | E（1366×768 溢出、架構圖、換頁） | 通過 | — | — |

- 備註：本次全部一次通過，沒有發生退回。前一輪暴露的兩個問題（架構圖漏掉 z̃、版面溢出）已在前一輪修正；本輪的 HTML 沿用修正後的版面設定，spec 也先以文字寫出架構圖的節點與連線，因此 v1 的弱點（篇幅與架構圖只在 E 檢查）這次沒有被觸發。
- 備註：檢查 B 目前由人工逐項核對，`tools/check.py` 尚無大綱檢查。

## [2026-11-19] schema | Ingest 改為 workflow v2
- 順序改為：1 抽取 → 2 四章節大綱（`slides/<...>.outline.md`）→ 3 寫入 Wiki → 4 逐頁 spec → 5 渲染 HTML → 6 記錄
- 檢查 C 新增對照大綱：預定段落與頁面是否建立、大綱外新增頁面列為警告
- 篇幅預算與架構圖對照從 E 提前到 D；`tools/check.py` 新增篇幅預算檢查與 `figure` 指令（輸出 PDF 頁面圖片供對照）
- 調整原因：第 1 輪的兩個問題（架構圖漏掉 z̃、版面溢出）都到渲染後才發現，根本原因卻在逐頁內容規劃；v1 重跑能一次通過，是因為沿用前一輪修好的版面與手動先寫出架構圖節點，這些都沒有寫進流程
- 篇幅預算校正：每條字數上限原訂 90 字元，以 WorDepth spec（1366×768 下已確認無溢出）測試時有 3 條（93～95 字元）被擋下，放寬為 100 字元

## [2026-11-19] ingest | Learning to Adapt CLIP for Few-Shot Monocular Depth Estimation（workflow v2）
- 來源：使用者提供 PDF（CVF Open Access 正式版，WACV 2024）→ `raw/2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation/`
- 新增頁面：
  - papers：[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]]
  - concepts：[[Few-Shot-Learning]]、[[Prompt-Tuning]]、[[Depth-Bins]]
  - entities：[[DepthCLIP]]
- 更新頁面：[[Vision-Language-Model]]、[[CLIP]]、[[NYU-Depth-V2]]、[[KITTI]]、[[Depth-Metrics]]、[[index]]
- 產出：`slides/2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation.outline.md`、`.spec.md`、`.html`（10 張）

| 節點 | 檢查 | 結果 | 問題 | 退回 |
|---|---|---|---|---|
| 1 抽取 | A | 通過 | 章節偵測把貢獻清單第 2 點誤認為章節標題（不影響結果） | — |
| 2 大綱 | B | 通過 | — | — |
| 2 大綱 | 使用者確認 | 通過 | — | — |
| 3 Wiki | C | 不通過 | 跨論文頁面上的 WorDepth 數值被判為原文找不到：檢查器只比對當前論文的 `paper.txt` | 修正 `check.py`：改依每頁 frontmatter `sources` 的所有論文比對 |
| 3 Wiki | C | 不通過 | paper 頁引用 WorDepth 的 DepthFormer 數值，但 `sources` 沒有列出 WorDepth | 回 3（第 1 次） |
| 3 Wiki | C | 通過 | 無大綱外新增頁面 | — |
| 4 spec | D（自動：對應、數值、篇幅） | 通過 | — | — |
| 4 spec | D（架構圖對照 Fig. 2） | 不通過 | 原圖 Scene Encoder 畫成兩個方塊（輸入影像、few-shot 訓練影像），spec 合成一個節點 | 回 4（第 1 次） |
| 4 spec | D（重跑） | 通過 | — | — |
| 4 spec | 使用者確認 | 通過 | — | — |
| 5 HTML | E（文字比對） | 不通過 | spec「Wiki：」欄位的段落編號（§4.1–4.3）被當成內容數值 | 修正 `check.py`：排除「Wiki：」欄位 |
| 5 HTML | E（文字比對，重跑） | 通過 | — | — |
| 5 HTML | E（1366×768 溢出、架構圖、換頁） | 通過 | — | — |

- 論文內的不一致（已寫入 paper 頁）：Table 3–4 的 RMSE / AELS 欄位疑似對調；Eq. 13–14 的 MARE / MSRE 公式疑似對調；DepthCLIP 的 NYU RMSE 在 Table 1 與 Table 5 不同；Table 2 的 ASTransformer 數值疑似誤植。
- 跨論文差異：DepthFormer 在 NYU V2 的數值與 WorDepth 報告的不同，已標註於 paper 頁與 [[NYU-Depth-V2]]。
- 修正後的 `check.py` 對 WorDepth 重跑檢查 C、E，皆通過。

## [2026-11-19] ingest | WorDepth 補齊為 workflow v2 格式
- 補建 `slides/2024_WorDepth-Variational-Language-Prior-for-Monocular-Depth-Estimation.outline.md`（內容為第 1 輪使用者確認的大綱）
- spec 的架構圖補上「範圍」「對照：Fig. 2」，HTML 第 4 張同步修正

| 節點 | 檢查 | 結果 | 問題 | 退回 |
|---|---|---|---|---|
| 3 Wiki | C（對照補建的大綱） | 通過 | 警告 4 項：[[Depth-Bins]]、[[Prompt-Tuning]]、[[DepthCLIP]]、[[2024_Learning-to-Adapt-CLIP-for-Few-Shot-Monocular-Depth-Estimation]] 不在 WorDepth 大綱內；均為第二篇 ingest 時建立、sources 也引用 WorDepth 的頁面，屬預期 | — |
| 4 spec | D（架構圖對照 Fig. 2） | 不通過 | 原圖中 μ̂、σ̂ 也以 detached gradient 輸入 Conditional Sampler（§3.2），spec 與 HTML 漏掉這條連線；另 spec 未說明只畫推論路徑 | 回 4（第 1 次） |
| 4 spec | D（重跑） | 通過 | — | — |
| 5 HTML | E（文字比對） | 通過 | — | — |
| 5 HTML | E（1366×768 溢出、架構圖、換頁） | 通過 | — | — |

- 備註：漏掉的 detached 連線在第 1 輪與 v1 重跑都沒有被發現，因為當時沒有「對照原圖」的檢查；v2 的檢查 D 第一次對照就抓到。

## [2026-11-19] schema | check.py 小修正
- 檢查 A：章節標題限制最多 4 個字，避免把「2. We recognize that ...」這類條列誤認為章節；兩篇重跑皆正確抓到 5 個章節
- index.md：更新 [[CLIP]] 的摘要（兩篇論文都有使用）

## [2026-11-19] schema | check.py 支援多種論文排版與數值格式
- 檢查 A：支援 ACM（「INTRODUCTION」全大寫無編號、「Table 1:」）與 Elsevier（「1.  Introduction」、「Table 1」無句點、「Fig. 1.」）排版
- 檢查 C：大綱的段落名稱只以「、」分隔（段落名稱本身可能含「, 」）；數值比對把同一行的「68.7 %」視為「68.7%」
- 原因：本輪三篇論文分別來自 ACM、CVF、Elsevier，初版檢查器只針對 CVF 排版設計（詳見下方各篇紀錄）

## [2026-11-19] ingest | Can Language Understand Depth?（workflow v2，B、D 使用者確認略過）
- 來源：使用者提供 PDF（ACM MM 2022 正式版）
- 新增頁面：[[2022_Can-Language-Understand-Depth]]、[[Zero-Shot-Transfer]]
- 更新頁面：[[DepthCLIP]]、[[Depth-Bins]]、[[Prompt-Tuning]]、[[Vision-Language-Model]]、[[CLIP]]、[[NYU-Depth-V2]]、[[index]]
- 產出：`slides/2022_Can-Language-Understand-Depth.outline.md`、`.spec.md`、`.html`（10 張）

| 節點 | 檢查 | 結果 | 問題 | 退回 |
|---|---|---|---|---|
| 1 抽取 | A | 不通過 | 找不到章節標題與 Table / Figure：ACM 排版為「INTRODUCTION」、「Table 1:」，檢查器只認 CVF 格式 | 修正 `check.py`（檢查器問題） |
| 1 抽取 | A | 通過 | — | — |
| 2 大綱 | B | 通過 | — | — |
| 2 大綱 | 使用者確認 | 略過（使用者授權） | — | — |
| 3 Wiki | C | 不通過 | 新增的 paper 頁與 [[Zero-Shot-Transfer]] 沒有寫進 index.md | 回 3（第 1 次） |
| 3 Wiki | C | 通過 | — | — |
| 4 spec | D（自動） | 通過 | — | — |
| 4 spec | D（架構圖對照 Fig. 2） | 通過 | 13 個節點與連線皆與原圖一致 | — |
| 4 spec | D（人工複查） | 不通過 | S8「後由 Hu et al. 實現」在 Wiki 標為補充，spec 未標註 | 回 4（第 1 次） |
| 4 spec | 使用者確認 | 略過（使用者授權） | — | — |
| 5 HTML | E（文字比對） | 通過 | — | — |
| 5 HTML | E（瀏覽器） | 不通過 | 架構圖把固定的 Depth Bins 畫成橘色（本簡報系列中橘色代表「可學」），語意錯誤 | 回 5（第 1 次） |
| 5 HTML | E（瀏覽器，重跑） | 通過 | — | — |

- 論文內的不一致（已寫入 paper 頁）：§4.4 的 rmse 1.186 與 Table 1 的 1.167 不同；§4.5 應引用 Fig. 3 卻寫 Table 3；Fig. 4 設定與主實驗不同；Table 2、3 的「最佳」標示與 rel 數值不符。

## [2026-11-19] ingest | Learning to Prompt CLIP for Monocular Depth Estimation: Exploring the Limits of Human Language（workflow v2，B、D 使用者確認略過）
- 來源：使用者提供 PDF（CVF Open Access 正式版，ICCVW 2023）
- 新增頁面：[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]]、[[CLIPMDE]]
- 更新頁面：[[DepthCLIP]]、[[Prompt-Tuning]]、[[Depth-Bins]]、[[Vision-Language-Model]]、[[CLIP]]、[[NYU-Depth-V2]]、[[KITTI]]、[[index]]
- 產出：`slides/2023_Learning-to-Prompt-CLIP-...outline.md`、`.spec.md`、`.html`（10 張）

| 節點 | 檢查 | 結果 | 問題 | 退回 |
|---|---|---|---|---|
| 1 抽取 | A | 通過 | 表格數值在抽取文字中被拆成單行，改以 `figure` 輸出頁面圖片核對 Table 3–7 | — |
| 2 大綱 | B | 通過 | — | — |
| 2 大綱 | 使用者確認 | 略過（使用者授權） | — | — |
| 3 Wiki | C | 不通過 | （1）新頁面又沒有寫進 index.md（與上一篇相同的錯誤）；（2）檢查器以「,」切分段落名稱，把「Learnable depth token（§3.1, Fig. 2）」切斷 | 回 3（第 1 次）；修正 `check.py`（檢查器問題） |
| 3 Wiki | C | 通過 | — | — |
| 4 spec | D（自動） | 通過 | — | — |
| 4 spec | D（架構圖對照 Fig. 1） | 不通過 | spec 漏掉 img_f 經 view / permute 攤平成 patch 的步驟 | 回 4（第 1 次） |
| 4 spec | D（重跑） | 通過 | — | — |
| 4 spec | 使用者確認 | 略過（使用者授權） | — | — |
| 5 HTML | E（文字比對） | 通過 | — | — |
| 5 HTML | E（瀏覽器） | 通過 | — | — |

- 跨論文差異：WorDepth Table 1 列本篇 NYU 的 log10 為 0.139，實為本篇的 RMSL（log10 為 0.128）；已寫入 paper 頁、[[CLIPMDE]]、[[NYU-Depth-V2]]。
- 寫 paper 頁時一度連到尚未建立的 [[2026_CLIP-Can-Understand-Depth]]，在跑檢查 C 前自行移除，待該篇 ingest 時補回。

## [2026-11-19] ingest | CLIP Can Understand Depth（workflow v2，B、D 使用者確認略過）
- 來源：使用者提供 PDF（Pattern Recognition 2026 正式版）
- 新增頁面：[[2026_CLIP-Can-Understand-Depth]]、[[FiLM]]、[[CLIPSeg]]
- 更新頁面：[[Prompt-Tuning]]、[[Vision-Language-Model]]、[[CLIP]]、[[CLIPMDE]]、[[DepthCLIP]]、[[NYU-Depth-V2]]、[[KITTI]]、[[SUN-RGBD]]、[[2023_Learning-to-Prompt-CLIP-for-Monocular-Depth-Estimation-Exploring-the-Limits-of-Human-Language]]、[[index]]
- 產出：`slides/2026_CLIP-Can-Understand-Depth.outline.md`、`.spec.md`、`.html`（10 張）

| 節點 | 檢查 | 結果 | 問題 | 退回 |
|---|---|---|---|---|
| 1 抽取 | A | 不通過 | 找不到章節標題與 Table / Figure：Elsevier 排版為「1.  Introduction」、「Table 1」（無句點）、「Fig. 1.」 | 修正 `check.py`（檢查器問題） |
| 1 抽取 | A | 通過 | — | — |
| 2 大綱 | B | 通過 | — | — |
| 2 大綱 | 使用者確認 | 略過（使用者授權） | — | — |
| 3 Wiki | C | 不通過 | 「68.7%」「75.6%」被判為原文找不到：原文寫成「68.7 %」 | 修正 `check.py`（檢查器問題） |
| 3 Wiki | C | 不通過 | 上一步的修正造成回歸：WorDepth 原文「2.039」換行接「% Improvement」被誤合併為「2.039%」 | 修正 `check.py`：只合併同一行空白（檢查器問題） |
| 3 Wiki | C | 通過 | SUN-RGBD 表格中間誤插空行，寫入時一併修正 | — |
| 4 spec | D（自動） | 通過 | — | — |
| 4 spec | D（架構圖對照 Fig. 2） | 通過 | L9 / L6 / L3 分別進入 3 個 transformer block、FiLM Mul / Add 對應 ⊗ / ⊕，與原圖一致 | — |
| 4 spec | 使用者確認 | 略過（使用者授權） | — | — |
| 5 HTML | E（文字比對） | 通過 | — | — |
| 5 HTML | E（瀏覽器） | 不通過 | 架構圖中 Input Image 的「→」與「↘」放在同一格而重疊 | 回 5（第 1 次） |
| 5 HTML | E（瀏覽器，重跑） | 通過 | — | — |

- 論文內的不一致與跨論文差異（已寫入 paper 頁）：Table 6 文字宣稱的「最佳」只在 CLIP-based 方法中成立；KITTI 表的 log10 欄混入 RMSElog 數值；ZoeDepth 參數 346M（文字）vs. 345,000k（表）；CaBins 的 NYU RMSE 0.041 疑似誤植；NeWCRFs 的 NYU RMSE 與 WorDepth 不同。

## [2026-11-19] lint | 全部 5 篇重跑檢查
- 修正後的 `check.py` 對 5 篇論文重跑 A、C（對照各自大綱）、D、E（文字）：全部通過
- 本輪觀察：
  - 「忘記更新 index.md」連續兩篇發生，都由檢查 C 攔下
  - 檢查器本身的問題（排版格式、分隔符號、數值格式、修正造成的回歸）共 5 次，多於內容錯誤
  - 架構圖相關問題 3 次：1 次在 D 對照原圖時攔下（缺步驟），2 次在 E 瀏覽器檢查時攔下（顏色語意、箭頭重疊，皆為版面呈現問題）
