# LaTeX 导言区与结构模板（ctex + XeLaTeX）

按论文元信息替换尖括号占位。颜色、页眉页脚可按用户审美删改。

```latex
% !TEX program = xelatex
\documentclass[12pt,a4paper]{ctexart}

% 正文中文（Windows 示例）
\setCJKmainfont{FangSong}[AutoFakeBold=2.5, AutoFakeSlant=0.2]
\setCJKsansfont{SimHei}[AutoFakeBold=2.5]
\setCJKmonofont{FangSong}

\usepackage{geometry}
\geometry{left=2.5cm,right=2.5cm,top=2.85cm,bottom=3.15cm}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{enumitem}
\usepackage{caption}
\usepackage{float}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{calc}
\usepackage{eso-pic}
\usepackage{hyperref}
\usepackage{xurl}
\setlength{\emergencystretch}{1.5em}
\usepackage{setspace}
\onehalfspacing

% 色系（可改）
\definecolor{AccentDeep}{HTML}{1F4E79}
\definecolor{AccentMid}{HTML}{2E75B6}
\definecolor{AccentWarm}{HTML}{C45911}
\definecolor{AccentSoft}{HTML}{D6E3F0}

\hypersetup{
  colorlinks=true,
  linkcolor=AccentDeep,
  citecolor=AccentDeep,
  urlcolor=AccentDeep,
  pdftitle={<中文标题>},
  pdfauthor={<作者>}
}

\ctexset{
  section = {format={\Large\bfseries\centering\color{AccentDeep}},
    beforeskip=1.5ex plus 0.5ex minus 0.2ex, afterskip=1.2ex plus 0.2ex},
  subsection = {format={\large\bfseries\color{AccentDeep!85!black}},
    beforeskip=1.2ex plus 0.3ex, afterskip=0.8ex plus 0.2ex},
  subsubsection = {format={\normalsize\bfseries\color{AccentMid}},
    beforeskip=1ex plus 0.2ex, afterskip=0.6ex plus 0.1ex}
}

\renewcommand{\abstractname}{{\Large\bfseries 摘\quad 要}}
\captionsetup{font=small,labelfont=bf}
\captionsetup[figure]{font=small,labelfont=bf,skip=6pt}
\setlength{\abovecaptionskip}{6pt}
\setlength{\belowcaptionskip}{4pt}
\setlength{\headheight}{18pt}
\setlength{\footskip}{30pt}
% 浮动：减少“图单独成页”与大面积空白
\renewcommand{\topfraction}{0.92}
\renewcommand{\bottomfraction}{0.85}
\renewcommand{\textfraction}{0.04}
\renewcommand{\floatpagefraction}{0.75}
\setlength{\textfloatsep}{10pt plus 2pt minus 4pt}
\setlength{\floatsep}{8pt plus 2pt minus 2pt}
\setlength{\intextsep}{8pt plus 2pt minus 2pt}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{{\color{AccentDeep}\small\bfseries <短标题>}}
\fancyhead[R]{{\color{AccentDeep}\small\itshape <期刊与卷年>}}
\renewcommand{\headrulewidth}{1.2pt}
\renewcommand{\headrule}{%
  {\color{AccentDeep}\hrule width\headwidth height\headrulewidth}%
  \vskip1.2pt
  {\color{AccentSoft}\hrule width\headwidth height0.8pt}}
\fancyfoot[C]{\tikz[baseline=(n.base)]{%
  \node[fill=AccentDeep,text=white,rounded corners=1.5pt,
    inner xsep=8pt,inner ysep=2.8pt,font=\small\bfseries] (n) {\thepage};}}
\fancyfoot[L]{{\color{AccentMid}\footnotesize <书名/短题>}}
\fancyfoot[R]{{\color{AccentMid}\footnotesize <版本说明>}}
\renewcommand{\footrulewidth}{0pt}

% 页缘装饰条（可选；不要右侧书口竖条除非用户要）
\AddToShipoutPictureBG{%
  \begin{tikzpicture}[remember picture,overlay]
    \fill[AccentDeep] (current page.south west) rectangle ([yshift=3.2mm]current page.south east);
    \fill[AccentSoft] ([yshift=3.2mm]current page.south west) rectangle ([yshift=4.0mm]current page.south east);
    \fill[AccentMid!25!white] ([yshift=4.0mm]current page.south west) rectangle ([yshift=5.0mm]current page.south east);
    \fill[AccentDeep] (current page.north west) rectangle ([yshift=-2.4mm]current page.north east);
    \fill[AccentSoft] ([yshift=-2.4mm]current page.north west) rectangle ([yshift=-3.1mm]current page.north east);
    \fill[AccentMid!25!white] ([yshift=-3.1mm]current page.north west) rectangle ([yshift=-3.9mm]current page.north east);
  \end{tikzpicture}}

\title{\heiti\Large <中文标题>\\[0.6em]
\normalfont\normalsize <English title>}
\author{
  <作者与单位>
}
\date{}

\begin{document}
\maketitle
\thispagestyle{fancy}

% 题目、作者（\maketitle）之后：摘要 → 关键词 → 原文信息 → 说明
% 均用段首加粗标签，不用 abstract 环境；段间 \vspace 稍大（约 1.2–1.6em）
\vspace{1.2em}
\noindent\textbf{摘要：}<摘要正文>

\vspace{1.6em}
\noindent\textbf{关键词：}<关键词>

\vspace{1.6em}
\noindent\textbf{原文信息：}<作者. 年份. 题. \textit{期刊} \textbf{卷}, 页/号.> \href{https://doi.org/...}{doi:...}

\vspace{1.6em}
\noindent\textbf{说明：}<翻译说明；非官方译本等>

\vspace{1.2em}
\newpage
\tableofcontents
\newpage

% ===== 正文 \section{...} 由 latex_XX 片段拼入 =====

\end{document}
```

