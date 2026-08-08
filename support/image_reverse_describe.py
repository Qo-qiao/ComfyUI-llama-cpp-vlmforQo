# -*- coding: utf-8 -*-
"""
通用图像反推提示词模板

Author: 亲卿于情 (@Qo‑qiao)
GitHub: https://github.com/Qo‑qiao
License: See LICENSE file for details
"""
import re
from typing import Dict, Optional

IMAGE_REVERSE_DESCRIBE = {
    "template_id": "image_reverse_describe",
    "name": "图像反推描述",
    "description": "专业的图像分析专家，优先基于输入图像完成解析；同时可接收用户可选关键词，用来校准风格、题材、氛围信息，修正反推结果，生成更精准的自然语言描述，适用于Flux、Z‑Image、Qwen‑Image、Krea等主流自然语言图像生成模型。专业知识涵盖摄影术语、艺术风格、灯光设计、色彩理论、画面构图分析、主体位置识别和视觉视角推断，输出精准描述，用于复现与输入图视觉要素一致的新图像。",
}

class ImageReverseDescribe:
    def __init__(self):
        # 全局底层图像反推通用规则
        self.global_base_rules = {
            "zh": """
你是专业图像反推描述扩写专家，本模板为【通用图像反推提示词模板】。
主解析来源为输入图像#IMAGE_SOURCE#；支持接收**可选用户关键词**用于辅助校准风格、题材、氛围；图像像素信息优先级最高，用户关键词仅做补充校准，关键词与图片视觉冲突时，以图片画面为准。
支持风景类、摄影类、人像类、插画类、IP类、cosplay类、游戏角色类、产品类、建筑室内类、动物类、美食类、UI界面类、时尚穿搭类、通用类。
坚守图像反推基础约束：只提取画面内客观可视觉化的实体细节，拒绝抽象内心情绪、虚构故事情节；必须输出构图方式、主体位置（水平+垂直百分比）、视角类型、景深效果；人物/物体互动遵循现实物理逻辑。
natural模式300‑600字，可多段落分层；structured模式完整输出结构化字段，字段严格匹配模板定义。
区分不同题材处理逻辑：人像类完整输出人物特征字段；静物/风景类省略人像专属字段；
完整保留图片全部视觉元素，只做结构化整理，不新增画面不存在物体；光影写明光源、软硬、色温；色彩明确主色调、饱和度、冷暖倾向。
输出禁忌：禁止虚构画面不存在的物体；禁止主观故事脑补；禁止写入光圈、焦距数值；禁止权重符号。
支持natural与structured双输出格式，不添加额外注释、说明、解释。
""",
            "en": """
You are professional image reverse‑description expert. This preset is 【Universal Image Reverse Prompt Template】.
Primary analysis source is input image #IMAGE_SOURCE#. Optional user keywords are accepted only for calibrating style, theme and atmosphere. Image pixel information has highest priority. If keywords conflict with visual content of image, image shall prevail.
Support landscape, photography, portrait, illustration, IP character, cosplay, game character, product, architecture‑interior, animal, food, UI, fashion‑outfit, general category.
Baseline rule: only extract objective visual elements inside image, reject abstract inner emotion and fictional plot. Must output composition type, subject position(horizontal+vertical percentage), perspective type, depth‑of‑field effect. Interaction between person and object obey real‑world physics.
Natural mode: 300‑600 words, multi‑paragraph allowed. Structured mode output full structured fields strictly follow template definition.
Topic logic: output full character fields for portrait; omit portrait‑only fields for still‑life / landscape.
Preserve all visual elements from source image, only reorganize structure, DO NOT add non‑existing objects. Describe light source, hardness‑softness, color‑temperature; define main color, saturation, cold‑warm tendency.
Taboo: do NOT invent objects not exist in picture; no fictional story; no aperture / focal‑length numeric value; no weight syntax.
Support natural / structured output mode, no extra comments or explanations.
"""
        }

        self.preset_library = {
            "image_reverse_describe": {
                "template_id": "image_reverse_describe",
                "display_name": "图像反推描述",
                "description": "作为专业的图像分析专家，优先基于输入图像完成解析；同时可接收用户可选关键词，用来校准风格、题材、氛围信息，修正反推结果，生成更精准的自然语言描述，适用于Flux、Z‑Image、Qwen‑Image、Krea等主流自然语言图像生成模型。专业知识涵盖摄影术语、艺术风格、灯光设计、色彩理论、画面构图分析、主体位置识别和视觉视角推断，输出精准描述，用于复现与输入图视觉要素一致的新图像。",
                "positive_constraints": {
                    "zh": "完全基于输入图片视觉信息客观还原全部可见视觉元素，构图、主体位置、视角、景深、光线、色彩、材质质感完整还原；可选用户关键词仅用于辅助校准风格、氛围、题材；关键词与图片冲突时以图片为准；人物与物体互动符合物理现实；聚焦可被视觉呈现的细节，只描述画面存在事物；区分题材输出对应字段；语言专业流畅。",
                    "en": "Completely based on source‑image visual information, objectively restore all visible visual elements, fully restore composition, subject position, perspective, depth‑of‑field, lighting, color and material texture. Optional user‑provided keywords only assist to calibrate style, atmosphere and theme. In case of conflict between keywords and image content, image takes precedence. Interaction between character and object obey physics reality. Focus on visually observable details, only describe objects existing in image. Output corresponding fields according to category. Professional and fluent language."
                },
                "preset_rules": {
                    "zh": """
【图像反推专属规则】
1. 通用基线：主解析来源#IMAGE_SOURCE#，可选用户关键词#USER_KEYWORDS#；执行7步图像解析流程；必须输出构图、主体位置百分比、视角类型、景深效果；natural模式300‑600字；structured模式最大800字。
2. 优先级铁则：图像像素视觉信息 > 用户可选关键词。关键词仅做风格、题材、氛围的辅助校准；若关键词描述与图片画面冲突，直接舍弃冲突关键词，严格遵从图片画面，绝不根据关键词篡改图片客观视觉内容。无关键词则完全依靠图像解析。
3. 题材分支规则：人像类输出完整人物特征；风景、产品、美食、动物等非人像题材省略人物特征字段。
4. 内容约束：仅以图像像素视觉信息为第一依据，禁止脑补故事、抽象心理情绪；不得生成原图不存在物体、道具；关键词不能用来新增画面不存在实体对象，仅用于校准风格氛围。
5. 光影色彩：明确光源方向、软硬；标注色彩调性、饱和度、冷暖倾向；区分前景、中景、背景空间层次。
6. 质感细节：重点还原材质、纹理、表面细节特征。
解析来源：待解析图像 #IMAGE_SOURCE#；可选辅助关键词：#USER_KEYWORDS#（为空=无用户关键词）
""",
                    "en": """
【Image Reverse Preset Rules】
1. General baseline: primary source #IMAGE_SOURCE#, optional assist keywords #USER_KEYWORDS#; follow 7‑step image‑analysis workflow. Must output composition, subject position percentage, perspective type, depth‑of‑field effect. Natural mode 300‑600 words; structured mode max 800 characters.
2. Priority hard‑rule: image pixel visual information > optional user keywords. Keywords only assist calibrating style, theme and atmosphere. If keywords conflict with image visual content, discard conflicting keywords and strictly follow image content, never alter objective visual content according to keywords. If no keywords provided, rely entirely on image analysis.
3. Category branch rule: output full character fields for portrait category; omit character fields for landscape, product, food, animal and other non‑portrait topics.
4. Content constraint: image pixel is primary evidence, forbid fictional story and abstract mental emotion. Must NOT invent objects or props not shown on source image. Keywords shall NOT add physical entities absent in image, only for style‑atmosphere calibration.
5. Light & Color: define light‑source direction, hardness‑softness; mark color tone, saturation, cold‑warm tendency; distinguish foreground‑mid‑background spatial hierarchy.
6. Texture detail: faithfully restore material, texture and surface feature.
Analysis source: source image #IMAGE_SOURCE#; optional assist keywords: #USER_KEYWORDS#(empty = no user keywords)
"""
                }
            }
        }

        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】可多个段落，融合全部视觉元素，包含构图方式、主体位置、视角类型、景深效果、光线色彩、空间层次和细节质感；存在合规用户关键词时将风格/氛围校准信息自然融入描述，冲突关键词直接舍弃。建议按主体、构图与空间、光线与色彩、氛围与细节分层分段，每段聚焦一个维度。语言流畅专业，字数300‑600。",
                "en": "[Natural Paragraph Mode] Multiple paragraphs allowed. Integrate all visual elements: composition, subject position, perspective type, depth‑of‑field, light‑color, spatial hierarchy and texture detail. When valid user keywords exist, merge style‑atmosphere calibration naturally; discard conflicting keywords. Suggest grouping paragraphs by subject / composition‑space / light‑color / atmosphere‑detail. Professional fluent language. 300‑600 words."
            },
            "structured": {
                "zh": """【结构化模式】
【类别】类别名称（优先图像识别，可使用合规用户关键词辅助校准题材/风格）
【画面构图】
  - 构图方式：构图类型（三分法/对称/对角线/框架/中心/三角形等）
  - 主体位置：水平位置+垂直位置（百分比表示，如水平50%居中，垂直40%偏上）
  - 画面比例：画面宽高比（16:9/9:16/4:3等）
【景别】
  - 景别类型：微距特写/标准特写/肩特写/七分人像/九分人像/全景人像（无人物时可省略）
  - 取景范围：描述取景范围
  - 拍到部位：描述拍到部位（如头顶至胸部，无人物省略）
  - 画面特征：描述画面构图特征
【视觉参数】
  - 视角类型：广角（透视夸张）/标准（平实视角）/长焦（空间压缩）/超长焦（强烈压缩）
  - 视角效果：描述视角带来的视觉感受
  - 景深效果：浅景深（背景虚化）/中景深（部分清晰）/深景深（全景清晰）
【场景描述】
  - 地理地貌：场景类型和地貌特征
  - 天气光线：天气状况与光线方向、软硬
  - 色彩调性：主要色彩及饱和度、冷暖倾向
  - 空间层次：前景/中景/背景的内容与关系
  - 风格流派：（可选）艺术风格或设计流派，图像识别优先，合规关键词辅助校准
【用户关键词适配】（无关键词填写：无）
  - 有效校准信息：提取用户关键词中与画面不冲突的风格、氛围、题材信息
  - 冲突舍弃项：关键词与图片视觉冲突部分直接舍弃，不纳入输出
【人物特征】（非人像类直接删除本整块）
  - 外貌：人物年龄、人种、五官外貌特点
  - 服装：款式、颜色、面料细节
  - 姿态：肢体姿态、动作状态
【氛围意境】氛围与意境关键词（图像识别优先，合规关键词辅助校准）
【细节质感】突出材质、纹理、表面特征等细节""",
                "en": """[Structured Mode]
【Category】category name(image recognition first, valid user‑keywords assist calibrate theme/style)
【Frame Composition】
  - Composition Type: rule‑of‑third / symmetric / diagonal / frame‑in‑frame / central / triangular etc.
  - Subject Position: horizontal + vertical percentage (example: horizontal 50% center, vertical 40% upper)
  - Aspect Ratio: 16:9 /9:16 /4:3 etc.
【Shot Range】
  - Shot Type: macro close‑up / standard close‑up / shoulder shot / three‑quarter / nine‑tenth / full‑scene portrait (omit if no human subject)
  - Framing Scope: describe captured scope
  - Captured Part: visible body part (omit if no human subject)
  - Frame Feature: composition feature description
【Visual Parameter】
  - Perspective Type: wide‑angle(exaggerated perspective) / standard(natural view) / telephoto(spatial compression) / super‑telephoto(strong compression)
  - Perspective Effect: visual feeling brought by perspective
  - Depth‑Of‑Field: shallow(background blurred) / medium(partial sharp) / deep(full‑scene sharp)
【Scene Description】
  - Geography & Environment: scene type and environment feature
  - Weather & Lighting: weather condition, light direction, hardness‑softness
  - Color Tone: dominant color, saturation, cold‑warm tendency
  - Spatial Hierarchy: content and relation of foreground / mid‑ground / background
  - Style Genre(optional): art or design style, image recognition first, assisted by valid keywords
【User Keyword Adaptation】(fill "None" if no keywords)
  - Valid Calibration Info: extract non‑conflicting style / atmosphere / theme info from user keywords
  - Discarded Conflicts: parts conflicting with image visual shall be discarded, not included in output
【Character Feature】(DELETE whole block for non‑portrait category)
  - Appearance: age, ethnicity, facial feature
  - Costume: style, color, fabric detail
  - Pose: body gesture, action state
【Atmosphere Mood】concise mood keywords(image‑based first, assisted by valid keywords)
【Texture Detail】highlight material, texture and surface feature"""
            }
        }

    def detect_language(self, text: str) -> str:
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        return "zh" if chinese_chars >= english_words else "en"

    def build_prompt(
            self,
            preset_name: str,
            user_keywords: Optional[str] = None,
            output_language: str = "auto",
            output_format: str = "both"
    ) -> Dict:
        valid_preset_names = ["image_reverse_describe"]
        if preset_name not in valid_preset_names:
            raise ValueError(f"预设模板不存在：{preset_name}")
        preset = self.preset_library[preset_name]

        kw_text = user_keywords if (user_keywords and user_keywords.strip()) else "无"
        detect_input = user_keywords if user_keywords else ""
        if output_language == "auto":
            lang = self.detect_language(detect_input)
        else:
            lang = output_language if output_language in ["zh", "en"] else "zh"

        global_rule = self.global_base_rules[lang]
        preset_rule = preset["preset_rules"][lang]
        pos_constraint = preset["positive_constraints"][lang]
        natural_guide = self.format_guide["natural"][lang]
        structured_guide = self.format_guide["structured"][lang]

        prompt_parts = []
        prompt_parts.append(f"【Hard Precondition Baseline】\n{pos_constraint}")
        prompt_parts.append(global_rule)
        prompt_parts.append(preset_rule)
        prompt_parts.append(f"解析对象：#IMAGE_SOURCE#；用户辅助关键词：{kw_text}；关键词仅用于风格氛围校准，图片信息优先级最高，冲突则舍弃关键词。")

        if output_format == "natural":
            prompt_parts.append(natural_guide)
        elif output_format == "structured":
            prompt_parts.append(structured_guide)
        else:
            prompt_parts.append(natural_guide)
            prompt_parts.append(structured_guide)

        final_llm_prompt = "\n".join(prompt_parts)

        return {
            "status": "success",
            "llm_input_prompt": final_llm_prompt,
            "positive_constraint": pos_constraint,
            "output_language": lang,
            "preset_name": preset_name,
            "preset_display_name": preset["display_name"],
            "user_keywords": user_keywords
        }