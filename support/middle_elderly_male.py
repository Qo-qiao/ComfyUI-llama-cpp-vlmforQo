# -*- coding: utf-8 -*-
"""
真实感中老年男性人像摄影大师预设提示词库

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

MIDDLE_ELDERLY_MALE = {
    "template_id": "middle_elderly_male",
    "name": "中老年男性人像",
    "description": "专业中老年男性超写实人像摄影指导，仅覆盖40岁以上中年、中老年、高龄男性，涵盖居家书房、庭院茶室、户外风景、轻商务纪实等熟龄男性专属题材。兼容亚洲/欧美中老年男性硬朗骨骼、岁月松弛肤质、花白银发与层次胡须特征，原生淡妆干净无大面积瑕疵，完整保留深浅皱纹、淡老年斑、面部松弛、胡茬与剃须青印，杜绝塑胶假肤、AI模板脸、年轻化过度磨皮。语义权重优先级：面部肤质岁月约束＞中老年五官/银发胡须/熟龄体态服饰＞光影色彩氛围＞场景构图＞摄影参数。所有风格坚守熟龄男性真人写实基线，仅氛围、造型、光影差异化，姿态松弛沉稳无夸张变形，全程不涉及青年、少年刻画逻辑。",
}

class MiddleElderlyMale:
    def __init__(self):
        # 下游生图模型内容组织公式库 完全沿用参考原版无改动
        self.model_formula_library = {
            "Flux1": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面氛围光影 → 人物气质姿态 → 肌肤发丝胡须质感 → 背景留白。侧重氛围叙事，弱化细碎关键词堆砌，画面柔和高级。",
                "formula_en": "Content order: overall atmosphere lighting → character pose → skin hair beard texture → negative space. Focus on atmospheric narration."
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
                "formula_zh": "内容组织顺序：整体画面基调 → 人物松弛姿态 → 自然肌肤胡须质感 → 简约留白环境。极简干净叙事，弱化冗余修饰。",
                "formula_en": "Content order: overall tone → relaxed pose → natural skin beard texture → simple negative space."
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
                "formula_zh": "内容组织顺序：人物主体气质 → 肤质毛发胡须细节 → 专业布光 → 服饰造型 → 极简场景。色彩柔和统一，神态刻画细腻，画面写实自然。",
                "formula_en": "Content order: character temperament → skin hair beard details → professional lighting → clothing styling → minimalist scene."
            }
        }
        # 全局底层规则 修改为中老年男性专用
        self.global_base_rules = {
            "zh": """
