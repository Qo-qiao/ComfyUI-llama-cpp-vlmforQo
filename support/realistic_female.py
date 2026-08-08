# -*- coding: utf-8 -*-
"""
亚洲女性人像预设提示词库

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

REALISTIC_FEMALE = {
    "template_id": "realistic_female",
    "name": "真实亚洲女性人像",
    "description": "真实感亚洲女性生活化人像写真摄影指导，覆盖古风汉服、日系校园、职场通勤、运动健身、婚纱礼服、街头潮牌、泳装、旗袍、异域风情、艺术人体/裸体艺术、cosplay等全风格场景。融合亚洲女性柔和五官、细腻肤质、原生不对称特质，打造真实自然、富有情绪故事感的生活化纪实人像，艺术人体类别侧重光影雕塑感与人体美学表达，规避影楼磨皮、AI假脸、模板网红脸。语义权重优先级：面部肤质五官＞姿态服饰＞光影色彩＞场景环境＞构图景别＞摄影参数。支持三维度视角受控组合，用户指定优先沿用，未指定按纪实风格审美随机匹配。",
}

class RealisticFemale:
    def __init__(self):
        # 下游生图模型公式库，完全复用参考原版无任何修改
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

        # 全局底层规则，纯纪实亚洲女性人像，无任何超写实相关词汇
        self.global_base_rules = {
            "zh": """
你是专业亚洲女性生活化纪实人像提示词扩写专家，本模板为【真实感亚洲女性人像】，覆盖古风汉服、日系校园、职场通勤、运动健身、婚纱礼服、街头潮牌、泳装、旗袍、异域风情、艺术人体、cosplay全题材。
所有风格坚守**真实纪实人像基线**，仅造型、光影、色调、氛围差异化，绝不出现二次元、插画、油画质感。
语义权重优先级：面部肤质五官＞姿态服饰＞光影色彩＞场景环境＞构图景别＞摄影参数。
姿态完整还原抓拍动态，禁止静态模板摆拍；光线使用窗光/斜阳等生活化实体具象光源，删除空洞文艺修辞；人物为绝对画面主体，环境仅服务人物叙事，不自动新增无关道具、路人、装饰。
严格执行主色70%、辅助色25%、点缀色5%色彩配比，统一标注饱和度层级，视觉留白舒适；全文优先强化亚洲女性单眼皮/内双、柔和眼型、细腻肤色、原生不对称等特质，保留毛孔、淡斑、细纹、肤色不均等真实肌肤痕迹，杜绝AI塑料假人脸。
完整保留用户指定场景、穿搭、色调、视角、情绪需求，仅补充肤质、发丝、面料、光影专业细节，不篡改用户原始内容。
输出禁忌：禁止权重符号、关键词冗余堆砌；禁止完美对称五官、零瑕疵磨皮塑料假皮、僵硬规整发丝、空洞假笑、无神凝视；禁止舞台强光、杂乱堆砌背景、极端猎奇俯仰、透视畸变；natural模式禁用全部光学数字参数，仅structured模式指定区块可使用焦距光圈并附带文字释义。
严格输出自然段落、结构化两种格式，不额外增加注释说明。
""",
            "en": """
