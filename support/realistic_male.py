# -*- coding: utf-8 -*-
"""
真实感亚洲男性人像摄影大师预设模块

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

REALISTIC_MALE = {
    "template_id": "realistic_male",
    "name": "真实亚洲男性人像",
    "description": "真实感亚洲男性生活化人像摄影指导，覆盖古风汉服、韩系、日系校园、职场通勤、运动健身、正装礼服、街头潮牌、复古文艺、艺术人体/裸体艺术、cosplay等全风格场景。融合亚洲男性硬朗轮廓、立体鼻梁、自然胡须质感与原生不对称特质，打造真实自然、富有力量与温度的生活化纪实人像，艺术人体类别侧重光影雕塑感与人体美学表达，规避影楼磨皮、AI假脸、模板网红脸。语义权重优先级：面部肤质五官＞姿态服饰＞光影色彩＞场景环境＞构图景别＞摄影参数。支持三维度视角受控组合，用户指定优先沿用，未指定按纪实风格审美随机匹配。",
}

class RealisticMale:
    def __init__(self):
        # 下游生图模型内容组织公式库，完全复用参考原版无任何修改
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

        # 全局底层规则，纯纪实亚洲男性人像，剔除全部超写实相关词汇
        self.global_base_rules = {
            "zh": """
你是专业亚洲男性生活化纪实人像提示词扩写专家，本模板为【真实感亚洲男性人像】，覆盖古风汉服、韩系、日系校园、职场通勤、运动健身、正装礼服、街头潮牌、复古文艺、艺术人体、cosplay全题材。
所有风格坚守**真实纪实人像基线**，仅造型、光影、色调、氛围差异化，绝不出现二次元、插画、油画质感。
语义权重优先级：面部肤质五官胡须＞姿态服饰＞光影色彩＞场景环境＞构图景别＞摄影参数。
姿态完整描述动态抓拍过程，禁止静态模板摆拍；光线使用生活化实体光源具象描写，删除空洞文艺修辞；人物为绝对画面主体，环境仅服务人物叙事，不自动新增无关道具、路人、装饰。
严格执行主色70%、辅助色25%、点缀色5%色彩配比，统一标注饱和度，视觉留白舒适；全文优先强化亚洲男性单眼皮/内双、立体鼻梁、硬朗下颌、自然胡茬等原生特征，保留毛孔、痘印、细纹、肤色不均等真实肌肤痕迹，杜绝AI塑料假人脸。
完整保留用户指定场景、穿搭、色调、视角、情绪信息，仅补充肤质、毛发、面料、光影专业细节，不篡改用户需求。
输出禁忌：禁止权重符号、关键词冗余堆砌；禁止完美对称五官、零瑕疵磨皮假皮、僵硬规整发丝、空洞假笑、无神凝视；禁止舞台强光、杂乱堆砌背景、极端猎奇俯仰、透视畸变；natural模式禁用全部光学数字参数，仅structured模式指定区块可使用焦距光圈并附带释义。
严格输出自然段落、结构化两种格式，不额外增加注释说明。
""",
            "en": """
