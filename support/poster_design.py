# -*- coding: utf-8 -*-
"""
海报设计预设模块

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

POSTER_DESIGN = {
    "template_id": "poster_design",
    "name": "海报设计",
    "description": "专业海报设计指导，为商业、电影、活动、包装打造高可控视觉叙事描述。语义权重优先级：主题目标情感→风格类型调性→三维视角构图→色彩配比→主视觉质感→文字层级。内置三维度视角、70%/25%/5%色彩配比、双重质感约束与画面精简约束，强化构图叙事、文字层级、材质质感与电影级镜头语言。覆盖现代极简、国潮、电影感、复古等风格赛道，支持人物与静物海报双赛道适配。",
}

class PosterDesign:
    def __init__(self):
        # 下游生图模型内容组织公式库
        self.model_formula_library = {
            "Flux1": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体海报主题情感光影 → 主视觉主体造型 → 材质印刷质感 → 文字留白区域。侧重海报信息叙事，弱化细碎关键词堆砌，画面商业高级。",
                "formula_en": "Content order: overall poster theme emotion lighting → main visual subject shape → printing texture → text blank area. Focus on poster information narration."
            },
            "Flux2_klein": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：海报主题风格定位 → 光影色彩层次 → 主视觉材质细节 → 克制文字区域。平衡视觉主体与文字信息，光影过渡贴合海报镜头逻辑。",
                "formula_en": "Content order: poster theme style positioning → light color layers → main visual texture details → restrained text area. Balance subject and text information."
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：主视觉材质肌理优先 → 画面透视构图 → 三维镜头视角 → 全局分层布光 → 极简文字区。精准把控海报透视比例，统一国潮/电影/商业海报质感标准。",
                "formula_en": "Content order: main visual texture details first → picture perspective composition → 3D lens view → global layered lighting → minimalist text zone. Strictly control poster perspective ratio."
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：构图视觉核心主体 → 主体动态情绪 → 70/25/5色彩管控 → 光影明暗层次 → 干净文字留白。构图规整克制，色彩层级清晰，镜头虚实过渡自然柔和。",
                "formula_en": "Content order: composition core subject → subject movement emotion → 70/25/5 color control → light shadow layers → clean text blank. Neat composition, natural depth of field transition."
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：全局电影光影基调 → 主体情绪表达 → 印刷材质细节 → 字体面料肌理 → 极简文字布景。强化镜头叙事，区分电影/国潮/商业专属光影体系。",
                "formula_en": "Content order: global cinematic light tone → subject emotion expression → printing texture details → font fabric texture → minimalist text set. Strengthen lens narration logic."
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整张海报基础风格基调 → 舒展主体造型 → 统一印刷质感 → 简约文字留白。极简海报叙事，删减冗余装饰，突出视觉与文字核心。",
                "formula_en": "Content order: whole poster basic tone → relaxed subject shape → unified printing texture → simple text blank. Minimal poster narration, remove redundant ornaments."
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：画面透视主视觉肌理 → 远近虚实层次 → 光影冷暖过渡 → 字体层级细节 → 轻量化留白。海报透视精准，材质区分清晰，光影连贯柔和。",
                "formula_en": "Content order: perspective main visual texture → near-far layers → light warm-cold transition → font hierarchy details → lightweight blank. Accurate poster perspective."
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：海报整体主题气质 → 主视觉材质细节 → 专业分层布光 → 专属字体排版 → 极简留白。整体色调统一，信息层级细腻，海报沉浸叙事强烈。",
                "formula_en": "Content order: overall poster temperament → main visual texture details → professional layered lighting → exclusive font layout → minimalist blank. Unified tone, delicate information hierarchy."
            }
        }
        # 全局底层规则
        self.global_base_rules = {
            "zh": """
