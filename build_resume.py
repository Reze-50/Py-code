# -*- coding: utf-8 -*-
"""Generate a styled Chinese resume (DOCX) for DeepSeek, LLM algorithm engineer role."""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = RGBColor(0x1F, 0x4E, 0x79)
INK = RGBColor(0x26, 0x26, 0x26)
GRAY = RGBColor(0x55, 0x55, 0x55)
MUTED = RGBColor(0x76, 0x76, 0x76)
ACCENT = RGBColor(0x2E, 0x75, 0xB6)

FONT = "微软雅黑"
USABLE_CM = 17.2
OUT = "DeepSeek-大模型算法工程师-简历.docx"

# ---------------------------------------------------------------- primitives


def set_char_spacing(run, pts):
    rPr = run._r.get_or_add_rPr()
    sp = OxmlElement("w:spacing")
    sp.set(qn("w:val"), str(int(pts * 20)))
    rPr.insert_element_before(
        sp,
        "w:w", "w:kern", "w:position", "w:sz", "w:szCs", "w:highlight", "w:u",
        "w:effect", "w:bdr", "w:shd", "w:fitText", "w:vertAlign", "w:rtl",
        "w:cs", "w:em", "w:lang", "w:eastAsianLayout", "w:specVanish", "w:oMath",
    )


def run(p, text, size=9.5, bold=False, color=INK, spacing=None, italic=False):
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = FONT
    rPr = r._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), FONT)
    if spacing:
        set_char_spacing(r, spacing)
    return r


def fmt(p, before=0, after=0, line=1.22, left=0.0, first=0.0, right=0.0,
        align=None, keep_next=False, keep_together=False):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    pf.left_indent = Cm(left)
    pf.right_indent = Cm(right)
    pf.first_line_indent = Cm(first)
    pf.keep_with_next = keep_next
    pf.keep_together = keep_together
    if align is not None:
        pf.alignment = align
    # disable Word's contextual spacing so our explicit spacing wins
    pPr = p._p.get_or_add_pPr()
    el = OxmlElement("w:contextualSpacing")
    el.set(qn("w:val"), "0")
    pPr.insert_element_before(
        el, "w:mirrorIndents", "w:suppressOverlap", "w:jc", "w:textDirection",
        "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl", "w:divId",
        "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange",
    )
    return p


def border(p, side="bottom", sz=8, color="1F4E79", space=4):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    el = OxmlElement("w:" + side)
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(sz))
    el.set(qn("w:space"), str(space))
    el.set(qn("w:color"), color)
    pbdr.append(el)
    pPr.insert_element_before(
        pbdr, "w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
        "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
        "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
        "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
        "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl",
        "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange",
    )


def right_tab(p, cm=USABLE_CM):
    p.paragraph_format.tab_stops.add_tab_stop(Cm(cm), WD_TAB_ALIGNMENT.RIGHT)


def section(doc, title, en=""):
    p = doc.add_paragraph()
    fmt(p, before=11, after=5.5, line=1.0, keep_next=True)
    run(p, title, size=11.5, bold=True, color=NAVY, spacing=1.0)
    if en:
        run(p, "   " + en, size=8, bold=False, color=MUTED, spacing=1.4)
    border(p, "bottom", sz=6, color="1F4E79", space=3)
    return p


def entry(doc, title, meta, date=None):
    p = doc.add_paragraph()
    fmt(p, before=6, after=1, line=1.15, keep_next=True)
    right_tab(p)
    run(p, title, size=10, bold=True, color=INK)
    if date:
        run(p, "\t" + date, size=8.5, color=MUTED)
    if meta:
        q = doc.add_paragraph()
        fmt(q, before=0, after=2, line=1.1, keep_next=True)
        run(q, meta, size=8.5, color=ACCENT)
    return p


def bullet(doc, label, text):
    p = doc.add_paragraph()
    fmt(p, before=0, after=1.6, line=1.28, left=0.62, first=-0.62)
    run(p, "▪ ", size=7.5, color=ACCENT)
    if label:
        run(p, label + "：", size=9, bold=True, color=RGBColor(0x17, 0x37, 0x5E))
    run(p, text, size=9, color=INK)
    return p


def body(doc, text, size=9, before=0, after=1.6, line=1.32, left=0.0, first=0.0):
    p = doc.add_paragraph()
    fmt(p, before=before, after=after, line=line, left=left, first=first)
    run(p, text, size=size, color=INK)
    return p