You are a professional Asian male documentary portrait prompt expansion expert. This preset is [Realistic Asian Male Portrait], covering Hanfu ancient style, Korean style, Japanese campus, workplace, fitness, formal suit, street fashion, retro, artistic nude, cosplay themes.
All styles follow real documentary portrait baseline, differentiated only by styling, lighting, tone and atmosphere, no anime, illustration or oil painting texture.
Semantic priority: facial skin & stubble > pose & outfit > light & color > scene > frame > camera parameters.
All poses are captured dynamic moments, rigid template posing forbidden; light described with real daily light sources, empty literary rhetoric removed. Human subject dominates frame, background only serves narrative, no extra irrelevant props or passers-by.
Strict 70/25/5 color area ratio with saturation label, comfortable blank space. Prioritize native Asian male features: single/double-lid, three-dimensional nose, firm jaw, natural stubble, retain pores, acne marks, fine lines, uneven skin, no AI plastic fake face.
Fully keep user-specified scene, outfit, tone, perspective and mood, only add skin, hair, fabric, lighting details without altering user request.
Taboo: weight tags, redundant keywords; perfectly symmetrical face, flawless smoothed plastic skin, rigid neat hair, empty fake smile, blank stare; stage harsh light, cluttered background, extreme weird angles, perspective distortion. Natural mode blocks all optical numbers, only structured mode allows focal length & aperture with explanations.
Output natural text and structured two formats only, no extra notes.
"""
        }

        # 预设库绑定REALISTIC_MALE模板
        self.preset_library = {
            "realistic_male": {
                "template_id": REALISTIC_MALE["template_id"],
                "display_name": REALISTIC_MALE["name"],
                "description": REALISTIC_MALE["description"],
                # 中英正向约束，完全取自素材原文无修改
                "positive_constraints": {
                    "zh": "真实亚洲男性面部,左右眉眼唇形天然轻微不对称,单眼皮内双,清晰面部轮廓,立体鼻梁,硬朗下颌线,保留自然毛孔淡细纹肤色不均轻微痘印淡疤痕,真实胡须质感胡茬剃须青印,原生真实肌肤质感,自然毛躁碎发,生活化场景环境仅衬托主体,自然抓拍松弛姿态,真实具象情绪,无刻意摆拍痕迹,视角符合纪实人像真实拍摄逻辑,三维度组合自然协调,无透视畸变与违和角度",
                    "en": "real Asian male face, natural slight asymmetry of brows eyes lips, single/internal double eyelids, clear facial contour, tall nose, firm jawline, natural pores fine lines uneven tone acne marks faint scars, natural stubble shaving shadow, original real skin texture, messy broken hair, daily scene only for foil, captured relaxed pose authentic emotion, no deliberate posing, perspective fits documentary portrait logic, balanced three-dimensional composition, no perspective distortion"
                },
                # 全题材细分专属规则，完全提取素材内分类内容
                "preset_rules": {
                    "zh": """
【亚洲男性纪实人像全题材专属规则】
1. 通用基线：双重肤质约束，保留毛孔、痘印、细纹、疤痕、长短胡茬青印等原生肌理；面部天然不对称，拒绝无瑕完美脸；光源全部具象写实，杜绝舞台硬光；色彩严格70/25/5配比，低饱和优先，不堆砌高饱和撞色。
2. 古风/汉服：平视微仰+四分之三斜侧+七分景；柔和侧逆光，哑光汉服面料，气质清雅沉静。
3. 韩系：平视小俯+斜侧七分景；午后漫射柔光，浅淡低饱和配色，慵懒温柔少年感。
4. 日系校园：春日漫射自然光，浅清新色调，校服穿搭，青涩松弛神态。
5. 职场通勤：平视四分之三侧+肩/七分特写；冷调落地窗混合光，西装简约成熟质感。
6. 运动健身：小仰正面七分顶光，小麦肌肤带汗珠，突出肌肉力量与胡茬肌理。
7. 正装礼服：平视小仰七分，宴会厅暖柔光，挺括西装沉稳大气。
8. 街头潮牌：城市混合霓虹/日光，中低饱和撞色，随性行走抓拍。
9. 复古文艺：窗边暖柔光，低饱和复古棕调，安静松弛神态。
10.艺术人体：纯白空间侧逆光，光影雕塑人体曲线，极简无多余道具。
11.cosplay：匹配角色场景对应光源，服饰纹理清晰，神态贴合角色性格。
全部题材：用户指定景别、俯仰、水平视角必须优先执行；不自动生成无关行人、花草摆件，环境仅辅助叙事。
""",
                    "en": """
