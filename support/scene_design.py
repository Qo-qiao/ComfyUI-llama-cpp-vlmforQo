# -*- coding: utf-8 -*-
"""
室外场景预设模块

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

SCENE_DESIGN = {
    "template_id": "scene_design",
    "name": "室外场景设计",
    "description": "专业场景设计指导，为自然风光、赛博朋克、科幻未来等全品类场景打造标准化、高可控的沉浸式视觉叙事描述。语义权重优先级：主题基调＞风格属性＞视角构图＞色彩空间＞光影质感＞尺度代入。内置三维度视角、70%/25%/5%色彩配比、双重质感约束与画面精简约束，强化空间层次、光影叙事与真实材质质感。",
}

class SceneDesign:
    def __init__(self):
        # 下游生图模型内容组织公式库
        self.model_formula_library = {
            "Flux1": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面主题氛围光影 → 空间层次结构 → 材质肌理色彩 → 远景留白。侧重场景叙事，弱化细碎关键词堆砌，画面空间感高级完整。",
                "formula_en": "Content order: overall scene theme & lighting → spatial hierarchy structure → texture & color → background negative space. Focus on scene narrative."
            },
            "Flux2_klein": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：场景核心主题风格 → 光影空间层次 → 地貌建筑材质 → 克制远景环境。平衡材质细节与空间氛围感，光影过渡贴合物理逻辑。",
                "formula_en": "Content order: core scene theme & style → light & spatial layers → terrain building texture → restrained background environment. Balance texture details and spatial atmosphere."
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：材质肌理细节优先 → 空间透视轮廓 → 三维视角构图 → 全局布光光影 → 极简远景。精准把控透视比例，杜绝空间畸变，统一风格材质标准。",
                "formula_en": "Content order: texture details first → spatial perspective contour → 3D view composition → global lighting → minimalist background. Strictly control perspective proportion, unify style texture standards."
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：构图视觉重心 → 空间远近层次 → 色彩配比管控 → 光影明暗层次 → 干净远景。严格遵循70%/25%/5%色彩配比，构图规整精简，大气透视自然柔和。",
                "formula_en": "Content order: composition visual focus → near-mid-far layers → color ratio control → light shadow hierarchy → clean background. Follow 70%/25%/5% color proportion, neat composition, natural atmospheric perspective."
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：全局光影氛围基调 → 空间尺度情绪 → 场景材质细节 → 地貌建筑面料 → 极简远景布景。强化光影叙事与空间纵深感，区分不同风格专属光效。",
                "formula_en": "Content order: global lighting atmosphere tone → spatial scale emotion → scene texture details → terrain building material → minimalist background set. Strengthen light narrative and depth of field, distinguish exclusive light effects for each style."
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面主题基调 → 舒展空间层次 → 统一材质质感 → 简约留白远景。极简叙事逻辑，删减冗余装饰元素，突出核心场景主体。",
                "formula_en": "Content order: overall scene theme tone → relaxed spatial layers → unified texture quality → simple blank background. Minimalist narrative, remove redundant decorations, highlight core scene subject."
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：空间透视与材质肌理 → 远近景层次 → 光影明暗过渡 → 建筑地貌细节 → 轻量化远景。强化空间透视准确度，材质区分清晰，光影层次柔和连贯。",
                "formula_en": "Content order: spatial perspective & texture → near-far layers → light shadow transition → terrain building details → lightweight background. Accurate spatial perspective, distinct textures, soft continuous lighting layers."
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：场景整体主题气质 → 材质空间细节 → 专业全局布光 → 风格专属造型元素 → 极简远景。色调统一协调，空间层次刻画细腻，画面沉浸叙事感强。",
                "formula_en": "Content order: overall scene theme temperament → texture spatial details → professional global lighting → style exclusive elements → minimalist background. Unified tone, delicate spatial layers, strong immersive narrative."
            }
        }
        # 全局底层规则
        self.global_base_rules = {
            "zh": """
