# 分出版社 PDF 内容提取技巧

按出版社/刊系列记录**双栏、图、表、参考文献、摘要**等抽取要点，加快 `original_extracted.txt`、裁图与文献切分。  
新出版社按同样小节结构追加即可（Wiley、AGU、GSA、Nature 系列等）。

## 期刊→出版社速查（易错）

| 缩写/刊名 | 出版社 |
|---|---|
| **JMG**（Journal of Metamorphic Geology） | **Wiley** |
| LITHOS、EPSL、GCA、Precambrian Res. | Elsevier |
| **J. Petrol.**（Journal of Petrology）、Geol. Mag. | **Cambridge University Press** |
| Tectonics | Wiley |
| Gondwana Res. | Elsevier |
| Geology、GSA Bulletin | GSA |
| GRL、JGR、G-cubed | AGU |
| Nature、Nat. Commun.、Nat. Geosci. | Nature Portfolio |
| **Front. Earth Sci.** 等 Frontiers 系（10.3389/…） | **Frontiers**（MDPI 同为 OA 双栏可参考） |

**栏数判定速查**（先定栏数再选启发式）：

| 栏数 | 判据 | 阅读序 | 已验证刊例 |
|---|---|---|---|
| 单栏 | 多为全宽 block | 按 y | Elsevier 综述（LITHOS 536–537） |
| 双栏 | x0/x1 直方图两簇 | 每页 L→R，各自 y 序 | Frontiers（x≈50/305）、Elsevier 双栏正文 |
| 三栏 | x0 三簇（留 3–5 pt 容差） | c0→c1→c2 | GSA Geology（x≈33/213/393） |

通用底线（任何出版社）：

- `sys.stdout.reconfigure(encoding='utf-8')`；文件 `encoding='utf-8'`。
- **先语义重排再翻译**，禁止按物理行硬译。
- 图题与正文、页眉 running head 分离；裁图后 PIL 查顶/底暗像素。
- 文献列表与正文分开抽；`et al.` 勿译。

---

## Elsevier（LITHOS / EPSL / GCA / Precambrian Res. 等）· 已用 Wei-2026-Lithos 验证

刊例：LITHOS 536–537 (2026) 108536（Invited Review，单栏 + 通栏图为主；亦常见双栏正文）。

### 1. 版面结构（先摸清再切）

| 元素 | 典型位置 | 抽取注意 |
|---|---|---|
| 刊眉 | 页顶 | `C. Wei and B. Wang L I T H O S …`、`Contents lists available at ScienceDirect` → 删 |
| 页码 | 页底/顶 | 单独数字行 → 删 |
| 文章类型 | 首页 | `Invited Review Article` 等可留作元数据 |
| 摘要+关键词 | 首页 | **双栏时关键词栏与摘要正文交错**；勿把 `Keywords:` 列当摘要 |
| 作者单位 | 首页 | `a/b/c` 上标；Elsevier 常一行多单位 |
| 正文 | 单栏或双栏 | 本篇综述偏单栏通栏；实验/案例文常见双栏 |
| 图 | 多为**通栏** | 图题常在图下方 `Fig. N.`；少数在右栏（如 Fig.12） |
| 表 | 通栏 | `Table N` + 表题；成分表 10+ 列易挤 |
| 参考文献 | 文末 | 按字母序；`Surname, X.X., year.` |

### 2. 全文抽取顺序（推荐）

1. **PyMuPDF `get_text('dict')` 按 block**（比纯 `pdfplumber.extract_text` 少行交错）。  
2. 每页：页眉/页脚块剔除 → 若 `x0` 明显分两栏则 **左栏 y 序 → 右栏 y 序**；若多为全宽 block 则按 y。  
3. 去 `===== PAGE n =====` 可保留在中间件，**入译稿前删**。  
4. 软连字符 `­`、行尾 `-\n` 连接词合并（`pro­grade`→`prograde`）。

**双栏判定启发式（本项目用过）：**

```text
left  = blocks with x0 < 300
right = blocks with x0 >= 300
若 left、right 均 ≥3 个 body block → 按 L→R
否则按 y 排序全宽
页眉 y < 55；页脚 y > 760
```

### 3. 章节切分锚点（Elsevier 惯例）

- `1. Introduction`、`2. …`、`7. Summary`、`Acknowledgements`、`References`  
- **坑**：双栏下 `7. Summary` 可能插在 CRediT/Declaration 中间 → 切完后用 `7. Summary`…`Chunjing Wei:`/`CRediT` 核对，**摘要与总结勿对调**。  
- `References` 有时无独立行、与 `Appendix A` 粘连 → 用首条 `Barnicoat` 等字母序条目或 `(?m)^References\s*$`。

### 4. 摘要与关键词

- 结构常为：`A R T I C L E  I N F O` / `A B S T R A C T` / `Keywords:` 列 + 摘要正文段。  
- **验收**：中译后首页不得残留 `This study presents` 等英文句首（见 pitfalls 7.1）。  
- 关键词：`Phase equilibria; Pseudosection; …` → 中文分号列表。

### 5. 图（Figures）

