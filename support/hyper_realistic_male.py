# -*- coding: utf-8 -*-
"""
超写实男性人像预设提示词库

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

HYPER_REALISTIC_MALE = {
    "template_id": "hyper_realistic_male",
    "name": "超写实男性人像",
    "description": "全能超写实真人复刻商业男士人像摄影指导，全覆盖古风国风、现代都市、复古胶片、暗黑轻奢、时尚杂志、高端职场、极简棚拍、科幻男士人像等全题材。兼容亚洲/欧美男性五官骨骼、胡茬体态特征，面部干净精致，无痘印、无明显瑕疵，保留原生毛孔与自然皮肤肌理，杜绝塑料假肤、AI模板脸、网红过度磨皮感。语义权重优先级：面部骨骼肤质胡茬＞体态姿态服饰＞光影色调氛围＞场景构图＞摄影参数。所有风格坚守真人写实基线，仅氛围与造型差异化，古风、职场、胶片、科幻均为题材分支，不脱离超写实核心，所有男士模特姿态沉稳克制，无夸张僵硬表现。",
}

class HyperRealisticMale:
    def __init__(self):
        # 下游生图模型内容组织公式库，与女性模板结构一致
        self.model_formula_library = {
            "Flux1": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面氛围光影 → 人物气质姿态 → 肌肤发丝胡茬质感 → 背景留白。侧重氛围叙事，弱化细碎关键词堆砌，画面柔和高级。",
                "formula_en": "Content order: overall atmosphere lighting → character pose → skin hair stubble texture → negative space. Focus on atmospheric narration."
            },
            "Flux2_klein": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：人物核心体态五官骨骼 → 光影立体层次 → 服饰面料质感 → 克制极简环境。平衡男士肌理真实感与氛围感，光影过渡细腻自然。",
                "formula_en": "Content order: character face bone and body → lighting layers → clothing texture → restrained environment. Balance realism and atmosphere."
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：真人肤质胡茬细节优先 → 面部五官骨骼轮廓 → 男士挺拔体态姿态 → 专业棚拍布光 → 极简场景。极致还原男性原生肌肤、胡茬质感，严格控制面部畸变。",
                "formula_en": "Content order: real skin & stubble texture first → facial bone contour → male body posture → studio lighting → minimalist scene."
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：构图视觉重心 → 人物神态挺拔体态 → 色彩和谐管控 → 光影层次 → 干净背景。色彩精准管控，构图规整克制，画面干净通透，强化男士肤色自然过渡。",
                "formula_en": "Content order: composition focus → expression and posture → color harmony → lighting layers → clean background."
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：电影级光影氛围 → 男士体态沉稳情绪 → 胶片颗粒质感细节 → 服饰面料 → 极简布景。强化影调层次与高级禁欲氛围感。",
                "formula_en": "Content order: cinematic lighting → male body emotion → film texture details → fabric → minimalist set."
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面基调 → 男士沉稳松弛摆姿 → 自然肌肤胡茬质感 → 简约留白环境。极简干净叙事，弱化冗余修饰。",
                "formula_en": "Content order: overall tone → relaxed male pose → natural skin stubble texture → simple negative space."
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：面部五官肤质胡茬 → 挺拔体态姿态 → 光影层次 → 服饰细节 → 轻量极简环境。强化男性面部立体骨骼，光影层次柔和，画面干净通透。",
                "formula_en": "Content order: facial skin stubble features → male body posture → lighting layers → fabric details → lightweight environment."
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：男士主体沉稳气质 → 肤质发丝胡茬细节 → 专业塑型布光 → 服饰造型 → 极简场景。色彩柔和统一，眉眼神态刻画细腻，画面写实自然。",
                "formula_en": "Content order: male character temperament → skin hair stubble details → professional lighting → clothing styling → minimalist scene."
            }
        }

        # 全局底层通用规则，中英双语，适配男性人像
        self.global_base_rules = {
            "zh": """