def add_page_field(p, instr, size=8):
    r = p.add_run()
    r.font.size = Pt(size)
    r.font.color.rgb = MUTED
    r.font.name = FONT
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "begin")
    r._r.append(fld)
    r2 = p.add_run()
    r2.font.size = Pt(size)
    r2.font.color.rgb = MUTED
    r2.font.name = FONT
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = " %s " % instr
    r2._r.append(it)
    r3 = p.add_run()
    r3.font.size = Pt(size)
    r3.font.color.rgb = MUTED
    r3.font.name = FONT
    f2 = OxmlElement("w:fldChar")
    f2.set(qn("w:fldCharType"), "separate")
    r3._r.append(f2)
    r4 = p.add_run("1")
    r4.font.size = Pt(size)
    r4.font.color.rgb = MUTED
    r4.font.name = FONT
    r5 = p.add_run()
    r5.font.size = Pt(size)
    r5.font.color.rgb = MUTED
    r5.font.name = FONT
    f3 = OxmlElement("w:fldChar")
    f3.set(qn("w:fldCharType"), "end")
    r5._r.append(f3)


# ---------------------------------------------------------------- document

doc = Document()

# base style
normal = doc.styles["Normal"]
normal.font.name = FONT
normal.font.size = Pt(9.5)
normal.font.color.rgb = INK
rPr = normal.element.get_or_add_rPr()
rFonts = rPr.find(qn("w:rFonts"))
if rFonts is None:
    rFonts = OxmlElement("w:rFonts")
    rPr.insert(0, rFonts)
for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
    rFonts.set(qn(attr), FONT)
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.space_after = Pt(0)
normal.paragraph_format.line_spacing = 1.22

sec = doc.sections[0]
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.top_margin = Cm(1.45)
sec.bottom_margin = Cm(1.4)
sec.left_margin = Cm(1.9)
sec.right_margin = Cm(1.9)
sec.header_distance = Cm(0.9)
sec.footer_distance = Cm(0.75)

# ---------------------------------------------------------------- header
p = doc.add_paragraph()
fmt(p, before=0, after=1, line=1.0)
run(p, "DeepSeek", size=25, bold=True, color=NAVY, spacing=1.5)
run(p, "   深度求索 · 通用大语言模型", size=9, color=MUTED, spacing=1.0)

p = doc.add_paragraph()
fmt(p, before=1, after=3, line=1.0)
run(p, "大模型算法工程师", size=11.5, bold=True, color=INK)
run(p, "   求职意向：预训练与架构 / 强化学习后训练 / 推理系统优化", size=9, color=GRAY)

p = doc.add_paragraph()
fmt(p, before=0, after=6, line=1.0)
run(p, "杭州 · 中国", size=8.5, color=GRAY)
run(p, "　|　", size=8.5, color=RGBColor(0xBF, 0xBF, 0xBF))
run(p, "+86 138 5710 2024", size=8.5, color=GRAY)
run(p, "　|　", size=8.5, color=RGBColor(0xBF, 0xBF, 0xBF))
run(p, "talent@deepseek.com", size=8.5, color=GRAY)
run(p, "　|　", size=8.5, color=RGBColor(0xBF, 0xBF, 0xBF))
run(p, "github.com/deepseek-ai", size=8.5, color=GRAY)
border(p, "bottom", sz=10, color="1F4E79", space=6)

# ---------------------------------------------------------------- summary
section(doc, "个人概述", "PROFILE")
p = doc.add_paragraph()
fmt(p, before=0, after=0, line=1.42)
run(
    p,
    "通用大语言模型，671B 总参数 / 37B 激活 / 128K 上下文。以「用更少算力逼近更强的智能」为研究主线，"
    "在超大规模预训练、稀疏专家架构、强化学习推理与推理系统优化上具备从公式到万卡集群的完整落地经验；"
    "代表工作 DeepSeek-V3 与 DeepSeek-R1 均以技术报告与开源权重完整交付。"
    "期待加入以 AGI 为目标的团队，继续压低训练与推理的成本曲线，把模型能力推进到下一个数量级。",
    size=9,
    color=INK,
)

# ---------------------------------------------------------------- education
section(doc, "教育背景", "EDUCATION")
entry(doc, "浙江大学　计算机科学与技术　博士（直博）", None, "2020.09 – 2025.03")
p = doc.add_paragraph()
fmt(p, before=0, after=3, line=1.2, left=0.0)
run(p, "研究方向：大语言模型预训练与强化学习　·　导师：林之远 教授　·　GPA 3.92 / 4.00（专业前 5%）", size=8.5, color=GRAY)

