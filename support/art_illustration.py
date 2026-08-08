# -*- coding: utf-8 -*-
"""
艺术插画预设模块

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

ART_ILLUSTRATION = {
    "template_id": "art_illustration",
    "name": "艺术插画",
    "description": "专业艺术插画创作指导，为全品类风格打造标准化高可控视觉叙事描述。语义权重优先级：核心主题情感→风格类型笔触→三维视角构图→色彩配比→主体细节→光影氛围。内置三维度视角、70%/25%/5%色彩配比、双重质感约束与画面精简约束，强化风格统一、笔触质感、构图叙事与意境表达。覆盖水彩、油画、扁平、国潮、水墨工笔等风格赛道。",
}

class ArtIllustration:
    def __init__(self):
        # 下游生图模型内容组织公式库
        self.model_formula_library = {
            "Flux1": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面主题情感氛围 → 画种风格笔触质感 → 主体造型细节 → 留白背景。侧重插画意境叙事，弱化细碎关键词堆砌，画面艺术感柔和高级。",
                "formula_en": "Content order: overall picture theme emotion atmosphere → illustration style brush texture → subject shape details → blank background. Focus on artistic conception narration."
            },
            "Flux2_klein": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：插画主题与画种风格 → 色彩光影层次 → 主体笔触材质 → 克制留白。平衡手绘笔触细节与画面氛围感，光影过渡贴合插画艺术逻辑。",
                "formula_en": "Content order: illustration theme & painting style → color light layers → subject brush material → restrained blank. Balance hand-painted brush details and picture atmosphere."
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：主体笔触肌理细节优先 → 画面构图透视轮廓 → 三维视角构图 → 全局分层布光 → 极简留白。精准把控插画透视比例，统一水彩/油画/国潮等各类画风质感标准。",
                "formula_en": "Content order: subject brush texture details first → picture composition perspective contour → 3D view layout → global layered lighting → minimalist blank. Strictly control illustration perspective, unify texture standards of watercolor/oil/guochao styles."
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：构图视觉重心主体 → 主体动态神态 → 70/25/5色彩管控 → 光影明暗层次 → 干净留白。构图规整克制，色彩层级清晰严格遵循配比，虚实透视过渡自然柔和。",
                "formula_en": "Content order: composition visual focus subject → subject movement expression → 70/25/5 color control → light shadow layers → clean blank. Neat restrained composition, clear color layers following fixed ratio, natural virtual perspective transition."
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：全局情绪光影基调 → 主体形体情感表达 → 画种笔触质感细节 → 纸张肌理面料 → 极简布景。强化插画情绪光影叙事，区分水彩/油画/国潮专属笔触体系。",
                "formula_en": "Content order: global emotional light tone → subject form emotion expression → painting brush texture details → paper texture fabric → minimalist set. Strengthen emotional light narration, distinguish exclusive brush systems for each style."
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整幅插画主题基调 → 舒展主体动态 → 统一笔触质感 → 简约留白。极简插画叙事逻辑，删减冗余装饰杂物，突出画面核心叙事主体。",
                "formula_en": "Content order: whole illustration theme tone → relaxed subject movement → unified brush texture → simple blank. Minimal illustration narration, remove redundant decorations, highlight core narrative subject."
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：主体造型笔触肌理 → 远近虚实层次 → 光影冷暖过渡 → 辅助元素细节 → 轻量化留白。强化插画透视准确度，不同画种笔触区分清晰，光影层次连贯柔和。",
                "formula_en": "Content order: subject shape brush texture → near-far virtual layers → light warm-cold transition → auxiliary element details → lightweight blank. Accurate illustration perspective, distinct brushes for styles, soft continuous lighting layers."
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：插画整体主题气质 → 主体笔触材质细节 → 专业分层光影 → 风格专属纹样元素 → 极简留白。整幅画面色调统一协调，意境刻画细腻，插画沉浸叙事感强烈。",
                "formula_en": "Content order: overall illustration theme temperament → subject brush material details → professional layered light → style exclusive pattern elements → minimalist blank. Unified picture tone, delicate artistic conception, strong immersive illustration narration."
            }
        }
        # 全局底层规则
        self.global_base_rules = {
            "zh": """
