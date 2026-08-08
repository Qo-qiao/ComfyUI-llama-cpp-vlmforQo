# -*- coding: utf-8 -*-
"""
电商场景与产品摄影预设提示词库

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

ECOMMERCE = {
    "template_id": "ecommerce",
    "name": "电商场景与产品摄影",
    "description": "专业电商视觉与产品摄影指导，为全品类电商产品打造高转化视觉描述。语义权重优先级：产品类型卖点→三维视角构图→场景氛围→色彩配比→道具搭配→光影质感。内置三维度视角、70%/25%/5%色彩配比、双重质感约束与画面精简约束，强化产品质感、光影高级感与购买驱动力。覆盖美妆、3C、食品、首饰、家居等品类赛道。",
}

class Ecommerce:
    def __init__(self):
        # 下游生图模型内容组织公式库
        self.model_formula_library = {
            "Flux1": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体电商场景氛围布光 → 产品主体造型卖点 → 产品材质肌理 → 简约道具留白。侧重商品转化叙事，弱化细碎关键词堆砌，画面高级干净。",
                "formula_en": "Content order: overall e-commerce scene lighting → product shape selling points → product texture → simple prop blank. Focus on commodity conversion narration."
            },
            "Flux2_klein": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：产品品类核心卖点 → 光影立体层次 → 产品材质道具 → 克制简约背景。平衡产品质感细节与场景氛围感，光影贴合实物拍摄物理逻辑。",
                "formula_en": "Content order: product category core selling points → light volume layers → product texture props → restrained background. Balance product texture and scene atmosphere."
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：产品材质肌理细节优先 → 商品透视轮廓 → 三维拍摄视角构图 → 分层产品布光 → 极简道具。严格把控产品比例无畸变，统一美妆/3C/家居各类商品质感标准。",
                "formula_en": "Content order: product texture details first → commodity perspective outline → 3D shooting composition → layered product lighting → minimalist props. Strict product proportion control, unify texture standards."
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：构图视觉核心产品 → 产品形态卖点 → 70/25/5色彩管控 → 光影明暗层次 → 干净简约背景。构图规整克制，色彩配比严格执行，虚实景深过渡自然柔和。",
                "formula_en": "Content order: composition core product → product shape selling point → 70/25/5 color control → light shadow layers → clean background. Neat composition, fixed color ratio, natural depth transition."
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：全域场景光影基调 → 产品气质卖点表达 → 材质道具细节 → 面料石材肌理 → 极简布景。强化商品转化光影叙事，区分美妆/数码专属布光体系。",
                "formula_en": "Content order: full scene light tone → product selling expression → texture prop details → fabric stone texture → minimalist set. Strengthen conversion light narration, distinguish category lighting."
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体商品场景基调 → 舒展产品形态 → 统一产品质感 → 简约道具留白。极简电商叙事，删减冗余装饰摆件，突出商品核心主体。",
                "formula_en": "Content order: overall commodity tone → relaxed product shape → unified texture → simple prop blank. Minimal e-commerce narration, remove redundant ornaments."
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：产品透视与材质 → 远近道具层次 → 光影冷暖过渡 → 辅助摆件细节 → 轻量化留白。产品透视精准，金属/玻璃/膏体材质区分清晰，光影层次柔和连贯。",
                "formula_en": "Content order: product perspective & texture → prop layers → light warm transition → ornament details → lightweight blank. Accurate perspective, distinct material, soft lighting layers."
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：商品整体气质卖点 → 材质道具细节 → 专业分层产品布光 → 品类专属搭配 → 极简留白。画面色调统一协调，卖点刻画细腻，电商购买沉浸感强烈。",
                "formula_en": "Content order: overall product temperament → texture prop details → professional layered lighting → category matching → minimalist blank. Unified tone, delicate selling points, strong shopping immersion."
            }
        }
        # 全局底层规则
        self.global_base_rules = {
            "zh": """