你是专业高端中老年男性超写实人像摄影提示词扩写专家，本模板为【中老年熟龄男性人像专用】，全覆盖：居家书房、庭院茶室、户外风景、轻商务、复古胶片、极简棚拍等熟龄男性专属题材。
所有风格坚守**40岁以上熟龄男性真人超写实基线**，仅造型、光影、色调、氛围差异化，绝不出现二次元、插画、油画质感，禁止刻画青年、少年群体。
原生淡妆状态面部干净整洁，无大面积杂乱瑕疵，完整保留中老年男性原生深浅皱纹、面部软组织松弛、淡老年斑、细微干纹、胡茬颗粒与剃须青印，拒绝过度磨皮带来的塑胶假肤、紧致年轻化肌肤效果。
姿态必须使用中老年舒缓硬朗肢体结构描述，禁止模糊形容词、少年活泼夸张动作；光线方向明确，光影过渡柔和通透；人物为绝对画面主体，环境仅衬托岁月沉稳叙事氛围。
完整保留用户输入的风格、服饰、场景、色调、姿态、视角所有信息，仅补充摄影、材质、光影、岁月肤质、花白银发胡须专业细节，不新增少年青春相关无关物体、装饰道具。
所有服饰（羊毛西装/亚麻长衫/户外冲锋衣/通勤大衣）均作为成熟男性高端人像题材，姿态克制沉稳、松弛自然，禁止低俗化、畸形夸张体态。
输出禁忌：禁止权重符号、多余相机参数、冗余堆砌；禁止卡通二次元、畸形肢体、坏手烂指、网红假脸、磨皮蜡皮；禁止少年风杂乱背景、空洞甜腻假笑、自拍抓拍、透视畸变、强行紧致年轻化。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional photorealistic portrait prompt expert exclusively for middle-aged and elderly men. This preset covers all mature male themes: home study, courtyard teahouse, outdoor scenery, light business, retro film, minimalist studio.
All styles strictly adhere to photorealistic baseline for men aged 40+, differentiated only by styling, lighting, tone and atmosphere, no illustration, anime or oil painting texture; depictions of young boys and teenagers are forbidden.
Light natural makeup, clean face without large blemishes, fully retain natural wrinkles, sagging facial tissue, faint age spots, fine dry lines, stubble and shaving shadow of mature male skin; reject plastic fake skin and artificially tightened youthful skin caused by heavy retouching.
All poses described with relaxed stiff limb structure for elder men, no vague words or exaggerated youthful movements. Clear light direction and soft shadow transition. Male subject dominates the frame, background only serves aging steady narrative atmosphere.
Completely retain user input style, clothing, scene, tone, pose and perspective. Only supplement professional details of photography, texture, light, aged skin, gray-white hair and beard, no irrelevant youthful decorations or props.
All costumes (wool suit, linen long gown, outdoor jacket, commuter overcoat) are high-end mature male portrait themes with restrained steady relaxed poses, no vulgar or deformed exaggerated body shapes.
Taboo: no weight symbols, redundant camera parameters, anime/cartoon/illustration, deformed anatomy, defective hands, over-retouched wax skin, messy youthful background, empty sweet fake smile, snapshot selfie, perspective distortion, forced youthful tightening.
Strictly output two formats without extra comments.
"""
        }
        # 唯一主预设模板，绑定中老年男性template_id，完全对齐参考层级结构
        self.preset_library = {
            "middle_elderly_male": {
                "template_id": "middle_elderly_male",
                "display_name": MIDDLE_ELDERLY_MALE["name"],
                "description": MIDDLE_ELDERLY_MALE["description"],
                # 中英双语前置约束 中老年男性专属
                "positive_constraints": {
                    "zh": "影视级超写实真人质感，40岁以上中老年男性硬朗松弛面部骨骼，眉眼唇皱纹分布天然轻微不对称；原生淡妆干净无大面积瑕疵，完整保留深浅皱纹、面部松弛肌理、淡老年斑、肤色不均、细微干纹、真实胡茬与剃须青印，零过度磨皮、无塑胶蜡皮、无AI网红模板脸；柔软分层花白/全白发丝，层次自然胡须，干净克制中老年男性生活化布景，松弛沉稳真人抓拍姿态，内敛睿智平静成熟情绪，无透视畸变。居家/茶室/户外/商务/胶片均为熟龄男性题材分支，不破坏岁月写实基线，姿态沉稳从容",
                    "en": "Cinematic photorealistic real human texture, stiff sagging facial bone structure unique to men over 40, natural slight asymmetry of eyes, eyebrows, lips and wrinkle distribution; light natural makeup without large blemishes, fully retain deep & shallow wrinkles, sagging facial texture, faint age spots, uneven skin tone, fine dry lines, real stubble and shaving shadow, no over-smoothing, no plastic wax skin, no AI influencer template face; soft layered gray-white hair, naturally layered beard, restrained daily scene matching elder men, relaxed steady snapshot pose, restrained wise calm mature emotion, no perspective distortion. Home/teahouse/outdoor/business/film are mature male theme branches only, never break aging realism baseline with steady calm posture"
                },
                # 中老年男性全风格细分专属规则
                "preset_rules": {
                    "zh": """
【中老年男性人像专属规则】
1. 通用基线：仅刻画40岁-70+熟龄男性，完整保留皱纹、面部松弛、淡老年斑、花白头发、层次胡须等原生年龄特征，禁止磨皮淡化、强行紧致年轻化；原生淡妆干净无大面积瑕疵，留存岁月肌理与自然毛孔，杜绝完美对称五官、蜡像假肤、光滑无胡茬下颌。
2. 亚洲中老年男性刻画：方正柔和松弛轮廓，平缓硬朗骨骼，浅淡分散老年斑，花白短发；胡须分短胡茬/修剪胡/薄络腮，带清晰剃须青印；适配书房、中式茶室、居家场景，窗纱暖漫射光，低饱和深棕、炭灰沉稳色系。
3. 欧美中老年男性刻画：立体深邃骨骼、深眼窝、清晰松弛下颌线，面部沟壑岁月纹理，银灰短发，厚重层次络腮胡；适配山间户外、极简商务、画廊，侧逆光/冷调天光，低饱和深灰、墨蓝暗调色系。
4. 书房成熟稳重风格：深色羊毛西装、针织内搭，坐姿沉思抓拍，木书桌椅、瓷杯道具，午后侧窗暖柔光，深灰深蓝主色调，凸显内敛思考气质。
5. 茶室睿智儒雅风格：亚麻长衫、针织开衫，品茶慢动作，竹帘滤柔光，竹木青瓷道具，米棕温润色系，平和沉静神态。
6. 户外风景纪实风格：防风户外冲锋衣、抓绒内搭，山间观景台，落日侧逆光，保留户外晒斑、古铜肤质，深棕炭灰搭配自然山川色彩，从容远眺神态。
7. 复古胶片纪实风格：轻微胶片暖颗粒，老旧民居/老街场景，工装、厚外套，暖褪色光影，完整保留胡须、面部岁月纹理，不弱化年龄痕迹。
8. 极简棚拍商务风格：纯色低饱和深色背景，均匀柔光箱布光，西装正装，聚焦面部须发、皱纹肌理，沉稳克制神态。
所有题材仅围绕熟龄男性创作，用户指定场景、服饰、视角优先保留，仅补充岁月肤质、银发胡须、成熟光影细节，不新增少年青年相关元素。
""",
                    "en": """
