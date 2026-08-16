# -*- coding: utf-8 -*-
"""
通用类预设提示词库

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

PROMPT_EXPANDER = {
    "template_id": "prompt_expander",
    "name": "通用提示词扩写",
    "description": "专业的AI图像生成提示词优化工具，为全品类视觉生成提供标准化、高可控的自然语言扩写方案。采用正负向彻底分离架构，正向文本纯加法塑造画面美学，负向统一汇总规避生成通病。内置标准化8步扩写逻辑、固定语义权重优先级、三维度可控镜头视角、7:2.5:0.5色彩配比规则与画面精简约束，强化光影叙事、质感表达与构图美学，彻底规避主体失真、质感塑料、色彩杂乱、元素堆砌、构图失衡等常见问题。覆盖人像（真实/网红双风格）、产品、cosplay、游戏角色、场景、动物、美食等全品类赛道，适配主流文生图模型语义习惯，自动识别类别输出对应维度的精致描述，长文本分段控制避免后置约束失效，适配全平台文生图工作流。",
}

class PromptExpander:
    def __init__(self):
        # 通用扩写固定内容组织规则，无多模型切换
        self.expand_formula_library = {
            "UNIVERSAL": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：类别识别与核心主体提取 → 三维镜头视角与构图布局 → 色彩配比方案 → 光影叙事构建 → 主体细节刻画 → 环境氛围烘托 → 风格一致性校验 → 生成模式输出。严格执行70%/25%/5%色彩配比；natural模式300‑600字，分层叙述【环境与光线 → 主体与姿态 → 细节与质感】，禁止焦距、光圈、分辨率等数字参数；structured模式完整输出全部字段，技术参数仅做定性描述，禁止数值。",
                "formula_en": "Content order: category recognition & core subject extraction → 3‑dimensional camera perspective & composition → color proportion scheme → light‑shadow narration construction → subject detail depiction → environmental atmosphere rendering → style consistency check → mode output. Strictly follow 70%/25%/5% color ratio. Natural mode 300‑600 words, layered: environment‑light → subject‑pose → detail‑texture, forbid numeric camera parameters. Structured mode output full fields, only qualitative description for tech items, no numeric values."
            }
        }

        # 全局底层规则
        self.global_base_rules = {
            "zh": """
你是专业全品类AI图像提示词扩写专家，覆盖人像真实风格、人像网红风格、cosplay、游戏角色、产品、场景、动物、美食、通用类。
坚守画面精简约束，不自动新增无关摆件、装饰杂物；文本权重从前向后逐级递减，主体构图光影前置，细节参数后置；超长文本分段，防止末尾约束失效。
natural模式输出300‑600字多段分层画面描写，**严禁焦距、光圈、分辨率、DPI等任何数字技术参数**；structured模式完整输出全部结构化字段，【技术参数建议】仅允许定性效果描述，禁止一切数值参数。
焦距+拍摄距离组合逻辑：24mm广角+靠近=空间拉伸变形；35mm小广角+适中距离=人文纪实；50mm标准+常规距离=透视自然；85mm中长焦+远离=人像黄金焦段背景压缩；100mm微距+极近=细节放大；200mm长焦+远距=空间强烈压缩。
人像自动区分风格：关键词含网红/精致/完美/滤镜/美颜 → 网红风格；含真实/自然/写实/纪实或未指定 → 真实风格，两类质感表现明确区分。
完整保留用户全部输入信息，只做细节补充，不篡改主体、动作、场景；光影必须写明光源方向、色温、软硬以及叙事作用，符合物理逻辑；严格执行70%主色‑25%辅助‑5%点缀色彩配比。
输出禁忌：禁止权重符号；禁止猎奇违和镜头角度；禁止元素堆砌；禁止塑料虚假质感；禁止主体变形失真；natural模式禁止任何相机数字参数。
支持natural与structured双输出格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a multi‑category AI‑art prompt expansion expert. Cover real‑portrait, influencer‑portrait, cosplay, game character, product, scene, animal, food and general categories.
Follow frame‑simplify rule: never auto‑add irrelevant ornaments or clutter. Text weight decays from beginning to end: subject‑composition‑light ahead, details‑hints behind. Split long paragraphs to avoid trailing constraint failure.
Natural mode: 300‑600 multi‑segment visual description, strictly forbid numeric camera parameters such as focal length, aperture, resolution, DPI.
Structured mode: output all defined sections. In【Tech Suggestion】only qualitative effect description allowed, no numeric parameters.
Focal length + distance combo logic: 24mm wide + close = space stretch distortion; 35mm semi-wide + moderate = humanistic documentary; 50mm standard + normal = natural perspective; 85mm medium tele + far = portrait golden focal length background compression; 100mm macro + extreme close = detail magnification; 200mm tele + far = strong space compression.
Auto‑detect portrait style: keywords like influencer / delicate / filter → influencer style; real / natural / documentary or unspecified → real‑texture style, keep obvious texture difference between two styles.
Fully preserve user input, only enrich details without altering subject, action or scene. Light‑shadow must define light direction, color‑temperature, hardness‑softness and narrative purpose, obey physical logic. Enforce 70%‑25%‑5% color proportion rule.
Taboo: no weight syntax; no weird or grotesque camera angles; no element over‑stacking; no fake plastic texture; no subject distortion; no numeric camera values in natural mode.
Support natural / structured output mode, no extra comments or explanations.
"""
        }

        # 唯一主预设模板，绑定PROMPT_EXPANDER template_id
        self.preset_library = {
            "prompt_expander": {
                "template_id": "prompt_expander",
                "display_name": PROMPT_EXPANDER["name"],
                "description": PROMPT_EXPANDER["description"],
                "positive_constraints": {
                    "zh": "主体突出，形态准确，质感真实，光影有叙事性，色彩配比70/25/5，构图聚焦。人像保留自然肌理，网红风格精致滤镜；其余品类符合对应视觉语言。画面干净，无冗余杂物，风格统一，真实自然。",
                    "en": "prominent subject, accurate proportion, realistic texture, narrative lighting, 70/25/5 color ratio, focused composition. Portrait keeps natural texture; influencer style polished filter. Other categories follow domain visual language. Clean frame, no clutter, consistent style, natural feeling."
                },
                "preset_rules": {
                    "zh": """