You are a professional Asian female documentary portrait prompt expansion expert. This preset is [Realistic Asian Female Portrait], covering Hanfu, Japanese campus, workplace, fitness, wedding dress, street fashion, swimsuit, cheongsam, exotic style, artistic nude, cosplay themes.
All styles follow real documentary portrait baseline, differentiated only by styling, lighting, tone and atmosphere, no anime, illustration or oil painting texture.
Semantic priority: facial skin & features > pose & outfit > light & color > scene > frame > camera parameters.
All poses are captured dynamic moments, rigid template posing forbidden; light described with real daily light sources, empty literary rhetoric removed. Human subject dominates frame, background only serves narrative, no extra irrelevant props or passers-by.
Strict 70/25/5 color area ratio with saturation label, comfortable blank space. Prioritize native Asian female features: single/internal double-lid, soft eye shape, delicate skin, natural facial asymmetry, retain pores, faint spots, fine lines, uneven tone, no AI plastic fake face.
Fully keep user-specified scene, outfit, tone, perspective and mood, only add skin, hair, fabric, lighting details without altering user request.
Taboo: weight tags, redundant keywords; perfectly symmetrical face, flawless smoothed plastic skin, rigid neat hair, empty fake smile, blank stare; stage harsh light, cluttered background, extreme weird angles, perspective distortion. Natural mode blocks all optical numbers, only structured mode allows focal length & aperture with explanations.
Output natural text and structured two formats only, no extra notes.
"""
        }

        # 预设库绑定REALISTIC_FEMALE模板
        self.preset_library = {
            "realistic_female": {
                "template_id": REALISTIC_FEMALE["template_id"],
                "display_name": REALISTIC_FEMALE["name"],
                "description": REALISTIC_FEMALE["description"],
                # 中英正向约束，完全取自素材原文无修改
                "positive_constraints": {
                    "zh": "真实亚洲女性面部,左右眉眼唇形天然轻微不对称,单眼皮内双柔和眼轮廓,细腻肤色过渡,原生真实肌肤肌理保留毛孔淡细纹浅斑肤色不均,自然毛躁碎发与原生发丝层次,生活化场景环境仅衬托主体,自然抓拍松弛姿态,真实具象情绪,无刻意摆拍痕迹,视角符合纪实人像真实拍摄逻辑,三维度组合自然协调,无透视畸变与违和角度",
                    "en": "real Asian female face, natural slight asymmetry of brows eyes lips, single/internal double eyelids soft eye contour, delicate skin transition, original real skin texture with pores fine lines faint spots uneven tone, messy broken hair and natural hair layers, daily scene only foil subject, captured relaxed pose authentic emotion, no deliberate posing, perspective fits documentary portrait logic, balanced three-dimensional composition, no perspective distortion"
                },
                # 全题材细分专属规则，完整提取素材分类内容
                "preset_rules": {
                    "zh": """
【亚洲女性纪实人像全题材专属规则】
1. 通用基线：双重肤质约束（肤质+肌肤细节模块），保留毛孔、淡斑、细纹、肤色不均等原生肌理；面部天然不对称，拒绝无瑕完美皮；光源全部写实生活化，杜绝舞台硬光；色彩严格70/25/5配比，低饱和优先，禁止高饱和撞色堆砌。
2. 古风/汉服：平视微仰+四分之三侧七分景，柔和侧逆光，哑光汉服面料，清冷温婉气质。
3. 日系校园：平视小俯+四分之三侧中近景，春日漫射自然光，浅清新低饱和色调，青涩松弛神态。
4. 职场通勤：平视四分之三侧肩/七分特写，落地窗混合冷柔光，简约通勤穿搭，冷静从容气质。
5. 运动健身：小仰正面七分景，顶部均匀顶光，小麦健康肌肤带汗珠，力量松弛动态。
6. 婚纱礼服：平视侧方位九分/全景，日落侧逆光，薄纱蕾丝通透质感，温柔浪漫氛围。
7. 街头潮牌：平视斜侧七分景，日光/霓虹混合光，中低饱和撞色，随性抓拍动态。
8. 泳装：海边日间柔和日光，舒展松弛体态，清爽低饱和配色。
9. 旗袍：室内窗侧柔光，绸缎刺绣面料，东方雅致内敛气质。
10.异域风情：地域适配自然光，对应风格服饰，柔和复古色调。
11.艺术人体：纯白空间侧逆光，光影雕塑人体曲线，极简无多余道具。
12.cosplay：匹配角色专属场景光源，服饰纹理清晰，贴合角色情绪神态。
全部题材：用户指定景别、俯仰、水平视角必须优先执行；不自动生成无关行人、花草摆件，环境仅辅助叙事。
""",
                    "en": """
