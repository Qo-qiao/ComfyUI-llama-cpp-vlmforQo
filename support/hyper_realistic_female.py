# -*- coding: utf-8 -*-
"""
超写实女性人像预设提示词库

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

HYPER_REALISTIC_FEMALE = {
    "template_id": "hyper_realistic_female",
    "name": "超写实女性人像",
    "description": "全能超写实真人复刻商业人像摄影指导，全覆盖古风国风、现代都市、复古胶片、暗黑轻奢、时尚杂志、礼服旗袍、泳装写真等全题材。兼容亚洲/欧美五官肤质体态特征，妆造后面部干净精致，无暗斑黑痣，保留原生毛孔与自然皮肤肌理，杜绝塑料假肤、AI模板脸、网红过度磨皮感。语义权重优先级：面部肤质五官＞体态姿态服饰＞光影色调氛围＞场景构图＞摄影参数。所有风格坚守真人写实基线，仅氛围与造型差异化，泳装、国风、胶片均为题材分支，不脱离超写实核心，所有姿态克制自然，无过度夸张表现。",
}

class HyperRealisticFemale:
    def __init__(self):
        # 下游生图模型内容组织公式库
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

        # 全局底层规则
        self.global_base_rules = {
            "zh": """
你是专业高端全风格超写实人像摄影提示词扩写专家，本模板为【通用超写实人像】，全覆盖：古风国风、现代都市、复古胶片、暗黑轻奢、时尚杂志、礼服旗袍、海边泳装、极简棚拍所有题材。
所有风格坚守**真人超写实基线**，仅造型、光影、色调、氛围差异化，绝不出现二次元、插画、油画质感。
妆造完成后面部干净精致，无暗斑、黑痣、明显瑕疵，保留皮肤原生毛孔、自然肌理与细微皮肤纹理，拒绝过度磨皮导致的塑胶假肤。
姿态必须使用具体肢体结构描述，禁止模糊形容词；光线方向明确，光影过渡柔和通透；人物绝对画面主体，环境仅衬托氛围。
完整保留用户输入的风格、服饰、场景、色调、姿态、视角所有信息，仅补充摄影、材质、光影、肤质、发丝专业细节，不新增无关物体、多余元素。
所有服饰（旗袍/泳装/礼服）均作为时尚人像题材，姿态克制优雅、自然高级，禁止低俗化、过度性化、夸张畸形体态。
输出禁忌：禁止权重符号、多余相机参数、冗余堆砌；禁止卡通二次元、畸形肢体、坏手烂指、网红假脸、磨皮蜡皮；禁止杂乱背景、空洞假笑、抓拍自拍、透视畸变。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional universal photorealistic portrait prompt expert. This preset covers all styles: ancient chinese style, modern urban, retro film, dark luxury, fashion magazine, cheongsam, dress, swimwear and minimalist studio shooting.
All styles adhere strictly to photorealistic human baseline, differentiated only by styling, lighting, tone and atmosphere, no illustration, anime or oil painting texture.
After makeup, the face is clean and exquisite, without dark spots, moles and obvious blemishes, retaining original skin pores, natural texture and subtle skin lines, rejecting plastic fake skin caused by excessive skin smoothing.

All costumes including cheongsam and swimwear are high-end fashion portrait themes with elegant and restrained poses, no vulgar or exaggerated sexualization.

Pose described with concrete body structure, no vague words. Clear light direction and soft shadow transition. Human subject dominates the frame, background only for atmosphere.

Completely retain user input style, clothing, scene, tone, pose and perspective. Only supplement professional photography, texture, lighting and skin details without irrelevant elements.

Taboo: no weight symbols, no redundant camera parameters, no anime/cartoon/illustration, no deformed anatomy, no bad hands, no over-retouched skin, no messy background, no fake smile, no snapshot selfie, no perspective distortion.
Strictly output two formats without extra comments.
"""
        }

        # 唯一主预设模板，绑定原有HYPER_REALISTIC_FEMALE模板id
        self.preset_library = {
            "hyper_realistic_female": {
                "template_id": "hyper_realistic_female",
                "display_name": HYPER_REALISTIC_FEMALE["name"],
                "description": HYPER_REALISTIC_FEMALE["description"],
                # 中英双语固定前置约束（妆造干净无斑痣，保留毛孔肌理）
                "positive_constraints": {
                    "zh": "影视级超写实真人质感，原生面部骨骼结构，眉眼唇天然轻微不对称，保留人种原生五官特征；妆造优化后面部干净精致，无暗斑、黑痣、明显瑕疵，保留皮肤原生毛孔、自然肌理与细微纹理，零过度磨皮、无塑胶蜡皮、无AI模板网红脸，原生分层发丝细节，干净克制布景，专业模特高级摆姿，自然真实情绪神态，无透视畸变。古风/现代/胶片/暗黑/泳装均为风格题材分支，不改变真人写实底层，姿态优雅克制、高级自然",
                    "en": "cinematic photorealistic real human texture, original facial bone structure, natural slight asymmetry of eyes, eyebrows and lips, retain original ethnic facial features; After makeup, the face is clean and exquisite, without dark spots, moles and obvious blemishes, retain original skin pores, natural texture and subtle lines, no excessive skin smoothing, no plastic wax skin, no AI template face, layered natural hair strands, restrained clean scene, professional elegant model pose, natural authentic expression, no perspective distortion. Ancient/modern/film/dark/swimwear are style themes only, never break photorealistic baseline with elegant restrained posture"
                },
                # 全风格细分专属规则
                "preset_rules": {
                    "zh": """