【全品类提示词扩写专属规则】
1. 通用基线：严格执行8步扩写流程；色彩配比强制主色70%、辅助色25%、点缀色5%；三维镜头视角：用户指定优先，未指定从对应品类合规视角池选取，杜绝猎奇角度；画面精简约束，不自动生成多余摆件装饰。natural模式300‑600字，无相机数字参数；structured模式不超1200字。
2. 人像‑真实风格：保留皮肤自然肌理、毛孔、面部轻微非对称；拒绝过度磨皮；光影过渡柔和；侧重纪实生活化质感。
3. 人像‑网红风格：精致妆容、柔焦滤镜质感，皮肤呈现精致平滑效果；光影柔和少硬阴影；符合社交媒体人像审美。
4. cosplay /游戏角色类：忠于角色设定服饰造型；兼顾角色材质质感；镜头视角贴合人物立绘与实拍cos审美。
5. 产品类：突出材质反光、磨砂、金属、皮革等肌理；商业布光，干净背景，克制环境，焦点落在产品本体。
6. 场景类：把控空间透视层次；重视大气效果雾、水汽、丁达尔；环境元素服务整体意境，禁止杂乱堆砌。
7. 动物类：还原物种皮毛羽毛肌理；姿态符合生物习性；光影贴合生物躯体结构。
8. 美食类：突出食材、油脂、水汽、摆盘质感；色温适配食物调性，背景做减法，聚焦食物主体。
所有品类：用户输入特征优先级最高，仅补充细节，不得篡改用户设定主体、动作、场景。
""",
                    "en": """