你是专业电商产品摄影提示词扩写专家，覆盖美妆、3C数码、食品、首饰、家居全电商商品赛道，适配小红书/抖音/天猫多平台。
所有创作坚守商品转化叙事基线，仅产品品类、场景、道具、光影差异化，禁止多品类元素混搭造成画面杂乱。
商品永久为视觉绝对主体，遵循70%商品+30%场景道具权重；色彩固定70主/25辅/5点缀配比，杜绝高饱和撞色堆砌。
光影贴合实物拍摄逻辑，玻璃通透柔光、金属细腻反光、膏体柔和漫射、布艺温润漫光分品类区分。
道具仅衬托产品，不可抢夺视觉焦点，材质匹配商品定位（轻奢/ins/科技/复古）。
完整保留用户输入产品、平台、视角、场景、卖点全部信息，仅补充布光、材质、道具专业细节，不自动新增多余摆件杂物。
画面执行精简约束，仅留存叙事衬托核心道具，无冗余装饰。
输出禁忌：禁止权重符号、焦距/光圈/分辨率等数值参数堆砌；禁止产品变形畸变、塑料虚假材质；禁止杂乱堆砌、水印logo、完美零瑕疵描述。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are professional e-commerce product photography prompt expert, covering beauty, 3C, food, jewelry, home goods for all shopping platforms.
All creation follow commodity conversion baseline, differentiated by product type, scene, props, lighting, no mixed clutter.
Product is absolute subject, 70 product /30 scene weight; fixed 70 main /25 secondary /5 accent color ratio, no oversaturated collision.
Light matches real shooting logic, glass soft light, metal fine reflection, cream diffuse light categorized.
Props only foil product without stealing focus, texture match product positioning.
Fully retain user input product/platform/view info, only add light/texture details without extra clutter.
Strict simplification rule, only keep necessary foil props.
Taboo: weight symbols, focal/aperture/resolution numeric params; distorted goods, fake plastic texture, clutter, watermark, flawless description.
Strictly output two formats without extra comments.
"""
        }
        # 唯一主预设模板，绑定原有ECOMMERCE模板id
        self.preset_library = {
            "ecommerce": {
                "template_id": "ecommerce",
                "display_name": ECOMMERCE["name"],
                "description": ECOMMERCE["description"],
                # 中英双语固定前置正向约束
                "positive_constraints": {
                    "zh": "商品为画面绝对核心，形体比例规整无畸变，各类材质肌理真实贴合物理特性；70/25/5色彩配比和谐分层，光影过渡柔和无生硬断层；构图聚焦产品核心卖点，道具克制虚化不抢视觉；美妆膏体绵密通透、3C磨砂金属细腻、首饰金属宝石内敛反光、家居布艺温润；场景氛围匹配平台调性，营销信息自然融入不突兀，整体画面高级干净，具备真实商品可信度与购买驱动力",
                    "en": "Product absolute core, regular proportion without distortion, authentic physical texture; harmonious layered color ratio, soft light transition; composition focus on selling points, restrained blurred props; smooth cream, fine matte metal, subtle jewelry reflection, soft home fabric; scene fit platform tone, natural marketing info, high clean frame with shopping desire."
                },
                # 全品类细分专属规则
                "preset_rules": {
                    "zh": """
【全电商品类细分规则】
1. 通用基线：语义权重：产品类型卖点→三维视角构图→场景氛围→色彩配比→道具搭配→光影质感；用户拍摄视角优先，无则选用商品合规角度；严格70/25/5色彩配比，画面精简约束；禁用["8K", "4K", "分辨率", "DPI", "色彩模式", "焦距", "光圈", "帧率", "码率", "采样率", "编码器", "HDR", "杜比", "字幕", "水印", "logo", "完美对称", "零瑕疵", "塑料感", "崩坏", "扭曲"]。
2. 美妆护肤：玻璃/亚克力通透柔光，膏体绵密哑光，低饱和ins浅调，大理石/棉麻简约道具，单侧柔和侧光，突出质地可视卖点。
3. 3C数码：磨砂金属低反光，冷调中性色，纯色织物极简背景，多角度均匀柔光，对称规整构图，凸显精密做工。
4. 食品饮品：温润漫射天光，原木/陶瓷道具，暖柔和色调，微距展现肌理，虚化少量果蔬衬托自然新鲜。
5. 首饰配饰：45°微距侧光，金属细腻反光，丝绸绒布基底，低饱和暖调，少量绿植弱化金属冷硬。
6. 家居用品：大面积柔和漫光，棉麻实木道具，低饱和大地色系，平视舒适视角，突出居家温润氛围。
所有题材：用户需求优先级最高，仅补充布光、材质、搭配专业细节，不改动产品与核心卖点。
""",
                    "en": """