你是专业高端全风格超写实男士人像摄影提示词扩写专家，本模板为【通用超写实男性人像】，全覆盖：古风国风、现代都市、复古胶片、暗黑轻奢、时尚杂志、高端职场、极简棚拍、科幻男士人像所有题材。
所有风格坚守**真人超写实基线**，仅造型、光影、色调、氛围差异化，绝不出现二次元、插画、油画质感。
男士面部干净精致，无痘印、无明显瑕疵，保留皮肤原生毛孔、自然肌理、浅细纹与自然肤色层次，拒绝过度磨皮导致的塑胶假肤。
姿态必须使用具体肢体结构描述，全部采用专业男模标准摆姿，禁止模糊形容词；光线方向明确，光影过渡柔和通透；男士绝对画面主体，环境仅衬托氛围。
完整保留用户输入的风格、服饰、场景、色调、姿态、视角所有信息，仅补充摄影、材质、光影、肤质、胡茬、发丝专业细节，不新增无关物体、多余元素。
所有男士穿搭、国风锦袍、职场西装、时尚大衣均作为高端男士人像题材，姿态沉稳克制、硬朗高级，禁止夸张畸形体态、过度柔弱造型。
输出禁忌：禁止权重符号、多余相机参数、冗余堆砌；禁止卡通二次元、畸形肢体、坏手烂指、网红假脸、磨皮蜡皮；禁止杂乱背景、空洞假笑、抓拍自拍、透视畸变。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional universal photorealistic male portrait prompt expert. This preset covers all styles: ancient chinese style, modern urban, retro film, dark luxury, fashion magazine, business elite, minimalist studio, sci-fi male portrait.
All styles adhere strictly to photorealistic human baseline, differentiated only by styling, lighting, tone and atmosphere, no illustration, anime or oil painting texture.
Male face is clean and exquisite, no acne marks, no obvious blemishes, retain original skin pores, natural texture, shallow fine lines and natural skin tone layers, reject plastic fake skin caused by excessive skin smoothing.
All male outfits, hanfu, business suits and fashion coats belong to high-end male portrait themes with steady and restrained poses, no exaggerated deformed body or overly soft figure.
Pose described with concrete body structure, no vague words. Clear light direction and soft shadow transition. Male subject dominates the frame, background only for atmosphere.
Completely retain user input style, clothing, scene, tone, pose and perspective. Only supplement professional photography, texture, lighting, skin, stubble and hair details without irrelevant elements.
Taboo: no weight symbols, no redundant camera parameters, no anime/cartoon/illustration, no deformed anatomy, no bad hands, no over-retouched skin, no messy background, no fake smile, no snapshot selfie, no perspective distortion.
Strictly output two formats without extra comments.
"""
        }

        # 唯一主预设库，绑定超写实男性人像专属模板
        self.preset_library = {
            "hyper_realistic_male": {
                "template_id": "hyper_realistic_male",
                "display_name": HYPER_REALISTIC_MALE["name"],
                "description": HYPER_REALISTIC_MALE["description"],
                "positive_constraints": {
                    "zh": "影视级超写实真人质感，原生硬朗男性面部骨骼结构，清晰下颌线条，眉眼唇天然轻微不对称，精准区分亚洲/欧美男性原生五官特征；男士面部干净精致，无痘印、无明显瑕疵，保留皮肤原生毛孔、自然肌理、浅细纹与自然肤色层次，零过度磨皮、无塑胶蜡皮、无AI模板网红帅哥脸，原生分层蓬松发丝、自然短绒胡茬细节，干净克制极简布景，专业男模沉稳高级摆姿，内敛真实沉稳情绪神态，无透视畸变。古风/职场/胶片/暗黑/科幻均为风格题材分支，不改变真人写实底层，姿态挺拔克制、硬朗有力量感",
                    "en": "cinematic photorealistic real human texture, tough original male facial bone structure, clear jawline, natural slight asymmetry of eyes, eyebrows and lips, distinguish Asian / European male native facial features; Male face clean and exquisite, no acne marks, no obvious blemishes, retain original skin pores, natural texture, shallow fine lines and natural skin tone layers, no excessive skin smoothing, no plastic wax skin, no AI template handsome face, layered fluffy hair and natural stubble, restrained clean scene, steady professional male model pose, calm authentic expression, no perspective distortion. Ancient / business / film / dark / sci-fi are style themes only, never break photorealistic baseline with upright restrained powerful posture"
                },
                "preset_rules": {
                    "zh": """
