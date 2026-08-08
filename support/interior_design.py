# -*- coding: utf-8 -*-
"""
室内设计预设模块

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

INTERIOR_DESIGN = {
    "template_id": "interior_design",
    "name": "室内设计",
    "description": "专业室内设计指导，为全品类居住与公共空间打造标准化、高可控的空间叙事描述。语义权重优先级：空间类型与风格基调＞视角构图＞硬装软装＞灯光色彩＞人文细节。内置三维度视角、70%/25%/5%色彩配比、双重质感约束与画面精简约束，强化硬装基底、软装层次、灯光叙事与生活温度。",
}

class InteriorDesign:
    def __init__(self):
        # 下游生图模型内容组织公式库
        self.model_formula_library = {
            "Flux1": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体室内空间基调灯光 → 硬装软装整体布局 → 材质肌理软装细节 → 留白过渡区域。侧重居家氛围叙事，弱化细碎关键词堆砌，空间温润高级。",
                "formula_en": "Content order: overall interior tone & lighting → hard & soft decoration layout → texture and furnishing details → blank transition area. Focus on home atmosphere narration."
            },
            "Flux2_klein": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：室内风格与空间类型 → 灯光明暗层次 → 硬装软装材质肌理 → 克制留白区域。平衡材质触感细节与居家氛围感，光影过渡贴合室内物理照明逻辑。",
                "formula_en": "Content order: interior style & space type → light shadow layers → hard/soft decoration texture → restrained blank area. Balance texture tactile details and home atmosphere."
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：墙面地面天花材质细节优先 → 室内空间透视轮廓 → 三维人视视角构图 → 全屋分层布光 → 极简留白。精准把控室内透视比例，统一各类家装材质标准。",
                "formula_en": "Content order: wall/floor/ceiling texture details first → interior perspective contour → 3D human view composition → whole layered lighting → minimalist blank. Strictly control indoor perspective, unify home texture standards."
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：构图视觉核心区域 → 空间动线家具排布 → 70/25/5色彩管控 → 多层照明光影层次 → 干净过渡留白。构图规整克制，色彩层级清晰，室内透视自然柔和。",
                "formula_en": "Content order: composition core area → space circulation & furniture layout → 70/25/5 color control → multi-layer lighting → clean blank. Neat composition, clear color layers, natural indoor perspective."
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：全屋整体灯光氛围基调 → 空间尺度与人居动线 → 硬装软装材质细节 → 布艺木质面料肌理 → 极简边角布景。强化灯光情绪叙事，区分各类家装专属照明方案。",
                "formula_en": "Content order: whole space lighting tone → space scale & circulation → hard/soft decoration details → fabric wood texture → minimalist edge set. Strengthen emotional light narration, distinguish exclusive lighting for home styles."
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：全屋基础风格基调 → 舒展流畅室内动线 → 统一全屋材质质感 → 简约留白边角。极简居家叙事，删减冗余摆件装饰，突出空间生活核心。",
                "formula_en": "Content order: whole space basic tone → smooth circulation → unified full-space texture → simple edge blank. Minimal home narration, remove redundant ornaments, highlight living core."
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：硬装材质与空间透视 → 远近家具层次 → 多层照明明暗过渡 → 软装人文细节 → 轻量化留白。强化室内透视精准度，材质触感区分清晰，灯光层次柔和连贯。",
                "formula_en": "Content order: hard decoration & perspective → near-furniture layers → multi-light transition → soft furnishing human details → lightweight blank. Accurate indoor perspective, distinct tactile textures, soft continuous lighting layers."
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：室内整体风格气质 → 硬装软装材质细节 → 全屋分层专业布光 → 风格专属家具软装 → 极简留白。全屋色调统一协调，空间人文细节细腻，居家沉浸感强烈。",
                "formula_en": "Content order: overall interior temperament → hard/soft texture details → whole layered professional lighting → style exclusive furniture → minimalist blank. Unified space tone, delicate human details, strong immersive home sense."
            }
        }
        # 全局底层规则
        self.global_base_rules = {
            "zh": """