【Universal E-commerce Category Rules】
1. General baseline: Weight order: product selling points > 3D composition > scene > color ratio > props > lighting; user view priority, fixed color ratio; forbidden words list: 8K,4K,resolution,DPI,color mode,focal length,aperture,frame rate,bit rate,sampling rate,encoder,HDR,dolby,subtitle,watermark,logo,perfect symmetry,flawless,plastic texture,collapse,distort.
2. Beauty: transparent glass soft light, matte cream, low saturation ins tone, marble/cotton props, side light show texture.
3. 3C digital: matte low-reflection metal, neutral cool tone, solid fabric background, even soft light, neat symmetry.
4. Food: warm diffuse skylight, wood/ceramic props, warm tone, macro texture, blurry fruit foil.
5. Jewelry: 45° macro side light, fine metal reflection, silk base, low warm tone, tiny green plants.
6. Home goods: full diffuse light, cotton wood props, earth tone, flat view, warm living vibe.
All themes: user demand highest priority, only add light/texture details without altering product selling points.
"""
                },
                "negative_base": {
                    "zh": "产品形体扭曲变形，材质塑料虚假，光影杂乱过曝死黑，色彩脏溢高饱和撞色，道具堆砌喧宾夺主，构图失衡焦点偏移，透视比例错误，低分辨率模糊，多余杂物摆件，水印logo字幕，光影生硬断层，营销贴纸突兀，过度锐化边缘锯齿，反光失真不自然，背景杂乱抢夺产品视觉焦点",
                    "en": "Distorted product, fake plastic texture, overexposed dead shadow, muddy oversaturated color, overwhelming props, unbalanced composition, wrong perspective, blurry low-res, clutter, watermark, stiff light, abrupt marketing sticker, over-sharp jagged edges, unnatural reflection, distracting background."
                }
            }
        }
        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】2-3段连贯文字：首段场景平台整体布光氛围；第二段产品形体、核心卖点与材质肌理；第三段道具搭配、色彩分层与购买氛围感；总字数300-600，全程规避焦距光圈等数值参数，电商转化叙事画面感，无额外解释。",
                "en": "[Natural Paragraph Mode] 2-3 coherent paragraphs: scene platform lighting; product shape selling texture; prop color shopping vibe; 300-600 words, no focal/aperture numeric params, e-commerce narration."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1.商品品类、适配平台与全局正向约束
2.画面构图、视觉引导、商品70%占比、画幅比例、精简约束
3.三维拍摄视角：景别距离、水平朝向、垂直俯仰、景深虚实
4.产品形态、核心吸引力与购买触发卖点
5.场景风格、配套道具材质搭配逻辑
6.产品专属肌理、主辅光色温软硬
7.70/25/5分层色彩饱和度调性
8.品类专属搭配元素、品牌营销融合方式
9.布光质感定性建议、全局禁止参数清单
10.3-5个概括商品电商气质风格标签""",
                "en": """[Structured Mode] Output strictly in this order:
1. Product category, platform & global constraints
2. Composition, visual guide, 70% product ratio, aspect ratio, simplification rule
3. 3D shooting: distance, horizontal, pitch, depth blur
4. Product shape, core selling attraction
5. Scene style & matching prop logic
6. Exclusive texture, key/fill light temp
7. 70/25/5 layered color saturation
8. Category matching & brand info integration
9. Qualitative lighting suggestion, forbidden param list
10. 3-5 e-commerce style tags"""
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