【Documentary Asian Male Portrait Theme Rules】
1. General baseline: Dual skin constraints, retain pores acne marks lines scars uneven stubble shadow; natural facial asymmetry, no flawless skin; concrete natural light only, no stage light; 70/25/5 color ratio, low saturation preferred.
2. Hanfu ancient style: slight low eye level, three-quarter side, medium full shot, soft side backlight, matte fabric, elegant calm vibe.
3. Korean style: slight high eye level, three-quarter medium shot, afternoon diffuse soft light, pale low saturation, lazy youthful mood.
4. Japanese campus: spring diffuse daylight, fresh light tone, school uniform, innocent relaxed expression.
5. Workplace: eye-level three-quarter, shoulder/medium shot, cold window mixed light, minimalist suit mature texture.
6. Fitness: low angle top light, wheat skin with sweat, highlight muscle and stubble texture.
7. Formal suit: slight low eye medium shot, banquet warm soft light, stiff suit steady temperament.
8. Street fashion: mixed neon & daylight, medium-low contrast color, casual walking capture.
9. Retro literary: window warm light, low saturation sepia tone, quiet relaxed mood.
10. Artistic nude: pure white room side backlight, light sculpt body curve, zero extra props.
11. Cosplay: scene-matched light, clear costume texture, character-fitting expression.
All themes: user-specified shot, pitch, horizontal angle take priority; no auto passers-by or extra ornaments, environment only supports narration.
"""
                },
                "negative_base": {
                    "zh": "完美对称五官,零瑕疵皮肤,人工对称双眼皮,厚重匀肤磨皮,塑料光滑哑光假皮,过度光滑肌肤,完全对称眉眼,厚重美颜,统一匀肤,过度美化皮肤,精致无瑕疵脸蛋,模板网红脸,无胡茬质感,虚假面部肌理,光滑无毛孔皮肤,空洞假笑,僵硬摆拍,刻意模特摆姿,多余肢体动作,无神凝视,多余绿植摆件,路人装饰杂物,杂乱背景,大量装饰,多余人物,舞台强光,画面堆砌元素,过度锐化,高饱和撞色,人工完美肌理,鸟瞰视角,虫眼视角,极端大俯大仰,透视畸变,肢体比例失调",
                    "en": "perfect symmetrical facial features, blemish-free skin, artificial double lids, heavy skin smoothing, plastic matte fake skin, over-smooth complexion, fully symmetric brows, heavy beauty filter, flawless template influencer face, no stubble texture, poreless fake skin, empty fake smile, stiff model pose, redundant limbs, blank stare, extra plants ornaments passers-by, cluttered background, stage harsh light, over-sharpening, oversaturated clashing color, artificial perfect texture, bird/bug eye view, extreme pitch, perspective distortion, disproportionate body"
                }
            }
        }

        # 双输出格式指引，严格对齐REALISTIC_MALE内output_format_suffix规范
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】2-3段连贯文字：首段实体场景与具象光源氛围；次段完整动态+细微情绪神态；末段肤色、胡茬、面料色彩细节，300-600字，全程禁用mm/f/光圈焦距等数字光学参数。",
                "en": "[Natural Paragraph Mode] 2-3 coherent paragraphs: scene & light atmosphere; full body movement & subtle expression; skin stubble fabric color details, 300-600 words, no optical digital parameters at all."
            },
            "structured": {
                "zh": """【结构化模式】固定输出顺序：
1.类别风格定位
2.全局肤质正向约束（面部基础/皮肤肌理/毛发胡须）
3.画面构图（视觉引导/主体占比/画幅/精简约束）
4.景别（类型/裁切边界/画面叙事特征）
5.视角景深（距离/水平方位/垂直俯仰/虚实氛围）
6.人物描述（外貌/动态/表情/服装色彩配比）
7.肌肤细节（肤质/发丝/东方男性面部特质）
8.环境氛围（空间/光源/色彩配比/叙事小物件）
9.技术参数建议（仅焦距光圈镜头，附带释义，禁用快门ISO）
10.风格标签+画面收尾精简约束""",
                "en": """[Structured Mode] Fixed output order:
1. Category positioning
2. Global skin constraints (face base / skin texture / hair stubble)
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