你是专业全品类艺术插画提示词扩写专家，覆盖水彩、油画、扁平、国潮、水墨工笔、奇幻二次元全插画题材。
所有创作坚守插画视觉叙事基线，仅主题情感、画种笔触、色彩光影、构图布局差异化，禁止多种画风混搭造成画面割裂跳变。
画面遵循70%主体视觉权重+30%环境配比，色彩固定70主/25辅/5点缀层级，无杂乱高饱和撞色堆砌。
光影贴合对应画种艺术表现逻辑，水彩通透柔光、油画厚重明暗、国潮对比高光、水墨淡染层次区分明确。
笔触、线条、色块统一匹配对应风格，国潮融合传统纹样现代平涂，水墨突出宣纸浓淡留白，油画厚堆肌理，水彩晕染渗透。
完整保留用户输入主题、插画风格、画幅、视角、主体、色调全部信息，仅补充笔触、纸张肌理、光影、传统纹样专业细节，不自动新增无关装饰杂物。
画面执行严格精简约束，仅留存叙事核心元素，多余装饰全部剔除。
输出禁忌：禁止权重符号、分辨率/DPI/画布尺寸等数值技术参数堆砌；禁止画风混乱、透视扭曲、塑料虚假平涂质感；禁止字幕水印logo、完美对称、零瑕疵等违规描述。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional full-category art illustration prompt expert, covering watercolor, oil painting, flat, guochao, ink meticulous, fantasy anime illustration themes.
All creations follow illustration visual narrative baseline, differentiated only by theme emotion, painting brush, color light, composition layout, no mixed styles causing picture fragmentation.
Picture follows 70 subject visual weight +30 environment ratio, fixed 70 main /25 secondary /5 accent color layers, no messy oversaturated color collision.
Light complies with each painting's artistic logic: transparent soft watercolor, thick oil light contrast, guochao highlight contrast, ink light wash layers clearly distinguished.
Brushes, lines, color blocks match corresponding styles; guochao combines traditional patterns & modern flat paint, ink highlights xuan paper shade blank, oil thick texture, watercolor diffusion penetration.
Fully retain user input theme, illustration style, frame, view, subject, tone info, only supplement brush, paper texture, light, traditional pattern details without irrelevant decorations.
Strict frame simplification rule, only keep core narrative elements, remove redundant ornaments.
Taboo: no weight symbols, stacked numeric technical params like resolution/DPI/canvas size; no chaotic styles, distorted perspective, fake plastic flat texture; no subtitles watermarks logos, perfect symmetry, flawless description.
Strictly output two formats without extra comments.
"""
        }
        # 唯一主预设模板，绑定原有ART_ILLUSTRATION模板id
        self.preset_library = {
            "art_illustration": {
                "template_id": "art_illustration",
                "display_name": ART_ILLUSTRATION["name"],
                "description": ART_ILLUSTRATION["description"],
                # 中英双语固定前置正向约束
                "positive_constraints": {
                    "zh": "插画风格统一连贯，构图叙事逻辑严谨，70/25/5色彩配比和谐分层，笔触线条色块质感统一无跳变，透视比例精准无畸变；水彩通透晕染、油画厚重堆叠、国潮传统纹样融合、水墨浓淡留白、扁平利落色块等各类画种专属质感完整；光影明暗冷暖过渡自然无生硬断层，画面干净聚焦主体，仅保留叙事核心元素；国风插画保有笔墨宣纸气韵，写实油画肌理厚重，水彩通透轻盈，整体意境饱满，兼具画面叙事力与手绘艺术温度",
                    "en": "Unified consistent illustration style, rigorous composition narrative logic, harmonious layered 70/25/5 color ratio, unified brush line block texture without jump, accurate perspective without distortion; complete exclusive texture for watercolor transparent diffusion, thick oil stacking, guochao traditional pattern fusion, ink shade blank, neat flat color blocks; natural warm-cold light transition without stiff break, clean picture focusing subject, only core narrative elements retained; chinese illustration retains ink & xuan paper charm, thick realistic oil texture, light transparent watercolor, full artistic conception, both picture narrative power and hand-painted warmth."
                },
                # 全风格细分专属规则
                "preset_rules": {
                    "zh": """
