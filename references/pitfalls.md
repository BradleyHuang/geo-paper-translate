# 实作踩坑记录（Johnson-2021-ESR 等项目沉淀）

按「现象 → 原因 → 做法」记录。遇到异常先查此表。

## 1. Python / 正则 / 字符串

### 1.1 `re.sub` 替换串吞掉 `\b`
**现象**：`\begin{figure}` 变成 `\x08egin{figure}`，图环境损坏，图消失或报错。  
**原因**：`re.sub` 的 replacement 模板把 `\b` 当特殊转义。  
**做法**：替换串用 `chr(92)+'begin{figure}'`，或 `lambda m: BS+'begin{figure}'`。写完检索 `chr(8)` / `egin{figure}`。

### 1.2 非 raw 字符串 / heredoc 吞 `\`
**现象**：图注行尾 `\` 变成 `\`，表格 `\\` 丢失，短栈换行失败。  
**做法**：LaTeX 代码入盘用 `r'''...'''` 或 `BS=chr(92)` 拼接；heredoc 用 `<< 'PY'` 勿插值。写完 `repr()` 抽查含反斜杠行。

### 1.3 终端中文 `UnicodeEncodeError`
**现象**：`'gbk' codec can't encode...`。  
**做法**：脚本开头 `sys.stdout.reconfigure(encoding='utf-8')`；或写文件用 `encoding='utf-8'`，少 `print` 特殊符号。

### 1.4 复杂正则在 shell 中二次转义
**现象**：`bad escape \c` / `missing )`。  
**做法**：路径、includegraphics 匹配优先 `str.find` / `str.replace`；必须用正则时把脚本写入 `.py` 文件再执行。

## 2. PDF 抽取

### 2.1 双栏交错
**现象**：摘要与关键词行交叉；图注混入邻栏正文；章节标题嵌进句中。  
**做法**：按 `Fig. N.` / `N. Title` 锚点切块后**语义重排**；不要按物理行顺序直译。可用 pdfplumber `extract_text` + 人工/模型重排，或 PyMuPDF `get_text('blocks')` 按栏合并。

### 2.2 图注不完整 / 混入正文
**现象**：caption 里出现 “See text for discussion” 之前的邻栏句子或页眉 `T. Johnson et al.`。  
**做法**：用 block 级提取，遇字号/栏位跳变或页眉样式则切断；清洗 `T. Johnson et al.`、期刊 running head。

### 2.3 图区 bbox 误判
**现象**：裁到正文残字、裁进上一图、横轴刻度被切、四联图与邻图粘连。  
**做法**：
- clip = drawings∪images 的紧包围，**上缘**取正文块 bottom 与图形 top 之间；
- 同页多图按图题 y/x 分栏或分带；
- 矢量图无 image 时用 `page.get_drawings()`；
- 裁完用 PIL 查顶/底条带暗像素，抽查预览图。

### 2.4 竖长图
**现象**：照片叠层图撑破页面、压页脚。  
**做法**：`height=0.70–0.75\textheight, width=\textwidth, keepaspectratio`。

## 3. LaTeX 版式

### 3.1 `[H]` 大片留白
**现象**：图+长图注 > 剩余版面时整块甩下页，上页空半页。  
**做法**：用 `[!htbp]`（**必须带 `p`**，见 3.14）；长图注 `\footnotesize`；锚点靠近首次「图 N」；收紧 `floatsep`。需要强行嵌入正文再考虑 `[H]`，并确认图注总高可放下。

### 3.2 长 URL 不断行
**现象**：`https://serc.carleton.edu/...` 顶出版心。  
**做法**：`\usepackage{xurl}`；正文写 `\url{...}`；`\setlength{\emergencystretch}{1.5em}`。

### 3.3 中文字体
**做法**：XeLaTeX + `\setCJKmainfont{FangSong}`（Windows）或 Fandol 体系；标题可继续 `\heiti`。仅 pdfLaTeX 易缺字体。

