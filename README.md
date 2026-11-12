# geo-paper-translate

将地学（及相关领域）英文学术论文 PDF 翻译为**可编译的中文 LaTeX 译本**的 Claude Agent Skill：正文全译、原图自动裁切插入、图注与术语按地学惯例统一、XeLaTeX 排版出 PDF，可附论文解读/公式详解教学附录。

## 交付物

对一篇论文执行后，在 PDF 所在目录生成：

```text
{第一作者姓}-{年份}-{期刊缩写}/
├── {…}-中文译本.tex / .pdf   # XeLaTeX 两遍编译的成品（正文、图、文献、附录）
├── figures/fig01.png …       # 从原文 PDF 按页坐标自动裁切的插图
├── sections/section_*.txt    # 分章节原文抽取（中间件，可留）
└── original_extracted.txt    # 全文抽取备份
```

- 参考文献保留英文；图注、术语表中文；术语以 `references/terminology.md` 为准（全岩成分、含量、$P$–$T$ 估算、视剖面图等用户沉淀译名）。
- 交付前按 SKILL.md 验收清单 1–10 自检（图序、术语残留、摘要必须整段中文、中文路径编译等）。

## 运行环境（新电脑首次使用前必装）

Skill 本体只是 Markdown 指令，拷贝即被识别；执行依赖 **Python 抽取库** 与 **XeLaTeX** 两部分，均须**系统级安装**（任何目录可用），**不要**在工作目录内创建临时虚拟环境（venv）。

### 1) Python 3.10+（加入 PATH）

```bash
# Windows: python.org 安装包勾选 "Add python.exe to PATH"，或 winget install Python.Python.3.12
# macOS:   brew install python

python -m pip install --upgrade pip
python -m pip install pymupdf pdfplumber pillow lxml

# 验证（四个都打印 ok 即就绪）
python -c "import fitz; print('fitz ok')"
python -c "import pdfplumber; print('pdfplumber ok')"
python -c "import PIL; print('PIL ok')"
python -c "import lxml; print('lxml ok')"
```

| 包 | 用途 |
|---|---|
| `pymupdf`（fitz） | 读 PDF、分栏重排、裁图、渲染校验（核心，必需） |
| `pdfplumber` | 表格/文本抽取备用通道 |
| `pillow`（PIL） | 裁图边缘自检 |
| `lxml` | 解析 docx 补充材料的 OMML 公式（无 SI docx 可不装） |

### 2) XeLaTeX（编译译本的硬性依赖）

- 推荐 **TeX Live 完整版**（https://tug.org/texlive/）：ctex、xeCJK、fancyhdr、tikz、eso-pic、hyperref、xurl 等模板宏包一次装齐；
- 或 **MiKTeX**（https://miktex.org/）：安装时把 “Install missing packages on the fly” 设为 yes，否则首次编译会卡在缺包提示。
- 验证：`xelatex --version` 任意目录可运行；首次真实编译即宏包冒烟测试。

### 3) 中文字体

模板默认仿宋（`FangSong`）+ 黑体（`SimHei`）：**Windows 自带**；macOS/Linux 无同名字体时编译报 font-not-found——改为系统已有中文字体（如 Noto Sans CJK SC）或补装同名字体。

### 4) skill 安装位置

把整个 `geo-paper-translate/` 文件夹复制（或 clone）到：

```text
Windows:  C:\Users\<用户名>\.claude\skills\geo-paper-translate\
macOS:    ~/.claude/skills/geo-paper-translate/
```

重启会话后即被发现。本 skill 不需要 Office、网络服务或付费软件，全部流程本地完成。

## 使用

在装有本 skill 的 Claude 会话中：

```text
请用 geo-paper-translate 翻译这篇文献，附上论文解读附录：
D:\path\to\paper.pdf
```

工作流：读术语/坑点/分出版社提取参考 → 分通道抽取（摘要/正文/图题/文献）→ 分章并行翻译 → 自动裁图 → 拼装主文档 → XeLaTeX 编译两遍 → 验收清单自检 → 交付（可选回写新刊提取技巧与新译名）。

## 仓库文件结构

```text
SKILL.md                          # 主流程：交付物、抽取/翻译/裁图/拼装/编译/验收、环境节
references/
├── terminology.md                # 地学译名总表（用户多轮纠正沉淀）+ 残留清单
├── pitfalls.md                   # 实作踩坑（含 §7 拼装验收、§9 拼装期 LaTeX 陷阱）
├── extract_by_publisher.md       # 分出版社提取技巧：Elsevier/GSA/Wiley/AGU/Nature 等
├── latex-template.md             # ctex + XeLaTeX 导言区与封面模板
└── appendix-guide.md             # 公式详解/论文解读附录写作框架
scripts/
└── extract_figures.py            # 按图题锚点裁图参考脚本
README.md                         # 本说明
```

## 相关规范

- 交付前必过 SKILL.md「验收清单 1–10」；Windows 中文文件名须用 Python `subprocess` + `os.chdir` 调 XeLaTeX。
- 新刊提取技巧按「现象→做法」回写 `references/extract_by_publisher.md`；用户纠正译名只进 `references/terminology.md`。