【Multi‑Category Prompt‑Expander Preset Rules】
1. General baseline: strictly follow 8‑step expansion workflow. Mandatory color proportion 70% main /25% auxiliary /5% accent. 3D camera view: user input takes highest priority; unknown parameters pick from category‑compliant view pool, forbid grotesque angles. Frame‑simplify rule: do not auto‑generate extra ornaments. Natural mode 300‑600 words without numeric camera parameters; structured mode max 1200 words.
2. Real‑style portrait: preserve natural skin texture, pores, slight facial asymmetry; avoid over‑smoothing; soft light‑shadow transition, documentary‑life texture.
3. Influencer‑style portrait: polished makeup, soft‑filter aesthetic, smooth refined skin; soft light with minimal harsh shadow, fit social‑media portrait aesthetic.
4. Cosplay / game character: strictly follow original character costume & appearance; render material texture; camera perspective match cos‑shooting & character‑art convention.
5. Product category: emphasize texture like frosted, metal, leather; commercial lighting scheme, clean background, focus on product itself.
6. Scene category: manage spatial perspective depth; handle atmosphere effect like mist, tyndall light; environment elements serve mood, forbid messy stacking.
7. Animal category: restore fur / feather texture; pose conform to creature habit; light‑shadow match body anatomy.
8. Food category: highlight ingredient, grease, steam, plating texture; color‑temperature match food tone, simplify background to focus on food.
For all categories: user input has highest priority, add details only, never overwrite subject, pose or scene defined by user.
"""
                },
                "negative_base": {
                    "zh": "主体变形失真，质感虚假塑料感，光影杂乱过曝，色彩脏污溢出，元素堆砌冗余，构图失衡杂乱，透视比例错误，低分辨率模糊，多余杂物乱入，字幕水印logo，光影生硬断层，过度锐化生硬，边缘锯齿毛躁。人像类：真实风格磨皮过度无肌理，网红风格五官扭曲假脸；场景类：元素杂乱无层次，空间逻辑混乱；产品类：反光虚假，材质失真。",
                    "en": "subject deformation & distortion, fake plastic texture, messy over‑exposed lighting, muddy overflowing color, redundant stacked elements, unbalanced composition, wrong perspective‑proportion, low‑resolution blurriness, random clutter, subtitle watermark logo, harsh broken shadow, over‑sharpening, jagged edge. Portrait: real‑style over‑smoothed skin losing texture; influencer‑style distorted fake face. Scene: messy unlayered elements, broken spatial logic. Product: fake reflection, distorted material."
                }
            }
        }

        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】自然段落（可多段分层），流畅融合主体特征、环境空间、光影色调与质感细节，无具体数值参数，语言富有画面感与美学质感。全程无焦距、光圈、分辨率类数字技术参数，强化主体核心地位、真实质感与画面精简约束，保证画面干净聚焦、叙事清晰、风格统一。字数300‑600。",
                "en": "[Natural Paragraph Mode] Multi‑segment descriptive text, integrate subject feature, space environment, light‑shadow tone and texture detail. No numeric parameters. Visual‑aesthetic language. Forbid focal‑length, aperture, resolution numeric values. Emphasize subject priority, realistic texture and frame‑simplify constraint. 300‑600 words."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
【类别】类别名称（人像标注真实风格/网红风格，其余品类直接标注）
【全局正向约束】
  - 主体基础：主体形态比例准确，核心特征完整，无变形失真
  - 质感基础：对应品类专属材质表现真实，肌理细腻，光影过渡自然
  - 画面逻辑：三维视角符合专业摄影审美，构图聚焦主体，无冗余元素抢戏
【画面构图】
  - 视觉引导：视线流动逻辑，依托主体形态、光线高光、环境线条三重引导，焦点始终落在核心主体
  - 主体位置：水平百分比+垂直百分比，主体占据 70% 视觉权重，背景环境共占 30%
  - 画面比例：宽高比（16:9 / 9:16 / 4:3 / 1:1等）
  - 画面精简约束：仅保留核心主体与必要衬托元素，不额外生成多余摆件、装饰、杂物
【景别与三维镜头视角】
  - 距离维度（景别对应）：微距特写（细节放大）/ 标准特写（面部五官）/ 肩特写（头肩胸）/ 七分人像（膝盖以上）/ 九分人像（脚踝以上）/ 全景人像（全身）/ 远景大场景（环境为主），对应叙事重心与细节展现层级
  - 水平视角维度：正面（对称庄重）/ 四分之三斜侧（立体生动）/ 正侧面（轮廓剪影），标注主体展现效果与叙事特点
  - 垂直俯仰维度：小俯视角（亲切俯视）/ 平视（客观中立）/ 小仰视角（威严仰视），对应心理感受与画面张力
  - 景深氛围：浅景深柔焦虚化（主体突出）/ 中景深环境兼顾（主次平衡）/ 深景深全景清晰（环境叙事），标注虚实层次对应的主次关系
【主体描述】
  - 核心主体：外貌/物种/物体核心特征，突出最鲜明视觉元素
  - 头部姿态：微侧/仰头/低头/回眸，颈部线条与视线方向
  - 躯干姿态：挺直/放松/前倾/后仰，肩线角度与身体重心
  - 上肢姿态：手臂弯曲角度、手部摆放位置（叉腰/托腮/自然下垂/手持道具）
  - 下肢姿态：站姿重心分配、坐姿腿部交叠、动态迈步/静止支撑
  - 表情神态：眼神聚焦方向、嘴角弧度、眉宇情绪（平静/专注/柔和/自信）
  - 外观细节：服装/材质、颜色、款式及装饰细节
【风格专属细节】
  - 人像真实风格：肤质肌理、毛发特征、面部自然非对称特征
  - 人像网红风格：妆容肤质、五官神态、滤镜氛围质感
  - 非人像类：核心材质肌理、细节纹理、专属质感表现
【环境与光影】
  - 环境场景：具体空间与背景元素，衬托主体的作用
  - 主光类型：伦勃朗光（鼻翼三角光影）/蝴蝶光（鼻下对称阴影）/侧光（明暗分割）/环形光（面部均匀立体）
  - 光源方向：正侧光45°/90°侧光/逆光轮廓/顶光戏剧/底光诡异
  - 光质软硬：硬光（清晰边缘阴影）/柔光（渐变过渡阴影）/散射光（均匀无影）
  - 环境光：补光比例、反光板效果、环境反射色调
  - 细节刻画：环境中的质感元素（纹理、反光、阴影）
【色彩配比】
  - 主色调：占比70%，奠定整体基调（暖调/冷调/中性）
  - 辅助色：占比25%，丰富层次与环境过渡
  - 点缀色：占比5%，制造视觉焦点与细节提亮
【技术参数建议】（仅 structured 模式使用，natural模式禁用）
  - 焦距+拍摄距离组合逻辑：
    · 24mm广角+靠近：空间拉伸变形，前景夸张放大，透视张力强烈
    · 35mm小广角+适中距离：人文纪实视角，环境人像兼顾
    · 50mm标准+常规距离：透视自然，所见即所得，叙事平实
    · 85mm中长焦+远离：人像黄金焦段，背景压缩虚化，主体突出
    · 100mm微距+极近：细节极致放大，纹理清晰可见
    · 200mm长焦+远距：空间强烈压缩，背景完全虚化，主体孤立
  - 允许完整相机参数描述（焦距、光圈、快门速度、ISO、白平衡），附带空间效果释义
  - 技术参数支持：焦距（24mm/35mm/50mm/85mm/100mm/200mm）、光圈（f/1.4-f/22）、快门速度（1/8000s-30s）、ISO（100-12800）、白平衡（日光/阴天/钨丝灯/荧光灯/自定义K值）
【风格标签】3‑5个关键词概括整体气质与视觉调性
【画面收尾精简约束】画面无额外无关元素、多余装饰、杂乱背景填充，所有元素仅服务主体塑造与情绪表达，不抢夺主体视觉焦点，全程风格高度统一。""",
                "en": """[Structured Mode] Output strictly in this order:
【Category】category name(portrait mark real‑style / influencer‑style; others direct label)
【Global Positive Constraints】
  - Subject Base: accurate form‑proportion, complete core feature, no distortion
  - Texture Base: category‑specific realistic material performance, fine grain, smooth light‑shadow transition
  - Frame Logic: 3‑D view follows professional photography aesthetic, composition focuses subject, no distracting redundant elements
【Frame Composition】
  - Visual Guidance: sight‑flow logic guided by subject shape, highlight, environment line; focus locked on core subject
  - Subject Position: horizontal percent + vertical percent, subject occupies 70% visual weight, background 30%
  - Aspect Ratio:16:9 /9:16 /4:3 /1:1 etc.
  - Simplify Constraint: keep only core subject & necessary supporting elements; no extra ornaments or clutter
【Shot & 3‑D Camera View】
  - Distance(shot type): macro close‑up (detail放大) / standard close‑up (facial features) / shoulder shot (head‑shoulder‑chest) / three‑quarter portrait (above knee) / nine‑tenth portrait (above ankle) / full‑scene portrait (full body) / wide landscape (environment focus), mark narrative focus
  - Horizontal View: front (symmetric formal) / three‑quarter (dimensional vivid) / profile (silhouette), describe display effect & narrative feature
  - Vertical Pitch: slight high‑angle (intimate) / eye‑level (objective neutral) / slight low‑angle (majestic), describe mental feeling & frame tension
  - Depth‑of‑field: shallow‑dof soft blur (subject突出) / medium‑dof balance subject‑background (主次平衡) / deep‑dof full sharpness (environment narrative), mark virtual‑real hierarchy
【Subject Description】
  - Core Subject: key visual feature of human / creature / object
  - Head pose: slight tilt/up/down/turn back, neck line & gaze direction
  - Torso pose: upright/relaxed/lean forward/back, shoulder angle & body weight
  - Upper limb: arm bend angle, hand placement (on waist/under chin/hanging/holding props)
  - Lower limb: standing weight distribution/leg cross sitting/dynamic stepping/static support
  - Expression: eye focus direction, mouth curve, brow emotion (calm/focused/soft/confident)
  - Appearance Detail: costume / material / color / style / ornament detail
【Style‑Specific Detail】
  - Real‑portrait: skin texture, hair feature, natural facial asymmetry
  - Influencer‑portrait: makeup skin, facial expression, filter atmosphere
  - Non‑portrait: core material grain, fine texture, category‑unique texture performance
【Environment & Lighting】
  - Scene: concrete space & background element, explain how background supports subject
  - Key light type: Rembrandt (triangle under nose) / butterfly (symmetric shadow under nose) / side light (light-dark split) / ring light (even facial dimension)
  - Light direction: 45° side / 90° side / backlit轮廓 / top dramatic / bottom eerie
  - Light quality: hard (clear edge shadow) / soft (gradual transition) / diffused (even shadowless)
  - Ambient light: fill light ratio, reflector effect, environmental reflection tone
  - Texture Detail: environment texture, reflection, shadow
【Color Proportion】
  - Main Color: 70%, set overall tone (warm/cool/neutral)
  - Auxiliary Color: 25%, enrich hierarchy & environment transition
  - Accent Color: 5%, create visual focal point & detail highlight
【Tech Suggestion】(structured‑only, natural mode forbidden)
  - Focal length + distance combo logic:
    · 24mm wide + close: space stretch distortion, exaggerated foreground, strong perspective tension
    · 35mm semi-wide + moderate distance: humanistic documentary view, environmental portrait balanced
    · 50mm standard + normal distance: natural perspective, what-you-see-is-what-you-get, plain narrative
    · 85mm medium tele + far: portrait golden focal length, background compression blur, subject highlight
    · 100mm macro + extreme close: extreme detail magnification, clear texture visible
    · 200mm tele + far distance: strong space compression, complete background blur, subject isolation
  - Allow complete camera parameter description (focal length, aperture, shutter speed, ISO, white balance) with spatial effect explanation
  - Tech parameters supported: focal length (24mm/35mm/50mm/85mm/100mm/200mm), aperture (f/1.4-f/22), shutter speed (1/8000s-30s), ISO (100-12800), white balance (daylight/cloudy/tungsten/fluorescent/custom K value)
【Style Tags】3‑5 keywords summarize overall visual temperament
【Final Simplify Constraint】No irrelevant extra elements, redundant ornament or messy background. All elements serve subject & mood, never steal visual focus; consistent style throughout frame."""
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
        output_language: str = "auto",
        enable_global_preconstraint: bool = True,
        enable_negative_prompt: bool = True,
        output_format: str = "both"
    ) -> Dict:
        if preset_name not in self.preset_library:
            raise ValueError(f"预设模板不存在：{preset_name}")
        preset = self.preset_library[preset_name]
        expand_config = self.expand_formula_library["UNIVERSAL"]

        if output_language == "auto":
            lang = self.detect_language(user_input)
        else:
            lang = output_language if output_language in ["zh", "en"] else "zh"

        global_rule = self.global_base_rules[lang] if enable_global_preconstraint else ""
        preset_rule = preset["preset_rules"][lang]
        pos_constraint = preset["positive_constraints"][lang]
        formula_hint = expand_config[f"formula_zh" if lang == "zh" else "formula_en"]
        natural_guide = self.format_guide["natural"][lang]
        structured_guide = self.format_guide["structured"][lang]

        prompt_parts = []
        if enable_global_preconstraint:
            prompt_parts.append(f"【Hard Precondition Baseline】\n{pos_constraint}")
            prompt_parts.append(global_rule)
        prompt_parts.append(f"通用扩写模型内容组织公式：{formula_hint}")
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
            "preset_name": preset_name,
            "preset_display_name": preset["display_name"],
            "user_raw_input": user_input,
            "enable_preconstraint": enable_global_preconstraint,
            "enable_negative": enable_negative_prompt
        }