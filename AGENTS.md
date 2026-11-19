# MDE Paper Wiki — Schema

這是一個以 **單目深度估計（Monocular Depth Estimation, MDE）** 論文為主題的 LLM Wiki，參考 Karpathy 的 LLM Wiki 作法。
使用者負責提供論文與決定重點；LLM 負責讀論文、撰寫與維護 Wiki、產生每篇論文的 HTML 簡報。

- **讀者**：使用者本人（MDE 研究者），目的是快速理解每篇論文的內容。
- **語言**：繁體中文，專有名詞保留英文（例如「相對深度（relative depth）」、`AbsRel`、`scale-invariant loss`）。

## 目錄結構

```
llm-wiki-slides/
├── AGENTS.md                 ← 本文件（schema）
├── raw/                      ← 原始論文（唯讀，不修改）
│   └── <YYYY>_<Paper-Title>/
│       ├── paper.pdf
│       ├── paper.txt         ← 由 PDF 抽出的全文（含頁碼標記），供檢查與搜尋
│       └── meta.md           ← 標題、作者、出處等書目資訊
├── tools/
│   └── check.py              ← 抽取與各節點的自動檢查
├── wiki/
│   ├── index.md              ← 內容目錄（每頁一行摘要）
│   ├── log.md                ← 操作紀錄（只追加）
│   ├── papers/               ← 每篇論文一頁，依簡報四章節整理
│   ├── concepts/             ← 概念、方法元件（如 scale-invariant loss、self-supervised depth）
│   ├── entities/             ← 資料集、評估指標、模型（如 KITTI、NYU Depth v2、δ<1.25、MiDaS）
│   └── syntheses/            ← 跨論文比較與綜合整理
└── slides/
    ├── <YYYY>_<Paper-Title>.outline.md ← 四章節大綱（使用者確認後才寫 Wiki）
    ├── <YYYY>_<Paper-Title>.spec.md   ← 逐頁內容（簡報的唯一內容來源）
    └── <YYYY>_<Paper-Title>.html
```

### 命名規則

- 論文資料夾與檔名：`<發表年份>_<論文標題>`，標題的空白改為 `-`，去除 `: , ? !` 等標點，保留原本大小寫。
  例：`2021_Vision-Transformers-for-Dense-Prediction`
- 同一篇論文的 `raw/` 資料夾、`wiki/papers/` 頁面、`slides/` 簡報使用相同名稱。
- concept / entity 頁面以英文名稱命名，例如 `wiki/entities/KITTI.md`、`wiki/concepts/Scale-Invariant-Loss.md`。

## 頁面格式

### 連結

- 使用 Obsidian 的 `[[wikilink]]`，例如 `[[KITTI]]`、`[[2021_Vision-Transformers-for-Dense-Prediction]]`。
- 第一次提到已有頁面的概念、資料集、模型時，一律加上連結。

### Frontmatter

每個 Wiki 頁面開頭都加上 YAML frontmatter：

```yaml
---
type: paper | concept | entity | synthesis
tags: [mde, ...]
sources: [2021_Vision-Transformers-for-Dense-Prediction]   # 內容依據的論文
updated: YYYY-MM-DD
---
```

### 引用

- 每個重要說法、數據都要標出處，格式為 `（§3.2）`、`（Table 2）`、`（Fig. 3）`；跨論文頁面需加上論文，例如 `（[[2021_Vision-Transformers-for-Dense-Prediction]], Table 1）`。
- 數值必須照抄論文表格，不得估算或改寫；沒有出處的內容不寫入 Wiki。
- 論文沒有提到、屬於 LLM 補充的背景知識，需標註「（補充）」。

### Paper 頁面結構（`wiki/papers/`）

依簡報的四個章節組織，方便直接轉成簡報：

```markdown
# <論文標題>

> 出處：<會議／期刊 年份>｜作者：<第一作者 et al.>｜原文：[[raw/.../meta.md]]

## 一句話總結
## Introduction        ← 研究背景、動機、現有方法的問題
## Method              ← 方法、架構、loss、訓練設定
## Experimental Results ← 資料集、評估指標、重點數據與 ablation
## Conclusions         ← 結論與限制（含論文自述的限制）
## 相關頁面             ← 連到的 concepts / entities / 其他論文
```

## Workflows

### Ingest（一次一篇，workflow v2）