| 技巧 | 说明 |
|---|---|
| 图题识别 | 行首 `Fig. N.` 且长度 >50；正文 `see Fig. 3.` 不是图题 |
| 图区 | 通常在图题**上方**；clip 上缘 = max(最后正文 bottom, drawings top−ε) |
| 通栏 vs 分栏 | caption.x1−x0 > ~400 或跨 x=300 → 全宽裁 |
| 右栏小图 | 如 ACF+投影四联图，caption 在右栏时只裁右栏图区 |
| 分辨率 | `Matrix(2.2–2.8)` |
| 校验 | 顶 30–40px 暗像素比；目检面板字母 a/b/c |

本篇 12 图：p3–p15，图题多在页中下；Fig.2 在 p4 图题 y≈675，图在上方 y≈294–668。

### 6. 表格

- Elsevier 成分表：`scriptsize/footnotesize` + `\arraystretch` + 长首列改脚注（见 pitfalls 7.9）。  
- 抽取：`pdfplumber.extract_table` 或人工按 `&` 对齐；**数值逐格核对，勿让子代理猜列**。

### 7. 参考文献

1. 从 `References`（或首条字母序）到文末。  
2. 去页码行、running head、`(For interpretation…)`。  
3. 条目边界：`\.(?=\s*(?:(?:van|von|de)\s)?(?:\w+\s){0,2}\w{2,},\s?[A-Z]\.)`（首字母后带句点）。  
4. Elsevier 常见：`Contrib. Mineral. Petrol.`、`Gondwana Res.`、`Precambrian Res.`、`Lithos` → **保留英文**；`J. Petrol.` 属剑桥，勿当 Elsevier 刊名。  
5. 乱码：`G´eol`、`pou´ebo`、`O’ Hara` 尽量原样；`et al.` 保留。  
6. 验证：条目含年份、首字母序单调、点名文献可 grep。

### 8. 公式与特殊符号

- 度数：`◦C` / `◦` → `$^\circ\mathrm{C}$`。  
- 矿物缩写 Whitney and Evans：Amp, Grt, Pl, Cpx, Opx, Qz, L…  
- 反应式：`Amp+Qz=Cpx+Pl+L` → `equation` + `\tag{R1a}`。

### 9. 一键检查（Elsevier 交稿前）

```text
英文摘要句首=0
页眉 LITHOS / ScienceDirect =0（译稿内）
Fig. N. 行首图题 12 个 ↔ figNN.png 12
References 条目数合理且含年份
modelling→模拟；pseudosection→视剖面图
```

---

## Cambridge University Press（Journal of Petrology、Geological Magazine 等）· 待补

> **J. Petrol. = Journal of Petrology = Cambridge**（勿写入 Elsevier/Wiley）。

- [ ] 刊眉/页码样式  
- [ ] 双栏/单栏与图题 `Fig. N.`  
- [ ] 摘要结构  
- [ ] 参考文献 CUP style 与切分  
- [ ] 附图/SI  

## Wiley（Journal of Metamorphic Geology、Tectonics 等）· 已用 Yakymchuk-2023-JMG 验证

> **JMG = Journal of Metamorphic Geology = Wiley**（勿写入 Elsevier）。  
> EPSL = Earth and Planetary Science Letters = **Elsevier**（勿写入 Wiley）。  
> DOI 前缀 Wiley 常见 `10.1111/...`；Elsevier 为 `10.1016/...`。


刊例：Yakymchuk, C., 2023, *J. Metamorph. Geol.* **41**, 719–743（JMG，Wiley）。单篇短文（约 10 图），双栏正文 + 通栏/半栏图混排。

### 1. 版面结构（JMG）

| 元素 | 位置/特征 | 抽取注意 |
|---|---|---|
| 刊眉 | 页顶 | `Author (year) 中文译本` 对应原文 running head 为作者+刊名+卷页；译稿 fancyhdr 自拟 |
| DOI | 首页正文附近 | `doi:10.1111/jmg.xxxxx`（Wiley 10.1111） |
| 摘要 | 首页作者下 | 无 `ARTICLE INFO` 框；摘要为连续段；关键词常一行 |
| 正文 | **双栏** | x0 约左 35–290 / 右 300–560（与 Elsevier 同量级） |
| 章节 | 数字节 | `1 Introduction`…`5 Conclusions`、`Acknowledgements`、`References` |
| 图 | 通栏或半栏 | 图题 `Fig. N.`；JMG 用 **Fig.** 不是 Figure |
| 表 | 通栏 | `Table N` |
| 参考文献 | 文末双栏 | Wiley：`Surname, A.B., Year. Title. Journal Vol, pages.` |

### 2. 全文抽取顺序

1. PyMuPDF `get_text('dict')` 按 block，或 pdfplumber 抽完后**按双栏 y 重排**。
2. **双栏交错**：同一逻辑段左右栏穿插，必须先 L 栏 y 序 → R 栏 y 序，再译。
3. 软连字符 `­`、行尾连字符合并。
4. 章节锚点：`1 Introduction`、`2 …`、`Conclusions`、`Acknowledgements`、`References`（无句点或有句点两种都出现过，用正则 `\d+\.\s+` 与字面 `Conclusions` 并用）。

### 3. 摘要与首页（本会话定稿版式，已写入 latex-template）

