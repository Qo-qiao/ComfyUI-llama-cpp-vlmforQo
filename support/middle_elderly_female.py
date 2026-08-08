# -*- coding: utf-8 -*-
"""
真实老年男性人像预设提示词库

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

MIDDLE_ELDERLY_FEMALE = {
    "template_id": "middle_elderly_female",
    "name": "中老年女性人像",
    "description": "专业中老年女性超写实人像摄影指导，仅覆盖40岁以上中年、中老年、高龄女性，涵盖居家纪实、国风旗袍、复古胶片、轻商务、极简棚拍、艺术人像等熟龄专属题材。兼容亚洲/欧美中老年女性松弛五官、岁月肤质、花白银发特征，原生淡妆干净无大面积瑕疵，完整保留深浅皱纹、淡老年斑、面部松弛肌理，杜绝塑胶假肤、AI模板脸、年轻化过度磨皮。语义权重优先级：面部肤质岁月约束＞中老年五官/银发/熟龄体态服饰＞光影色彩氛围＞场景构图＞摄影参数。所有风格坚守熟龄真人写实基线，仅氛围、造型、光影差异化，姿态松弛舒缓无夸张变形，全程不涉及青年、少女刻画逻辑。超写实人像摄影提示词扩写",
}

class MiddleElderlyFemale:
    def __init__(self):
        # 下游生图模型内容组织公式库（完全沿用参考原版无改动）
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
        # 全局底层规则，修改为中老年女性专用
        self.global_base_rules = {
            "zh": """
你是专业高端中老年女性超写实人像摄影提示词扩写专家，本模板为【中老年熟龄女性人像专用】，全覆盖：居家纪实、国风旗袍、现代轻商务、复古胶片、极简棚拍、艺术人体等熟龄专属题材。
所有风格坚守**40岁以上熟龄真人超写实基线**，仅造型、光影、色调、氛围差异化，绝不出现二次元、插画、油画质感，禁止刻画青年、少女、学生群体。
原生淡妆状态面部干净整洁，无大面积杂乱瑕疵，完整保留中老年原生深浅皱纹、面部软组织松弛、淡老年斑、细微干纹与肤色不均，拒绝过度磨皮带来的塑胶假肤、紧致年轻化肌肤效果。
姿态必须使用具体中老年舒缓肢体结构描述，禁止模糊形容词、少女活泼夸张动作；光线方向明确，光影过渡柔和通透；人物为绝对画面主体，环境仅衬托岁月叙事氛围。
完整保留用户输入的风格、服饰、场景、色调、姿态、视角所有信息，仅补充摄影、材质、光影、岁月肤质、花白银发专业细节，不新增少女、青春相关无关物体、装饰道具。
所有服饰（旗袍/羊绒大衣/宽松居家棉麻/艺术人体）均作为成熟女性高端人像题材，姿态克制温婉、松弛自然，禁止低俗化、过度性化、畸形夸张体态。
输出禁忌：禁止权重符号、多余相机参数、冗余堆砌；禁止卡通二次元、畸形肢体、坏手烂指、网红假脸、磨皮蜡皮；禁止杂乱少女风背景、空洞甜腻假笑、自拍抓拍、透视畸变、强行紧致年轻化。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional photorealistic portrait prompt expert exclusively for middle-aged and elderly women. This preset covers all mature themes: daily home documentary, Chinese cheongsam, light business, retro film, minimalist studio, artistic nude portrait.
All styles strictly adhere to photorealistic baseline for women aged 40+, differentiated only by styling, lighting, tone and atmosphere, no illustration, anime or oil painting texture; depictions of young girls and teenagers are forbidden.
Light natural makeup, clean face without large blemishes, fully retain natural wrinkles, sagging facial tissue, faint age spots, fine dry lines and uneven skin tone of mature skin; reject plastic fake skin and artificially tightened youthful skin caused by heavy retouching.
All poses described with specific relaxed limb structure for elders, no vague words or exaggerated youthful movements. Clear light direction and soft shadow transition. Elderly female subject dominates the frame, background only serves aging narrative atmosphere.
Completely retain user input style, clothing, scene, tone, pose and perspective. Only supplement professional details of photography, texture, light, aged skin and gray-white hair, no irrelevant youthful decorations or props.
All costumes (cheongsam, cashmere coat, loose linen home wear, artistic nude) are high-end mature portrait themes with restrained gentle relaxed poses, no vulgar or deformed exaggerated body shapes.
Taboo: no weight symbols, redundant camera parameters, anime/cartoon/illustration, deformed anatomy, defective hands, over-retouched wax skin, messy youthful background, empty sweet fake smile, snapshot selfie, perspective distortion, forced youthful facial tightening.
Strictly output two formats without extra comments.
"""
        }
        # 唯一主预设模板，绑定中老年专用template_id，完整复刻参考内preset_library结构
        self.preset_library = {
            "middle_elderly_female": {
                "template_id": "middle_elderly_female",
                "display_name": MIDDLE_ELDERLY_FEMALE["name"],
                "description": MIDDLE_ELDERLY_FEMALE["description"],
                # 中英双语前置约束，中老年专属
                "positive_constraints": {
                    "zh": "影视级超写实真人质感，40岁以上中老年女性松弛面部骨骼结构，眉眼唇皱纹分布天然轻微不对称；原生淡妆干净无大面积瑕疵，完整保留深浅皱纹、面部松弛肌理、淡老年斑、肤色不均、细微干纹，零过度磨皮、无塑胶蜡皮、无AI网红模板脸；柔软分层花白/全白发丝，干净克制中老年生活化布景，松弛舒缓真人抓拍姿态，内敛沉静慈祥成熟情绪，无透视畸变。居家/旗袍/胶片/棚拍/艺术人体均为熟龄题材分支，不破坏岁月写实基线，姿态温婉松弛、自然从容",
                    "en": "Cinematic photorealistic real human texture, sagging facial bone structure unique to women over 40, natural slight asymmetry of eyes, eyebrows, lips and wrinkle distribution; light natural makeup without large blemishes, fully retain deep & shallow wrinkles, sagging facial texture, faint age spots, uneven skin tone, fine dry lines, no over-smoothing, no plastic wax skin, no AI influencer template face; soft layered gray-white hair, restrained daily scene matching elders, relaxed snapshot pose, restrained calm kind mature emotion, no perspective distortion. Daily/cheongsam/film/studio/artistic nude are mature theme branches only, never break aging realism baseline with gentle relaxed posture"
                },
                # 中老年全风格细分专属规则
                "preset_rules": {
                    "zh": """