你是专业全品类室内设计提示词扩写专家，覆盖客厅、卧室、茶室、厨房、办公等居住/公共全空间，包含奶油、新中式、日式、现代、轻奢、中古等全部家装风格。
所有创作坚守室内人居叙事基线，仅空间类型、家装风格、灯光色调、家具布局差异化，禁止混搭多种风格造成空间割裂。
空间遵循完整硬装体系（墙/地/顶），家具排布形成流畅人行动线；色彩固定70主/25辅/5点缀配比，无杂乱高饱和撞色堆砌。
灯光分层设计：基础照明、重点照明、氛围照明，色温匹配空间功能，光影过渡符合室内自然光与人造光物理逻辑。
硬装软装材质区分清晰，木质、布艺、石材、微水泥、硅藻泥等肌理贴合对应家装风格，触感与视觉表现统一。
完整保留用户输入的空间类型、家装风格、视角景别、家具、灯光色调全部信息，仅补充材质、照明、透视、人文摆件专业细节，不自动新增多余杂物、无效装饰。
画面执行严格精简约束，仅保留功能与叙事核心摆件，人物动线舒适自然。
输出禁忌：禁止权重符号、尺寸/分辨率/DPI/坐标等数值技术参数堆砌；禁止风格混乱、透视扭曲、塑料虚假材质、摆件堆砌；禁止字幕水印logo、完美对称、零瑕疵等违规描述。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional full-category interior design prompt expert, covering living room, bedroom, tea room, kitchen, office and other residential/public spaces, including cream, neo-chinese, japanese, modern, light luxury, vintage home styles.
All creations follow indoor living narrative baseline, differentiated only by space type, home style, lighting tone and furniture layout, no mixed styles causing space fragmentation.
Complete hard decoration system (wall/floor/ceiling), furniture layout forms smooth human circulation; fixed 70 main /25 secondary /5 accent color ratio, no messy oversaturated color collision.
Layered lighting design: ambient, task, accent lighting, color temperature matches space function, light transition complies with indoor natural & artificial light physical logic.
Distinct hard & soft decoration textures, wood, fabric, stone, micro-cement, diatom mud fit matching home styles, unified tactile and visual performance.
Fully retain all user input info including space type, home style, view shot, furniture, lighting tone, only supplement texture, lighting, perspective, human ornament details without redundant clutter.
Strict frame simplification rule, only keep functional & core narrative ornaments, comfortable human circulation.
Taboo: no weight symbols, stacked numeric technical parameters such as size/resolution/DPI/coordinate; no chaotic styles, distorted perspective, fake plastic texture, piled ornaments; no subtitles watermarks logos, perfect symmetry, flawless description.
Strictly output two formats without extra comments.
"""
        }
        # 唯一主预设模板，绑定原有INTERIOR_DESIGN模板id
        self.preset_library = {
            "interior_design": {
                "template_id": "interior_design",
                "display_name": INTERIOR_DESIGN["name"],
                "description": INTERIOR_DESIGN["description"],
                # 中英双语固定前置正向约束
                "positive_constraints": {
                    "zh": "家装风格统一稳定，室内空间逻辑通顺合理，各类材质肌理真实自然，多层灯光层次分明，色彩配比合规和谐，空间透视比例精准，画面干净克制精简，仅留存核心硬装、功能家具与人文摆件；全屋硬装基底完整扎实，软装搭配协调舒适，灯光色温贴合空间功能、烘托情绪，家具排布动线流畅自然；不同家装风格保留专属材质与设计语言，整体空间兼具审美质感与生活化温度，通透自然富有呼吸感",
                    "en": "Stable unified home style, reasonable indoor spatial logic, authentic all kinds of texture, distinct multi-layer lighting, compliant harmonious color ratio, precise space perspective proportion, clean restrained frame, only core hard decoration, functional furniture & human ornaments retained; complete solid whole-house hard decoration, coordinated comfortable soft furnishing, lighting color temperature matches space function & sets mood, smooth circulation from furniture layout; each home style retains exclusive texture & design language, space owns both aesthetic texture and living warmth, transparent natural breathable sense."
                },
                # 全风格细分专属规则
                "preset_rules": {
                    "zh": """
【全风格室内专属细分规则】
1. 通用基线：遵循语义权重顺序：空间类型与风格基调＞视角构图＞硬装软装＞灯光色彩＞人文细节；三维人视视角优先沿用用户指定，无指定选取室内舒适合规角度；严格执行70%/25%/5%色彩配比，画面精简约束；禁用["8K", "4K", "分辨率", "DPI", "色彩模式", "尺寸", "坐标", "渲染参数", "帧率", "码率", "采样率", "编码器", "HDR", "杜比", "字幕", "水印", "logo", "完美对称", "零瑕疵", "塑料感", "崩坏", "扭曲"]。
2. 现代奶油风：微水泥、艺术涂料、原木亚麻柔和材质，无主灯漫射柔光，低饱和暖米色系，软装圆润柔和，绿植陶土小件点缀，动线开阔松弛。
3. 新中式茶室/居室：胡桃实木、微水泥、和纸材质，对称均衡布局，暖黄纸灯自然光结合，低饱和木灰主色，水墨、枯植、铜器人文摆件，东方禅意氛围。
4. 日式空间：榻榻米、硅藻泥、棉麻原木素净材质，无主灯带漫射光，低饱和米稻草色系，极简软装，书法、青苔、手工陶制小件，朴素安静。
5. 现代极简原木：实木地板、乳胶漆、棉麻布艺，主次灯分层中性自然光，干净低饱和木白配色，少量绿植装饰，家具线条利落，留白充足。
6. 轻奢风格：大理石、金属细框、丝绒软装，重点射灯+主灯高通透照明，低饱和浅灰金配色，玻璃、金属精致摆件，高级精致。
7. 中古复古：做旧实木、丝绒、复古瓷砖，暖黄复古落地台灯，暖棕复古主色调，复古画册、老式陶器、绿植，复古慵懒氛围。
所有题材：用户指定内容优先级最高，仅补充硬装、灯光、材质、人文摆件专业细节，不篡改空间类型、家装风格与核心布局。
""",
                    "en": """