**题目作者之后：** 摘要 → 关键词 → 原文信息 → 说明（段首标签 `摘要：`/`关键词：`/`原文信息：`/`说明：`，**不用** abstract 环境）；段间距约 1.2–1.6em。  
- **不写**「关键词（原刊）」独立块（与摘要后关键词重复）。  
- 「原文信息」为 `\noindent\textbf{原文信息：}Yakymchuk, C., 2023. …`（**同一行**，不换行）。  
- 通识章节标题（引言/方法/结果/讨论/结论/致谢）**只中文**，不加（Introduction）等。

### 4. 图（JMG 实测 10 图）

| 项 | 已验证做法 |
|---|---|
| 图题识别 | `Fig. N.` 行；与正文 `Fig. N` 引用区分 |
| 双编号坑 | **图注正文禁止写「图 N：」**；`\caption` 会自动加「图 N」，否则出现「图 2：图 6：」 |
| 图号对齐 | `figNN.png` 的 NN = 原刊图号；若出现顺序也是 1…N 可不用 setcounter |
| 图序 | 按图号 1→N 安插；插入点 = max(全文首次「图 N」/`\ref` 段末, 上一幅图结束)；**全部在结论/致谢前** |
| 尺寸锁定 | 用户指定 100%/60% 等**不再被 aspect 启发式改写** |
| 竖长图 | 如 JMG 图 9 示意插图 aspect≈2.6，必须 `height=0.72\textheight, keepaspectratio`，否则图注被挤出页面（页上只剩页眉） |
| 校验 | PyMuPDF 扫 PDF「图1…图10」首次页码须递增；`.aux` `\newlabel` 交叉核对图号 |

**JMG 图号—内容对应（便于抽图对图）：** 1 湿花岗岩固相线/反应；2 矿物 Zr 含量（Bea）；3–4 P–T 视剖面与熔体/转熔矿物；5 熔体性质与饱和 Zr；6 Bulk D_Zr；7–8 变泥质岩/MORB 等压加热 Zr 预算；9 Zr 来源去向示意；10 锆石稳定上限。裁切后按**图注内容**核对，不只信文件名。

### 5. 文献切分

- 参考文献从 `References` 起到文末；JMG 条目 `Author, A.B., Year. Title. Journal Vol, Pages.`  
- 译稿参考文献**保留英文**；`et al.` 不译。  
- 与附录/支持信息粘连时用首条作者姓或 `(?m)^References\s*$`。

### 6. 一键检查（Wiley/JMG 交稿前）

1. 图 1…N 页码递增，且均在结论/致谢前。  
2. 图注无双编号；图号=figNN=图注内容。  
3. 用户指定图宽未被改掉。  
4. 首页顺序：摘要→关键词→原文信息→说明；无「关键词（原刊）」。  
5. 章节标题无英文括注。  
6. 竖长图未导致「空页只剩页眉」（图注必须可见）。  

## AGU（Tectonics / JGR / GRL / G3 等）· 已用 Knight-2025-TECT（Tectonics 2025）验证

> **新旧两代 AGU 版式完全不同**：2020s Wiley 平台电子版（DOI `10.1029/…`，agupubs.onlinelibrary.wiley.com）≠ 1990s 扫描双栏版（如 Royden-1993-JGR）。动手前先判断：电子版文本层完好、无 OCR 烂字；扫描版每页是一整页位图、公式要渲染读图（同 SI 公式处理，§4）。

刊例：Knight, B. S. et al., 2025, *Tectonics* **44**, e2024TC008509（主文 18 页 + Supporting Information 10 页）。

### 1. 版面结构（新版 AGU/Wiley 平台）

| 元素 | 位置/特征 | 抽取注意 |
|---|---|---|
| 版心 | **不是传统双栏**：左侧窄作者信息栏（x≈31–150）+ 单栏正文（x≈167–570） | 按双栏切 x≈300 会把信息栏切碎；全宽图跨 x≈50–550 |
| 页眉/页脚 | 页眉横线 y≈69；页脚 running head y≈761 | 裁图勿裁入 |
| **下载水印** | 右缘竖排 x≈585–591 + 每页散行文本块 | 见 §2 清洗 |
| 首页 | Key Points（要点列表）+ Abstract + Plain Language Summary + CRediT + Received/Accepted | Key Points 译「要点」列表；通俗摘要译「通俗语言摘要」 |
| 章节 | `1. Introduction`、`2. …`、`3.1.` 小节、`Conflict of Interest`、`Data Availability Statement`、`Acknowledgments`、`References` | 数字节锚点；声明类小节也要译 |
| 图/表 | 图题 **`Figure N.`**（AGU 不用 `Fig.`） | 与 JMG 的 `Fig.` 区分 |
| SI | 独立 PDF：Text S1–Sn、Figure S1、Tables S1–Sn、Movies S1–Sn 说明 | 合并翻译见 §4 |

### 2. 全文抽取与水印清洗

1. pdfplumber / PyMuPDF 直接抽（文本层完好）；**每页重复的 Wiley 水印碎片**混入正文：`Downloaded from https://agupubs…`、`See the Terms and Conditions…`、`Wiley Online Library`、机构名（如 `Nanyang Technological University Lee Wee Nam Library`）等短行竖贯全页。
2. 清洗：逐行删含 `Downloaded|Terms and Conditions|onlinelibrary|agupubs|Wiley Online Library|OA articles|are governed by|the applicable Creative` 的行；抽块时跳过 x>580 窄块。
3. 其余照常：软连字符合并；章节按锚点切分。

