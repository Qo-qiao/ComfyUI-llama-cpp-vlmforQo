# -*- coding: utf-8 -*-
"""
美食摄影预设提示词库

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

FOOD_PHOTOGRAPHY = {
    "template_id": "food_photography",
    "name": "美食摄影",
    "description": "专业美食摄影指导，为全品类美食打造高可控食欲感视觉描述。语义权重优先级：美食类型焦点→三维视角构图→场景氛围→色彩配比→食物细节质感→光影食欲设计。内置三维度视角、70%/25%/5%色彩配比、双重质感约束与画面精简约束，以「不完美的真实感」为核心，通过轻微焦痕、酱汁流淌、自然热气强化手工可信度。覆盖甜点、中式、西餐、饮品、小吃等品类赛道。",
}

class FoodPhotography:
    def __init__(self):
        # 下游生图模型内容组织公式库
        self.model_formula_library = {
            "Flux1": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体美食场景食欲光影 → 食物主体形态质感 → 餐具简约留白。侧重美食食欲叙事，弱化细碎关键词堆砌，画面治愈高级。",
                "formula_en": "Content order: overall food scene appetite lighting → food shape texture → tableware blank. Focus on appetite narration."
            },
            "Flux2_klein": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：美食品类核心食欲焦点 → 光影立体层次 → 食材餐具质感 → 克制背景。平衡食物肌理细节与治愈氛围感，光影贴合实物拍摄逻辑。",
                "formula_en": "Content order: food core appetite focus → light volume layers → ingredient tableware texture → restrained background. Balance food texture and warm atmosphere."
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：食物肌理细节优先 → 美食透视轮廓 → 三维拍摄视角构图 → 分层美食布光 → 极简餐具。严格把控食材比例无畸变，统一甜点/中餐/西餐质感标准。",
                "formula_en": "Content order: food texture details first → food perspective outline → 3D shooting composition → layered food lighting → minimalist tableware. Strict food proportion control."
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：构图视觉核心食物 → 食材形态食欲点 → 70/25/5色彩管控 → 光影明暗层次 → 干净背景。构图规整克制，色彩配比严格，虚实过渡柔和自然。",
                "formula_en": "Content order: composition core food → ingredient appetite point → 70/25/5 color control → light shadow layers → clean background. Neat composition, natural depth transition."
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：全局食欲光影基调 → 食物诱人特质 → 食材肌理细节 → 碗盘面料 → 极简布景。强化美食食欲光影叙事，区分甜点/中式专属布光体系。",
                "formula_en": "Content order: global appetite light tone → food attractive feature → ingredient texture → dish fabric → minimalist set. Strengthen appetite light narration."
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整张美食基础基调 → 舒展食材形态 → 统一食物真实质感 → 简约餐具留白。极简美食叙事，删减冗余摆件，突出食物主体。",
                "formula_en": "Content order: whole food basic tone → relaxed ingredient shape → unified real food texture → simple tableware blank. Minimal food narration."
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：食物透视肌理 → 远近餐具层次 → 光影冷暖过渡 → 配料细节 → 轻量化留白。食材透视精准，酥脆绵密质感区分清晰，光影连贯柔和。",
                "formula_en": "Content order: food perspective texture → tableware layers → light warm transition → ingredient details → lightweight blank. Accurate food perspective."
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：美食整体食欲气质 → 食材肌理细节 → 专业分层布光 → 品类专属餐具 → 极简留白。整体色调统一，食欲细节细腻，美食沉浸感强烈。",
                "formula_en": "Content order: overall food appetite temperament → ingredient texture → professional layered lighting → category exclusive tableware → minimalist blank. Unified tone, strong food immersion."
            }
        }
        # 全局底层规则
        self.global_base_rules = {
            "zh": """
