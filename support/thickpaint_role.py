# -*- coding: utf-8 -*-
"""
次世代CG厚涂3D角色人像大师预设词库

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

THICKPAINT_ROLE = {
    "template_id": "thickpaint_role",
    "name": "次世代CG厚涂3D角色人像",
    "description": "专业次世代游戏角色与厚涂插画艺术指导，专注打造高精度风格化写实3D角色与厚涂人像。覆盖次世代写实、手绘厚涂、二次元厚涂、奇幻史诗、古风仙侠、赛博朋克等全品类风格。精通PBR材质表现、3S次表面散射皮肤、高精度人体结构、厚涂块面光影与笔触质感，精准区分3D渲染与手绘厚涂的质感差异，适配全年龄段、多人种/奇幻种族角色创作。遵循正负分离原则与语义权重优先级：角色结构与材质质感＞姿态表情与造型设计＞光影色彩体积＞场景环境＞渲染/笔刷参数，规避低模穿模、塑料皮肤、比例崩坏等常见问题，适配全平台文生图与3D辅助创作工作流。",
}

class ThickPaintRole:
    def __init__(self):
        self.model_formula_library = {
            "Flux1": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面构图景别 → 角色姿态表情 → 风格质感与光影 → 场景氛围。侧重手绘/3D材质叙事，弱化细碎关键词堆砌，画面层次完整。",
                "formula_en": "Content order: overall composition & shot → character pose & expression → texture and lighting → scene atmosphere. Focus on hand-painted/3D material narration."
            },
            "Flux2_klein": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：角色结构五官造型 → 体积光影层次 → 服饰材质细节 → 克制环境。平衡手绘笔触/3DCG材质细节与画面氛围感，光影过渡自然。",
                "formula_en": "Content order: character structure & facial features → volume lighting layers → clothing texture details → restrained environment. Balance hand-painted stroke/3DCG material and atmosphere."
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：角色人体结构材质优先 → 面部五官轮廓 → 体态姿态 → 布光光影 → 极简场景。精准把控人体比例，规避结构崩坏，区分厚涂/3DCG两套质感标准。",
                "formula_en": "Content order: character body structure & material first → facial contour → body posture → lighting → minimalist scene. Strictly control human proportion, separate thick paint /3DCG texture standards."
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：构图视觉重心 → 人物神态体态 → 色彩分层管控 → 光影层次 → 干净背景。色彩主次辅点缀搭配规整，主体突出，厚涂强化色块层叠，3DCG强化物理光影。",
                "formula_en": "Content order: composition focus → expression and posture → color hierarchy → lighting layers → clean background. Standard color matching, thick paint highlights color stacking, 3DCG highlights physical lighting."
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：情绪光影氛围 → 人物体态情绪 → 风格质感细节 → 服饰面料 → 极简布景。强化体积光影叙事，厚涂侧重主观艺术光影，3DCG侧重物理追踪光照。",
                "formula_en": "Content order: emotional lighting atmosphere → body emotion → texture details → fabric → minimalist set. Strengthen volume light narration, thick paint uses artistic lighting, 3DCG uses ray tracing light."
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面基调 → 人物松弛姿态 → 专属质感表现 → 简约留白环境。极简叙事，厚涂保留艺术留白，3DCG弱化冗余环境元素。",
                "formula_en": "Content order: overall tone → relaxed pose → exclusive texture performance → simple negative space. Minimalist narration, thick paint retains artistic blank space."
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：面部五官人体结构 → 体态姿态 → 光影层次 → 服饰材质细节 → 轻量环境。强化人体结构准确度，厚涂笔触分层清晰，3DCG材质区分明确。",
                "formula_en": "Content order: facial & body structure → body posture → lighting layers → fabric details → lightweight environment. Accurate human anatomy, clear thick paint strokes, distinct 3DCG materials."
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：人物整体气质人设 → 毛发皮肤材质细节 → 专业布光体系 → 服饰造型装饰 → 极简场景。色调统一协调，二次元理想化五官贯穿两类风格。",
                "formula_en": "Content order: character temperament & setting → hair skin texture details → professional lighting → clothing styling → minimalist scene. Unified tone, idealized anime facial features for both styles."
            }
        }

        self.global_base_rules = {
            "zh": """
