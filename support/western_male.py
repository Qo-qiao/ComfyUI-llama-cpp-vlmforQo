# -*- coding: utf-8 -*-
"""
真实感欧美男性人像预设提示词库

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

WESTERN_MALE = {
    "template_id": "western_male",
    "name": "真实欧美男性人像",
    "description": "业欧美男性人像摄影指导，打造真实自然、富有男性魅力与故事感的人像描述。语义权重优先级：面部肤质五官胡须＞人物姿态服饰＞光影色彩＞场景环境＞构图景别＞摄影参数。支持三维度视角受控组合，用户指定优先沿用。",
}

class WesternMale:
    def __init__(self):
        # 下游生图模型内容组织公式库（完全复用参考原版无改动）
        self.model_formula_library = {
            "Flux1": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面氛围光影 → 人物气质姿态 → 肌肤发丝质感 → 背景留白。侧重氛围叙事，弱化细碎关键词堆砌，画面柔和高级。",
                "formula_en": "Content order: overall atmosphere lighting → character pose → skin hair texture → negative space. Focus on atmospheric narration."
            },
            "Flux2_klein": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：人物核心体态五官 → 光影立体层次 → 服饰质感 → 克制环境。平衡细节真实感与氛围感，光影过渡细腻自然。",
                "formula_en": "Content order: character face and body → lighting layers → clothing texture → restrained environment. Balance realism and atmosphere."
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：真人肤质细节优先 → 面部五官轮廓 → 体态姿态 → 光影布光 → 极简场景。极致还原皮肤原生质感，严格控制面部畸变。",
                "formula_en": "Content order: real skin texture first → facial contour → body posture → studio lighting → minimalist scene."
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：构图视觉重心 → 人物神态体态 → 色彩和谐管控 → 光影层次 → 干净背景。色彩精准管控，构图规整克制，画面干净通透，强化肤色自然过渡。",
                "formula_en": "Content order: composition focus → expression and posture → color harmony → lighting layers → clean background."
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：电影级光影氛围 → 人物体态情绪 → 胶片质感细节 → 服饰面料 → 极简布景。强化影调层次与高级氛围感。",
                "formula_en": "Content order: cinematic lighting → body emotion → film texture details → fabric → minimalist set."
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面基调 → 人物松弛姿态 → 自然肌肤质感 → 简约留白环境。极简干净叙事，弱化冗余修饰。",
                "formula_en": "Content order: overall tone → relaxed pose → natural skin texture → simple negative space."
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：面部五官肤质 → 体态姿态 → 光影层次 → 服饰细节 → 轻量环境。强化面部立体感，光影层次柔和，画面干净通透。",
                "formula_en": "Content order: facial skin features → body posture → lighting layers → fabric details → lightweight environment."
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：人物主体气质 → 肤质毛发细节 → 专业布光 → 服饰造型 → 极简场景。色彩柔和统一，神态刻画细腻，画面写实自然。",
                "formula_en": "Content order: character temperament → skin hair details → professional lighting → clothing styling → minimalist scene."
            }
        }

        # 全局底层规则（纯欧美男性纪实人像，无超写实词汇）
        self.global_base_rules = {
            "zh": """
