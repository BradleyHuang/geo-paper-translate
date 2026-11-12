---
name: geo-paper-translate
description: 将地球科学（或相关地学）英文学术论文 PDF 翻译为中文并用 LaTeX（ctex/XeLaTeX）排版成完整译本。Use whenever the user wants to translate a geoscience paper, petrology/geology/tectonics paper, or Earth-Science Reviews/journal article into Chinese with LaTeX typesetting, or asks for 中文译本、翻译排版、LaTeX 翻译、论文中译、全文翻译并排版. Also use when the user names a PDF under Zotero-PDF or asks to 新建文件夹并翻译某篇论文. Produces .tex + compiled PDF with cropped figures, Chinese captions, and geological terminology conventions.
---

# 地学论文中文翻译 · LaTeX 排版

把一篇地学英文 PDF 做成**可编译的中文 LaTeX 译本**：正文全译、图裁切插入、图注中译、术语按地学惯例统一、版式现代可读。

写术语与译名前，必读 [references/terminology.md](references/terminology.md)。  
动手前扫一眼 [references/pitfalls.md](references/pitfalls.md)——里面是实作中踩过的坑，能省大量返工。  
**按出版社抽正文/图/文献**先看 [references/extract_by_publisher.md](references/extract_by_publisher.md)（已含 Elsevier/LITHOS、**GSA/Geology 三栏**、**Wiley/JMG、AGU 新版、Nature 主刊**；剑桥等留空待补）。  
导言区与封面模板见 [references/latex-template.md](references/latex-template.md)。  
写公式详解/论文解读附录时，按 [references/appendix-guide.md](references/appendix-guide.md)。

## 运行环境（新电脑首次使用前必装）

本 skill 本体是 Markdown 指令，拷贝即被识别；执行依赖 **Python 抽取库** 与 **XeLaTeX 编译环境**两部分，均须**系统级安装**（任何目录可用）；**不要**在工作目录内创建临时虚拟环境（venv），也不要只在某个项目里装宏包。

### 1) Python 3.10+（加入 PATH）

- Windows：python.org 安装包勾选 “Add python.exe to PATH”，或 `winget install Python.Python.3.12`；macOS：`brew install python`。
- 全局安装依赖（pip 默认进用户/系统 site-packages，对所有项目生效）：

```bash
python -m pip install --upgrade pip
python -m pip install pymupdf pdfplumber pillow lxml
```

| 包 | import 名 | 用途（缺了会怎样） |
|---|---|---|
| `pymupdf` | `fitz` | 读 PDF、分栏重排、裁图、渲染校验（**核心，必需**） |
| `pdfplumber` | `pdfplumber` | 表格/文本抽取的备用通道（部分出版社流程用到） |
| `pillow` | `PIL` | 裁图边缘自检（缺了跳过目检，仍可出图） |
| `lxml` | `lxml` | 解析 docx 补充材料里的 OMML 公式（无 SI docx 可不装） |

验证：

```bash
python -c "import fitz; print('fitz ok')"
python -c "import pdfplumber; print('pdfplumber ok')"
python -c "import PIL; print('PIL ok')"
python -c "import lxml; print('lxml ok')"
```

### 2) XeLaTeX 发行版（编译译本 PDF 的硬性依赖）

- 推荐 **TeX Live 完整版**（https://tug.org/texlive/，Windows 用 `install-tl-windows.exe`，选 full 方案）——ctex、xeCJK、fancyhdr、tikz、eso-pic、hyperref、xurl 等模板所需宏包一次装齐。
- 或 **MiKTeX**（https://miktex.org/，安装时勾选 “Install missing packages on the fly” 为 yes，否则首次编译会卡在缺包提示）。
- 验证：`xelatex --version` 在任意目录可运行。首次真实编译即为宏包冒烟测试（`ctexart` + XeLaTeX 中文文档）。

### 3) 中文字体

模板（references/latex-template.md）默认 `\setCJKmainfont{FangSong}`（仿宋）与 `\setCJKsansfont{SimHei}`（黑体）：