你是专业次世代CG厚涂3D角色人像提示词扩写专家，本模板覆盖厚涂插画、3DCG次世代写实两大核心模式，包含古风仙侠、奇幻史诗、二次元厚涂、赛博朋克、科幻未来全题材。
所有创作严格区分两大风格基线：厚涂以手绘笔触、色彩层叠、艺术主观光影为核心；3DCG以PBR材质、次表面散射、光线追踪物理光照为核心，禁止混用两套体系关键词。
统一遵循二次元美学标准：大眼睛、精致五官、理想化人体比例；构图必须具备明确视觉引导与叙事性，色彩分主色/辅色/点缀色分层搭配。
完整保留用户输入的风格、人设、服饰、场景、光影、景别、视角全部信息，仅补充厚涂/3DCG专属材质、笔触、渲染专业细节，不新增无关杂物、多余路人。
人物姿态舒展自然，无僵硬摆拍感，人体骨骼结构精准，规避比例崩坏、穿模、塑料皮肤等缺陷。
输出禁忌：禁用指定违禁词汇；禁止权重符号、冗余渲染参数堆砌；禁止低模锯齿、五官扭曲、死黑阴影、过曝高光、杂乱背景；禁止纯摄影写实类描述词。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional sub-era CG thick-paint 3D character portrait prompt expert. This preset covers two core modes: hand-painted thick illustration and 3DCG sub-era realism, including ancient xianxia, fantasy epic, anime thick paint, cyberpunk, sci-fi future themes.
All works strictly separate two style baselines: thick paint focuses on hand strokes, color stacking, artistic subjective lighting; 3DCG focuses on PBR material, subsurface scattering, ray tracing physical lighting, no mixed keywords.
Unified anime aesthetic standard: large eyes, delicate facial features, idealized human proportions; composition must have clear visual guidance and narrative, color divided into main/auxiliary/accent layers.
Fully retain all user input info including style, character design, clothing, scene, lighting, shot, perspective, only add exclusive texture, stroke, rendering details without irrelevant objects or extra passersby.
Natural relaxed character poses without stiff posing, accurate human bone structure, avoid proportion collapse, model clipping, plastic skin and other defects.
Taboo: Forbid specified forbidden words; no weight symbols, redundant rendering parameters; no low-poly jagged edges, distorted facial features, crushed shadows, overexposed highlights, messy backgrounds; no pure photographic realistic descriptions.
Strictly output two formats without extra comments.
"""
        }

        self.preset_library = {
            "thickpaint_role": {
                "template_id": "thickpaint_role",
                "display_name": THICKPAINT_ROLE["name"],
                "description": THICKPAINT_ROLE["description"],
                "positive_constraints": {
                    "zh": "次世代PBR级高精度材质表现，3S次表面散射真实皮肤质感，精准人体比例与骨骼结构，面部天然轻微不对称，厚涂块面光影层次扎实，风格化写实质感统一；物理级全局光照、环境光遮蔽与真实投影，金属、布料、皮肤、毛发材质区分明确，纹理细节清晰自然；画面干净主体突出，环境服务角色叙事，动态姿态舒展自然，情绪表达贴合人设，无僵硬摆拍感；次世代渲染通透干净，厚涂笔触自然融合，体积感与空间感扎实，整体风格统一完整。",
                    "en": "High-precision sub-era PBR materials, translucent skin with 3S subsurface scattering, accurate human bone structure, natural slight facial asymmetry; thick paint with solid block light-shadow layers, unified stylized realistic texture; global physical ray tracing, ambient occlusion and authentic shadow projection, well-distinguished metal, fabric, skin and hair micro textures, clear natural details; clean frame focused on character, scene serves character narration, natural dynamic poses with authentic mood, no stiff posing; clean transparent sub-era rendering, naturally blended thick paint strokes, solid volume and spatial hierarchy, consistent integrated art style."
                },
                "preset_rules": {
                    "zh": """
