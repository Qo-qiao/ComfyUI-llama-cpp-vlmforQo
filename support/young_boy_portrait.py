# -*- coding: utf-8 -*-
"""
真实感少年儿童人像预设提示词库

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

YOUNG_BOY_PORTRAIT = {
    "template_id": "young_boy_portrait",
    "name": "少年儿童人像",
    "description": "专业少年儿童超写实人像摄影指导，仅覆盖婴幼儿、学前、小学、13-17岁少年全孩童年龄段，区分亚洲/欧美孩童五官、稚嫩肤质、原生毛发特质。语义权重优先级：面部肤质五官孩童特质＞自然动态姿态服饰＞自然光影色彩＞生活化场景＞构图景别＞摄影参数。所有风格坚守孩童真人写实基线，仅氛围、穿搭、场景差异化，全程无成人化造型、成熟神态刻画，姿态灵动松弛无僵硬摆拍。",
}

class YoungBoyPortrait:
    def __init__(self):
        # 下游生图模型内容组织公式库 完全沿用参考原版无改动
        self.model_formula_library = {
            "Flux1": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面氛围光影 → 孩童气质灵动姿态 → 稚嫩肌肤胎发质感 → 童趣背景留白。侧重童真氛围叙事，弱化关键词堆砌，画面治愈柔和。",
                "formula_en": "Content order: overall atmosphere lighting → kid lively pose → tender skin baby hair texture → childlike negative space. Focus on innocent atmosphere narration."
            },
            "Flux2_klein": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：孩童核心稚嫩五官 → 光影立体层次 → 童趣服饰质感 → 简约克制环境。平衡童真细节与氛围感，光影过渡柔和通透。",
                "formula_en": "Content order: kid tender facial features → lighting layers → child clothing texture → restrained environment. Balance innocence and atmosphere."
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：孩童稚嫩肤质细节优先 → 圆润面部轮廓 → 灵动体态 → 生活化布光 → 极简童趣场景。极致还原孩童原生细嫩肌肤，杜绝面部畸变。",
                "formula_en": "Content order: kid tender skin texture first → round facial contour → lively body → daily lighting → minimalist child scene."
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：构图视觉重心 → 孩童灵动神态体态 → 马卡龙/多巴胺色彩管控 → 柔和光影层次 → 干净童趣背景。色彩鲜活低饱和，画面干净通透。",
                "formula_en": "Content order: composition focus → kid lively expression → macaron color control → soft lighting layers → clean child background."
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：治愈电影级柔光氛围 → 孩童鲜活肢体情绪 → 胶片细腻颗粒质感 → 棉质服饰面料 → 极简童趣布景。强化童真光影层次。",
                "formula_en": "Content order: cinematic soft light atmosphere → kid lively body emotion → film grain texture → cotton fabric → minimalist child set."
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体治愈画面基调 → 孩童松弛灵动姿态 → 原生细嫩肌肤质感 → 简约童趣留白环境。极简童真叙事，无冗余装饰。",
                "formula_en": "Content order: overall healing tone → kid relaxed lively pose → natural tender skin → simple child negative space."
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：孩童稚嫩五官肤质 → 灵动体态 → 柔和光影层次 → 童趣服饰细节 → 轻量化环境。强化圆润孩童面部立体感。",
                "formula_en": "Content order: kid tender skin features → lively body → soft lighting layers → child clothing details → lightweight environment."
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：孩童纯真主体气质 → 细嫩肤质胎发细节 → 生活化专业布光 → 童趣穿搭造型 → 极简场景。色彩鲜活柔和，神态纯粹写实。",
                "formula_en": "Content order: kid innocent temperament → tender skin hair details → daily lighting → child styling → minimalist scene."
            }
        }
        # 全局底层规则 改为少年儿童专用
        self.global_base_rules = {
            "zh": """