【全插画专属细分规则】
1. 通用基线：遵循语义权重：核心主题情感→风格类型笔触→三维视角构图→色彩配比→主体细节→光影氛围；用户指定画幅视角优先，无指定选取合规审美角度；严格70%/25%/5%色彩配比，画面精简约束；禁用["8K", "4K", "分辨率", "DPI", "色彩模式", "帧率", "码率", "采样率", "编码器", "HDR", "杜比", "字幕", "水印", "logo", "完美对称", "零瑕疵", "塑料感", "崩坏", "扭曲"]。
2. 水彩插画：湿画法晕染渗透，薄透半透明色块，松软细碎笔触，低饱和柔和色调，纸面轻微肌理，远景雾虚，光斑细碎柔光。
3. 油画风格：厚涂堆叠/刮刀肌理，厚重颜料块面，明暗强对比，中高饱和色彩，画布颗粒质感，硬边粗笔触。
4. 扁平插画：干净利落平涂色块，无复杂渐变，清晰轮廓线条，几何简化造型，高饱和明快配色，极简装饰。
5. 国潮风格：传统云雷/龙凤纹样+现代平涂，粗书法线条，红金墨主色调，明暗高光对比，浮雕式装饰元素。
6. 水墨工笔：宣纸浓淡墨色，工笔精细铁线/游丝描，大面积留白，低饱和素雅，远山淡染、近景重墨。
7. 奇幻二次元：细腻分层软笔触，通透漫射光影，理想化人物造型，冷暖渐变柔和，梦幻低饱和氛围。
所有题材：用户指定内容优先级最高，仅补充对应画种笔触、纸张、纹样、光影专业细节，不篡改插画主题与核心构图。
""",
                    "en": """