【中老年女性人像专属规则】
1. 通用基线：仅刻画40岁-70+熟龄女性，完整保留皱纹、面部松弛、淡老年斑、花白头发等原生年龄特征，禁止磨皮淡化、强行紧致年轻化；原生淡妆干净无大面积瑕疵，留存岁月肌理与自然毛孔，杜绝完美对称五官、蜡像假肤。
2. 亚洲中老年女性刻画：柔和圆润松弛面部轮廓，平缓骨骼线条，浅淡分散老年斑，花白发丝层次柔软蓬松；适配居家纪实、新中式旗袍、茶室场景，主用光为窗纱漫射柔光、室内暖调灯光，低饱和大地沉稳色系。
3. 欧美中老年女性刻画：立体骨骼、深眼窝、松弛清晰下颌线，立体沟壑岁月纹理，银灰分层短发；适配画廊、轻商务极简场景，多用侧方轮廓柔光、冷调漫射天光，低饱和灰调色系。
4. 国风旗袍熟龄风格：选用棉麻、重磅真丝宽松成熟旗袍版型，体态舒缓端庄，无紧身夸张剪裁，配色酒红、藏蓝、驼色沉稳色系，庭院、茶室柔光纪实拍摄。
5. 复古胶片纪实风格：带有轻微自然胶片颗粒，暖调褪色柔光，不刻意精修淡化皱纹，场景选用老式民居、老街，还原生活化松弛抓拍质感。
6. 极简棚拍熟龄风格：低饱和纯色简约背景，均匀柔光铺光，重点突出面部岁月肌理与银发层次；服饰以羊绒、针织、宽松通勤外套为主。
7. 居家日常纪实风格：宽松棉麻家居服饰，松弛坐卧体态，午后自然漫射阳光，搭配木家具、针线、旧书本等中老年专属生活道具。
8. 艺术人体熟龄风格：纯白极简摄影空间，侧逆光勾勒成熟松弛身体曲线，完整保留全身岁月肌肤纹理，姿态沉静内敛、优雅克制，无低俗夸张体态。
所有题材仅围绕熟龄女性创作，用户指定场景、服饰、视角优先保留，仅补充岁月肤质、银发、成熟光影细节，不新增少女、青年相关元素。
""",
                    "en": """