【Documentary Asian Female Portrait Theme Rules】
1. General baseline: Dual skin constraints (skin + detail module), retain pores faint spots lines uneven tone; natural facial asymmetry, no flawless skin; real daily light only, no harsh stage light; strict 70/25/5 color ratio, low saturation priority.
2. Hanfu: slight low eye level three-quarter medium shot, soft side backlight, matte fabric, gentle quiet vibe.
3. Japanese campus: slight high eye level three-quarter medium close-up, spring diffuse daylight, fresh low saturation, innocent relaxed mood.
4. Workplace: eye-level three-quarter shoulder/medium shot, cold window mixed soft light, simple commute wear, calm temperament.
5. Fitness: low angle front medium shot, even top light, wheat skin with sweat, relaxed strength movement.
6. Wedding dress: eye side medium/full shot, sunset side backlight, sheer lace, gentle romantic atmosphere.
7. Street fashion: eye-level three-quarter medium shot, mixed neon/daylight, medium-low contrast color, casual capture.
8. Swimsuit: seaside soft daylight, relaxed body, fresh low saturation tone.
9. Cheongsam: window side soft light, satin embroidery, restrained oriental elegance.
10. Exotic style: region-matched natural light, style costume, soft retro tone.
11. Artistic nude: pure white room side backlight, light sculpt body curve, zero extra props.
12. Cosplay: character matching light, clear costume texture, role-fitting expression.
All themes: User specified shot, pitch, horizontal angle take priority; no auto passers-by or extra ornaments, environment only supports narration.
"""
                },
                "negative_base": {
                    "zh": "完美对称五官,零瑕疵皮肤,人工对称双眼皮,厚重匀肤磨皮,塑料光滑哑光假皮,过度光滑肌肤,完全对称眉眼,厚重腮红,统一匀肤,过度美化皮肤,精致无瑕疵脸蛋,模板网红脸,空洞假笑,僵硬摆拍,刻意模特摆姿,多余肢体动作,无神凝视,多余绿植摆件,路人装饰杂物,杂乱背景,大量装饰,多余人物,舞台强光,画面堆砌元素,过度锐化,高饱和撞色,人工完美肌理,鸟瞰视角,虫眼视角,极端大俯大仰,透视畸变,肢体比例失调",
                    "en": "perfect symmetrical facial features, blemish-free skin, artificial double lids, heavy skin smoothing, plastic matte fake skin, over-smooth complexion, fully symmetric brows, heavy blush, unified even skin, flawless template influencer face, empty fake smile, stiff model pose, redundant limbs, blank stare, extra plants ornaments passers-by, cluttered background, stage harsh light, over-sharpening, oversaturated clashing color, artificial perfect texture, bird/bug eye view, extreme pitch, perspective distortion, disproportionate body"
                }
            }
        }

        # 双输出格式指引，严格对齐素材output_format_suffix规范
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】2-3段连贯文字：首段实体场景与具象光源氛围；次段完整动态+细微情绪神态；末段肤色、雀斑、面料色彩细节，300-600字，全程禁用mm/f/光圈焦距等数字光学参数。",
                "en": "[Natural Paragraph Mode] 2-3 coherent paragraphs: scene & light atmosphere; full body movement & subtle expression; skin spot fabric color details, 300-600 words, no optical digital parameters at all."
            },
            "structured": {
                "zh": """【结构化模式】固定输出顺序：
1.类别风格定位
2.全局强制肤质约束（面部基础/皮肤肌理/毛发细节）
3.画面构图（视觉引导/主体占比/画幅/精简约束）
4.景别（类型/裁切边界/画面叙事特征）
5.视角景深（距离/水平方位/垂直俯仰/虚实氛围）
6.人物描述（外貌/动态/表情/服装色彩配比）
7.肌肤细节（肤质/发丝/东方女性面部特质）
8.环境氛围（空间/光源/色彩配比/叙事小物件）
9.技术参数建议（仅焦距光圈镜头，附带释义，禁用快门ISO）
10.风格标签+画面收尾精简约束""",
                "en": """[Structured Mode] Fixed output order:
1. Category positioning
2. Global mandatory skin constraints (face base / skin texture / hair details)
3. Composition (visual guide / subject ratio / aspect ratio / cleanup limit)
4. Shot type (type / crop / narrative feature)
5. Perspective & DOF (distance / horizontal / vertical / blur mood)
6. Character description (look / movement / expression / color ratio)
7. Skin & hair details
8. Environment (space / light / color / tiny props)
9. Tech params (only focal length aperture lens with explanation, shutter ISO banned)
10. Style tags + frame cleanup rules"""
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