entry(doc, "浙江大学　计算机科学与技术　学士", None, "2016.09 – 2020.06")
p = doc.add_paragraph()
fmt(p, before=0, after=0, line=1.2)
run(p, "优秀毕业论文：长文本推理的注意力稀疏化加速　·　GPA 3.90 / 4.00（专业前 3%）", size=8.5, color=GRAY)

# ---------------------------------------------------------------- experience
section(doc, "核心研究与工程经历", "EXPERIENCE")

entry(
    doc,
    "DeepSeek-V3：671B 稀疏基座模型预训练",
    "核心算法工程师 · 基础模型预训练组 · 杭州",
    "2024.01 – 至今",
)
bullet(doc, "架构设计", "提出 MLA 多头潜在注意力与 DeepSeekMoE 无辅助损失负载均衡策略，KV Cache 压缩至 MHA 的约 1/4，671B 总参数下每 token 仅激活 37B，同时降低训练与推理成本。")
bullet(doc, "训练系统", "主导 DualPipe 双向流水线并行与 FP8 混合精度训练方案，实现计算与通信全重叠，端到端吞吐提升 1.8×、全程无可见精度回退；以 2.788M H800 GPU 小时完成 14.8T token 预训练。")
bullet(doc, "训练目标", "引入 MTP 多 token 预测目标提升数据效率，并原生支持推测解码，解码吞吐再提升 1.8×。")
bullet(doc, "数据工程", "搭建 14.8T token 多源语料清洗、去重与配比流水线，中英数理代码配比经系统性消融确定，脏数据率降至 0.3% 以下。")
bullet(doc, "交付结果", "MMLU 88.5、MATH-500 90.2、HumanEval 82.6，以约 1/10 的训练成本达到闭源前沿模型水平；技术报告共同第一作者，权重开源后 GitHub 50k+ Stars。")

entry(
    doc,
    "DeepSeek-R1：强化学习驱动的推理能力",
    "强化学习方向负责人 · 后训练组",
    "2024.06 – 2025.01",
)
bullet(doc, "算法验证", "以 GRPO 完成大规模纯强化学习训练，验证模型可自发涌现长链思考、自我验证与反思行为（R1-Zero），AIME 2024 由 15.6% 提升至 79.2%。")
bullet(doc, "训练流程", "设计「少量冷启动 SFT → 拒绝采样迭代 → 多阶段 RL」流水线，解决长思维链可读性与中英混杂问题，在提升推理能力的同时保持通用对话能力不退化。")
bullet(doc, "能力蒸馏", "将 R1 的推理能力蒸馏至 1.5B–70B 稠密模型，7B 学生模型 MATH-500 达 92.8%、AIME 2024 达 55.5%，全面超过同规模开源模型。")
bullet(doc, "评测体系", "搭建覆盖数学、代码、逻辑与安全的自动化评测与回归平台，单轮全量评测由 6 小时缩短至 40 分钟，支撑每日多次训练迭代。")

entry(
    doc,
    "长上下文与推理系统：DeepSeek-V2 / Coder 系列",
    "算法工程师 · 预训练与推理组",
    "2023.06 – 2024.01",
)
bullet(doc, "上下文扩展", "以两阶段继续预训练结合 YaRN 将窗口由 4K 扩展至 128K，长文检索任务全深度准确率 > 98%，长文摘要 ROUGE-L 提升 6.4 个点。")
bullet(doc, "推理优化", "落地 PagedAttention、KV Cache 低比特量化与连续批处理，单卡吞吐提升 2.3×，P99 延迟下降 40%，同等算力下服务成本降低一半以上。")
bullet(doc, "代码模型", "参与 DeepSeek-Coder 数据构造（87% 代码 / 10% 英文 / 3% 中文）与 FIM 训练目标设计，HumanEval 达 90%+，支持 16K 仓库级补全。")

# ---------------------------------------------------------------- papers
section(doc, "代表论文与开源", "PUBLICATIONS")
papers = [
    ("DeepSeek-V3 Technical Report", "共同第一作者", "2024", "arXiv:2412.19437"),
    ("DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", "共同第一作者", "2025", "arXiv:2501.12948"),
    ("DeepSeekMath: Pushing the Limits of Mathematical Reasoning（GRPO）", "核心作者", "2024", "arXiv:2402.03300"),
    ("DeepSeekMoE / DeepSeek-Coder / DeepSeek-V2 系列", "核心贡献者", "2023 – 2024", "技术报告"),
]
for title, role, year, venue in papers:
    p = doc.add_paragraph()
    fmt(p, before=0, after=0, line=1.2, left=0.46, first=-0.46, keep_next=True)
    run(p, "▪ ", size=7.5, color=ACCENT)
    run(p, title, size=8.8, bold=True, color=INK)
    q = doc.add_paragraph()
    fmt(q, before=0, after=1.5, line=1.12, left=0.46)
    run(q, role + "　·　" + venue, size=8, color=MUTED)
    run(q, "\t" + year, size=8, color=MUTED)
    right_tab(q)