【Universal Interior Exclusive Rules】
1. General baseline: Follow semantic weight order: space type & style tone > view composition > hard & soft decoration > lighting color > human details; user-specified human view takes priority, select comfortable indoor angle if unspecified; strictly implement 70%/25%/5% color ratio, frame simplification rule; forbidden words list: 8K,4K,resolution,DPI,color mode,size,coordinate,render parameter,frame rate,bit rate,sampling rate,encoder,HDR,dolby,subtitle,watermark,logo,perfect symmetry,flawless,plastic texture,collapse,distort.
2. Modern cream style: micro-cement, art coating, soft linen log texture, diffuse no-main lamp soft light, low saturation warm cream tone, round soft furnishing, green plant clay ornaments, open relaxed circulation.
3. Neo-Chinese tea room/living space: walnut solid wood, micro-cement, washi texture, symmetrical layout, warm paper lamp plus natural light, low saturation wood-gray main color, ink painting withered plant bronze ornaments, oriental zen atmosphere.
4. Japanese space: tatami, diatom mud, linen log plain texture, no-main lamp strip diffuse light, low saturation rice straw tone, minimalist furnishing, calligraphy moss handmade pottery, plain quiet vibe.
5. Modern minimalist log: solid wood floor, latex paint, cotton linen fabric, neutral natural light with main & auxiliary lamp layers, clean low saturation wood-white color, few green plants, neat furniture lines, ample blank space.
6. Light luxury style: marble, thin metal frame, velvet furnishing, spot task lamp + main high-transparency lighting, low saturation light gray gold color, glass metal delicate ornaments, advanced exquisite sense.
7. Vintage mid-century: aged solid wood, velvet, retro tile, warm vintage floor lamp, warm brown retro main tone, old albums vintage pottery green plants, lazy retro atmosphere.
All themes: User-specified content highest priority, only supplement hard decoration, lighting, texture, human ornament details without altering space type, home style and core layout.
"""
                },
                "negative_base": {
                    "zh": "家装风格混乱跳变，材质虚假塑料质感，灯光刺眼曝光失衡，色彩脏污溢出，构图失衡杂乱，家具摆件冗余堆砌，室内透视逻辑错误，空间比例变形，画面低分辨率模糊，多余杂物乱入，装饰摆件杂乱堆砌，字幕水印logo，光影生硬断层，空间闭塞压抑，家具动线拥堵混乱，过度锐化生硬，家具边缘锯齿，家具比例失调，墙地拼接错误，装饰毫无章法，廉价网红质感",
                    "en": "Chaotic mixed home styles, fake plastic texture, dazzling overexposed lighting, muddy overflowing color, unbalanced cluttered composition, redundant piled furniture ornaments, wrong indoor perspective logic, distorted space proportion, blurry low-res frame, irrelevant clutter, stacked messy decorations, subtitles watermarks logos, stiff disjointed lighting, cramped closed space, blocked messy furniture circulation, over-sharpened rigid texture, jagged furniture edges, disproportionate furniture, wrong wall-floor splicing, disordered decorations, cheap internet celebrity texture"
                }
            }
        }
        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】2-3段连贯文字：第一段全屋空间格局与整体家装风格；第二段硬装墙地顶材质与分层灯光设计；第三段软装家具排布、人文摆件与整体色彩意境；总字数300-600字，全程规避尺寸、坐标等数值参数，语言居家叙事富有画面感，无额外解释。",
                "en": "[Natural Paragraph Mode] 2-3 coherent paragraphs: whole space layout & home style; wall/floor/ceiling hard texture & layered lighting; furniture layout human ornaments & overall color artistic conception; 300-600 words, avoid size/coordinate numeric parameters, home narrative visual language without extra explanation."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1.室内空间类型与全局家装正向约束
2.画面构图、视觉引导、核心区域占比、画幅比例、精简约束
3.三维人视景别视角：远近距离、水平朝向、垂直俯仰、景深虚实
4.硬装完整体系：墙面材质、地面肌理、天花造型处理
5.软装家具布局、动线走向、布艺配饰搭配
6.照明整体方案、三层光源、色温空间氛围
7.70/25/5色彩配比、全屋材质触感搭配
8.墙面艺术、绿植、摆件人文细节
9.色温质感补充、全局禁止参数项
10.3-5个概括家装气质风格标签""",
                "en": """[Structured Mode] Output strictly in this order:
1. Indoor space type & global home positive constraints
2. Frame composition, visual guide, core area proportion, aspect ratio, simplification rule
3. 3D human shot view: distance, horizontal orientation, vertical pitch, depth of field blur
4. Complete hard decoration system: wall texture, floor grain, ceiling molding
5. Soft furniture layout, circulation trend, fabric matching
6. Whole lighting scheme, three-layer light source, color temperature space mood
7. 70/25/5 color ratio, full-space tactile texture matching
8. Wall art, green plants, ornament human details
9. Color temperature texture supplement, global forbidden numeric parameters
10. 3-5 style tags summarizing home temperament"""
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