### 3. 摘要与首页

- 首页四段沿用 latex-template 版式；**关键词自拟**（AGU 无关键词行，从 Key Points/主题提炼中文关键词）。
- DOI 用短显示防超宽：`\href{https://doi.org/…}{doi:…}`（长 `\url` 在原文信息行会顶出版心）。
- **作者/单位行必须限宽**：AGU 作者多、单位长，一行放不下会被版心右侧裁掉（用户截图可见）。作者拆 2 行、单位每行 `\small` 独立成行（`\small` 只作用到行尾，pitfalls 7.17/8.5）。

### 4. Supporting Information 合并翻译（AGU 惯例独立文件）

- 译本中作独立章节「支持信息（附件）」（参考文献后、译者附录前），首句注明为原文 S1 全译；公式沿用原编号（`\tag{}`）不与正文抢号。
- **SI 公式 pdfplumber 抽取常烂**（上下标/分式全乱）→ **渲染读图法**：`Matrix(3–5)` 渲染公式页、按坐标裁公式局部、Read 看图抄式；参数对照表 S1 核量纲。
- SI 大表（材料性质、模型列表）主代理逐格抽（pitfalls 6.4）；**表印误与正文矛盾**（如表 S2 速度条件排印与正文相反）→ 按正文更正并注明「原刊排印如此」。
- Movies S1–Sn 只有文字说明，译成 `itemize` 列表；横版整页图（SI 页可为 870×584 pt 横版）整页即图。

### 5. 参考文献

- 单栏列表：`Author, A. B., … (2025). Title. \textit{Journal}, \textbf{vol}(issue), pages.` + `\url{https://doi.org/…}`；enumitem `itemize`。
- 引文 `et al.` 保持英文（terminology 三·引文节）。

### 6. 图裁切（Knight 实测 11 图 = 主文 10 + SI 1）

- 图题识别：**行首** `Figure N.` 且块长>50（pitfalls 7.2）；图题在图下方。
- **像素剖面精测边界**：2× 渲染页 → numpy 行/列墨迹剖面（灰度<200）定内容 bbox，替代反复目检；裁完抽查顶/底 30–40 px 暗像素比（pitfalls 7.3）。
- clip 规避：页眉线 y≈69、页脚 y≈761、右缘水印 x≈585–591；图题文字不裁入（译本重写图注）。
- 多面板演化图（A–E + 应变率面板）裁全宽；半宽图按正文栏 x 范围。

### 7. 一键检查（AGU 新版交稿前）

- [ ] 水印残留=0：`Downloaded|Terms and Conditions|onlinelibrary` 计数为 0
- [ ] Key Points（要点）与通俗语言摘要已译；声明类小节齐
- [ ] 图注 `Figure N`→「图 N」序 1..N **非降**（同页按文本位置先后，pitfalls 8.6）
- [ ] SI 章节含公式、表 S1/S2、Movies 说明；表印误处有更正注
- [ ] 首页四段齐；作者/单位行无超版心（`get_text('blocks')` 查 x1>556 块数=0）

## GSA（Geology / GSA Bulletin / Geosphere）· 已用 Liu-2026-GEO（Geology）验证

刊例：Geology（GSA），Gold OA，三栏正文 + 通栏/半通栏图；页宽约 594 pt（A4 近似），栏起点 **x≈33 / 213 / 393**（栏宽约 170，栏隙约 10）。

### 1. 版面结构

| 元素 | 典型位置 | 抽取注意 |
|---|---|---|
| DOI / 收稿日期 | 首页右上（y&lt;120, x&gt;380） | 勿当正文栏；否则 `body_y0` 被拉到 y≈36，页眉/单位全进正文 |
| 题目/作者/单位 | 首页通栏 | 单位换行块 `x1` 可能 &lt;500 → 仍属页眉，按 **y ≤ body_y0** 归页眉，勿按全宽启发式 |
| ORCID/邮箱盒 | 首页左栏**偏下**（y≈630–700） | 深在正文区仍属页眉元数据：`orcid.org`、`@`、`\d{4}-\d{4}` 强制进 header |
| 摘要 | 首页左两栏通栏（x0=33, x1≈383） | 不是三栏之一的「宽栏」；按 y 序整块抽出 |
| 正文 | 三栏，阅读序 **c0→c1→c2** | 用 `x0` 直方图定边界：`col0 x0&lt;213`，`col1 213≤x0&lt;393`，`col2 x0≥393`；**边界要留 3–5 pt 容差**（浮点 392.99 误入中栏） |
| 图题 | `Figure N.`（**不是** `Fig. N.`） | 通栏或仅跨左两栏（如 Fig.4 caption `x1≈383`） |
| 补充材料脚注 | 嵌在中栏正文里 | 行首 `1Supplemental`，后续同栏行并入 note，**勿留在正文栏流** |
| 参考文献 | 文末三栏；起始可能在**中栏中部** | 见 §7 |
| 页脚 | y≈750 刊眉条 + 页码；y≈772 `Downloaded from…` 水印 | `footer_y = page_h − 32`（勿用 −75，会切掉 y≈718 的正文末行） |