【男士全风格超写实专属规则】
1. 通用基线：男士面部干净精致，无痘印、无明显瑕疵，保留皮肤原生毛孔、浅细纹、自然肤色层次；保留面部轻微不对称，杜绝完美蜡像脸、网红过度磨皮帅哥脸；肤色过渡自然均匀，高光不过曝，暗部不死黑，光影层次通透，强化自然胡茬生长肌理。
2. 古风国风风格：强化东方男士利落下颌、内敛清俊骨相、温润沉稳气质，适配锦袍、素色汉服、玉饰古风造型；优先柔和侧逆柔光、漫射棚布光，低饱和素雅清冷色调。
3. 现代职场风格：适配西装、轻奢通勤穿搭、极简灰度影棚；光影干净立体塑型，色调低饱和冷调高级，体态挺拔规整，适配轻奢室内、纯色棚拍场景。
4. 复古胶片风格：保留真实胶片颗粒、复古暖调褪色质感、柔和漫射光；肤质保留原生毛孔、浅细纹、自然肤色层次，不重度精修，氛围怀旧儒雅。
5. 暗黑轻奢风格：高对比伦勃朗侧光、低饱和暗调质感、硬朗明暗分割；气质冷冽禁欲贵气，极简深色布景，突出男士立体骨骼与疏离气场。
6. 男士时尚杂志风格：硬光柔光组合立体修容光影、高清通透写实质感；体态利落舒展、力量感线条，适配纯色影棚、高端轻奢置景。
7. 极简男士肖像风格：纯色纯白/灰度影棚布景，正面蝴蝶柔光，弱化多余装饰；聚焦面部骨骼、胡茬、毛孔肌理，气质清冷纯粹。
8. 科幻艺术人像风格：冷调硬光、金属低饱和配色、未来极简布景；男士体态硬朗富有张力，服饰金属面料肌理清晰。
所有风格：用户指定内容优先，仅补充专业光影、肤质、胡茬、面料细节，不篡改用户题材与氛围。
""",
                    "en": """
【Universal Photorealistic Preset Rules for Male Portrait】
1. General baseline: Male face is clean and exquisite, no acne marks, no obvious blemishes, retain original skin pores, shallow fine lines and natural skin tone layers; keep slight facial asymmetry, no perfect wax face or over-retouched internet celebrity male face. Natural uniform skin tone, no overexposed highlight or crushed shadow, transparent light and shadow layers, emphasize natural stubble texture.
2. Ancient Chinese style: Sharp jawline and gentle oriental bone structure for asian men, suitable for hanfu and jade accessories; soft side backlight, low saturation elegant tone.
3. Modern business style: Suits and commute outfits, minimalist gray studio; clean three-dimensional lighting, low saturation cold tone, upright body in light luxury indoor or solid color studio.
4. Retro film style: Authentic film grain, warm faded tone, soft diffused light, retain skin pores, shallow fine lines and natural skin tone layers without heavy retouching, retro elegant atmosphere.
5. Dark luxury style: High contrast chiaroscuro side light, low saturation dark tone, cold and restrained temperament, minimalist dark background to highlight male bone and alienated aura.
6. Men fashion magazine style: Mix hard & soft light for three-dimensional shadow, neat powerful body line, solid color studio and light luxury scene.
7. Minimalist male portrait: Pure white / gray studio, front butterfly soft light, no redundant decoration, focus on facial bone, stubble and pore texture, pure cold temperament.
8. Sci-fi art portrait: Cold hard light, metal low saturation color scheme, futuristic minimalist set, tough male body and clear metal fabric texture.
All styles: user-specified content takes priority, only supplement professional light, skin, stubble and fabric details, without altering user's theme and atmosphere.
"""
                },
                "negative_base": {
                    "zh": "完美对称五官，过度磨皮无毛孔，塑料蜡皮，AI网红帅哥模板脸，僵硬摆拍，空洞假笑，肢体畸形，柔弱纤细体态，无胡茬光滑面部，坏手多手指，透视畸变，高饱和艳色，画面杂乱，二次元插画质感，卡通动漫画风，舞台刺眼强光，曝光异常",
                    "en": "perfect symmetrical face, excessively smoothed skin without pores, plastic wax skin, AI template handsome male face, stiff pose, empty fake smile, deformed limbs, weak slender figure, smooth face without stubble, bad hands, extra fingers, perspective distortion, oversaturated bright color, cluttered frame, anime illustration style, cartoon anime art style, harsh stage strong light, abnormal exposure"
                }
            }
        }

        # 输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】三段连贯文字：第一段场景布光整体氛围；第二段人物姿态视线表情体态；第三段肤质发丝胡茬面料色彩调性，300‑600字纯画面描写。",
                "en": "[Natural Paragraph Mode] Three coherent paragraphs: scene‑lighting‑atmosphere; pose‑gaze‑expression‑body; skin‑hair‑stubble‑fabric‑color tone, 300‑600 words pure visual description."
            },
            "structured": {
                "zh": """【结构化模式】严格顺序输出：
1.人种五官轮廓特征
2.风格与服饰造型定位
3.肤质与毛发胡茬原生细节
4.构图景别与视觉重心
5.视角方位与俯仰角度
6.姿态体态与表情神态
7.色彩配比与整体调性
8.专业布光方式与光影层次
9.画面精简约束与环境要求""",
                "en": """[Structured Mode] Output strictly in this order:
1. Ethnic facial features
2. Style and clothing positioning
3. Skin hair stubble natural details
4. Composition shot type and visual focus
5. View angle and pitch
6. Pose body and facial expression
7. Color ratio and overall tone
8. Professional lighting method
9. Frame simplification constraint"""
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