你是专业欧美男性人像摄影提示词扩写专家，本模板为【真实感欧美男性人像】，覆盖职场/通勤、运动/健身、正装/商务、街头/潮牌、休闲、通用全题材。
所有风格坚守**真实纪实人像基线**，仅造型、光影、色调、氛围差异化，绝不出现二次元、插画、油画质感。
语义权重优先级：面部肤质五官胡须＞人物姿态服饰＞光影色彩＞场景环境＞构图景别＞摄影参数。
姿态必须完整描述动态抓拍过程，禁止静态摆拍表述；光线使用具象生活化实体光源描述，删除空泛抽象光影修辞；人物为绝对画面主体，环境仅服务人物叙事，不新增无关道具、行人、装饰。
严格执行色彩70%/25%/5%面积配比，统一标注饱和度层级，视觉留有舒适留白；全程强化欧美男性原生面部特征，保留胡茬青印、雀斑、毛孔、细纹、肤色不均、淡痣等原生肌肤痕迹，杜绝AI虚假光滑人脸。
完整保留用户输入的风格、服饰、场景、色调、姿态、视角所有信息，仅补充摄影、材质、光影、肤质、发丝、胡须专业细节，不篡改用户指定内容。
输出禁忌：禁止权重符号、冗余堆砌；禁止完美对称五官、零瑕疵塑料假皮、规整僵硬发丝、空洞假笑、无神凝视；禁止舞台强光、杂乱背景、透视畸变、极端俯仰视角；natural模式禁用全部光学数字参数，仅structured模式限定字段可使用指定摄影参数。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional European and American male portrait prompt expansion expert. This preset is [Realistic European American Male Portrait], covering workplace commuting, sports fitness, formal business, street fashion, casual and general themes.
All styles adhere strictly to real documentary portrait baseline, differentiated only by styling, lighting, tone and atmosphere, no illustration, anime or oil painting texture.
Semantic weight priority: facial skin, facial features and beard > character posture and clothing > light and shadow color > scene environment > composition shot > photographic parameters.
Posture must fully describe dynamic capture process, static posing description is forbidden; light is described with concrete real-life physical light sources, empty abstract light and shadow rhetoric is deleted; character is absolute frame subject, environment only serves character narration, no irrelevant props, pedestrians or decorations added.
Strictly implement color area ratio of 70%/25%/5%, mark saturation level uniformly, reserve comfortable blank space visually; always strengthen native facial features of European and American men, retain original skin traces such as beard stubble shadow, freckles, pores, fine lines, uneven skin tone and faint moles, eliminate AI fake smooth human face.
Completely retain all user input information including style, clothing, scene, tone, posture and perspective, only supplement professional details of photography, material, light and shadow, skin, hair and beard without altering user-specified content.
Taboo: no weight symbols, redundant stacking; perfectly symmetrical facial features, blemish-free plastic fake skin, rigid neat hair, empty fake smile, empty staring gaze; stage strong light, messy background, perspective distortion, extreme pitch angle; natural mode disables all optical digital parameters, only structured mode allows designated photographic parameters in limited fields.
Strictly output two formats without extra comments.
"""
        }

        # 预设库绑定WESTERN_MALE模板
        self.preset_library = {
            "western_male": {
                "template_id": WESTERN_MALE["template_id"],
                "display_name": WESTERN_MALE["name"],
                "description": WESTERN_MALE["description"],
                # 中英正向约束（原文positive_constraints完整迁移）
                "positive_constraints": {
                    "zh": "真实欧美男性面部,左右眉眼眉毛唇形天然轻微不对称,深邃双眼皮,深眼窝,高立体鼻梁,清晰立体面部轮廓,蓝绿棕系天然瞳孔,自然毛孔,淡细纹,细微肤色不均,自然雀斑,面部淡痣,胡茬长短不一,剃须青印,生长不均,原生真实肌肤质感,自然毛躁碎发,生活化发丝痕迹,画面干净简洁,环境仅衬托人物主体,姿态沉稳自然,抓拍真实情绪,无刻意摆拍痕迹,拍摄视角符合纪实人像真实拍摄逻辑,三维度组合自然协调,无透视畸变与违和角度",
                    "en": "real European and American male face, natural slight asymmetry of left and right eyebrows, eyes and lip shape, deep double eyelids, deep eye sockets, tall three-dimensional nose bridge, clear three-dimensional facial contour, natural blue/green/brown pupils, natural pores, faint fine lines, slight uneven skin tone, natural freckles, faint moles on face, uneven length beard stubble, shaving shadow, uneven growth, original real skin texture, natural frizzy broken hair, daily hair traces, clean and concise frame, environment only sets off character subject, steady natural posture, captured real emotion, no deliberate posing traces, shooting perspective conforms to real documentary portrait logic, three-dimensional combination natural and coordinated, no perspective distortion or incongruous angle"
                },
                # 全题材细分规则，严格取自WESTERN_MALE原文分类
                "preset_rules": {
                    "zh": """