### 2. 页眉 / 正文分界（关键启发式）

```text
1) 排除 header_meta：y1<120 且 x0>380（DOI/收稿）；含 orcid.org / 邮箱 / \d{4}-\d{4} 的盒
2) body_y0 = min{ y0 : x0≥213, 非全宽, len(text)>2, y0>120, 非 header_meta }
3) 页眉 = y1 ≤ body_y0+5 或 header_meta（即使 y 很深）
4) 页脚 = y0 ≥ page_h−32
5) 正文分栏按上表；面板字母 A–F（宽&lt;40）单独收集，随早图注输出
```

**整行合并**：同栏内 `|y0 差|≤2.5` 为同一视觉行，按 x 排序拼接；段落断点 `y0−prev_y1 > 4.5`。  
**去连字符**：拼接时 `piece.endswith('-')` 或软连字符 `­` → 去掉连字符直接接下一段；全文再 `(?<=[A-Za-z])-\s+(?=[a-z])` 收尾。

### 3. 章节锚点

- `ABSTRACT` / `INTRODUCTION` / `SAMPLES AND METHODS` / `RESULTS` / `DISCUSSION AND IMPLICATIONS` / `ACKNOWLEDGMENTS` / `REFERENCES CITED`
- 讨论小节标题可能**折行断开**（如 `Diffusion-Controlled Element Transport` + 下一行 `and Fluid-Mediated Connectivity`）→ 在 DISCUSSION…ACKNOWLEDGMENTS 区间用带 `\s*` 的整段正则搜，勿只搜半句。
- **小节顺序以页内坐标为准**（同页多栏同 y 时按 c0→c1→c2），勿信文件名：本项目 `section_disc_model` 与 `section_disc_pulses` 内容曾与文件名对调，译前用首句语义核对。

### 4. 摘要与首页

- 摘要整块中文后接关键词；`说明` 注明附录「不属于原文内容」（若有附录）。
- 题目下作者单位多行：`\small` 只作用于首行 → 用  
  `\parbox{0.96\textwidth}{\centering\small 单位1；\\单位2；\\单位3}`，避免字号不一。
- CITATION 行、刊眉条（`Geological Society of America | GEOLOGY | Volume XX`）入稿前删。

### 5. 图（Figures）

| 技巧 | 说明 |
|---|---|
| 图题识别 | 行首/块首 `Figure N.`；正文 `Figs. 1A` 不是图题 |
| 图与图题相对位置 | GSA 常见**图在图题上方**；用 caption.y0 反推 clip 底，顶缘 drawings/images top−ε |
| 多面板 | A–F 面板字母是短文本块；勿裁进图注文字（图注改中译） |
| 半通栏图 | caption.x1 &lt; 全宽（如仅到 x≈383）→ 只裁左两栏宽度 |
| 分辨率 | `Matrix(2.2–2.8)`；本项目 2.5 |
| 手工 clip | 图区常跨多栏通栏，用页坐标矩形比「按栏猜」稳；裁完 PIL/目检面板完整 |

**版式联动（用户常改）**：

- 高图独占一页且上部留白 → **缩小 `width`（如 0.88\textwidth）+ 图注 `\footnotesize` + `[b]` 或 `[!htbp]`**，让上文进入同页；勿用 `[H]`。
- 两图挤同页、页底大段空白 → **拆开插入点**（如图2 随结果、图3 随讨论首小节），避免 float page。
- 图首次引用在讨论后半 → 图环境放进**该小节标题后**，不要堆在讨论总输入之后。
- 图注勿在致谢/附录片段里再写一遍正文（`% figN:` 注释掉的标签下的**图注正文仍会排版**）→ 只保留 figure 环境内的 caption，或整段删除。

### 6. 表格与 SI

- 成分表与 Elsevier 同：`\footnotesize` + `\arraystretch`；大表主代理逐格抽。
- SI 常为单独 `docx`：正文文本可抽；**公式是 OMML**，用 lxml 解析 `oMath` 得式 S1–S6 再写附录；xlsx 数据表可直接读。

### 7. 参考文献（三栏）

1. 起点：`REFERENCES CITED`（可能在**中栏 y≈450+**，不在页顶）。
2. 阅读序：起始页 **中栏自 REFERENCES 起 → 右栏全文**；其后页 **c0→c1→c2**；跨页续条目（栏顶半句）靠列拼接自然衔接。
3. 切分：`\.(?=\s*(?:(?:van|von|de)\s)?(?:\w+\s){0,2}\w{2,},\s?[A-Z]\.)`（首字母后带句点，同 pitfalls 6.3）；DOI 碎片并回前条。
4. 断词收尾：`(?<=[A-Za-z])-\s+(?=[a-z])` 去掉行尾连字符空格（`metamor- phic`→`metamorphic`）。
5. 校验：约 30–40 条、含年份、首条/末条与正文引用可 grep；`et al.` 保留。
6. URL 包 `\url{}`，先修 `doi.org//` 双斜杠。

### 8. 一键检查（GSA 交稿前）