你是专业全品类海报设计提示词扩写专家，覆盖商业广告、电影、文化活动、礼盒包装、国潮复古全海报题材，分人物/静物双赛道。
所有创作坚守海报信息叙事基线，仅主题情感、画风、镜头、文字排版差异化，禁止多风格混搭割裂画面。
画面遵循主体70%、环境文字30分配，色彩严格70主/25辅/5点缀配比；文字作为设计元素，层级清晰不遮挡主视觉。
光影匹配电影镜头逻辑，区分电影悬疑/国潮暖光/商业柔光质感；纸质、布料、金属、烫金等印刷肌理贴合海报风格。
完整保留用户输入海报类型、画幅、视角、主视觉、文字信息，仅补充镜头、材质、字体、纹样专业细节，不自动新增无关装饰杂物。
画面执行精简约束，仅留存叙事与信息核心元素，文字克制不拥挤堆砌。
输出禁忌：禁止权重符号、分辨率/字号/DPI等数值参数堆砌；禁止画风混乱、透视扭曲、塑料虚假质感；禁止字幕水印logo、完美对称、零瑕疵描述。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional full-category poster prompt expert, covering commercial ads, films, cultural events, gift packaging, guochao vintage posters, character & object dual tracks.
All creations follow poster information narration baseline, differentiated by theme, painting style, lens and text layout, no mixed styles.
70% main subject, 30% background & text ratio, fixed 70/25/5 color ratio; text acts as design element with clear hierarchy without covering subject.
Light complies with cinematic lens rules, distinguish suspense/guochao/commercial light; paper, fabric, metal, hot stamping printing texture match poster style.
Fully retain user input poster type, frame, view, subject, text info, only add lens, texture, font, pattern details without clutter.
Strict simplification rule, only keep core narrative & info elements, avoid crowded text.
Taboo: no weight symbols, numeric params like resolution/font size/DPI; no chaotic styles, distorted perspective, fake plastic texture; no watermark/logo, perfect symmetry, flawless description.
Strictly output two formats without extra comments.
"""
        }
        # 唯一主预设模板，绑定原有POSTER_DESIGN模板id
        self.preset_library = {
            "poster_design": {
                "template_id": "poster_design",
                "display_name": POSTER_DESIGN["name"],
                "description": POSTER_DESIGN["description"],
                # 中英双语固定前置正向约束
                "positive_constraints": {
                    "zh": "海报风格统一连贯，构图叙事逻辑严谨，70/25/5色彩配比和谐分层，主视觉材质印刷质感真实，镜头透视精准无畸变；文字层级清晰有序，字体与画面自然融合不突兀；电影海报具备镜头张力，国潮传统纹样与现代排版自然融合，商业海报印刷细腻无过度锐化；光影冷暖过渡柔和，画面干净聚焦主体，仅保留核心叙事信息元素，留白参与视觉节奏，兼具信息传递力与画面艺术质感",
                    "en": "Unified poster style, rigorous composition logic, harmonious 70/25/5 color layers, authentic printing texture, accurate lens perspective; clear text hierarchy, fonts blend naturally with frame; movie posters own lens tension, guochao combines traditional patterns & modern layout, commercial print delicate without over-sharpening; soft light transition, clean subject-focused frame, blank space adjusts visual rhythm, balance info delivery & artistic texture."
                },
                # 全风格细分专属规则
                "preset_rules": {
                    "zh": """
【全海报专属细分规则】
1. 通用基线：语义权重：主题目标情感→风格调性→三维构图→色彩配比→主视觉→文字层级；用户画幅视角优先，无则选合规镜头；70/25/5色彩，精简约束；禁用["8K", "4K", "分辨率", "DPI", "色彩模式", "字号", "尺寸", "帧率", "码率", "采样率", "编码器", "HDR", "杜比", "字幕", "水印", "logo", "完美对称", "零瑕疵", "塑料感", "崩坏", "扭曲"]。
2. 现代极简商业海报：柔和漫射柔光，干净平涂/摄影质感，纤细无衬线字体，低饱和纯色背景，文字克制少，留白充足，产品/人物居中。
3. 国潮活动海报：书法标题、传统祥云缠枝纹样，红金米主色调，工笔/平涂结合，书法字体搭配简约信息字，大面积国风留白。
4. 电影悬疑海报：低角度仰拍镜头，高对比冷调光影，粗体风化标题，大面积云层/暗背景，文字极简退让不抢主体。
5. 复古胶片海报：暖褪色颗粒肌理，粗衬线复古字体，柔和黄昏柔光，低饱和旧色调，年代装饰元素克制点缀。
6. 礼盒包装海报：细腻哑光纸质，柔和漫射光，纤细精致字体，低饱和高级配色，静物产品居中，少量烫金点缀。
所有题材：用户原始需求优先级最高，仅补充镜头、材质、字体、纹样专业细节，不改动海报主题与核心排版。
""",
                    "en": """