【欧美男性纪实人像全题材专属规则】
1. 通用基线：双重肤质约束叠加，保留毛孔、细纹、肤色不均、自然雀斑、淡痣、胡茬长短与剃须青印等真实肌理，杜绝虚假光滑肤质；面部天然轻微不对称，拒绝完美对称五官；光线全部采用具象生活化光源描写，规避舞台式强光；色彩严格执行70%/25%/5%面积配比，标注饱和度层级，无高饱和撞色堆砌。
2. 职场/通勤风格：适配写字楼、简约办公空间，穿搭西装、通勤衬衫；光影以落地窗冷白自然光+室内暖灯混合柔光，色调中性低饱和，气质从容儒雅，姿态松弛放空。
3. 运动/健身风格：适配工业风健身房，力量器械、训练地面场景；顶光均匀柔和，肌肤保留运动汗珠、舒展毛孔，体态展现发力动态，神情专注坚韧，小麦健康肤色为主，突出胡茬肌理。
4. 正装/商务风格：高档酒店宴会厅、商务会客室布景；室内暖调混合柔光，定制西装礼服面料突出挺括质感，情绪沉稳内敛，暗调低饱和主色调，修剪整齐短胡茬。
5. 街头/潮牌风格：城市街道、街角橱窗生活化场景，午后斜阳或阴天漫射柔光；休闲潮牌穿搭，行走、倚靠抓拍动态，随性硬朗气质，低饱和复古街头色调。
6. 休闲风格：居家客厅、郊外草坪、咖啡馆日常场景，窗边自然光为主；简约休闲穿搭，坐姿倚靠松弛抓拍，温和沉稳气质，柔和中性色调。
所有题材：用户指定景别、方位、俯仰视角必须严格沿用；未指定维度从合规纪实视角池随机抽取；不自动新增无关道具、装饰、行人，环境仅作为叙事载体。
""",
                    "en": """