```text
英文摘要句首=0
刊眉 Geological Society of America / Downloaded from =0
Figure N. 图题数 ↔ figNN.png
图注无双编号；图序页码递增且在参考文献前
REFERENCES 条目含年份；et al. 未译成「等」
footer 未切正文末行（对照 y≈718 是否还在）
```

---

## Frontiers（Front. Earth Sci. / Tectonics 等 10.3389/…）· 已用 Ritter-2024-FES 验证

刊例：Front. Earth Sci. 12:1286468（2024），CC BY 开放获取，双栏正文 + 文内嵌图，页宽约 595 pt（A4），栏起点 **x≈50 / 305**（左栏 x1≈290，右栏 x1≈546）。

### 1. 版面结构

| 元素 | 典型位置 | 抽取注意 |
|---|---|---|
| 页眉 | y≈35 通栏 | `Ritter et al. 10.3389/feart.2024.1286468`（作者+DOI 一行）→ 删 |
| 页脚 | y≈800 通栏 | `Frontiers in Earth Science NN frontiersin.org`（NN=页码）→ 删 |
| 首页右侧元数据盒 | 右栏上部 | EDITED BY / REVIEWED BY / CORRESPONDENCE / RECEIVED / ACCEPTED / CITATION / COPYRIGHT 一整列 → **全部删**，但其中 CITATION 行可作「原文信息」素材 |
| 题目/作者/单位 | 首页通栏 | 单位上标数字；通讯作者带 `*` |
| 摘要+关键词 | 首页左栏起 | 摘要无 `Abstract` 标题（Frontiers 版式），段后 `keywords` 行逗号分隔；关键词行与正文易混 |
| 正文 | 双栏 | 阅读序每页 **L→R** |
| 图 | **文内嵌**（非文末集中） | 图在上、图题在下；见 §5 |
| 表 | 可跨页续表 | `TABLE 1 …` + `(Continued)` 续页；见 §6 |
| 尾部声明 | 结论之后 | 见 §8「Z 形回流」——Frontiers 最大坑 |
| 参考文献 | 文末双栏 | 见 §7 |

### 2. 全文抽取顺序与栏判定

**pdfplumber 对 Frontiers 粘词严重**（`PUBLISHED 15February2024`、`Allrock compositions`）；用 **PyMuPDF `get_text('dict')` 按 block** 抽，块内行拼接已含正常空格。

栏判定（本项目验证）：

```text
full-width = (x1-x0) > 0.6*W          # 页眉/页脚/表续题
left       = x1 < 300                 # 左栏 x1≈290
right      = 其余                     # 右栏 x0≈305
⚠ 禁用 x0<0.52W 判左栏：右栏 x0=305 < 309.5 会整栏误判入左
每页阅读序 = left.y 序 → right.y 序；full-width 按 y 嵌入
```

去噪行（正则删）：`Ritter et al.`、`10.3389/feart.…`、`Frontiers in Earth Science`、`frontiersin.org`、独立两位页码行 `^\d{2}$`。首页右侧元数据盒按 **x0>305 且 y<500 且为标题式短行**（全大写/`Correspondence` 等）成块删除，勿逐行删（会误删正文）。

### 3. 章节锚点

- 数字编号带句点：`1 Introduction`、`2 Methods`、`2.1 Hydration process`、`3 Numerical results`、`3.1 …`、`3.2.1 …`、`4 Discussion`、`4.4 Model limitations`、`5 Conclusion`。
- 标题为 Title Case（不是全大写）；切分时要求**行首独立成行**，防正文句中命中。
- 多级编号 `3.2.1` 直接可用锚点，无需再猜层级。

### 4. 摘要与首页

- 摘要块无 `Abstract` 字样 → 以「题目/单位之后的首段」为界，直到 `keywords` 行。
- 关键词行原文即逗号分隔小写短语（`subduction initiation, subduction evolution, …`）→ 中文顿号列表。
- 「原文信息」直接改写 CITATION 盒：`Ritter S, Balázs A, Ribeiro J, Gerya T. 2024. … Front. Earth Sci. 12:1286468. doi:10.3389/feart.2024.1286468`；期刊缩写保留 `Front. Earth Sci.`。

### 5. 图（Figures）

| 技巧 | 说明 |
|---|---|
| 图题识别 | 块首 **`FIGURE N |`**（全大写 + 竖线！）；正文 `Figure 2A)` 引用不是图题 |
| 图位置 | 图题**上方**同页内嵌；每图恰好 1 张栅格图（`page.get_images` =1） |
| 图区 bbox | **直接用 image 的 bbox ±3 pt** 即可；页上 4 条 drawings 是版心装饰框（x≈50/546 两条竖线+上下横线），勿并入 clip |
| 页眉残字 | clip top 取 image.y0−3 即可（页眉块 y≈35，图 y0≈94，天然隔离） |
| 跨栏图 | image.x0≈130–82 不等，均在版心内；不用分栏，直接整图 |
| 分辨率 | `Matrix(2.5)`（本项目 2.2–2.8 区间内） |
| 校验 | 顶/底/左/右 8px 条带均值=255（全白边）即未切到内容；再目检面板 |
| 图注格式 | 中文图注**不带「图 N：」前缀**；`FIGURE N |` 之后整段全译（含缩写释义表）；清理夹入的页眉页脚行 |