【Universal Illustration Exclusive Rules】
1. General baseline: Follow semantic weight: core theme emotion > style brush > 3D composition > color ratio > subject details > light atmosphere; user-specified frame view takes priority, select compliant aesthetic angle if unspecified; strictly 70/25/5 color ratio, frame simplification rule; forbidden words list: 8K,4K,resolution,DPI,color mode,frame rate,bit rate,sampling rate,encoder,HDR,dolby,subtitle,watermark,logo,perfect symmetry,flawless,plastic texture,collapse,distort.
2. Watercolor illustration: wet diffusion wash, thin transparent color blocks, soft fine brush, low saturation soft tone, slight paper grain, blurry background, tiny soft light spots.
3. Oil painting style: thick impasto / palette knife texture, heavy pigment blocks, strong light contrast, medium-high saturation, canvas grain, rough hard-edge strokes.
4. Flat illustration: neat flat color blocks, no complex gradient, clear outline lines, simplified geometric shape, bright high saturation color, minimal ornaments.
5. Guochao style: traditional dragon cloud pattern + modern flat paint, bold calligraphy lines, red gold black main tone, highlight contrast, embossed decorative elements.
6. Ink meticulous painting: xuan paper ink shade, fine meticulous line drawing, large blank space, low saturation elegant, light distant mountain dark foreground ink.
7. Fantasy anime: delicate layered soft brush, transparent diffuse light, ideal character shape, soft warm-cold gradient, dream low saturation vibe.
All themes: User-specified content highest priority, only supplement brush/paper/pattern/light details without altering illustration theme & core composition.
"""
                },
                "negative_base": {
                    "zh": "多种画风混乱跳变，色彩脏污溢出色块，构图失衡主体偏移，装饰杂物冗余堆砌，线条断续崩坏扭曲，透视逻辑错误，塑料平涂虚假质感，光影生硬断层强光，笔触杂乱无层次，边缘锯齿毛躁，过度锐化，字幕水印logo，高饱和杂乱撞色，画面空洞无叙事，元素堆砌抢夺视觉焦点，前后画风不统一",
                    "en": "Mixed chaotic painting styles, muddy overflow color blocks, unbalanced shifted subject, stacked redundant ornaments, broken distorted lines, wrong perspective logic, fake plastic flat texture, stiff harsh light break, disorder layered brushes, jagged edges, over-sharpening, subtitles watermarks logos, messy oversaturated color collision, empty non-narrative frame, stacked distracting elements, inconsistent front-back painting style"
                }
            }
        }
        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】2-3段连贯文字：首段插画构图、画幅与整体主题情感基调；第二段主体造型、专属笔触与色彩分层；第三段全局光影、纸面肌理与画面意境；总字数300-600字，全程规避分辨率、DPI、画布尺寸等数字参数，手绘艺术化叙事语言，无额外解释。",
                "en": "[Natural Paragraph Mode] 2-3 coherent paragraphs: illustration composition frame & overall theme emotion; subject shape exclusive brush & color layers; global light paper grain & artistic conception; 300-600 words, avoid resolution/DPI/canvas numeric params, hand-painted artistic narration without extra explanation."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1.插画品类、画种风格与全局正向约束
2.画面构图、视觉引导、主体70%占比、画幅比例、精简约束
3.三维景别视角：距离、水平朝向、垂直俯仰、景深虚实
4.核心主体造型、动态、辅助叙事次要元素
5.专属笔触、线条、材质肌理、画种技法表现
6.光源方向、冷暖明暗过渡、全局光影氛围
7.70/25/5分层色彩配比、整体饱和度调性
8.国风/国潮专属传统纹样、水墨留白元素
9.场景环境、核心意境与情感表达
10.笔刷、纸张质感定性建议、全局禁止参数清单
11.3-5个概括插画气质的风格标签""",
                "en": """[Structured Mode] Output strictly in this order:
1. Illustration category, painting style & global positive constraints
2. Frame composition, visual guide, 70% subject proportion, aspect ratio, simplification rule
3. 3D shot view: distance, horizontal orientation, vertical pitch, depth blur
4. Core subject shape, movement, secondary narrative elements
5. Exclusive brush, line, material texture, painting technique performance
6. Light source direction, warm-cold transition, global light atmosphere
7. 70/25/5 layered color ratio, overall saturation tone
8. Traditional patterns & ink blank elements for chinese/guochao styles
9. Scene environment, core artistic conception & emotion expression
10. Qualitative brush/paper texture suggestion, global forbidden param list
11. 3-5 style tags summarizing illustration temperament"""
            }
        }

    def detect_language(self, text: str) -> str:
        import re
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        return "zh" if chinese_chars >= english_words else "en"

    def build_prompt(
        self,
        user_input: str,
        preset_name: str,
        downstream_model: str,
        output_language: str = "auto",
        enable_global_preconstraint: bool = True,
        enable_negative_prompt: bool = True,
        output_format: str = "both"
    ):
        if preset_name not in self.preset_library:
            raise ValueError(f"预设模板不存在：{preset_name}")
        if downstream_model not in self.model_formula_library:
            raise ValueError(f"不支持的下游模型：{downstream_model}")
        preset = self.preset_library[preset_name]
        model_config = self.model_formula_library[downstream_model]
        if output_language == "auto":
            lang = self.detect_language(user_input)
        else:
            lang = output_language if output_language in ["zh", "en"] else "zh"
        global_rule = self.global_base_rules[lang] if enable_global_preconstraint else ""
        preset_rule = preset["preset_rules"][lang]
        pos_constraint = preset["positive_constraints"][lang]
        formula_hint = model_config[f"formula_{lang}"]
        natural_guide = self.format_guide["natural"][lang]
        structured_guide = self.format_guide["structured"][lang]
        prompt_parts = []
        if enable_global_preconstraint:
            prompt_parts.append(f"【Hard Precondition Baseline】\n{pos_constraint}")
            prompt_parts.append(global_rule)
        prompt_parts.append(f"下游模型内容组织公式：{formula_hint}")
        prompt_parts.append(preset_rule)
        prompt_parts.append(f"用户原始需求：{user_input}")
        if output_format == "natural":
            prompt_parts.append(natural_guide)
        elif output_format == "structured":
            prompt_parts.append(structured_guide)
        else:
            prompt_parts.append(natural_guide)
            prompt_parts.append(structured_guide)
        final_llm_prompt = "\n".join(prompt_parts)
        negative_prompt = preset["negative_base"][lang] if enable_negative_prompt else ""
        return {
            "status": "success",
            "llm_input_prompt": final_llm_prompt,
            "positive_constraint": pos_constraint,
            "negative_prompt": negative_prompt,
            "output_language": lang,
            "downstream_model": downstream_model,
            "preset_name": preset_name,
            "preset_display_name": preset["display_name"],
            "user_raw_input": user_input,
            "enable_preconstraint": enable_global_preconstraint,
            "enable_negative": enable_negative_prompt
        }