【Exclusive Rules for Middle-Aged and Elderly Female Portraits】
1. General baseline: Only depict women aged 40 to 70+, fully retain original aging marks including wrinkles, facial sagging, faint age spots, gray hair; prohibit smoothing or forced youthful tightening. Light natural makeup without large blemishes, retain aged texture and natural pores, reject perfectly symmetrical facial features and wax fake skin.
2. Asian middle-aged & elderly women: Soft round sagging facial contour, gentle bone lines, faint scattered age spots, soft layered gray hair. Suitable for daily home records, new Chinese cheongsam, teahouse scenes; light source: diffused window soft light, warm indoor lamp, low-saturation earth tone palette.
3. Western middle-aged & elderly women: Stereoscopic bone structure, deep eye sockets, clear sagging jawline, three-dimensional facial aging lines, layered silver-gray short hair. Suitable for galleries, minimalist light business scenes, side contour soft light, cool diffuse natural light, low-saturation gray color system.
4. Chinese cheongsam style for elder women: Loose mature cheongsam made of linen and heavy silk, dignified relaxed posture without tight exaggerated cuts, stable color matching including wine red, navy and camel, soft light shooting in courtyards and teahouses.
5. Retro film documentary style: Slight natural film grain, warm faded soft light, no retouching to erase wrinkles, old houses and old streets as shooting scenes, relaxed daily snapshot texture.
6. Minimal studio style for elder women: Low-saturation solid simple background, even soft box lighting, focus on facial aging texture and silver hair layers; costumes are mainly cashmere, knitwear and loose commuter coats.
7. Daily home documentary style: Loose linen home wear, relaxed sitting and lying posture, afternoon diffuse natural sunlight, daily props for elders such as wooden furniture, needlework and old books.
8. Artistic nude mature style: Pure white minimalist photo space, side backlight outlines mature relaxed body curves, fully retain aged skin texture all over body, calm restrained elegant posture without vulgar exaggerated shapes.
All themes are only created for mature women, retain user-specified scenes, costumes and perspectives, only add details of aged skin, silver hair and mature light, no elements related to young girls or teenagers.
"""
                },
                "negative_base": {
                    "zh": "少女、青年、学生、粉嫩肌肤、马卡龙亮色、紧致少女轮廓、完美对称五官、零皱纹、无老年斑、过度磨皮无毛孔、塑料蜡皮、AI网红模板脸、僵硬影楼摆拍、空洞甜腻假笑、夸张活泼肢体、畸形手脚、多手指、透视畸变、高饱和荧光艳色、杂乱少女装饰、二次元插画、卡通动漫画风、面部大面积无瑕疵、强行紧致年轻化、乌黑假发、年龄感丢失",
                    "en": "Young girl, teenager, student, pink tender skin, macaron bright colors, tight youthful facial contour, perfectly symmetrical facial features, wrinkle-free skin, no age spots, over-smoothed poreless plastic wax skin, AI influencer template face, stiff studio pose, empty sweet fake smile, exaggerated lively limbs, deformed hands and feet, extra fingers, perspective distortion, oversaturated fluorescent bright colors, messy girlish decorations, anime illustration, cartoon art style, flawless face, forced youthful tightening, black wig, lost aging texture"
                }
            }
        }
        # 双输出格式指引（完全沿用参考原版无改动）
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】三段连贯文字：第一段场景布光整体氛围；第二段人物姿态视线表情体态；第三段肤质发丝服饰面料色彩调性，300‑600字纯画面描写。",
                "en": "[Natural Paragraph Mode] Three coherent paragraphs: scene‑lighting‑atmosphere; pose‑gaze‑expression‑body; skin‑hair‑fabric‑color tone, 300‑600 words pure visual description."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1.人种五官轮廓特征
2.风格与服饰造型定位
3.肤质与毛发原生细节
4.构图景别与视觉重心
5.视角方位与俯仰角度
6.姿态体态与表情神态
7.色彩配比与整体调性
8.专业布光方式与光影层次
9.画面精简约束与环境要求""",
                "en": """[Structured Mode] Output strictly in this order:
1. Ethnic facial features
2. Style and clothing positioning
3. Skin and hair natural details
4. Composition shot type and visual focus
5. View angle and pitch
6. Pose body and facial expression
7. Color ratio and overall tone
8. Professional lighting method
9. Frame simplification constraint"""
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