你是专业全品类场景设计提示词扩写专家，本模板覆盖自然风光、城市景观、赛博朋克、科幻未来、历史古迹全题材。
所有创作坚守场景叙事基线，仅主题、光影、色调、空间结构差异化，不混用多种风格造成画面割裂。
空间严格划分前景、中景、远景三层结构，大气透视过渡自然，透视比例准确无畸变；色彩固定遵循70%主色/25%辅助色/5%点缀色配比，无杂乱高饱和撞色堆砌。
光影贴合物理规律，明确主光、辅助光方向与软硬色温，利用丁达尔、霓虹、晨昏等特殊光效烘托氛围；材质肌理匹配对应场景风格，地貌、建筑、水体、植被质感符合现实物理逻辑。
完整保留用户输入的主题、风格、视角、景别、色调、空间元素全部信息，仅补充材质、光影、色彩、透视专业细节，不自动新增无关道具、杂物、多余装饰。
画面严格执行精简约束，仅保留叙事核心元素；尺度参照使用人物、建筑、生物强化空间代入感，具象元素承载画面情绪。
输出禁忌：禁止权重符号、分辨率/DPI/焦距等数字技术参数堆砌；禁止风格混乱、透视扭曲、元素堆砌、塑料虚假质感；禁止字幕水印logo、完美对称、零瑕疵等违规描述。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional full-category scene design prompt expert. This preset covers natural scenery, urban landscape, cyberpunk, sci-fi future, historical relics themes.
All creations follow scene narrative baseline, differentiated only by theme, lighting, tone and spatial structure, no mixed styles causing picture fragmentation.
Space is strictly divided into foreground, midground and background, natural atmospheric perspective transition, accurate perspective proportion without distortion; fixed 70% main /25% secondary /5% accent color ratio, no messy oversaturated color collision.
Lighting complies with physical rules, clear direction, softness and color temperature of key light & fill light, use special light effects such as Tyndall, neon, dawn/dusk to set atmosphere; texture matches scene style, terrain, building, water, vegetation textures conform to physical logic.
Fully retain all user input info including theme, style, view, shot, tone, spatial elements, only supplement professional texture, lighting, color, perspective details without irrelevant props or redundant decorations.
Strict frame simplification rule, only keep core narrative elements; scale reference uses figures, buildings, creatures to strengthen spatial substitution, concrete elements carry picture emotion.
Taboo: no weight symbols, no stacked digital technical parameters such as resolution/DPI/focal length; no chaotic styles, distorted perspective, element clutter, fake plastic texture; no subtitles, watermarks, logos, perfect symmetry, flawless description.
Strictly output two formats without extra comments.
"""
        }
        # 唯一主预设模板，绑定原有SCENE_DESIGN模板id
        self.preset_library = {
            "scene_design": {
                "template_id": "scene_design",
                "display_name": SCENE_DESIGN["name"],
                "description": SCENE_DESIGN["description"],
                # 中英双语固定前置正向约束
                "positive_constraints": {
                    "zh": "风格统一稳定，空间层次清晰分明，光影叙事自然流畅，色彩配比和谐合规，透视比例精准无误，大气透视过渡真实柔和，画面干净主体突出，仅留存核心叙事元素；自然风光保留原生地貌肌理，赛博科幻统一结构逻辑与霓虹光效质感，历史古迹还原时代建筑肌理；光影随空间自然流动，氛围情绪饱满具象，各类材质质感贴合物理逻辑，画面兼具沉浸感与完整叙事张力",
                    "en": "Stable unified style, distinct spatial layers, natural smooth light narrative, harmonious compliant color ratio, precise perspective proportion, soft authentic atmospheric perspective transition, clean frame with prominent subject, only core narrative elements retained; natural scenery retains native terrain texture, cyberpunk & sci-fi unify structural logic and neon light texture, historical sites restore era architectural texture; light flows naturally with space, full concrete atmosphere emotion, all textures fit physical logic, frame with immersive sense and complete narrative tension"
                },
                # 全风格细分专属规则
                "preset_rules": {
                    "zh": """
【全风格场景专属细分规则】
1. 通用基线：遵循语义权重顺序：主题基调＞风格属性＞视角构图＞色彩空间＞光影质感＞尺度代入；三维视角优先沿用用户指定，无指定则选取合规审美角度；严格执行70%/25%/5%色彩配比，画面精简约束，禁用["8K", "4K", "分辨率", "DPI", "色彩模式", "帧率", "码率", "采样率", "编码器", "HDR", "杜比", "字幕", "水印", "logo", "完美对称", "零瑕疵", "塑料感", "崩坏", "扭曲", "焦距", "坐标"]。
2. 自然风光风格：突出原生山石、植被、水体自然肌理，依托晨昏、云海、雾霭塑造大气透视；主光源选用日光、天光，搭配丁达尔自然光束，低饱和柔和冷暖色调，以林木、飞鸟、野生动物作为尺度参照。
3. 城市现代景观：写实建筑结构，玻璃、混凝土、金属材质区分清晰，城市漫射天光，傍晚暖调城市光，利用行人、车辆构建空间尺度，构图依托街道透视线引导视觉。
4. 赛博朋克风格：潮湿反光路面、多层霓虹光效、全息投影、悬浮载具，多方向漫射霓虹光源，冷暖撞色光影，雾气柔化远景，以行人、机械构件作为尺度锚点。
5. 科幻未来风格：悬浮建筑、透明透光材质、流动数据光带、行星天体，落日/宇宙冷调天光，建筑折射反射光效，飞行器、人形参照物凸显宏大空间尺度。
6. 历史古迹风格：风化石材、木质古建筑肌理，柔和漫射自然光，黄金时刻暖调光影，古树木、人物雕像作为尺度参照，色调低饱和复古沉稳。
所有题材：用户指定内容优先级最高，仅补充材质、光影、透视专业细节，不篡改场景主题、氛围与核心元素。
""",
                    "en": """