**版式联动（本项目实测）**：图注长 + `height` 未限 → 整块超 `\topfraction`，`[!htb]` 无 `p` 会被压到参考文献之后（pitfalls 3.14）→ **一律 `[!htbp]`**；竖长多面板图 `height=0.72\textheight,keepaspectratio`。

### 6. 表格

- `pdfplumber.extract_table` 对 Frontiers 表格效果好（本项目 29 行×9 列表 1 一次抽净）。
- 续表页有重复表头 + `TABLE 1 (Continued)` 行 → 删表题行、保留表头一次。
- **组行**（如 `wet olivine for the weak zone, V=1.3 J/Pa`）是分组标题，用 `\multicolumn{9}{l}{…}` 占整行，勿当数据行。
- 脚注 a–f 跟在表后（`a reference model.` `b exhumed weak zone…`）→ 并入 `\caption` 尾部或 `\footnotesize` 注；表头缩写释义行（`model no.=model number, …`）同样并入 caption。
- 数值里的 `×`（`50x63`）可保留 `50×63`；上标脚注 `m1a,b` → `m1$^{a,b}$`。

### 7. 参考文献（双栏、可跨栏续条目）

1. 起点 `References` 标题可能在**左栏下部**（本项目 y≈656），不在页顶。
2. 阅读序：每页 L→R；条目内**跨栏续写**（上一栏末尾半句、下一栏顶部接续，本项目 Hickey-Vargas 条目）→ 跨栏块**并回前条**。
3. 条目切分：起点正则须允许复姓前缀与年份后缀：
   `^(?:[A-Z…][\w…-]+,\s?[A-Z]\.|(?:van|von|de|da)\s+[A-Z][\w-]+,\s?[A-Z]\.)`
   年份校验 `\((19|20)\d\d[a-z]?\)`（`2011a` 勿漏）。
4. 未匹配起点的块 = 续条目/DOI 尾巴 → `prev + ' ' + block` 合并；合并后逐条**换行压空格**（Frontiers 抽取会把单条目断成多行碎片）。
5. 校验：条目数（本项目 91）、每条含年份、首作者字母序单调（`van Keken` 归入 K）、`et al.` 保留。
6. Frontiers 文献末尾 `doi:10.…` 直接可 `\url{}`；期刊名 `Earth-Science Rev.`、`Solid earth` 等原样保留（大小写不统一是原文如此）。

### 8. 尾部声明的「Z 形回流」（Frontiers 特有大坑）

结论之后的固定序列：**Data availability → Author contributions → Funding → Acknowledgments → Conflict of interest → Publisher's note → Supplementary material → References**。问题是它**不是**简单 L→R 一顺：常见版式是

```text
左栏：…结论尾 → Data availability → Author contributions（开头）
右栏：Author contributions（续）→ Funding → Ack → Conflict → Publisher → Supplementary
左栏（再往下）：References（标题+起始条目）
右栏（同高）：参考文献续
```

**重建法**：同一页按 y 分带——上带（`y < References 标题 y`）内先 L 后 R，下带（参考文献区）先 L 后 R；**勿整页 L→R**（会把 Funding/致谢插进作者贡献中间、或把 References 标题提到 Funding 之前）。切完顺序核对：`Data availability` → `Author contributions` → … → `References` 必须依次出现。

### 9. 一键检查（Frontiers 交稿前）

```text
英文摘要句首=0（首页为中文摘要+关键词）
页眉 Frontiers in Earth Science / frontiersin.org / 10.3389 / 页码 =0
首页右侧 EDITED BY/REVIEWED BY/CITATION 元数据盒 =0（「原文信息」除外）
FIGURE N | 图题 10 个 ↔ figNN.png 10；图注无双编号
图序页码递增且全部在参考文献起始页之前（pitfalls 3.14）
References 条目数合理、每条含年份（含 2011a 型）、字母序单调
et al. 未译成「等」（terminology.md）
```

---

## Nature（Nature 主刊）· 已用 Xie-2026-Nature 验证

刊例：Xie et al., 2026, *Nature*, doi:10.1038/s41586-026-11280-2（主文 6 页 + Methods/尾栏 + 参考文献 100 条 + Extended Data 10 图，共 20 页原文）。

### 1. 版面结构