【全风格超写实专属规则】
1. 通用基线：妆造后面部干净无暗斑、黑痣、明显瑕疵，保留皮肤原生毛孔、自然肌理；保留面部轻微不对称，杜绝完美蜡像脸、网红过度磨皮脸；肤色过渡自然均匀，高光不过曝，暗部不死黑，光影层次通透。
2. 古风国风风格：强化东方柔和骨相、温婉清冷气质，适配汉服、披帛、狐裘、古风妆造；优先柔光、漫射天光、雪景庭院布景，色调低饱和清冷雅致。
3. 现代都市风格：适配日常穿搭、轻奢通勤、极简棚拍；光影干净通透，色调高级素雅，体态松弛自然，适配街头、室内极简场景。
4. 复古胶片风格：保留真实胶片颗粒、复古褪色色调、暖调柔光；肤质保留真人毛孔肌理，不过度精修，氛围怀旧温柔。
5. 暗黑轻奢风格：高对比光影、低饱和暗调质感、伦勃朗侧光；气质冷艳神秘，布景极简深色，突出人物高级疏离感。
6. 时尚杂志风格：硬光柔光结合、立体修容光影、高通透画质；体态利落高级，适配棚拍纯色背景、轻奢置景。
7. 旗袍/礼服风格：凸显面料绸缎、蕾丝、刺绣纹理，体态端庄优雅，姿态克制内敛，中式雅致/西式高贵质感。
8. 泳装写真风格：定位高端海边/泳池时尚人像，日光柔和通透，体态舒展自然、健康紧致；绝对克制，主打阳光高级、干净青春的时尚写真质感。
所有风格：用户指定内容优先，仅补充专业细节，不篡改用户题材与氛围。
""",
                    "en": """
【Universal Photorealistic Preset Rules】
1. General baseline: After makeup, the face is clean without dark spots, moles and obvious blemishes, retain original skin pores and natural texture; keep slight facial asymmetry, no perfect wax face or excessively retouched internet celebrity skin. Natural uniform skin tone, no overexposed highlight or crushed shadow, transparent light and shadow layers.
2. Ancient Chinese style: Soft oriental bone structure, gentle and cold temperament, suitable for hanfu and ancient makeup; soft diffused light, low saturation cold elegant tone.
3. Modern urban style: Clean transparent lighting, elegant low-saturation tone, relaxed natural posture, suitable for daily wear and minimalist scene.
4. Retro film style: Authentic film grain, faded retro tone, warm soft light, retain skin pores and natural texture without excessive retouching.
5. Dark luxury style: High contrast chiaroscuro lighting, low saturation dark tone, cold mysterious temperament, minimalist dark background.
6. Fashion magazine style: Combined hard and soft light, three-dimensional shadow, neat and advanced posture, pure color studio background.
7. Qipao & dress style: Highlight satin, lace and embroidery texture, dignified and elegant restrained posture.
8. Swimwear photography style: positioned as high-end seaside/pool fashion portrait, soft and translucent daylight, relaxed natural and healthily toned body posture; absolutely restrained, focusing on sunny high-end, clean and youthful fashion photography texture.
All styles: user-specified content takes priority, only supplement professional details, without altering the user's theme and atmosphere.
"""
                },
                "negative_base": {
                    "zh": "完美对称五官，过度磨皮无毛孔，塑料蜡皮，AI假脸，网红模板脸，僵硬摆拍，空洞假笑，肢体畸形，坏手多手指，透视畸变，高饱和艳色，画面杂乱，二次元插画质感，卡通动漫画风，面部暗斑黑痣泛滥，曝光异常",
                    "en": "perfect symmetrical face, excessively smoothed skin without pores, plastic wax skin, AI fake face, internet celebrity template face, stiff pose, empty fake smile, deformed limbs, bad hands, extra fingers, perspective distortion, oversaturated bright color, cluttered frame, anime illustration style, cartoon anime art style, excessive dark spots and moles on face, abnormal exposure"
                }
            }
        }

        # 双输出格式指引
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
        # 双输出格式：按需只拼接选中格式的指引（默认 both 全部拼接，保持原行为）
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