【Universal Scene Exclusive Rules】
1. General baseline: Follow semantic weight order: theme tone > style attribute > view composition > color space > light texture > scale substitution; user-specified 3D view takes priority, select aesthetic compliant angle if unspecified; strictly implement 70%/25%/5% color ratio, frame simplification rule; forbidden words list: 8K,4K,resolution,DPI,color mode,frame rate,bit rate,sampling rate,encoder,HDR,dolby,subtitle,watermark,logo,perfect symmetry,flawless,plastic texture,collapse,distort,focal length,coordinate.
2. Natural scenery style: Highlight native rock, plant, water natural texture, build atmospheric perspective via dawn/dusk, sea of clouds, mist; key light adopts sunlight, skylight, match Tyndall natural light beam, low saturation soft warm-cold tone, use woods, birds, wild animals as scale reference.
3. Modern urban landscape: Realistic building structure, clear differentiation of glass, concrete, metal texture, city diffuse skylight, warm evening urban light, construct spatial scale with pedestrians and vehicles, composition guided by street perspective lines.
4. Cyberpunk style: Wet reflective pavement, multi-layer neon light, holographic projection, suspended vehicles, multi-direction diffuse neon light source, warm-cold contrasting light, mist softens background, take pedestrians and mechanical components as scale anchor.
5. Sci-fi future style: Suspended architecture, transparent light-transmitting material, flowing data light strips, planetary celestial bodies, sunset/cosmic cool skylight, building refraction & reflection light effect, aircraft and humanoid reference highlight grand spatial scale.
6. Historical relic style: Weathered stone, wooden ancient building texture, soft diffuse natural light, warm golden hour light, ancient trees and human statues as scale reference, low saturation retro steady tone.
All themes: User-specified content highest priority, only supplement professional texture, light, perspective details without altering scene theme, atmosphere and core elements.
"""
                },
                "negative_base": {
                    "zh": "风格混乱跳变，色彩脏污溢出，构图失衡杂乱，元素堆砌冗余，透视逻辑错误，比例失调变形，低分辨率模糊，塑料虚假质感，多余无关元素乱入，杂物装饰堆砌，字幕水印logo，光影生硬断层，画面空洞无物，过度锐化生硬，边缘锯齿毛躁，空间层次混乱，大气透视失真，赛博元素生硬堆砌，科幻结构违背物理逻辑，历史场景违和穿越，地面漂浮无重力，物体比例失调",
                    "en": "Chaotic jumping styles, muddy overflowing color, unbalanced cluttered composition, redundant stacked elements, wrong perspective logic, distorted disproportionate scale, blurry low resolution, fake plastic texture, irrelevant redundant elements, stacked clutter decorations, subtitles watermarks logos, stiff disjointed lighting, empty hollow frame, over-sharpened rigid texture, jagged rough edges, disordered spatial layers, distorted atmospheric perspective, stiff piled cyber elements, sci-fi structures violating physical logic, anachronistic historical scene, floating ground without gravity, disproportionate objects"
                }
            }
        }
        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】2-3段连贯文字：第一段空间格局与整体光影氛围；第二段前景中远景分层空间层次与材质光影细节；第三段色彩配比、尺度参照与整体意境；总字数300-600字，全程规避数字技术参数，语言富有画面叙事感，无额外解释。",
                "en": "[Natural Paragraph Mode] 2-3 coherent paragraphs: spatial layout & overall light atmosphere; near-mid-far spatial layers & texture lighting details; color ratio, scale reference and overall artistic conception; 300-600 words, avoid all digital technical parameters, narrative visual language without extra explanation."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1.场景类型与全局风格正向约束
2.画面构图、视觉引导、主体占比、画幅比例、精简规则
3.三维景别视角：距离、水平朝向、垂直俯仰、景深虚实
4.三层空间层次：前景叙事功能、中景核心主体、远景延伸环境
5.材质肌理、主辅光源、阴影过渡、专属特殊光效
6.风格专属标识元素与时代结构特征
7.色彩配比、画面核心意境情绪
8.尺度参照物与情感代入锚点
9.技术质感补充与全局禁止项
10.3-5个概括画面气质的风格标签""",
                "en": """[Structured Mode] Output strictly in this order:
1. Scene type & global style positive constraints
2. Frame composition, visual guide, subject proportion, aspect ratio, simplification rule
3. 3D shot view: distance, horizontal orientation, vertical pitch, depth of field blur
4. Three-layer spatial hierarchy: foreground narrative function, midground core subject, background extended environment
5. Texture, key & fill light, shadow transition, exclusive special light effects
6. Style exclusive mark elements & era structural features
7. Color ratio, core artistic conception & emotion of frame
8. Scale reference object & emotional substitution anchor
9. Technical texture supplement & global forbidden items
10. 3-5 style tags summarizing overall visual temperament"""
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