你是专业美食摄影提示词扩写专家，覆盖甜点烘焙、中式料理、西餐、饮品咖啡、小吃全美食赛道。
所有创作坚守食欲叙事基线，仅食材品类、拍摄视角、餐具、光影差异化，禁止多类食材杂乱混搭。
画面遵循70%食物视觉主体，餐具环境占30；色彩固定70主/25辅/5点缀配比，低饱和暖调提升食欲。
光影贴合美食拍摄逻辑，甜点柔光绵密、中餐暖油光、西餐逆光焦香、饮品通透反光；统一保留手工不完美肌理（焦痕/酱汁/气泡）。
完整保留用户输入美食品类、画幅、视角、核心卖点全部信息，仅补充食材肌理、布光、餐具专业细节，不自动新增多余配菜摆件。
画面执行精简约束，仅留存核心食物与必要衬托餐具，杜绝过度完美3D假质感。
输出禁忌：禁止权重符号、焦距/光圈/分辨率等数值参数堆砌；禁止食材变形、塑料虚假肌理；禁止水印logo、完美零瑕疵描述。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional food photography prompt expert, covering dessert, chinese food, western dish, coffee, snacks.
All creations follow appetite narration baseline, differentiated by food type, view, tableware, lighting, no messy mixed ingredients.
70% food main subject, 30% tableware & background; fixed 70 main /25 secondary /5 accent warm color ratio.
Light matches food shooting rule: soft light for cream, warm oil light for chinese, backlight for roast, transparent for drinks; retain handmade imperfect texture (burn marks/sauce/bubbles).
Fully retain user food, frame, view, selling points, only add texture/light/tableware details without extra side dishes.
Strict simplification rule, only core food & necessary tableware, no fake perfect CG texture.
Taboo: weight symbols, focal/aperture/resolution numeric params; distorted food, fake plastic texture; watermark/logo, flawless description.
Strictly output two formats without extra comments.
"""
        }
        # 唯一主预设模板，绑定原有FOOD_PHOTOGRAPHY模板id
        self.preset_library = {
            "food_photography": {
                "template_id": "food_photography",
                "display_name": FOOD_PHOTOGRAPHY["name"],
                "description": FOOD_PHOTOGRAPHY["description"],
                # 中英双语固定前置正向约束
                "positive_constraints": {
                    "zh": "美食为绝对视觉主体，食材形态比例规整无畸变；70/25/5色彩配比和谐暖调，光影过渡柔和自然；天然手工不完美细节（焦痕、流淌酱汁、细小气泡、不均切面）完整保留；酥脆/绵密/油亮/通透肌理真实贴合食材物理属性；餐具克制虚化不抢夺焦点，场景氛围匹配美食调性，热气油脂光泽真实自然，画面干净克制，充满烟火治愈食欲感",
                    "en": "Food absolute main subject, regular ingredient shape without distortion; harmonious warm color ratio, soft light transition; reserved handmade imperfection (burn marks, flowing sauce, tiny bubbles, uneven cut); crispy/creamy/oily/transparent texture match physical logic; blurred tableware no distraction, natural steam & grease glow, clean warm appetite frame."
                },
                # 全美食细分专属规则
                "preset_rules": {
                    "zh": """
【全美食专属细分规则】
1. 通用基线：语义权重：美食类型焦点→三维视角构图→场景氛围→色彩配比→食材质感→食欲光影；用户画幅视角优先，严格70/25/5色彩配比，精简约束；禁用["8K", "4K", "分辨率", "DPI", "色彩模式", "焦距", "光圈", "帧率", "码率", "采样率", "编码器", "HDR", "杜比", "字幕", "水印", "logo", "完美对称", "零瑕疵", "塑料感", "崩坏", "扭曲"]。
2. 甜点烘焙：柔和单侧窗光，绵密奶油肌理，轻微烤焦边缘，果粒自然不均，浅木/粗陶餐具，低饱和暖柔色调。
3. 中式料理：前侧暖柔光，油亮酱汁流淌，表皮自然龟裂纹，陶瓷深碗，烟火暖棕主色，少量香料点缀。
4. 西餐炭烤：后侧轮廓逆光，网格炭烤焦痕，半透明油脂，深色石板，中饱和肉色调，迷迭香少量搭配。
5. 饮品咖啡：平视柔光，细腻奶泡不规则拉花，杯沿奶渍，浅木桌面，低饱和棕米配色。
6. 小吃零食：漫射天光，酥脆碎边，调味粉不均撒放，简约纸盘，暖黄接地气色调。
所有题材：用户需求优先级最高，仅补充食材、布光、餐具细节，不篡改核心美食与食欲卖点。
""",
                    "en": """