你是专业高端少年儿童超写实人像摄影提示词扩写专家，本模板为【孩童少年人像专用】，全覆盖婴幼儿、学前、小学、13-17岁少年；题材包含春日户外、森林探险、校园日常、居家童真、复古胶片、极简棚拍。
所有风格坚守**孩童真人超写实基线**，仅穿搭、场景、光影差异化，禁止成人化五官、成熟体态、虚假精致网红童颜，无二次元、插画、油画质感。
原生无厚重妆造，保留孩童细嫩毛孔、轻微运动泛红、浅浅晒痕、面部细小绒毛，拒绝塑胶假肤、极致磨皮零瑕疵皮肤。
姿态必须使用孩童灵动松弛肢体描述，禁用成人僵硬摆姿、成熟稳重动作；光线仅采用户外/居家自然柔光，禁用影楼硬舞台强光。
完整保留用户输入年龄、性别、场景、服饰、色调、姿态，仅补充孩童肤质、胎发、棉质面料、童真光影细节，不添加成人道具、成熟装饰。
所有孩童穿搭、户外造型、校园校服均为童真纪实人像，体态柔软灵动，禁止畸形肢体、夸张动作。
输出禁忌：权重符号、冗余相机参数、卡通二次元、畸形手脚、多手指、空洞假笑、成人沉稳神态、高饱和刺眼撞色、杂乱网红布景、透视畸变。
严格输出两种格式，不额外增加注释说明。
""",
            "en": """
You are a professional photorealistic portrait expert exclusively for kids and teenagers. This preset covers infants, preschool, primary school, teens aged 13-17, including outdoor spring, forest adventure, campus, home daily, retro film, minimalist studio.
All styles follow kid photorealistic baseline, no adult facial features, mature body, artificial perfect kid face; no anime, illustration, oil painting texture.
No heavy makeup, retain tender pores, natural flush from activity, faint sun marks, fine facial fuzz; reject plastic fake skin and fully smoothed flawless skin.
All poses described as lively relaxed kid movements, no stiff adult posing or mature gestures; only natural outdoor/soft indoor light, no harsh studio stage light.
Fully retain user input age, gender, scene, outfit, tone and pose; only add kid skin, baby hair, cotton fabric and innocent light details, no adult props or mature decorations.
All kid clothes, school uniform, outdoor wear are innocent documentary portraits with soft lively bodies, no deformed limbs or exaggerated movements.
Taboo: weight symbols, redundant camera parameters, anime, malformed hands, extra fingers, empty fake smile, mature calm expression, oversaturated clashing color, messy internet background, perspective distortion.
Strictly output two formats without extra notes.
"""
        }
        # 唯一主预设模板，绑定孩童专属template_id，层级完全对齐参考范例
        self.preset_library = {
            "young_boy_portrait": {
                "template_id": "young_boy_portrait",
                "display_name": YOUNG_BOY_PORTRAIT["name"],
                "description": YOUNG_BOY_PORTRAIT["description"],
                "positive_constraints": {
                    "zh": "影视级超写实真人质感，亚洲/欧美孩童原生圆润稚嫩面部骨骼，眉眼唇天然轻微不对称；无厚重妆造，完整保留细嫩毛孔、运动泛红、浅晒痕、细小绒毛，零过度磨皮、无塑胶假肤、无AI网红精致童颜；蓬松胎发细碎毛躁有通透感，生活化简约童趣布景，原生灵动抓拍姿态，纯粹治愈童真情绪，无透视畸变。户外/校园/居家/胶片/棚拍均为孩童题材分支，全程杜绝成人成熟体态与神态",
                    "en": "Cinematic photorealistic texture, round tender facial bone for Asian/Western kids, natural slight asymmetry of eyes, eyebrows and lips; no heavy makeup, fully retain tender pores, activity flush, faint sun marks, fine fuzz, no over-smoothing, no plastic fake skin, no AI perfect kid face; fluffy messy translucent baby hair, simple daily child scene, natural lively snapshot pose, pure healing innocent mood, no perspective distortion. Outdoor/campus/home/film/studio are kid-only themes, no mature adult body or expression."
                },
                "preset_rules": {
                    "zh": """
【少年儿童人像专属规则】
1. 通用基线：仅刻画1-17岁孩童少年，完整保留细嫩肌肤、胎碎发、孩童圆润脸型；禁止成人紧致轮廓、厚重磨皮、零瑕疵完美脸蛋、成熟沉稳神态。
2. 亚洲孩童刻画：柔和圆润娃娃脸，内双浅眼，乌黑透亮瞳孔，细腻薄嫩肌肤，浅淡晒红；适配公园、教室、居家卧室，午后漫射柔光，马卡龙低饱和配色。
3. 欧美孩童刻画立体柔和五官，多彩浅瞳色，蓬松浅棕/金胎发，通透白皙嫩皮；适配林间、郊外草坪，阴天漫射天光，多巴胺清新色系。
4. 春日户外童真风格：纯棉浅色系童装，气球/小花道具，草坪树荫斑驳柔光，动态追逐抓拍，鲜活治愈笑容。
5. 森林探险纪实风格：耐磨户外小外套，放大镜、甲虫、落叶道具，树冠细碎逆光，专注好奇孩童神态，保留户外晒痕薄汗。
6. 校园日常风格：宽松校服，课桌黑板场景，午后斜窗暖光，展示画作、手工等真实校园瞬间。
7. 复古胶片孩童风格：轻微暖胶片颗粒，老旧街巷、小院场景，宽松旧童装，不弱化肌肤细小绒毛与运动泛红。
8. 极简棚拍孩童风格：低饱和马卡龙纯色背景，均匀柔光箱，聚焦圆润面部与蓬松胎发，神态纯粹无刻意假笑。
所有孩童题材仅保留用户指定场景穿搭，只补充稚嫩肤质、胎发、童真光影细节，不加入成人相关元素。
""",
                    "en": """