【Documentary European American Male Portrait Theme Rules】
1. General baseline: Double skin texture constraints, retain real texture such as pores, fine lines, uneven skin tone, natural freckles, faint moles, uneven beard stubble and shaving shadow, eliminate fake smooth skin; natural slight facial asymmetry, reject perfectly symmetrical features; light described with daily physical light sources, avoid stage harsh light; strictly follow 70%/25%/5% color ratio with saturation marked, no oversaturated clashing colors.
2. Workplace/Commuting style: Office buildings, simple office space, suits and daily shirts; mixed cold window natural light + indoor warm soft light, neutral low saturation tone, calm elegant temperament, relaxed idle posture.
3. Sports/Fitness style: Industrial gym, strength equipment and training ground; even soft top light, sweat and open pores on skin, strength movement poses, focused tough expression, wheat healthy skin tone, highlight stubble texture.
4. Formal/Business style: Luxury hotel banquet hall, business lounge; indoor warm mixed soft light, stiff tailored suit fabric, calm introverted mood, dark low saturation main tone, neatly trimmed short stubble.
5. Street/Fashion style: City streets and shop windows, sunset or overcast diffuse soft light; casual fashion outfits, captured walking or leaning movements, tough casual vibe, low saturation retro street tone.
6. Casual style: Living room, suburban lawn, cafe, window natural light; simple casual clothes, relaxed sitting and leaning captures, mild steady temperament, soft neutral tones.
All themes: User-specified shot, horizontal azimuth and vertical pitch must be fully followed; unspecified dimensions randomly selected from compliant documentary perspective pool; no auto-generated irrelevant props, decorations or pedestrians, environment only serves narration.
"""
                },
                "negative_base": {
                    "zh": "完美对称五官,零瑕疵皮肤,人工对称双眼皮,厚重匀肤磨皮,塑料光滑哑光假皮,过度光滑肌肤,完全对称眉眼,厚重美颜,统一匀肤,过度美化皮肤,精致无瑕疵脸蛋,多余绿植,无关摆件,路人,装饰杂物,多余花草,多余家具,杂乱背景,大量装饰,多余人物,空洞假笑,僵硬摆拍,过度锐化,高饱和撞色,人工完美肌理,刻意模特摆姿,多余肢体动作,无神凝视,舞台强光,画面堆砌元素,虚假面部肌理,光滑无毛孔皮肤,无雀斑肤质,规整僵硬发丝,完美无瑕面容,鸟瞰视角,虫眼视角,极端大俯大仰,透视畸变,肢体比例失调",
                    "en": "perfect symmetrical facial features, blemish-free skin, artificial symmetrical double eyelids, heavy skin retouching, plastic smooth matte fake skin, overly smooth skin, fully symmetrical eyes and brows, heavy beauty filter, unified even skin, over-polished skin, flawless delicate face, extra green plants, irrelevant ornaments, passers-by, decorative clutter, extra flowers, redundant furniture, messy background, massive decorations, extra people, empty fake smile, stiff posing, over-sharpening, oversaturated clashing colors, artificial perfect texture, deliberate model posing, redundant limb movements, empty stare, stage harsh light, frame stuffed elements, fake facial texture, poreless smooth skin, freckle-free skin, rigid neat hair, flawless face, bird's-eye view, bug-eye view, extreme high/low angle, perspective distortion, disproportionate limbs"
                }
            }
        }

        # 输出格式指引，完全匹配WESTERN_MALE output_format_suffix规则
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】2-3段连贯文字：首段描述实体场景环境与明确光源光线氛围，次段刻画人物完整动态姿态与细微表情神态，末段补充肤色肌理、胡茬质感、雀斑、面料色彩细节。语言平实有画面感，全程无数字技术参数，300‑600字纯画面描写。",
                "en": "[Natural Paragraph Mode] 2-3 coherent paragraphs: first paragraph describes physical scene and light atmosphere; second paragraph depicts full dynamic posture and subtle facial expressions; third part adds skin texture, stubble, freckles and fabric color details. Plain descriptive language, no digital technical parameters, 300-600 words pure visual text."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1.类别风格定位
2.全局肤质正向约束（面部基础/皮肤肌理/毛发胡须细节）
3.画面构图（视觉引导/主体位置/画面比例/精简约束）
4.景别（类型/取景裁切范围）
5.视角与景深感知（距离/水平方位/垂直俯仰/景深氛围）
6.人物描述（外貌/姿态动作/表情神态/服装色彩配比）
7.肌肤与细节（肤质/毛发/面部五官胡须特征）
8.环境与氛围（空间/光线来源/色彩配比/细节元素）
9.技术参数建议（仅焦距、光圈、镜头类型，附带释义，禁用快门、ISO等）
10.风格标签+画面收尾精简约束""",
                "en": """[Structured Mode] Output in fixed order:
1. Category & style positioning
2. Global positive skin constraints (facial base / skin texture / hair & stubble details)
3. Frame composition (visual guide / subject position / frame ratio / simplification limit)
4. Shot type (type / frame cropping range)
5. Perspective & depth of field (distance / horizontal angle / vertical pitch / depth atmosphere)
6. Character description (appearance / movement / expression / clothing color ratio)
7. Skin & fine details (skin condition / hair / facial features & stubble)
8. Environment & atmosphere (space / light source / color ratio / minor elements)
9. Technical parameter suggestion (only focal length, aperture, lens type with explanation; shutter, ISO forbidden)
10. Style tags + frame cleanup constraints"""
            }
        }

    def detect_language(self, text: str) -> str:
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
    ) -> Dict:
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