| 元素 | 典型位置 | 抽取注意 |
|---|---|---|
| 双栏 | 左 x≈40–296 / 右 x≈306–563 | 按 L→R y 序重排 |
| 页眉 | 奇数页顶 `Nature \| www.nature.com \| N`；偶数页顶 `N \| Nature \| www.nature.com` | 按 `nature.com` 删；首页 `Article` 标签（y<45）删 |
| 首页元数据 | 标题通栏 y44–105；DOI/Received/Accepted/Published 在**左窄栏**（x≈40–200, y140–220）；**摘要在右半**（x≈217–562, y187–393，x0 不是左栏！）；单位行通栏 y710–745 | `in_p1_meta: y<410 或 y>705` 全归元数据；摘要单独通道 |
| 摘要 | 无 `Abstract` 标签，题目下首段即摘要 | 验收：中文整段（pitfalls 7.1） |
| 关键词 | **原刊无关键词行** | 译稿关键词自拟（同 AGU Key Points 先例） |
| 章节 | 无编号；**无 Introduction 标题**（摘要后正文直接开始） | 勿自造「引言」节；节标题=独立粗体短块 |
| 图题 | 主图 `Fig. N \|`；扩展数据 `Extended Data Fig. N \|`（竖线） | 行首+长度锚点；正文 `see Fig. 3` 不算 |
| Methods | 独立大节，子节标题与正文**同块内联**（首行粗体） | 块内按行拆 `##H##` 标题 |
| 尾部栏目 | Acknowledgements / Author contributions / Funding / Competing interests / Additional information——**标题词与正文同一行** | 宽松匹配 `startswith(标题词)` 切节；勿要求独立标题块 |
| 参考文献 | **分两段**：正文引用 1–48 在 `Online content` 框后（p6）；方法/ED 引用 49–100 在 Methods+Data availability 之后；**无 `References` 标题行**，编号行首 `N.\t` | 译稿自加 `\section{参考文献}` / `\section{参考文献（续）}`；两段中间隔着 Methods 属原刊版式，照抄 |
| Publisher's note | 在 refs1 之后（主文单元收尾），Methods 等在其后 | 属正常，勿以为页序错乱 |
| Online content | 正文后固定提示框（"Any methods, additional references…"） | 独立小节译出 |

### 2. 抽取顺序

1. PyMuPDF `get_text('dict')` 按块；页眉/页脚/`Article` 先剔。
2. 每页 **L 栏 y 序 → R 栏 y 序**（图与图题块剔除后）；全宽块极少。
3. **首页特判**：`y<410` 或 `y>705` 归元数据（标题/作者/DOI/日期/摘要/单位），正文从 y≈424 起。
4. 图内文字过滤：`图区 = drawings∪images`，**外扩 margin 22–30 pt**（面板字母 a–f、轴标签常在图框外 5–20 pt：如 `Rock/chondrite` 在框左 x307 vs 框 x333——margin 不够会裁掉轴名）；文字块与扩展区重叠 >50% 且（高<45 或短<120 字符）→ 判图内文字剔除。
5. 软连字符 reflow：行尾 `-`+下行小写→删连字符；行尾 `-`+下行大写→**保留**（`high-`+`Ti`）；含 `数字-Gyr-`→**保留**（`3.95-Gyr-`+`old`）；行尾 en-dash→直接接；其余空格拼接。全文仅 80 处行尾连字符、逐类核对过（本篇如此，换篇仍建议先抽样枚举）。
6. 参考文献块：行首 `^\d{1,3}\.(?:\s|$)` 计数 ≥2 才按条目拆（块内条目各成一项、条内 reflow）；**无编号的块=上一编号的续尾**，拼装时并回前条。

### 3. 图题与图裁切（14 图实测）

- **图题续段两型**：①跨栏同带（|Δy0|≤15、另栏、小写开头、len>30，如 Fig.1 右半）；②图题正下方 gap≤15 的续块（ED5 型，以 `207Pb` 开头）。迭代吸收直至无候选。
- ED2 特例：图在 p11 整页、p11 底只有 `See next page for caption.` 占位（剔），真图题在 p12 → 裁图页=11、题页=12，**底钳不要用 p12 的题 y0**。
- **Fig.4 图题与图分栏并排**（图在左栏、题在右栏同高）：题的 y0 **不能**压图底——仅当图与题 x 范围重叠时才用题 y0 钳底。
- clip 钳制：y0≥44（页眉 `Article`）、y1≤750（页脚）、x∈[36,567]；Matrix 2.6。
- **ED 图必须用独立计数器环境**（`\begin{edfigure}` 内重定义 `\figurename`+`\thefigure`），否则 `\caption` 渲染成「图5」而不是「扩展数据图1」；拼装时 EDBLOCK 要真用 `edfigure`（本项目曾漏包，QA 靠读 PDF 页文本抓出）。
- 主图页码必须 < refs1 页（aux `\newlabel` 校验）；**ED 图在参考文献之后是 Nature 惯例**，图序 QA 规则对 ED 放宽（只查 1–10 递增 + 题名渲染正确）。

### 4. 一键检查（Nature 交稿前）

```text
英文摘要句首=0；关键词自拟且非「关键词（原刊）」
页眉 nature.com / Article 标签 =0（译稿内）
Fig. N | 与 Extended Data Fig. N | 各 4+10 ↔ figNN/edfigNN.png
ED 图题渲染为「扩展数据图 N」（读 PDF 页文本，勿只查 aux）
主图 aux 页 8,9,10,12 型递增且 <refs1；Float too large=0；Overfull=0
refs 1–48 与 49–100 连续无缺重；et al. 未译「等」
缺字形警告=0（′ ″ ≥ U+02BC 已按 pitfalls 9 替换）
```

## 其他 / 预印本（arXiv, ESSOAr）· 待补

- [ ] 双栏预印本常见错切  
- [ ] 与正式版图号差异  

---

## 维护约定

1. 每完成一篇新出版社译本，把**可复用**技巧写入对应小节（现象→做法），勿只写项目流水账。  
2. 与 `pitfalls.md` 交叉引用编号（如 Elsevier 双栏摘要 → pitfalls 7.1）。  
3. 用户纠正译名仍进 `terminology.md`，不写在本文件。