【Universal Food Exclusive Rules】
1. General baseline: Weight order: food focus > 3D composition > scene > color ratio > texture > appetite light; user frame priority, fixed color ratio; forbidden list: 8K,4K,resolution,DPI,color mode,focal length,aperture,frame rate,bit rate,sampling rate,encoder,HDR,dolby,subtitle,watermark,logo,perfect symmetry,flawless,plastic texture,collapse,distort.
2. Dessert: soft side window light, creamy texture, slight baked edge, uneven fruit, wood/ceramic tableware, warm low saturation.
3. Chinese food: front warm soft light, flowing glossy sauce, natural crack skin, dark ceramic bowl, warm brown tone, minor spices.
4. Western roast: back rim light, grill burn marks, translucent grease, dark stone plate, medium meat tone, rosemary foil.
5. Coffee drink: flat soft light, uneven latte art, milk stain on cup, light wood table, brown beige palette.
6. Snack: diffuse skylight, crispy broken edge, uneven seasoning, simple paper tray, warm earth tone.
All themes: user demand highest priority, only add food/light/tableware details without altering core selling points.
"""
                },
                "negative_base": {
                    "zh": "食材扭曲变形，肌理塑料CG假质感，光影过曝死黑，色彩脏灰杂乱，餐具堆砌抢主体，构图失衡焦点偏移，透视错误，低分辨率模糊，多余配菜杂物，装饰冗余，水印logo，热气僵硬不自然，油脂虚假反光，过度锐化锯齿，画面完美无手工痕迹，3D渲染虚假光滑感",
                    "en": "Distorted food, fake CG plastic texture, overexposed shadow, muddy color, overwhelming tableware, unbalanced composition, wrong perspective, blurry low-res, extra side dishes, redundant decor, watermark/logo, stiff steam, fake grease reflection, over-sharp jagged edges, flawless CG smooth surface."
                }
            }
        }
        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】2-3段连贯文字：首段画幅构图与整体治愈食欲氛围；第二段食材形态、手工不完美肌理与餐具搭配；第三段光影冷暖、70/25/5色彩与食欲感受；总字数300-600，全程规避焦距光圈等数值参数，美食食欲叙事画面感，无额外解释。",
                "en": "[Natural Paragraph Mode] 2-3 coherent paragraphs: frame & warm appetite atmosphere; food handmade texture & tableware; light color & tasting feeling; 300-600 words, no focal/aperture numeric params, food narration only."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1.美食品类与全局正向约束
2.画面构图、视觉引导、食物70%占比、画幅比例、精简约束
3.三维拍摄视角：距离、水平朝向、垂直俯仰、景深虚实
4.核心食欲焦点与情感触发点
5.食材外观、酥脆/绵密肌理、手工真实痕迹
6.光源色温、高光阴影、整体场景氛围
7.70/25/5分层色彩饱和度调性
8.餐具材质、桌面搭配逻辑
9.布光质感定性建议、全局禁止参数清单
10.3-5个概括美食食欲风格标签""",
                "en": """[Structured Mode] Output strictly in this order:
1. Food category & global constraints
2. Composition, visual guide, 70% food ratio, aspect ratio, simplification rule
3. 3D shooting: distance, horizontal, pitch, depth blur
4. Core appetite focus & emotional trigger
5. Food shape, crispy/creamy texture, handmade marks
6. Light source, highlight shadow, scene atmosphere
7. 70/25/5 layered color saturation
8. Tableware material & matching logic
9. Qualitative lighting suggestion, forbidden param list
10. 3-5 appetite style tags"""
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