【Exclusive Rules for Middle-Aged and Elderly Male Portraits】
1. General baseline: Only depict men aged 40 to 70+, fully retain original aging marks including wrinkles, facial sagging, faint age spots, gray hair and layered beard; prohibit smoothing or forced youthful tightening. Light natural makeup without large blemishes, retain aged texture and natural pores, reject perfectly symmetrical facial features, wax fake skin and stubble-free smooth jaw.
2. Asian middle-aged & elderly men: Square soft sagging contour, gentle stiff bone, faint scattered age spots, gray short hair; stubble/trimming/thin beard with clear shaving shadow. Suitable for study, Chinese teahouse, home scenes, warm diffused window light, low-saturation dark brown & charcoal color palette.
3. Western middle-aged & elderly men: Stereo deep bone, deep eye sockets, clear sagging jawline, three-dimensional facial aging lines, silver-gray short hair, thick layered full beard. Suitable for mountain outdoors, minimalist business, galleries, side backlight / cool natural light, low-saturation dark gray & navy tone system.
4. Study steady mature style: Dark wool suit, knit innerwear, sitting thinking snapshot, wooden desk & chair, porcelain cup props, warm afternoon side window soft light, dark gray navy main tone, highlight restrained thinking temperament.
5. Teahouse wise elegant style: Linen long gown, knit cardigan, slow tea tasting movement, soft light filtered by bamboo curtain, bamboo & celadon props, warm beige brown palette, calm peaceful expression.
6. Outdoor landscape documentary style: Windproof outdoor jacket, fleece inner, mountain viewing platform, sunset side backlight, retain outdoor sun spots and bronze skin texture, dark brown charcoal matched natural mountain colors, calm overlooking expression.
7. Retro film documentary style: Slight warm film grain, old houses / old street scenes, workwear & thick coats, warm faded light, fully retain beard and facial aging texture without weakening age marks.
8. Minimal studio business style: Solid low-saturation dark background, even softbox lighting, formal suit, focus on facial hair and wrinkle texture, steady restrained expression.
All themes are only created for mature men, retain user-specified scenes, costumes and perspectives, only add details of aged skin, gray hair beard and mature light, no elements related to young boys or teenagers.
"""
                },
                "negative_base": {
                    "zh": "少年、青年、学生、粉嫩肌肤、马卡龙亮色、紧致少年轮廓、完美对称五官、零皱纹、无老年斑、过度磨皮无毛孔、塑料蜡皮、AI网红模板脸、僵硬影楼摆拍、空洞甜腻假笑、夸张活泼肢体、畸形手脚、多手指、透视畸变、高饱和荧光艳色、杂乱少年装饰、二次元插画、卡通动漫画风、面部大面积无瑕疵、强行紧致年轻化、乌黑假发、光滑无胡茬下颌、无剃须青印、整齐虚假统一胡须、年龄感丢失、油画滤镜、涂抹模糊质感",
                    "en": "Young boy, teenager, student, pink tender skin, macaron bright colors, tight youthful facial contour, perfectly symmetrical facial features, wrinkle-free skin, no age spots, over-smoothed poreless plastic wax skin, AI influencer template face, stiff studio pose, empty sweet fake smile, exaggerated lively limbs, deformed hands and feet, extra fingers, perspective distortion, oversaturated fluorescent bright colors, messy youthful decorations, anime illustration, cartoon art style, flawless face, forced youthful tightening, black wig, stubble-free smooth jaw, no shaving shadow, fake uniform neat beard, lost aging texture, oil painting filter, blurry smudged texture"
                }
            }
        }
        # 双输出格式指引 完全沿用原版无改动
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】三段连贯文字：第一段场景布光整体氛围；第二段人物姿态视线表情体态；第三段肤质发丝胡须服饰面料色彩调性，300‑600字纯画面描写。",
                "en": "[Natural Paragraph Mode] Three coherent paragraphs: scene‑lighting‑atmosphere; pose‑gaze‑expression‑body; skin hair beard fabric color tone, 300‑600 words pure visual description."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1.人种五官轮廓特征
2.风格与服饰造型定位
3.肤质毛发胡须原生细节
4.构图景别与视觉重心
5.视角方位与俯仰角度
6.姿态体态与表情神态
7.色彩配比与整体调性
8.专业布光方式与光影层次
9.画面精简约束与环境要求""",
                "en": """[Structured Mode] Output strictly in this order:
1. Ethnic facial features
2. Style and clothing positioning
3. Skin hair beard natural details
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
        