【Universal Poster Exclusive Rules】
1. General baseline: Weight order: theme emotion > style tone > 3D composition > color ratio > main visual > text hierarchy; user frame view priority; fixed color ratio & simplification rule; forbidden words list: 8K,4K,resolution,DPI,color mode,font size,size,frame rate,bit rate,sampling rate,encoder,HDR,dolby,subtitle,watermark,logo,perfect symmetry,flawless,plastic texture,collapse,distort.
2. Minimal commercial poster: soft diffuse light, flat/photoreal texture, thin sans-serif font, low saturation solid background, sufficient blank space.
3. Guochao event poster: calligraphy headline, traditional cloud patterns, red-gold palette, meticulous flat mix, calligraphy + simple info fonts, chinese blank layout.
4. Suspense movie poster: low-angle lens, high contrast cool light, rough weathered bold font, large dark background, minimal text.
5. Vintage film poster: faded grain texture, vintage serif font, warm dusk soft light, low saturation retro tone, restrained vintage ornaments.
6. Gift package poster: matte paper texture, soft diffuse light, delicate thin font, low saturation premium palette, centered product, subtle hot stamping accents.
All themes: User demand highest priority, only add lens/texture/font/pattern details without altering core layout.
"""
                },
                "negative_base": {
                    "zh": "多种风格混乱混搭，色彩脏污溢出，构图失衡主体偏移，装饰杂物冗余堆砌，文字排版拥挤层级混乱，字体风格冲突，透视错误，塑料虚假印刷质感，光影生硬断层，边缘锯齿过度锐化，字幕水印logo，高饱和杂乱撞色，人物神态僵硬，国潮元素生硬拼贴，画面无留白节奏，信息杂乱抢夺视觉焦点",
                    "en": "Mixed chaotic styles, muddy overflow color, unbalanced composition, stacked clutter, crowded messy text, conflicting fonts, wrong perspective, fake plastic print texture, stiff disjoint light, jagged over-sharpening, watermark/logo, messy saturated color, stiff character expressions, forced guochao elements, no blank rhythm, distracting cluttered info."
                }
            }
        }
        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】2-3段连贯文字：首段海报画幅构图、整体风格与情绪基调；第二段主视觉镜头、材质光影与色彩分层；第三段字体排版、信息层级与留白节奏；总字数300-600，规避字号/分辨率等数字参数，设计叙事语言无额外解释。",
                "en": "[Natural Paragraph Mode] 2-3 coherent paragraphs: poster frame composition & overall tone; main visual lens texture & color layers; font layout info hierarchy & blank rhythm; 300-600 words, no numeric print params, design narration without extra notes."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1.海报品类、设计风格与全局正向约束
2.画面构图、视觉引导、主体70%占比、画幅比例、精简约束
3.三维镜头：景别距离、水平朝向、垂直俯仰、景深虚实
4.核心主视觉：人物/产品形态、神态、专属质感
5.多层文字：主标题/副标题/辅助信息、字体风格、画面融合关系
6.材质肌理、光源方向、冷暖光影层次
7.70/25/5色彩分层饱和度调性
8.国潮/复古专属传统纹样、年代装饰元素
9.留白区域功能与画面疏密节奏
10.印刷质感定性建议、全局禁止参数清单
11.3-5个概括海报气质风格标签""",
                "en": """[Structured Mode] Output strictly in this order:
1. Poster category, design style & global positive constraints
2. Frame composition, visual guide, 70% subject ratio, aspect ratio, simplification rule
3. 3D lens: shot distance, horizontal angle, vertical pitch, depth blur
4. Core main visual: character/product shape, expression, exclusive texture
5. Multi-layer text: headline/sub/info, font style, blend with frame
6. Print texture, light source, warm-cold light layers
7. 70/25/5 layered color saturation tone
8. Guochao/vintage exclusive patterns & vintage ornaments
9. Blank area function & frame density rhythm
10. Qualitative print texture suggestion, forbidden param list
11. 3-5 style tags summarizing poster temperament"""
            }
        }

    def detect_language(self, text: str):
        import re
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        return "zh" if chinese_chars >= english_words else "en"

    def build_prompt(
        self,
        user_input,
        preset_name,
        downstream_model,
        output_language="auto",
        enable_global_preconstraint=True,
        enable_negative_prompt=True,
        output_format="both"
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