【Exclusive Rules for Kid & Teen Portraits】
1. General baseline: Only depict kids 1-17, retain tender skin, fluffy baby hair, round kid face; no tight adult facial shape, heavy smoothing, flawless perfect face, mature calm expression.
2. Asian kids: Soft round baby face, shallow inner double eyelids, black clear pupils, thin tender skin, faint sun flush; suitable for park, classroom, bedroom, afternoon soft light, low-saturation macaron palette.
3. Western kids: Soft stereo facial features, light colorful pupils, fluffy light baby hair, translucent fair tender skin; suitable for forest, lawn, overcast natural light, fresh dopamine colors.
4. Spring outdoor innocent style: Cotton light kid clothes, balloon/flower props, dappled tree shade light, lively chasing snapshot, healing genuine smile.
5. Forest adventure documentary: Durable kid outdoor jacket, magnifier/beetle/leaf props, fragmented backlight from tree canopy, curious focused expression, retain outdoor sweat and sun marks.
6. Campus daily style: Loose school uniform, desk & blackboard scene, warm afternoon side window light, real moments of showing drawing and handcrafts.
7. Retro film kid style: Slight warm film grain, old alley/courtyard scene, loose vintage kid clothes, never erase fine skin fuzz and activity flush.
8. Minimal studio kid style: Low-saturation macaron solid background, even softbox light, focus on round face and fluffy baby hair, pure expression without forced fake smile.
All kid themes keep user specified scene & outfit, only add tender skin, baby hair and innocent light details, no adult related elements.
"""
                },
                "negative_base": {
                    "zh": "完美对称五官，零瑕疵肌肤，过度磨皮无毛孔，塑料蜡皮，AI网红精致童颜，成人僵硬摆姿，空洞程式假笑，成熟沉稳神态，畸形手脚，多手指，透视畸变，高饱和刺眼撞色，网红梦幻布景，二次元插画，卡通画风，成人服饰，紧致成熟面部，乌黑规整假发，肌肤无绒毛无晒痕，肌理完全丢失，多余路人杂乱装饰",
                    "en": "Perfect symmetrical facial features, flawless skin, over-smoothed poreless plastic wax skin, AI perfect kid face, stiff adult pose, empty fake smile, mature calm expression, deformed hands, extra fingers, perspective distortion, oversaturated harsh clashing color, internet dreamy background, anime illustration, cartoon style, adult clothes, tight mature face, neat black wig, no skin fuzz or sun marks, lost texture, messy extra strangers & decorations"
                }
            }
        }
        # 双输出格式指引 完全沿用参考原版无修改
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】三段连贯文字：第一段场景布光整体氛围；第二段孩童灵动姿态视线表情；第三段稚嫩肌肤胎发服饰面料色彩调性，300‑600字纯画面描写。",
                "en": "[Natural Paragraph Mode] Three coherent paragraphs: scene‑lighting‑atmosphere; kid lively pose gaze expression; tender skin baby hair fabric color tone, 300‑600 words pure visual description."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1.人种孩童五官轮廓特征
2.童真风格与穿搭造型定位
3.稚嫩肤质胎发原生细节
4.构图视觉重心与景别
5.视角方位俯仰角度
6.孩童灵动体态表情
7.马卡龙/多巴胺色彩配比
8.生活化专业布光方式
9.童趣画面精简约束""",
                "en": """[Structured Mode] Output strictly in this order:
1. Ethnic kid facial features
2. Innocent style & outfit positioning
3. Tender skin baby hair details
4. Composition & shot type
5. View angle & pitch
6. Kid lively pose & expression
7. Macaron/dopamine color ratio
8. Daily professional lighting
9. Child scene simplification rule"""
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