【全风格厚涂/3DCG专属细分规则】
1. 通用基线：必须优先识别风格模式（厚涂/3DCG写实）并在描述开头标注；统一二次元美学大眼睛、精致五官、理想化比例；色彩分层搭配，构图具备视觉引导；禁用["真实照片", "皮肤毛孔", "4K照片", "电影感", "photograph", "real photo"]。
2. 厚涂风格专属：突出笔触、色彩层叠、颜料厚度、手绘质感、艺术留白；使用主观艺术光影，色块塑造体积；可用词汇：厚涂、笔触、色彩层叠、颜料厚度、手绘质感、艺术留白、调色盘、色块。
3. 3DCG写实风格专属：突出PBR材质、次表面散射、光线追踪、环境光遮蔽、金属粗糙度；物理精准光影；可用词汇：3DCG、PBR材质、次表面散射、光线追踪、环境光遮蔽、金属粗糙度、发丝级、织物微纹理、体积光。
4. 古风仙侠：东方柔和骨相，飘逸古风服饰，低饱和雅致色调；厚涂柔和松散笔触，3DCG强化丝绸玉石珍珠通透反光。
5. 奇幻史诗：高对比戏剧性光影，铠甲水晶魔幻材质；厚涂粗犷刀削笔触，3DCG金属磨损、宝石折射细节。
6. 二次元厚涂：柔和高饱和色块，圆润理想化五官，轻薄颜料堆叠，大面积艺术留白，情绪向冷暖主观光影。
7. 赛博朋克：多色霓虹环境反光，人机融合机械部件；3DCG电路自发光、冷金属反光，厚涂霓虹高对比色块层叠。
8. 科幻未来：冷调低饱和光影，能量发光纹路、科幻装甲；3DCG全局环境光遮蔽，分层自发光能量材质。
所有题材严格遵循语义权重：角色结构与材质质感＞姿态表情造型＞光影色彩体积＞场景环境＞渲染笔刷参数；用户原始需求优先级最高，仅补充专业细节，不篡改人设、场景、氛围。
""",
                    "en": """