## 章节标题

通识标题（引言/方法/结果/讨论/结论/致谢/参考文献等）**只写中文**，不加括号与英文。专业小节名按 terminology.md；英文仅在专业术语首次出现时跟在正文里。

## 图尺寸与顺序（锁定规则）

- **用户指定过的宽度/高度一律锁定**。例如 `width=\textwidth` 为 100%，`width=0.6\textwidth` 为 60%；写入后除非用户再改，后续脚本不得按纵横比重写。
- 只对未指定或竖长溢出的图用启发式；竖长图优先 `height=0.70-0.75\textheight, keepaspectratio`。
- **图按图号 1…N 依次出现**，且全部在结论/致谢之前。
- 图注**不要**写「图 N：」前缀（编号由 `\caption` 生成），避免双编号。
- 文件 `figNN.png` 的 NN 与正文图号一致。

## 图环境惯例

```latex
\begin{figure}[!htbp]
\centering
\includegraphics[width=0.8\textwidth]{figures/figNN.png}
\caption{中文图注正文，不带“图 N：”前缀}
\label{fig:figNN}
\end{figure}
```

- 浮动选项**必须含 `p`**（`[!htbp]`）：长图注的图超过 `\topfraction` 时，缺 `p` 会被推迟到参考文献之后（pitfalls 3.14）。
- 竖长图：`height=0.72\textheight, width=\textwidth, keepaspectratio`。
- 易独占一页的图：浮动用 `[!htbp]`，长图注用 `\footnotesize`，避免 `[H]`。
- **图勿堆在章末**：图环境紧随首次「图 N」/`\ref` 段落，但按图号 1…N 顺序安插。
- 目录前 `\newpage`，摘要在目录之前。
- 正文 URL：`\url{https://...}`。

## 表格

宽表：`\small` + `\renewcommand{\arraystretch}{1.5}` + `\resizebox{\textwidth}{!}{...}`。  
长行标签用括号并列（`15a/b (X=0)`），慎用单元格内 `\`。