流程為一個 graph：6 個生成節點，每個節點後接一道檢查；檢查不通過就沿退回邊回到指定節點，修正後重新檢查。B、D 兩道檢查通過後還需要使用者確認。

```
1 讀論文、抽取 ──A──▶ 2 四章節大綱 ──B+確認──▶ 3 寫入 Wiki ──C──▶
4 逐頁內容 spec ──D+確認──▶ 5 渲染 HTML ──E──▶ 6 記錄 log
```

| 節點 | 產出 | 檢查 | 不通過時退回 |
|---|---|---|---|
| 1 讀論文、抽取 | `paper.pdf`、`meta.md`、`paper.txt` | **A**：抽取完整（頁數相符、每頁有文字、各章節與 Table / Fig. 標題都抓得到） | 回 1 |
| 2 四章節大綱 | `slides/<...>.outline.md` | **B**：四章都有內容、每點都有出處與預定的 paper 頁段落、總張數 8～12；**使用者確認** | 回 2 |
| 3 寫入 Wiki | paper / concept / entity 頁、`index.md` | **C**：大綱的每個預定段落都存在於 paper 頁、大綱列出的 concept / entity 頁都已建立、大綱外新增的頁面需列出並說明；`[[wikilink]]` 無斷連結、無孤兒頁；frontmatter 齊全；數值都能在 `paper.txt` 找到；index 與頁面一致 | 回 3；大綱本身有缺漏則回 2 |
| 4 逐頁內容 spec | `slides/<...>.spec.md` | **D**：每頁內容都能在 paper 頁找到、數值一致；**篇幅預算**（見下方）；**架構圖**以節點與連線描述，並與論文原圖逐條對照；**使用者確認** | 回 4；Wiki 缺內容則回 3 |
| 5 渲染 HTML | `slides/<...>.html` | **E**：HTML 文字與 spec 一致（數值逐一比對）、1366×768 下無溢出、架構圖與 spec 的節點與連線一致、換頁正常 | 排版問題回 5；內容需要刪減或拆頁回 4（並重新經過 D） |
| 6 記錄 | `wiki/log.md`、提醒 commit | — | — |

每道檢查（含使用者確認）都要記錄結果；不通過時記下問題、退回到哪個節點、第幾次退回。

**v2 與 v1 的差異**：大綱移到 Wiki 之前，讓檢查 C 有大綱可以對照；篇幅與架構圖檢查從 E 提前到 D，E 只做最後確認。

#### 篇幅預算（檢查 D，由 `tools/check.py spec` 自動檢查）

- 每頁「內容」條列（含子條列）≤ 9 條，每條 ≤ 100 字元
- 每個表格 ≤ 7 列（不含表頭）
- 有表格的頁面，「內容」條列 ≤ 6 條

#### 架構圖對照（檢查 D）

- spec 的「圖表」以 `節點：` 與 `連線：` 列出架構圖，並註明 `對照：Fig. N`。
- 以 `python tools/check.py figure <raw 資料夾> <頁碼>` 將原圖所在頁輸出成圖片，逐條核對節點與連線是否與原圖一致，結果記錄在 log。

#### 節點細節

1. **取得論文**
   - 使用者給 PDF：放入 `raw/<YYYY>_<Paper-Title>/paper.pdf`。
   - 使用者給論文名稱：上網搜尋並下載 PDF。若有發表在期刊或會議，以正式版本為主（例如 CVF Open Access、NeurIPS / ICLR / AAAI proceedings、IEEE / Springer 等官方頁面），找不到可公開下載的正式版本時才使用 arXiv，並在 `meta.md` 註明。
2. **整理書目**：寫 `raw/<...>/meta.md`，內容包含：

   ```markdown
   # <論文完整標題>
   - 作者：
   - 出處：<會議或期刊全名（縮寫）>, <年份>
   - PDF 來源：<實際下載的網址>（正式版 / arXiv）
   - arXiv：<網址，若有>
   - 程式碼：<網址，若有>
   ```

3. **抽取全文**：`python tools/check.py extract <raw 資料夾>` 產生 `paper.txt`，並執行檢查 A。（以上 1～3 為節點 1）
4. **四章節大綱**（節點 2）：讀 `paper.txt`，寫 `slides/<...>.outline.md`（格式見下方），列出每章重點、出處、預定寫入的 paper 頁段落，以及預計新增或更新的 concept / entity 頁。執行檢查 B 後**停下來等使用者確認**；確認前不寫入 `wiki/`。
5. **寫入 Wiki**（節點 3）：
   - 依確認的大綱建立 `wiki/papers/<...>.md`，段落標題使用大綱中預定的名稱。
   - 新增或更新相關的 concepts / entities 頁面；新論文與舊頁面說法有出入時，在頁面中明確標註「與 [[某論文]] 不同：…」。
   - 更新 `wiki/index.md`。
   - 執行檢查 C：`python tools/check.py wiki <paper.txt> <outline.md>`。