- **Windows 自带**这两款字体，无需处理；
- macOS/Linux 若无同名字体，编译会报 font-not-found——改用系统已有中文字体（如 macOS 的 Songti SC/Heiti SC，Linux 的 Noto Sans CJK SC），或安装同名字体后再用模板。

### 4) skill 安装位置

整个 `geo-paper-translate/` 文件夹复制到 `C:\Users\<用户名>\.claude\skills\`（macOS/Linux：`~/.claude/skills/`），重启会话生效。

本 skill **不需要** Office、网络服务或 LaTeX 之外的付费软件；全部流程本地完成。

## 交付物

**必须在 PDF 所在目录下**新建 `{第一作者姓}-{年份}-{期刊缩写}/`（不是在 cwd 或别处；用户指定其他位置除外），例如 PDF 在 `Zotero-PDF/`，则建 `Zotero-PDF/Johnson-2021-ESR/` 或 `Zotero-PDF/Yakymchuk-2023-JMG/`：

```text
Johnson-2021-ESR/
├── Johnson-2021-ESR-中文译本.tex
├── Johnson-2021-ESR-中文译本.pdf
├── figures/fig01.png … figNN.png
├── section_*.txt          # 原文分段抽取（中间件，可留）
└── original_extracted.txt # 全文抽取备份
```

- 主文档用 `ctexart` + **XeLaTeX** 编译（Windows 下仿宋等中文字体依赖 XeLaTeX）。
- 图从原文 PDF **裁切**，不要只写 `\includegraphics` 占位。
- 图注、表注、术语表均为中文；专有名词首次出现附英文。
- 参考文献列表可保留英文原文（标准做法）。

## 工作流

### 1. 建目录并抽取全文

```bash
mkdir -p "{folder}/figures"
```

用 `pdfplumber` / PyMuPDF 抽全文到 `original_extracted.txt`。注意：

- 终端打印中文时设 `sys.stdout.reconfigure(encoding='utf-8')`，否则 GBK 报错。
- **先查 [references/extract_by_publisher.md](references/extract_by_publisher.md)** 对应出版社小节（Elsevier/LITHOS、**GSA/Geology 三栏**、**Frontiers/Front. Earth Sci. 双栏**已写，含栏数判定速查）；无匹配再用通用双栏启发式。
- 双栏/多栏 PDF 抽出的文本**栏间会交错**，翻译前必须按语义重排，不能逐行硬译。
- **GSA Geology**：正文是**三栏**（x≈33/213/393），不是双栏；`body_y0` 必须先排除右上 DOI/收稿与左下 ORCID 盒，否则页眉全进正文；图题是 `Figure N.` 不是 `Fig. N.`；页脚阈值 `page_h−32`（勿 −75）。细则见 extract_by_publisher GSA 节。
- 按章节标题切 `section_XX_*.txt`，便于并行翻译。用标题锚点定位起止，不要只靠行号。
- **讨论小节标题可能折行断开**（`…Transport` + `and Fluid-Mediated…`）→ 在章节区间内用带 `\s*` 的整段正则搜。
- **切分文件名不可信**：`section_disc_*` 曾与内容对调，译前用每节首句语义核对。
- 摘要、图题、参考文献**分通道**抽，勿与正文同一交错块直译（Elsevier 见 extract_by_publisher §3–7；GSA 见 §7）。
- SI 若为 docx：公式是 OMML，抽文本会丢 → lxml 解析 `oMath` 或按标准方程补全并注明。

### 2. 并行翻译正文

按章节分派子代理（或自行分块）译成 **LaTeX 片段**（不要 documentclass）：

1. 摘要 + 引言 + 第 2 章（变质/混合岩/薄片）
2. 热力学基础 + 相图/视剖面图
3. 开放封闭体系 + 各类源岩熔融 + 折返熔融
4. 微量元素 + 副矿物 + 总结 + 术语表

要求译者：

- 术语按 [references/terminology.md](references/terminology.md)，**禁止**再译成「赝剖面」「近晶」「灰瓦克」「角闪岩（岩石名）」等。
- 公式用 `equation` / `$...$`；引用保留 `(作者, 年份)`，**`et al.` 保持英文，禁止译成「等」**（如 `(Reagan et al., 2019)`）。
- 两栏交错处按语义重排。
- 产出文件如 `latex_00_02.tex` … 便于拼装。

### 3. 裁图并映射图号

用 PyMuPDF（`fitz`）按图题位置反推图区（Elsevier 见 extract_by_publisher §5；**GSA 见 §5**；**Frontiers 见 §5**）：

- **图题识别**：Elsevier/多数刊 `Fig. N.`；**GSA 是 `Figure N.`**；**Frontiers 是 `FIGURE N |`（全大写+竖线）**；AGU 常 `Figure 1.`。须行首/块首且长度 >50；正文 `see Fig. 3.` / `Figure 2A)` 不是锚点。
- 图题在左栏 → 裁左栏图区上方；右栏同理；跨栏图裁全宽；**半通栏**（caption.x1 未到页宽）只裁对应宽度。
- 图题若在页顶，图可能在本页下方或上一页底部，要探测 drawings/images 的 bbox。
- **页眉正文残字**易被误裁进图顶：clip 的 top 取正文块下缘与 drawings 上缘之间。
- 竖长多面板图（如 Fig.3 照片叠层）导出后限制 `height=0.72\textheight, keepaspectratio`，否则撑破版面。
- 分辨率建议 `Matrix(2.2–2.8)`，存 `figures/figNN.png`。
- **版面联动**：图过高独占一页留白 → 缩 `width` + 图注 `\footnotesize` + `[b]`；两图挤一页页底空白 → 拆开插入点；首次引用在讨论后半 → 图放进该小节，勿堆讨论末尾。

脚本可参考 [scripts/extract_figures.py](scripts/extract_figures.py)。

### 4. 拼装主文档

用 [references/latex-template.md](references/latex-template.md) 的导言区：

- 仿宋正文、黑体标题；页眉页脚色条可按用户喜好。
- `\usepackage{xurl}` + 正文 URL 一律 `\url{...}`，否则长链不断行顶出版心。
- 子片段按章节顺序拼接；补 `\section` 结构与 `\label`。

### 5. 插图与版式微调

章节标题：**引言、方法、结果、讨论、结论、致谢、参考文献、术语表、附录** 等通识标题只写中文，不加括号和英文；专业小节名（如“转熔锆石”）可用中文，必要时首次附英文。

版式默认：题目与作者之后依次为 **摘要 → 关键词 → 原文信息 → 说明**（段首加粗标签，不用 abstract 环境）；这四段之间用约 `1.2–1.6em` 的段间距；首页不重复「关键词（原刊）」；**摘要长时首页（至说明）允许自然溢出到第 2 页，不为压进一页而压缩段距/字号**；页眉左右两段勿重叠（左头文案 ≤ 20 字）；**目录另起一页**；图环境紧随首次图号引用段落，勿堆在章末；图 1 等小图可用 `width=0.6\textwidth`。（用户会反复改，属正常）

常见需求与做法：

| 用户说 | 做法 |
|---|---|
| 某图太高/跑出版心 | `height=0.7x\textheight, keepaspectratio` |
| 某图 50%/60%/80%/100% | 改 `width=0.x\textwidth` |
| 某图裁切不对（并进邻图/截掉轴） | 回 PDF 按页坐标重裁 clip |
| 图单独占一页、前页大段空白 | **不要用 `[H]`**；用 `[!htbp]`（**必须带 `p`**，缺 `p` 会把长图注的图推迟到参考文献之后），长图注 `\footnotesize`，锚点靠近首次「图 N」论述 |
| 图全挤到文末、日志却无 Float too large | 浮动选项缺 `p` → 改 `[!htbp]`（pitfalls 3.14）；或图注裸下划线进数学模式（pitfalls 3.15） |
| 表太宽/行距小 | `\arraystretch`、`\small`，必要时 `\resizebox{\textwidth}{!}` |
| 单元格要换行 | 优先「15a/b (X=0)」括号并列；`\` 在表格短栈里易丢反斜杠 |

竖长示意图可试 `wrapfigure` 半宽环绕（接近原文双栏效果），但单栏稿不等于双栏；效果差就改回浮动图。

### 6. 编译与自检

```bash
xelatex -interaction=nonstopmode "xxx-中文译本.tex"
# 跑两遍以稳定目录/交叉引用
```

检查：

- `Output written`、页数、无 `Float too large` / 严重 `Overfull`。
- 术语抽检：`赝剖面=0`、`灰瓦克=0`、`近晶=0`、岩石名「角闪岩」未误用于「角闪岩相」。
- 引文抽检：`et al.` 保持英文，引文式「等」=0（检索 `等\s*[,(（]\s*(19|20)\d\d`）。
- `includegraphics` 条数 ≈ 图数；图注中文齐全。

## 交付前验收清单（每次编译后自检）

编译两遍 XeLaTeX 后核对；失败项先修再交付，避免用户多轮纠图。

1. **图序**：PDF 中「图1…图N」出现页码单调递增；全部在参考文献起始页之前（缺 `p` 会把图推迟到文献后，pitfalls 3.14）。
2. **图号唯一**：图注只有一处编号（无「图 2：图 6：」式双编号）。
3. **图文对应**：编号、`figNN.png`、图注内容三者一致。
4. **图尺寸锁定**：用户指定的比例未被后续脚本改掉；禁止对全部图统一按纵横比重写。
5. **无溢出**：无 Float too large；竖长图未压页脚；图注在版心内。
6. **术语残留**：赝剖面=0、灰瓦克=0、近晶=0、建模=0、**模态=0**、**整体成分=0**（用全岩成分）、表 estimation 的「估计」=0（用估算）；「角闪岩」不单独作岩石名；「上角闪岩相」=0（高角闪岩相）；「角闪石榴辉岩/角闪石麻粒岩」=0；`et al.` 未被译成「等」（引文式「等」=0）。详见 terminology 末节清单。
7. **首页版式**：题目作者 → 摘要 → 关键词 → 原文信息 → 说明；**摘要正文必须为中文**（`This study presents` 等英文句首=0）；无「关键词（原刊）」；通识章节标题无英文括注；作者名可按用户要求中文化（如 魏春景、王彬）。
8. **URL**：长链为 `\url{}` 且不越界。
9. **目录**：另起一页；摘要在目录之前。
10. **编译环境**：中文 `.tex` 文件名用 Python `subprocess`+`os.chdir` 调 XeLaTeX，勿在 shell 里硬敲中文路径；交稿前 `pwd` 确认在译本目录。

图序检查（PyMuPDF）：逐页提取文本，记录「图 N」首次出现页码，断言 N=1..K 页码递增。

**尺寸锁定做法**：改图前读入当前 `includegraphics` 选项；只改用户点名的图。

## 附录写作（公式原理详解 / 论文解读，按需）

用户说「加附录帮助理解」「解释公式」「公式原理详解」「论文解读」「讲透这篇论文」「面向学生」时，在**参考文献之后**追加教学附录。两条产品线：

- **公式原理详解**：逐式讲来历、读法、比喻（传送带/高斯模糊/记账）、自洽检验、地质用途、小词典；范本结构见指南。
- **论文解读**：讲作者为何这么设计、证据链强弱、替代解释与排除、边界与局限。

必守：附录首段与首页「说明」均声明**「译者补充，不属于原文内容」**；公式复刻用 `equation*` 不抢正文编号；中文弯引号 `“”` 禁用 ASCII `"`；面向数学/数值基础弱的学生——先比喻后公式、每个符号给含义与量级、不省略「为什么敢这么假设」。框架与验收追加项详见 [references/appendix-guide.md](references/appendix-guide.md)。

## 质量标准

1. **忠实**：不删科学限定词（may / suggest / inferred），不擅自「润色」结论。
2. **地学译名统一**：以 [references/terminology.md](references/terminology.md) 为准；冲突时以用户当次纠正为准并更新术语表。
3. **图文对应**：图随文走；图注完整；尺寸不撑破页面。
4. **可编译**：交回前必须 XeLaTeX 成功出 PDF。

图一旦用户指定就锁定，后续不得自动按纵横比改写；图序必须 1…N 递增且在致谢之前。

## 踩坑速览（详见 pitfalls.md）

- Python/`re.sub` 替换串里 `\begin` 的 `\b` 会变成退格符 `\x08` → 用 `chr(92)` 拼接或 lambda 替换。
- Shell heredoc / 非 raw 字符串会吞 `\`，图注行尾 `\` 变 `\`。
- `[H]` 在图+图注过高时留下半页空白。
- 「角闪岩相」不可写成「斜长角闪岩相」。
- `peritectic` = **转熔**，不是「近晶」/「包体」。
- `pseudosection` = **视剖面图**。
- 双栏 PDF 图注与正文交织，直接截取会把邻栏句子写进 caption。
- `\title` 行距写 `\\[0.6em]`，漏成 `\[0.6em]` 会开不闭合的展示数学，报「group at level 1 / (\begingroup)」迷惑报错。
- docx 附图的 word/media 顺序可能与文内图号相反，抽图后目检面板标注再命名。
- docx 公式（OMML）抽文本会丢，需按标准方程补全并注明。
- 大表格（>10 行或 ≥8 列）由主代理逐格抽取写 LaTeX，勿让子代理从乱序文本猜列。
- 参考文献条目切分要求「首字母后带句点」，否则期刊缩写 `Res, Lett, p. 49.` 会被误当人名。
- 首页允许溢出到第 2 页；勿为塞进一页压缩版式。
- 检查脚本勿经 shell heredoc（吞 `\` 造成误报）；计数用 `grep -c` 复核。
- 摘要若只查「有摘要标签」会漏整段英文正文 → 必须查英文句首=0（pitfalls 7.1）。
- 图题 `Fig. N.` 首次命中常是正文引用 → 要求行首+长度（pitfalls 7.2）；**GSA 用 `Figure N.`**。
- Windows 下中文文件名 xelatex 用 Python 编译，勿 shell 硬路径（pitfalls 7.4）。
- bulk/modal/estimation 用户改名要长串优先全局替换并重编译（pitfalls 7.5–7.6）。
- 抽正文/图/文献优先按出版社查 `extract_by_publisher.md`；**Elsevier、GSA/Geology、Wiley/JMG、AGU 新版、Nature 主刊已写**；拼装期反斜杠/ED 计数器/缺字形陷阱见 pitfalls §9（Xie-2026-Nature）。
- GSA 三栏：`body_y0` 勿被右上 DOI/左下 ORCID 拉走；页脚 `page_h−32`；`section_disc_*` 文件名可能与内容对调（见 pitfalls 7.12–7.19）。
- 作者单位多行 `\small` 只作用首行 → `\parbox{\centering\small …}`。
- 致谢片段里残留的图注正文会再排一遍 → 图注只留在 `figure` 环境内。
- AGU 新版（Tectonics/JGR 2020s Wiley 平台）是「信息栏+单栏」不是双栏；每页下载水印按行清洗；SI 公式用渲染读图法抄录（pitfalls 8）。
- 作者/单位行超版心会被裁（截图可见）→ 作者拆行、单位逐行 `\small`；首页溢出 p2 允许不强塞（pitfalls 8.5 / 3.12）。
- 数值模拟论文的「模拟详解」附录用三本账框架（力/热/物质）+ 本构逐项比喻 + 设置问答（appendix-guide「模拟详解模式」）。