p = doc.add_paragraph()
fmt(p, before=2, after=0, line=1.3)
run(p, "开源：deepseek-ai 系列仓库累计 150k+ GitHub Stars，模型权重累计下载 1,000 万次以上；维护 3 个社区推理适配项目。", size=8.8, color=GRAY)

# ---------------------------------------------------------------- skills
section(doc, "专业技能", "SKILLS")
skills = [
    ("模型与算法", "Transformer / MoE 稀疏架构 / MLA 注意力 / 长上下文扩展（YaRN、RoPE）/ 多模态对齐 / 推测解码"),
    ("后训练", "SFT、RLHF（PPO / DPO / GRPO）、拒绝采样、过程奖励建模、能力蒸馏、数据配比与课程学习"),
    ("训练工程", "PyTorch、Triton、CUDA；Megatron-LM / DeepSpeed 深度改造；TP / PP / EP / DP 混合并行；FP8 / BF16；千卡—万卡集群稳定性（故障恢复 < 5 分钟）"),
    ("推理部署", "vLLM / SGLang / TensorRT-LLM 二次开发，KV Cache 管理、量化（INT4 / FP8）、连续批处理、PD 分离"),
    ("编程语言", "Python（精通）、C++ / CUDA（熟练）、Rust（了解）；熟悉 Linux 与大规模实验调度（Slurm / Kubernetes）"),
]
for label, text in skills:
    p = doc.add_paragraph()
    fmt(p, before=0, after=0.8, line=1.26, left=1.85, first=-1.85)
    run(p, label, size=9, bold=True, color=RGBColor(0x17, 0x37, 0x5E))
    run(p, "　", size=9)
    run(p, text, size=9, color=INK)

# ---------------------------------------------------------------- honors
section(doc, "荣誉与奖项", "HONORS")
honors = [
    "国家奖学金（2022、2024）　·　浙江大学优秀博士毕业生（2025）　·　深度求索年度技术突破奖（2024）",
    "ACM-ICPC 亚洲区域赛 金牌（2019）　·　全国大学生数学建模竞赛 一等奖（2018）　·　CCF 优秀学生论文奖（2024）",
]
for h in honors:
    p = doc.add_paragraph()
    fmt(p, before=0, after=1.0, line=1.28, left=0.46, first=-0.46)
    run(p, "▪ ", size=7.5, color=ACCENT)
    run(p, h, size=8.8, color=INK)

# ---------------------------------------------------------------- self assessment
section(doc, "自我评价", "SUMMARY")
p = doc.add_paragraph()
fmt(p, before=0, after=0, line=1.4)
run(
    p,
    "习惯把问题拆到第一性原理：先算清算力、数据与时间的效率账，再决定算法方向。"
    "坚持结果可复现、结论可证伪，重要工作一律以论文与开源代码交付。"
    "主导过 6 次千卡级训练任务的排期与故障复盘，能承担从目标设定到上线服务的端到端责任；抗压、直率，乐于被数据和实验说服。",
    size=9,
    color=INK,
)

# ---------------------------------------------------------------- footer
footer = sec.footer
fp = footer.paragraphs[0]
fp.text = ""
fmt(fp, before=0, after=0, line=1.0)
# the built-in Footer style carries a centred tab: retarget it to the right margin,
# otherwise the page number lands in the middle of the footer
footer_tabs = doc.styles["Footer"].paragraph_format.tab_stops
footer_tabs.clear_all()
footer_tabs.add_tab_stop(Cm(USABLE_CM), WD_TAB_ALIGNMENT.RIGHT)
fp.paragraph_format.tab_stops.clear_all()
right_tab(fp)
run(fp, "DeepSeek · 大模型算法工程师 · 求职简历", size=8, color=MUTED)
run(fp, "\t", size=8)
add_page_field(fp, "PAGE")
run(fp, " / ", size=8, color=MUTED)
add_page_field(fp, "NUMPAGES")

# ---------------------------------------------------------------- meta
cp = doc.core_properties
cp.title = "DeepSeek — 大模型算法工程师 求职简历"
cp.author = "DeepSeek"
cp.subject = "大模型算法工程师 求职简历"
cp.keywords = "大模型, LLM, 预训练, 强化学习, MoE, RLHF, 推理优化"
cp.comments = ""

doc.save(OUT)
print("saved:", OUT)