6. **逐頁內容 spec**（節點 4）：依大綱與 paper 頁寫 `slides/<...>.spec.md`（格式見下方），只能使用 paper 頁已有的內容。執行檢查 D：`python tools/check.py spec <spec.md> <paper 頁>`，加上架構圖對照，通過後**停下來等使用者確認**。
7. **渲染 HTML**（節點 5）：依 spec 產生 `slides/<...>.html`，只做排版，不新增內容。執行檢查 E：`python tools/check.py html <html> <spec.md>`，並以瀏覽器在 1366×768 下逐頁檢查溢出與架構圖。
8. **記錄**（節點 6）：在 `wiki/log.md` 追加一筆（格式見下方）。

### Outline 格式（`slides/<...>.outline.md`）

```markdown
# <論文標題> — Outline

## Introduction（N 張）
- <重點>（§1）→ 段落：<paper 頁的段落標題>

## Method（N 張）
...

## 預計頁面
- concepts：[[A]]、[[B]]
- entities：[[C]]
```

### Spec 格式（`slides/<...>.spec.md`）

```markdown
# <論文標題> — Slide Spec

## S1 · Cover
- 標題：
- 內容：
  - ...
- 圖表：（無／表格欄位與列／架構圖）
  - 架構圖時：`節點：`、`連線：`、`對照：Fig. N`
- 出處：§ / Table / Fig.
- Wiki：[[<paper 頁>#<段落>]]
```

### Query

1. 先讀 `wiki/index.md` 找相關頁面，再深入閱讀，回答時附上出處。
2. 有保留價值的回答（例如多篇論文的比較）存成 `wiki/syntheses/` 的新頁面，並更新 index 與 log。

### Lint

使用者要求時，檢查整個 Wiki：
- 頁面之間互相矛盾的說法
- 沒有被任何頁面連到的孤兒頁
- 被多次提到但沒有獨立頁面的概念、資料集、模型
- 斷掉的 `[[wikilink]]`
- 缺少出處的說法
- index.md 與實際頁面不一致

## HTML 簡報規格

- 單一、自包含的 HTML 檔（CSS / JS 內嵌），可直接用瀏覽器開啟，支援鍵盤左右鍵換頁。
- 結構：
  1. 封面：論文標題、作者、出處、年份
  2. **Introduction**：研究背景、動機、現有問題
  3. **Method**：方法或架構
  4. **Experimental Results**：重點實驗結果（以表格呈現關鍵數據）
  5. **Conclusions**：結論與限制
- 每章 1～3 張投影片，總長度以快速理解為原則（約 8～12 張）。
- 繁體中文，專有名詞保留英文；每張投影片底部標註內容出處（§ / Table / Fig.）。
- 內容只能來自對應的 spec（spec 又只能來自 `wiki/papers/` 頁面），不另外加入 Wiki 沒有的內容。

## index.md 格式

依分類列出所有頁面，每頁一行：

```markdown
## Papers
- [[2021_Vision-Transformers-for-Dense-Prediction]] — DPT：以 ViT 作為 dense prediction 的 encoder（ICCV 2021）
```

## log.md 格式

只追加、不修改舊紀錄。每筆以固定前綴開頭，方便用 `grep "^## \[" wiki/log.md` 查詢：

```markdown
## [YYYY-MM-DD] ingest | <論文標題>（workflow v2）
- 新增頁面：...
- 更新頁面：...
- 產出：...

| 節點 | 檢查 | 結果 | 問題 | 退回 |
|---|---|---|---|---|
| 1 抽取 | A | 通過 | — | — |
| 3 大綱 | B＋使用者確認 | 不通過 | <問題描述> | 回 3（第 1 次） |
| ... | | | | |
```

每次執行檢查（包含重新檢查）都記一列，退回欄寫「回 N（第 k 次）」。

操作類型：`ingest`、`query`、`lint`、`schema`（修改本文件時）。

## 版本控管

本資料夾為 git repository。每完成一次 ingest、query 或 lint，提醒使用者 commit。