### 3.4 表格过宽 / 列数不匹配
**现象**：`more & marks than preamble`；Overfull 200pt+。  
**做法**：核对 `&` 数与列格式列数；`\resizebox{\textwidth}{!}{...}`；`\arraystretch`；长标签改短写 `15a/b (X=0)` 而非强行 `\`。

### 3.5 `titlesec` 与 `ctex` 抢章节
**现象**：章节格式异常或警告。  
**做法**：优先只用 `\ctexset{section=...}`；确需 `titlesec` 再局部 `\titleformat`，避免两套同时改同一层级。

### 3.6 页眉高度
**现象**：`headheight is too small`。  
**做法**：`\setlength{\headheight}{18pt}` 以上，并相应加大 `\topmargin` 或用 geometry。

### 3.7 `wrapfigure` 半宽环绕
**现象**：用户想要原文双栏「左文右图」；单栏环绕可能仍占大半页（竖长图）。  
**做法**：可试 `wrapfigure{r}{0.46\textwidth}` + 高度限制；效果差就改回浮动图。不要假装是双栏。

## 4. 术语雷区（详见 terminology.md）

| 错误直译 | 问题 | 应为 |
|---|---|---|
| 赝剖面 / 假剖面 | 非地学惯例 | 视剖面图 |
| 近晶矿物 | 与 liquid crystal 混淆 | 转熔矿物 |
| 角闪岩（指岩石） | 与「角闪岩相」粘连 | 斜长角闪岩 |
| 灰瓦克 | 旧音译 | 杂砂岩 |
| 建模 | 软件语感 | 模拟 |
| H₂O 加入熔融 | 生硬 | 水致熔融 |
| 变熔岩/全熔岩 作主词 | 可作别称 | 初级/高级混合岩 为主词 |

保护规则：替换「角闪岩」→「斜长角闪岩」前，先把「角闪岩相」替换成占位符，再还原，否则会造出「斜长角闪岩相」。

## 5. 协作与验收

- 用户会多轮改图宽、图注、页眉页脚、译名——**改尺寸与译名走全文检索替换**，并给出变更表。
- 改动后必须重编译，并报告页数与关键检查项。
- 重要版本可留 `*.bak-xxx`，明确告知用户备份文件名。
- 交付前跑术语残留清单（terminology.md 末节）。

### 3.8 图注双重编号
**现象**：`图 2：图 6：……`，或图序与原刊不一致。  
**原因**：`\caption` 自动加「图 N」，图注正文又写「图 N：」；或按正文出现顺序浮动编号与原刊图号错位。  
**做法**：图注正文**不要**写「图 N：」；若需与原刊图号一致，用 `\setcounter{figure}{N-1}` 在 `\caption` 前强制编号，并保证 `figNN.png` 的 NN 与编号一致。

### 3.9 图尺寸被脚本顺手改掉
**现象**：用户指定 100% / 60% 之后，后续按纵横比自动分配宽度又把该图改小。
**原因**：每次重构 includegraphics 时用统一启发式覆盖了用户设定。
**做法**：用户指定过的比例记为**显式锁定尺寸**，后续脚本不得改写这些图的 width/height。全文替换前先读入当前选项；禁止对所有图做按 aspect 的统一 re.sub 重写。一旦写入 width=\textwidth 或 0.6\textwidth，除非用户再改，否则保持不变。

### 3.10 图序与浮动乱序
**现象**：图 3、4、5 晚于图 6 出现；有的图落到致谢/结论之后。
**原因**：按首次引用插入时，若用 inserted_upto 之后才搜锚点，会漏掉更早出现的后续图号，只能堆到文末；或浮动顺序与源顺序不一致。
**做法**：
- 按图号 1→N **顺序**安插；锚点在**全文**找第一次 \ref{fig:...} / 图 N；
- 插入点 = max(该锚点所在段末, 上一幅图结束位置)；
- 所有图必须在**结论/致谢之前**；
- 编译后扫描 PDF 中「图1…图N」首次出现页码，确认**单调递增**；
- 若出现顺序与原刊图号一致（1…N 顺序出现），不必 setcounter；若必须乱序出现但编号仍跟原刊，再用 setcounter{figure}{N-1}，并确认图注无双编号。

### 3.11 图号 / 文件 / 图注三方对应
**现象**：图注内容对的是原刊图 6，文件是 fig02，版面又编成图 3。
**做法**：锁定三元组 编号 == figNN.png == 图注正文所描述的那幅图。改图序或改名后跑 SKILL.md 验收清单。

### 3.12 首页硬塞一页（Fan-2024-GR）
**现象**：为把「摘要→关键词→原文信息→说明」压进第 1 页，把段间距从 1.6em 缩到 1.15em、压缩题头空隙。
**原因**：误以为首页必须一页。
**做法**：**首页允许自然溢出到第 2 页**，长摘要跨页完全正常；保持 1.2–1.6em 段间距，不要为塞进一页改段距/字号。只有页眉左右两段互相重叠才需处理（左头文案 ≤ 20 字，如「××与××（译本）」）。

### 3.13 `\[` 与 `\\[` 混淆 → “group at level 1” 迷惑报错（Fan-2024-GR）
**现象**：编译报 `(\end occurred inside a group at level 1) ### semi simple group (level 1) entered at line 106 (\begingroup)`；但全文 grep `\begingroup` 仅一处且已配对，报错行号也对不上。
**原因**：`\title` 里行距参数写成 `\[0.6em]`（丢一个反斜杠）——`\[` 是展示数学定界符，LaTeX 内部展开为 `\begingroup`，开了永不闭合的组；报错行号是 \maketitle 执行处，极具迷惑性。模板 latex-template.md 曾自带此坑（已修）。
**做法**：
- 标题/作者行距一律 `\\[0.6em]`（两个反斜杠）；
- 排查此类报错的顺序：数 `\begin{equation}`/`\end` 配对 → 数 `$` 奇偶 → grep `\[`（排除 `\\[`）→ 查 `.aux`/`.toc`；
- 自写检查脚本勿经 shell heredoc（`\b`/`\e` 被吞导致误报，如「equation 4/0」假阳性）；计数结论用 `grep -c` 复核。

### 3.14 图浮动缺 `p` → 全部推迟到参考文献之后（Ritter-2024-FES）
**现象**：图 1–5 正常，图 6–10 却一起落在参考文献之后的文末（如 36 页里挤在 32–36 页）；`Float too large` = 0，报错日志干净，极难定位。
**原因**：图环境写成 `[!htb]`（无 `p`）。长图注的图（图+注 ≈ 0.95 页）超过导言区 `\topfraction=0.92`，既不能作顶部浮动、也不能塞进「here/bottom」，LaTeX 只能把它们压队到 `\end{document}` 前统一输出。
**做法**：
- 图/表浮动一律 `[!htbp]`（模板默认已改）；验收必查「图 N 首现页码 < 参考文献起始页」；
- 辅助：长图注 `\footnotesize`、`\captionsetup[figure]{font=small}`；仍超高就降 `width` 或改 `height=0.72\textheight,keepaspectratio`；
- 诊断口诀：**「图挤文末 + 无 Float too large」→ 先查浮动选项有没有 `p`**。

### 3.15 文本模式裸下划线 → “Missing $ inserted”（Ritter-2024-FES）
**现象**：编译报 `! Missing $ inserted`，报错行指向图注末尾 `}`，但该行肉眼无 `$`；同页中文掉进 latin modern（`Missing character: There is no 成 (U+6210)`）。
**原因**：图注/正文里写了裸 `v_conv`、`V_a` 等未包进数学模式的下划线；LaTeX 在文本模式见 `_` 就插 `$`，随后整段进数学模式，中文全部缺字。报错行是「进数学模式后第一个不能吃的字符」的位置，**不是出错源头**。
**做法**：
- 下划线变量一律 `$v_{\mathrm{conv}}$`、`$V_a$`；
- 排查：先 `t.count('$')` 看全文奇偶 → 逐行累计找首次变奇的行 → 对可疑行再查 `[A-Za-z]_[A-Za-z0-9]`（先剥掉 `$...$` 再搜，避免误报公式内下标）；
- 交付前加一条：全文裸 `_`（数学模式外）= 0。

### 3.16 手写 `\begin{list}` 参数组多一个 `}`（Ritter-2024-FES）
**现象**：`! Extra }, or forgotten \endgroup` + `! \begin{list} ... ended by \end{document}`；参考文献区整段错乱。
**原因**：`\begin{list}{}{...}}` 结尾多写了 `}`（label 组 `{}`、参数组 `{...}` 各收一次，手拼时易多打）。
**做法**：参考文献/条目列表**不要手写 `list` 环境**，直接用已加载的 enumitem：
```latex
\begin{enumerate}[label={},leftmargin=*,itemindent=-1.5em]
\item ...
\end{enumerate}
```

## 6. 补充材料与参考文献（Fan-2024-GR 项目沉淀）

### 6.1 docx 附图顺序 ≠ 文内图号
**现象**：word/media/image1 实际是 Fig. S2、image2 是 Fig. S1，与文中出现顺序相反。
**做法**：抽 media 后生成缩略图**目检面板内嵌标注**（如 “RHP of strong/weak terranes=2/2” 对应 S1），核对图注再命名 figSN；勿按 media 序号猜。

### 6.2 docx 公式抽取丢失
**现象**：python-docx `paragraph.text` 只得 “where i and j represent…” 说明文字，OMML 公式本体全部丢失，公式 (1)–(10) 空白。
**做法**：按标准模型（如 I2VIS/Gerya 控制方程、流变律、固液相线熔融）补全为 LaTeX 公式，并在译者说明或附录注明「公式按原刊标准形式补出」；或改从出版社 PDF 版补充材料抽取。

### 6.3 参考文献双栏解交织与条目切分（Fan-2024-GR）
**现象**：pdfplumber 行文本左右栏逐行交错；简单按 `Surname, X.` 切会把 `Res, Lett, p. 49.`（期刊缩写）误判为人名，条目黏连或误切。
**做法**：
1. PyMuPDF `get_text('dict')` 按 block 的 x 坐标分栏（x<300 左栏），每页左栏→右栏依 y 排序合并；
2. 去页眉、页脚页码（`\b(?:30[0-9]|31[0-6])\b` 且两侧有空格才删，防误删页码范围 311–356）；
3. 条目边界正则要求**首字母后必须带句点**：`\.(?=\s*(?:(?:van|von|de)\s)?(?:\w+\s){0,2}\w{2,},\s?[A-Z]\.)`；
4. 验证：条目数合理（80–100）、每条含 (19|20)\d\d、首作者字母序单调、点名的易丢条目（Dessai、Huw Davies、Nábelek、Krystopowicz、Vilà、Stüwe）逐一 grep。

### 6.4 大表格别让子代理猜列（Fan-2024-GR）
**现象**：24×12 的表 S1 让翻译子代理从乱序文本推断列映射，反复试错直至 max_tokens 超时被中断。
**做法**：>10 行或 ≥8 列的表由**主代理用 python-docx `doc.tables` 逐格抽取**（`[c.text for c in row.cells]`）得到干净网格，直接写 LaTeX；子代理只译表题与表注。PDF 侧同理用 pdfplumber `extract_table`。

### 6.5 验收图号正则的空格变体
**现象**：ctex 图注可能渲染为「图S1:」（图与编号间无空格），按 `图\s*N[:：]` 查不到就误报缺图。
**做法**：正则用 `图\s*(?:S)?N\s*[:：]?`，并分别统计「图 N」与「图SN」出现页码；补充图编号（图 S1/S2）用 `\renewcommand{\thefigure}{S\arabic{figure}}` + `\setcounter{figure}{0}` 保持原刊编号。

### 6.6 Elsevier 抽取乱码 (cid:)
**现象**：`(cid:3)C`、`(cid:4)1`、`(cid:1)900` 等。
**做法**：翻译前批量还原：`(cid:3)`→℃、`(cid:4)`→−（负号/减号）、`(cid:1)`→≳、`(cid:5)(cid:6)(cid:7)`→（）× 等，按上下文核对。

## 7. 拼装、验收与 Windows 编译（Wei-2026-Lithos 沉淀）

### 7.1 摘要整段漏译（假验收）
**现象**：关键词已中文、首页有「摘要：」标签，但摘要正文仍是英文 `This study presents…`；验收只查了标签存在。  
**原因**：拼装时从 `section_00_abstract` 直接嵌英文，或子代理只译了关键词列；双栏下关键词与摘要正文交错，抽成 `Keywords: This study…` 误导。  
**做法**：
1. 摘要**单独中译**后再写入 `\textbf{摘要：}`，勿复用英文抽取块；  
2. 验收增加：`This study presents` / 英文句首 **=0**，且首页摘要区含中文；  
3. 仅检查「有摘要标签」**不算**通过。

### 7.2 图题锚点抓到正文引用
**现象**：`search_for("Fig. N.")` 命中正文 `shown in Fig. 1.`，裁出错误图或错号。  
**做法**：要求命中**行首** `Fig. N.` 且该行/块长度 >50 才是 caption；优先 `page.get_text('dict')` 找以 `Fig. N.` 开头的 line。

### 7.3 图顶裁进上方正文
**现象**：fig 顶条带暗像素高（正文残字）。  
**做法**：`body_bottom` = caption 上方最后正文块 bottom；clip.top = max(body_bottom+0.5, drawings.top-1.5)；裁后用 PIL 查顶 30–40px 暗像素比。

### 7.4 中文文件名 + shell 里 xelatex 找不到文件
**现象**：`xelatex Xxx-中文译本.tex` 报 `I can't find file`，或 `ls` 中文名乱码。  
**原因**：Windows bash 与 UTF-8 文件名/编码不一致；cwd 不在译本目录。  
**做法**：用 Python `subprocess` + `os.chdir(workdir)` 调 `xelatex`；**勿**依赖 shell 粘贴中文文件名。每条 Bash 若可能 `cd` 过，下一条先 `pwd`。

### 7.5 译名批量替换顺序
**现象**：先替短词再替长词会漏；`角闪石麻粒岩` 与 `角闪石二辉麻粒岩` 混淆。  
**做法**：**长串优先**；保留不该改的（整体平衡、整体岩石分析、角闪石二辉麻粒岩）；改完跑 terminology 残留清单。

### 7.6 bulk / modal / estimation 级联
**现象**：用户多轮改 bulk→全岩、模态→含量、估计→估算，反复返工。  
**做法**：首次交稿前主动用「全岩成分 / 含量 / 估算」；点名后全局替换并重编译两遍。

### 7.7 温度计中英对应写反
**现象**：译成「锆石中 Zr 和金红石中 Ti」（原文 Zr-in-rutile、Ti-in-zircon）。  
**做法**：固定 **金红石Zr / 锆石Ti温度计**。

### 7.8 解读附录矿物名与正文不一致
**现象**：附录写「紫苏辉石+矽线石」「堇青石+石英」，正文为 Opx+Sill=斜方辉石+矽线石、Spr+Qz=假蓝宝石+石英。  
**做法**：附录矿物组合必须与**正文首次括注**一致。

### 7.9 宽表拥挤
**现象**：12 列成分表行距过紧。  
**做法**：`\footnotesize` + `\arraystretch≥1.4` + `\tabcolsep≥5pt`；长标签改脚注；表头用 `$\mathrm{SiO_2}$`。

### 7.10 交付目录/文件缩写用真期刊名
**现象**：文件夹写成 `Wei-2026-PET`，期刊实为 LITHOS。  
**做法**：`{姓}-{年}-{期刊缩写}` 用**原刊名**；改名后同步 tex/pdf 并重编译。

### 7.11 作者单位与中文作者名
**现象**：封面残留实验室长串；作者仍为拼音/英文。  
**做法**：用户点名后封面用中文作者名；单位按用户要求可只保留学院；**原文信息**里的原刊作者引用保持英文（Wei, C., Wang, B.）。

### 7.12 GSA：`body_y0` 被页眉元数据拉走
**现象**：三栏正文抽成「页眉+摘要+单位」全进正文；右上 DOI/收稿日期把 `body_y0` 拉到 y≈36。  
**做法**：`body_y0` 只统计 `x0≥213 且 y0>120 且 非 header_meta`；`header_meta` 含右上 DOI/收稿（y&lt;120,x&gt;380）以及左下 ORCID/邮箱盒（即使 y&gt;550）。细则见 extract_by_publisher GSA §2。

### 7.13 GSA：页脚阈值切掉正文末行
**现象**：`footer_y = page_h − 75` 把 y≈718 的正文末行当页脚丢掉，段落残缺。  
**做法**：GSA 用 `footer_y = page_h − 32`（刊眉条约 y=750，水印 y≈772）；切完抽查倒数第二栏末段是否完整。

### 7.14 GSA：栏边界浮点误分
**现象**：`x0=393.0` 有时判入中栏（`392.99 < 393`），中/右栏串行。  
**做法**：`col_index` 用容差（如 `x0 < 393-5` 才算 c1）；或对 `round(x0)` 分桶；抽一段同 y 三行确认分属三栏。

### 7.15 讨论小节文件名与内容对调
**现象**：`section_disc_model.txt` 首句是脉冲结果、`section_disc_pulses.txt` 才是三种情形评估；子代理按文件名翻译会张冠李戴。  
**做法**：切分后**用每节首句语义核对**再派工；小节标题折行（`…Transport` + `and Fluid-Mediated…`）用带 `\s*` 的整段正则在 DISCUSSION…ACKNOWLEDGMENTS 区间搜。

### 7.16 致谢片段残留图注再排一遍
**现象**：图注在 `latex_04` 里只注释了 `% fig1:` 标签、正文未注释 → 致谢后出现「图1…图4」重复图注。  
**做法**：图注**只保留在 `figure` 环境**的 `\caption`；辅助片段若存图注须整段注释或删除；交稿前检索「致谢」同页是否再出现图注句。

### 7.17 作者单位 `\small` 只作用首行
**现象**：多行单位第一行小、后两行正常字号。  
**做法**：`\parbox{0.96\textwidth}{\centering\small 单位1\\单位2\\单位3}`，勿依赖裸 `\small` + `\\`。

### 7.18 高图独占一页 / 两图挤一页留白
**现象**：图+长图注接近整页 → 上（或下）大段空白；两图 float page 页底空白。  
**做法**：高图缩 `width`（0.85–0.9\textwidth）+ 图注 `\footnotesize` + `[b]`/`[!htbp]` 让上文进同页；两图**拆开插入点**（分别锚在结果与讨论）；勿用 `[H]`。

### 7.19 SI docx 公式是 OMML
**现象**：`docx2txt`/pdfplumber 抽补充材料，方程只剩文字或空白。  
**做法**：lxml 解析 `word/document.xml` 的 `m:oMath`（分数/上下标/根号/求和），线性化后写入附录 `equation`/`equation*` 并 `\tag{S1}`；与正文引用的 S1–S6 对齐。

## 8. AGU 新版 / Wiley 平台（Knight-2025-TECT 沉淀）

### 8.1 新旧 AGU 版式两代混用
**现象**：按旧 AGU 双栏（x≈300 分栏）切 2020s Wiley 平台电子版，把「左侧作者信息栏 + 单栏正文」切碎。  
**做法**：先判断版本：2020s 电子版（DOI `10.1029/…`）= 信息栏（x≈31–150）+ 单栏正文（x≈167–570）；1990s 扫描版（如 Royden-1993）才是双栏整页位图。分支详见 extract_by_publisher.md AGU 节。

### 8.2 Wiley 下载水印混入正文
**现象**：每页竖排水印碎片（`Downloaded from https://agupubs…`、`Terms and Conditions`、机构名）散成短行进正文，逐行交错。  
**做法**：抽完逐行删含 `Downloaded|Terms and Conditions|onlinelibrary|agupubs|Wiley Online Library|OA articles|are governed by` 的行；抽块跳过 x>580 窄块。

### 8.3 SI 公式 pdfplumber 抽取烂 → 渲染读图法
**现象**：SI 公式 (1)（位错/扩散蠕变）抽出为 `𝜂 = c 1/2 𝐴( * )…`，上下标/分式全乱。  
**做法**：`Matrix(3–5)` 渲染公式页 → 按坐标裁公式局部 → Read 看图抄式；参数对照表 S1 核量纲（活化能 J/mol、活化体积 m³/mol 量级合理性）。扫描版主文（Royden-1993 同法）。

### 8.4 SI 表印误与正文矛盾
**现象**：表 S2 某模型速度条件排印为 10，与正文 $v_c=2$ 矛盾。  
**做法**：以正文/模型命名（CV2=constant-2）为准更正表格，加注「原刊排印如此，按正文更正」；勘误类同（Royden 1993b 式处理）。

### 8.5 作者/单位行超版心被裁（用户截图可见）
**现象**：4 作者+上标一行、单位合并行过长，右侧被版心裁掉（`Luca Dal Zilio³'⁴` 尾巴、`（澳大利亚克…`）。  
**做法**：作者拆 2 行；单位每行 `\small` 独立成行（`\small` 只作用到行尾，7.17）；验收查 `get_text('blocks')` x1>556 块数=0。**塞页与 3.12 协调**：首页溢出 p2 允许、不强塞；仅用户要求首页收尾时用 `\begin{spacing}{1.05}` 包四段（勿改段距/字号）。DOI 长链用 `\href{…}{doi:…}` 短显示。

### 8.6 图序同页「严格递增」误报
**现象**：验收断言图 N 首现页码 strictly increasing，图 7/图 8 同页报 False，实则正确。  
**做法**：断言改**非降**；同页比较文本位置（`t.find('图7:') < t.find('图8:')`）。补充图（图 S1）编 `\setcounter{figure}{0}` + `\renewcommand{\thefigure}{S\arabic{figure}}` 或按译本连续编号并注明（见 6.5）。

### 8.7 Key Points / 通俗摘要的处理（AGU 特有）
**现象**：首页 Key Points、Plain Language Summary 被当杂项丢弃，或与摘要重复翻译。  
**做法**：Key Points 译「要点」列表（正文 `\section` 前 `itemize`）；Plain Language Summary 译「通俗语言摘要」段（紧随摘要后）；两者都不是关键词——关键词自拟。CRediT 作者贡献/声明类小节（Conflict of Interest、Data Availability Statement）也要译。

## 9. 拼装期 LaTeX 陷阱（Xie-2026-Nature 沉淀）

### 9.1 Python 拼接串里 `\\[2pt]` 少写一个反斜杠 → 显示数学
**现象**：单位/作者用 Python 字符串拼接时写 `"...Australia.\\[2pt]$^{5}..."`（源码两反斜杠 → 输出一反斜杠），生成稿是 `\[2pt]`——TeX 读作显示数学开始；报错 `Display math should end with $$` 却出现在很后面的 `\maketitle`/`\thispagestyle` 行，极难定位。
**做法**：非 raw 串中换行间距要写 `\\\\[2pt]`（输出两个反斜杠）或改用 raw 串；排查法：对可疑段做最小 `\maketitle` 试验二分；搜生成 `.tex` 中正文区裸 `\[`（methods 的 `\[...\]` 展示公式除外）。

### 9.2 `\author` 内空行
**现象**：`\author{ 名单 \n\n 单位 }` 报 `Paragraph ended before \author was complete`。
**做法**：`\author{名单\\[6pt]\parbox{...}{...}}`，禁空行；名单整行超宽（日志 Overfull >150pt）时拆两行 `\\`。

### 9.3 ED/补充图计数器：必须真用自定义环境
**现象**：定义了 `edfigure`（重定义 `\figurename`+`\thefigure`）但拼装时仍生成普通 `\begin{figure}`——`\caption` 按 figure 计数渲染成「图5」，aux 标签也变 5–14。
**做法**：ED 块用 `\begin{edfigure}…\end{edfigure}`；**QA 读 PDF 页文本**断言「扩展数据图 N」存在、「图{4+N}:」不存在（aux 可能被 hyperref 写成数字，不可单独作证）。

### 9.4 enumitem 双选项列表
**现象**：`\begin{enumerate}[start=49][leftmargin=...]` 报 `missing \item`（第二个 `[]` 被当正文）。
**做法**：合并单列表 `[start=49,leftmargin=...]`。

### 9.5 参考文献裸 `&` 与断行 URL
**现象**：refs 含裸 `&` → `Misplaced alignment tab`；PDF 抽出的 DOI 断行成 `https://doi.org/10.1130/ g39894`（URL 内空格）。
**做法**：拼 refs 时 `(?<!\\)&` → `\&`；URL 先并回斜杠后空格再 `\url{}`；refs 中的 `≥`/`≤` 也要换 `$\geq$`/`$\leq$`（见 9.6）。

### 9.6 缺字形（Missing character）
**现象**：`′`(U+2032) `″`(U+2033) `≥` `≤` `ʼ`(U+02BC，如 OʼNeil) `✉`(U+2709) 在 lmroman 下被丢弃（日志 `Missing character`，正文留空）。
**做法**：坐标 `′`/`″` → ASCII `'`/`''`；正文/文献 `≥`/`≤` → `$\geq$`/`$\leq$`（preamble 可定义 `\newcommand{\permil}{\text{\textperthousand}}` 兼容 `\permil`）；U+02BC → `'`；`✉` → `E-mail:`。交稿前数日志 `Missing character` = 0。

### 9.7 QA 图序要用 aux + 页文本双通道
**现象**：正文首现「图 N」页码受 TOC、交叉引用、同页多图影响会误报乱序；ED 又必须排在参考文献之后（Nature 惯例）。
**做法**：主图/ED 落页用 `\newlabel{fig:...}`（`{label}{page}` 第二字段）；ED 题名渲染另读页文本。主图 < refs1 页、ED 只查递增。见 extract_by_publisher Nature 节一键检查。