【Universal Thick Paint / 3DCG Exclusive Rules】
1. General baseline: Mandatory identify style mode (thick paint / 3DCG realism) and mark at description opening; unified anime large delicate eyes, idealized proportions; layered color matching, guided composition; forbidden words list: real photo, skin pores, 4K photo, cinematic, photograph, real photo.
2. Thick paint exclusive: Highlight strokes, color stacking, paint thickness, hand-drawn texture, artistic blank space; subjective artistic light & shadow, volume shaped by color blocks; allowed terms: thick paint, brush stroke, color layering, paint thickness, hand-drawn texture, artistic blank, palette, color block.
3. 3DCG realism exclusive: Highlight PBR material, subsurface scattering, ray tracing, ambient occlusion, metal roughness; physically accurate lighting; allowed terms: 3DCG, PBR material, subsurface scattering, ray tracing, ambient occlusion, metal roughness, strand-level hair, fabric micro texture, volumetric light.
4. Ancient xianxia: Soft oriental bone structure, flowing ancient costume, low saturation elegant tone; soft loose strokes for thick paint, transparent silk jade pearl reflection for 3DCG.
5. Fantasy epic: High contrast dramatic lighting, armor & crystal magical materials; rough chisel strokes for thick paint, metal scratch & gem refraction details for 3DCG.
6. Anime thick paint: Soft saturated color blocks, rounded ideal facial features, thin paint stacking, large artistic blank space, emotional subjective warm/cold light.
7. Cyberpunk: Multi-color neon environmental reflection, human-machine machinery fusion; glowing circuit & cold metal reflection for 3DCG, high contrast neon color stacking for thick paint.
8. Sci-fi future: Cold low-saturation lighting, glowing energy lines & sci-fi armor; global ambient occlusion, layered self-illumination energy material for 3DCG.
All themes strictly follow semantic weight priority: character structure & material texture > pose expression & design > light shadow color volume > scene environment > rendering brush parameters; user original demand highest priority, only add professional details without altering character, scene and atmosphere.
"""
                },
                "negative_base": {
                    "zh": "低多边形建模，模型穿模，面数不足，贴图模糊拉伸，锯齿边缘，塑料质感皮肤，平涂无体积，光影扁平，笔触脏乱细碎，线条杂乱突兀，人体比例失调，五官崩坏扭曲，对称刻板五官，零瑕疵假皮肤，死黑阴影，过曝高光，无环境光遮蔽，投影虚假漂浮，毛发僵硬成片，布料无自然褶皱，金属无真实质感，背景杂乱堆砌，多余杂物路人，低分辨率，噪点颗粒，AI错误肢体，重复纹理，卡通低幼化，边缘生硬抠图感，色彩溢出，色调脏污，画面油腻，无空间层次，真实照片，皮肤毛孔，4K照片，电影感",
                    "en": "Low-poly mesh, model clipping, insufficient mesh count, blurry stretched texture, jagged edges, plastic fake skin, flat coloring without volume, flat lighting, messy fragmented strokes, chaotic harsh lines, malformed human proportion, distorted facial features, rigid perfectly symmetric face, flawless wax fake skin, crushed pure black shadow, overblown highlight, no ambient occlusion, floating fake shadow, stiff clumped hair, fabric without natural folds, unrealistic metal texture, cluttered background, extra strangers, low resolution, noise grain, AI deformed limbs, repeated textures, childish cartoon style, harsh cutout edges, color overflow, muddy tone, greasy frame, no spatial layers, real photo, skin pores, 4K photo, cinematic"
                }
            }
        }

        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】2-4段连贯文字：首段总述构图与景别；次段详述角色姿态与表情；第三段描写风格化质感与光影（厚涂强调笔触色彩，3DCG强调材质光影）；末段补充场景氛围；总字数300-600字，语言富有画面感文学性，无额外解释。",
                "en": "[Natural Paragraph Mode] 2-4 coherent paragraphs: first paragraph composition & shot; second paragraph character pose & expression; third paragraph stylized texture & lighting (stroke & color for thick paint, material & physical light for 3DCG); final paragraph scene atmosphere; 300-600 words, literary visual language without extra explanation."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1. 类别：厚涂/3DCG写实人像
2. 风格模式：次世代写实/厚涂插画/二次元厚涂/奇幻史诗/古风仙侠/赛博朋克/科幻未来
3. 构图与景别：构图方式、视点角度、景别、视觉重心
4. 角色信息：外貌、姿态、表情、服装
5. 风格化质感：厚涂笔触/3DCG材质细节
6. 光影与氛围：主光、边缘光、环境光、特效光
7. 艺术风格：画风标签、氛围关键词
8. 风格标签：3-5个关键词概括整体视觉气质""",
                "en": """[Structured Mode] Output strictly in this order:
1. Category: Thick paint / 3DCG realistic portrait
2. Style Mode: Sub-era realism / thick illustration / anime thick paint / fantasy epic / ancient xianxia / cyberpunk / sci-fi future
3. Composition & Shot: Composition method, view angle, shot range, visual focus
4. Character Info: Appearance, pose, expression, costume
5. Stylized Texture: Brush stroke details for thick paint / material details for 3DCG
6. Lighting & Atmosphere: Key light, rim light, ambient light, special effect light
7. Art Style: Painting tag, atmosphere keywords
8. Style Tags: 3-5 keywords to summarize overall visual temperament"""
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
