# -*- coding: utf-8 -*-
"""
文生视频预设模块

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

UNIVERSAL_VIDEO = {
    "template_id": "universal_video",
    "name": "通用文生视频导演",
    "description": "专业的电影级视频提示词工程师，为 Wan2.2、LTX‑2.3、MiniMax‑H3 文生视频模型设计标准化、高可控的动态叙事描述。覆盖实拍类、动漫类两大核心赛道，适配古装、科幻、文艺、悬疑、治愈等全风格影片创作。采用正负向彻底分离架构，正向文本纯加法塑造动态画面，负向统一汇总规避生成通病。内置标准化8步扩写逻辑、固定语义权重优先级、三维度可控镜头视角、7:2.5:0.5色彩配比规则与画面精简约束，强化动态节奏、镜头语言、物理级光影与真实质感，彻底规避画面闪烁、肢体穿模、逻辑混乱、元素堆砌等常见问题。自动识别视频类别与风格，根据选择的视频模型输出适配该模型语义习惯的精准描述，长文本分段控制避免后置约束失效，适配全平台文生视频工作流。",
}

class UniversalVideo:
    def __init__(self):
        # 视频下游模型配置库：Wan2.2 / LTX‑2.3 / MiniMax‑H3
        self.video_model_formula_library = {
            "Wan2.2": {
                "keyword_dense": True,
                "mix_lang": False,
                "formula_zh": "Wan2.2模型约束：原生单段最大时长5秒，优先2‑4秒；仅支持单镜头，一个片段控制1‑2个核心动作，不要多段连续剧情；不生成音频，禁止写台词音效；支持负向提示词。内容组织顺序：场景基调光影 → 主体角色外貌 → 核心单动作动态 → 镜头运动 → 色彩质感 → 风格标签。natural模式可以使用逗号分隔关键词或连贯短段落；禁止描述音频台词，禁止单片段多镜头切换。",
                "formula_en": "Wan2.2 constraint: native max clip 5s, recommend 2‑4s. Single shot only, keep 1‑2 core actions per clip, no multi‑episode plot. No audio output, do not write dialogue or sound‑effect. Support negative prompt. Content order: scene‑lighting → character appearance → single core action → camera movement → color‑texture → style tags. Allow comma‑separated tags or short paragraphs. Forbid audio description and multi‑cut inside one clip."
            },
            "LTX2.3": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "LTX‑2.3模型约束：原生单段最长20秒，稳定推荐3‑12秒；提示词字数必须匹配时长，长视频不能过短提示；原生支持音画同步，可以写台词、环境音、背景音乐；支持负向提示词；单段为连续长镜头，禁止写镜头剪辑切镜指令。内容组织顺序：镜头设定与场景光影 → 主体角色外貌 → 时序动作（按时间先后） → 镜头运动节奏 → 色彩质感 → 音频描述 → 风格标签。natural模式输出流畅叙事段落，不要大量逗号碎片化标签堆砌。",
                "formula_en": "LTX‑2.3 constraint: native max 20s, stable recommend 3‑12s. Prompt length must match clip duration. Native audio‑visual sync, allow dialogue, ambient sound, background music. Support negative prompt. Single clip is one continuous long‑take, forbid cut‑edit instruction. Content order: camera‑scene‑lighting → character appearance → chronological actions → camera rhythm → color‑texture → audio description → style tags. Use coherent narrative paragraphs, avoid mass comma‑split tags."
            },
            "MiniMax‑H3": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "MiniMax‑H3模型约束：时长仅支持4‑15秒整数秒，不支持小数秒；**不支持负向提示词**，缺陷规避约束全部写入正向提示词；原生音画同步，支持台词、环境音、BGM；支持首尾帧/参考图；单段连续镜头，禁止写切镜剪辑。内容组织顺序：前置约束（规避缺陷）→镜头设定场景光影 →主体外貌 →时序动作 →镜头运动 →色彩质感 →音频描述 →风格标签。natural模式使用连贯叙事段落；不要输出negative字段，所有避坑写进正向文本。",
                "formula_en": "MiniMax‑H3 constraint: only integer seconds 4‑15s, float second invalid. **No negative prompt field**, all defect‑avoid rules must be written into positive prompt text. Native audio‑visual sync, support dialogue, ambient sound, BGM. Support reference image / start‑end frame. Single continuous shot, forbid cut instruction. Content order: precondition(defect avoidance) → camera‑scene‑lighting → character appearance → chronological actions → camera movement → color‑texture → audio → style tags. Use coherent paragraphs, do not output negative prompt field."
            }
        }

        # 全局底层通用规则（三个视频模型共用基础规则）
        self.global_base_rules = {
            "zh": """
你是专业电影级文生视频提示词扩写专家，覆盖实拍类、动漫类，全电影题材。
坚守视频生成基础约束：动作具备物理运动逻辑；画面精简，不自动新增无关摆件、路人、杂物；文本权重从前向后逐级递减，角色动态、镜头运动前置，细节参数后置；超长文本分段，防止末尾约束失效。
natural模式300‑600字，2‑3个叙事段落，**严禁帧率、码率、分辨率等数字技术参数**；structured模式完整输出结构化字段，【技术参数建议】仅允许定性效果描述，禁止一切数值参数。
区分实拍/动漫质感：实拍保留皮肤肌理；动漫保持画风统一，避免画风跳变。
完整保留用户全部输入信息，只做细节补充，不篡改主体、动作、场景；光影写明光源、色温、软硬以及随时间的变化；严格执行70%主色‑25%辅助‑5%点缀色彩配比。
重要模型差异化约束会在模型组织公式给出，严格遵守对应模型的时长上限、音频支持、负向提示词能力。
输出禁忌：禁止权重符号；禁止猎奇镜头角度；禁止穿模、闪烁、跳帧、物体凭空消失；禁止元素堆砌。
支持natural与structured双输出格式，不添加额外注释、说明、解释。
""",
            "en": """
You are professional cinematic video prompt expansion expert. Cover real‑shot / anime categories and full movie genres.
General video baseline: physically plausible motion logic; frame‑simplify rule, no auto‑add irrelevant ornaments or passers‑by. Text weight decays from front to back: character dynamics & camera motion first, details behind. Split long paragraphs to avoid trailing constraint failure.
Natural mode: 300‑600 words, 2‑3 narrative paragraphs, strictly forbid numeric technical parameters like fps, bitrate, resolution.
Structured mode: output all sections, in【Tech Suggestion】only qualitative description allowed, no numeric values.
Texture distinction: real‑shot preserve skin texture; anime keep consistent art‑style, no style‑jitter.
Fully preserve user input, enrich details only without altering subject, action or scene. Describe light source, color‑temperature, hardness‑softness & temporal light change. Enforce 70%‑25%‑5% color proportion rule.
Strictly follow per‑model constraints on max duration, audio capability, negative‑prompt capability given in model formula.
Taboo: no weight syntax; no grotesque camera angles; no penetration‑clipping, flicker, frame‑skip, object pop‑in/out; no element over‑stacking.
Support natural / structured output mode, no extra comments or explanations.
"""
        }

        # 唯一主预设模板，绑定UNIVERSAL_VIDEO template_id
        self.preset_library = {
            "universal_video": {
                "template_id": "universal_video",
                "display_name": UNIVERSAL_VIDEO["name"],
                "description": UNIVERSAL_VIDEO["description"],
                "positive_constraints": {
                    "zh": "电影级叙事质感，物理级动态与镜头运动逻辑，自然流畅的角色动作与环境变化，精准三维镜头视角与合理透视，真实光影过渡与色彩层次。实拍类保留原生皮肤纹理、生活化细节与自然光影过渡；动漫类保持统一画风、流畅线条与稳定色块。画面干净主体突出，仅保留核心叙事元素，无多余杂乱内容。节奏舒缓可控，动态前后连贯，全程风格统一，光影随时间自然变化，情绪通过镜头与动作具象传递。",
                    "en": "cinematic narrative quality, physically‑plausible dynamics & camera logic, smooth character & environment motion, accurate 3‑d camera perspective, reasonable perspective, natural light‑shadow transition & color hierarchy. Real‑shot: preserve native skin texture, life‑like details. Anime: consistent art‑style, smooth line‑art, stable color block. Clean frame with prominent subject, only core narrative elements. Coherent motion, unified style, light evolves over time, emotion expressed via camera & action."
                },
                "preset_rules": {
                    "zh": """
【文生视频通用专属规则】
1. 通用基线：执行8步视频扩写流程；强制70%‑25%‑5%色彩配比；三维镜头视角用户指定优先，未指定从合规视角池选取，杜绝猎奇角度；画面精简约束，不自动生成多余摆件装饰。natural模式300‑600字无相机数字参数；structured模式不超1500字。
2. 实拍类：保留皮肤自然肌理，光影过渡柔和；动作符合人体生理运动逻辑；镜头运动服务叙事，拒绝无意义炫技运镜。
3. 动漫类：画风全程统一，线条色块稳定；肢体运动流畅；规避画风跳变、线条杂线。
4. 动态设计：每个动作写明起始‑过程‑结束，尽量标注时间；环境动态与人物动态节奏匹配。
5. 音频处理：模型不支持音频时，完全删除台词、音效、BGM描述；模型支持音频，可合理加入环境音、台词、背景音乐。
6. 负向提示词处理：MiniMax‑H3禁止输出negative_prompt字段，所有缺陷规避写进正向；Wan2.2、LTX2.3正常输出负向提示。
所有题材：用户输入特征优先级最高，仅补充细节，不得篡改用户设定主体、动作、场景、时长。
""",
                    "en": """
【Video‑Generation General Preset Rules】
1. General baseline: follow 8‑step video expansion workflow. Mandatory color ratio 70%‑25%‑5%. User‑specified camera parameters take priority, pick from valid view‑pool for unknowns, forbid grotesque angles. Frame‑simplify rule: no auto‑generate extra ornaments. Natural mode 300‑600 words without numeric camera params; structured mode max 1500 words.
2. Real‑shot category: preserve natural skin texture, soft light‑shadow transition; human‑physiology‑compliant motion; camera movement serve narrative, avoid meaningless fancy camera work.
3. Anime category: consistent art‑style, stable lines & color blocks; smooth body motion; forbid style‑jitter & messy line‑art.
4. Motion design: describe start‑process‑end for each action, mark time span when possible. Sync environment dynamics with character rhythm.
5. Audio handling: remove dialogue / sfx / BGM for audio‑incapable model; add reasonable ambient sound, dialogue, BGM for audio‑capable model.
6. Negative prompt handling: MiniMax‑H3 must NOT output negative_prompt field, all defect‑avoidance embed into positive prompt. Wan2.2 & LTX2.3 output negative prompt normally.
For all categories: user input has highest priority, add details only, never overwrite subject, action, scene or duration.
"""
                },
                "negative_base": {
                    "zh": "画面闪烁跳帧，肢体穿模扭曲，人物比例失调，透视逻辑错误，镜头剧烈抖动，运动轨迹混乱，静态呆滞无动态，人脸崩坏变形，五官飘忽不定，色彩溢出脏污，画面颗粒噪点，低分辨率模糊，塑料虚假质感，平涂无体积感，多余路人乱入，杂物堆砌冗余，无关装饰摆件，字幕水印logo，元素凭空消失，物体漂浮无重力，光影生硬断层，节奏混乱突兀，画风前后不一，边缘锯齿抠图感，过度锐化生硬，卡通低幼失真",
                    "en": "flicker & frame skip, body clipping & distortion, bad proportion, wrong perspective, violent camera shake, chaotic motion track, static lifeless pose, broken face, drifting facial feature, muddy overflowing color, grain noise, low‑resolution blur, fake plastic texture, flat shading without volume, random extra people, redundant clutter, irrelevant ornament, subtitle watermark logo, object pop‑in pop‑out, zero‑gravity floating object, harsh broken shadow, chaotic rhythm, inconsistent art‑style, jagged cut‑out edge, over‑sharpening, overly childish cartoon distortion"
                }
            }
        }

        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】自然段落（2‑3段），首段确立场景空间、整体基调与光线氛围，次段描述角色动态序列与镜头运动节奏，末段补充光影质感、色彩层次与细节氛围。语言富有画面感与节奏感，全程无帧率、码率、分辨率类数字技术参数，强化动态连贯性、光影流动感与画面精简约束，保证画面干净聚焦、叙事清晰。字数300‑600。",
                "en": "[Natural Paragraph Mode] 2‑3 narrative paragraphs: first for scene‑space‑lighting‑mood; second for character dynamics & camera rhythm; last for light‑shadow‑color‑detail. Visual cinematic language. Forbid numeric parameters such as fps, bitrate, resolution. Emphasize motion coherence, flowing light‑shadow, frame‑simplify constraint. 300‑600 words."
            },
            "structured": {
                "zh": """【结构化模式】
【类别】实拍类/动漫类
【电影风格】古装片/科幻片/动作片/文艺片/悬疑片/纪录片/动漫电影/通用类
【全局正向约束】
  - 动态基础：物理级运动逻辑，角色动作连贯流畅，环境变化符合自然规律，无穿模、无扭曲、无跳帧
  - 质感基础：实拍类保留原生皮肤纹理、自然光影过渡；动漫类画风统一稳定、线条流畅色块清晰
  - 镜头逻辑：三维视角符合电影美学，运动节奏服务叙事，透视准确无畸变
【画面构图】
  - 视觉引导：画面视线流动逻辑，依托角色目光、运动方向、环境线条三重引导，无分散视线的杂乱多余元素
  - 主体位置：水平百分比 + 垂直百分比（如水平 55% 偏右，垂直 40% 偏上），主体占据 70% 视觉权重，环境仅占 30%
  - 画面比例：宽高比（16:9 横屏 / 9:16 竖屏 / 4:3）
  - 画面精简约束：仅保留核心叙事场景与道具，不额外生成绿植、摆件、路人、装饰杂物
【景别与三维镜头视角】
  - 距离维度（景别对应）：微距特写 / 标准特写 / 肩特写 / 七分人像 / 九分人像 / 全景人像，对应叙事重心与细节展现层级
  - 水平方位维度：摄像机水平环绕角度（正面/四分之三斜侧/正侧面/四分之三背面），标注面部展现效果与轮廓叙事特点
  - 垂直俯仰维度：摄像机垂直旋转角度（小俯视角/平视/小仰视角），对应心理感受（小俯的旁观疏离感/平视的平等沉浸感/小仰的张力力量感）
  - 镜头运动：运动类型（推/拉/摇/移/跟/升降/固定）、方向、速度与持续时间，搭配叙事作用释义
  - 景深氛围：主体清晰背景虚化 / 前后景都清晰 / 局部保留环境细节，标注虚实层次对应的画面效果
【动态与节奏】
  - 角色动作序列：起始状态 → 过程动态 → 结束定格，标注每段对应时长与肢体联动细节
  - 环境动态变化：背景元素的运动规律（光影移动、风吹物体、粒子漂浮）与节奏
  - 整体时间节奏：快慢分布，情绪递进节点
【角色描述】
  - 外貌特征：面部轮廓、发型发色、核心标识，突出对应风格与品类的专属特质
  - 姿态动态：完整身体动态与手部联动细节，强调自然运动逻辑，体态松弛舒展
  - 表情变化：眼神落点、面部肌肉变化的时间过程，标注清晰情绪走向，杜绝空洞静态表情
  - 服装造型：款式、颜色、面料材质，标注主色 / 辅助色 / 点缀色占比，搭配运动产生的自然褶皱动态
【质感与细节】
  - 皮肤/画风质感：实拍类保留原生肌肤纹理、自然光影过渡；动漫类线条流畅、色块稳定、画风统一
  - 毛发/线条质感：实拍类发丝层次自然、随动真实；动漫类线条干净、无多余杂线
  - 材质表现：布料、金属、木质、玻璃等材质动态反光与形变符合物理逻辑
  - 光影层次：光源方向、软硬、冷暖随时间的过渡变化，明暗过渡自然无断层
【环境与氛围】
  - 空间场景：精准具体地点及环境特征，无模糊抽象环境描述
  - 光线来源与变化：自然光 / 人工光，光线软硬、光位与冷暖色温，标注随时间的变化过程
  - 色调与色彩：主色调与点缀色明确划分，严格遵循 70%/25%/5% 面积配比，标注饱和度层级（低饱和 / 中饱和 / 高饱和），明确整体情绪倾向
  - 细节元素：少量服务叙事的质感物件，不堆砌多余装饰道具
【音频描述（模型支持音频才输出）】
  - 环境音效：环境声音细节
  - 人物台词：角色对白
  - 背景音乐：曲风、情绪氛围
【技术参数建议】（仅 structured 模式使用）
  - 镜头类型：标准定焦 / 长焦 / 广角 / 微距等，搭配对应视觉效果与叙事作用释义
  - 运动节奏：舒缓 / 中等 / 急促，搭配对应情绪氛围释义
  - 质感补充：可按需添加柔焦、胶片颗粒、动态模糊等光学效果术语，搭配效果说明
  - 技术禁止项：不出现帧率、码率、分辨率、采样率、编码器等无效参数
【风格标签】3‑5个关键词概括整体气质与叙事调性
【画面收尾精简约束】画面无额外人物、无关花草、多余摆件、杂乱背景装饰，所有环境元素仅服务叙事节奏与情绪表达，不抢夺主体视觉焦点。""",
                "en": """[Structured Mode] Output strictly follow sections:
【Category】real‑shot / anime
【Movie Style】costume / sci‑fi / action / literary / suspense / documentary / anime‑film / general
【Global Positive Constraints】
  - Motion Base: physically‑plausible motion, fluent character action, natural environment change, no clipping / distortion / frame‑skip
  - Texture Base: real‑shot keep native skin texture & soft light‑shadow; anime maintain unified art‑style, smooth lines, stable color blocks
  - Camera Logic: 3‑D view follow cinematic aesthetic, camera movement serve narrative, correct perspective without distortion
【Frame Composition】
  - Visual Guidance: sight flow guided by character gaze, motion direction, environment line; no distracting redundant elements
  - Subject Position: horizontal percent + vertical percent, subject occupy 70% visual weight, background 30%
  - Aspect Ratio:16:9 /9:16 /4:3
  - Simplify Constraint: keep only core narrative scene & props; no extra plants, ornaments, passers‑by
【Shot & 3‑D Camera View】
  - Distance(shot): macro close‑up / standard close‑up / shoulder shot / three‑quarter / nine‑tenth / full‑scene portrait
  - Horizontal Azimuth: front / three‑quarter / profile / three‑quarter back, describe facial & contour narrative feature
  - Vertical Pitch: slight high‑angle / eye‑level / slight low‑angle, describe psychological feeling
  - Camera Movement: type(push/pull/pan/track/follow/crane/static), direction, speed, duration & narrative purpose
  - Depth‑of‑field: subject sharp with bg blur / full sharp / partial detail reserved, mark virtual‑real hierarchy
【Motion & Rhythm】
  - Character Action Sequence: start → process → end freeze, mark time span & limb linkage detail
  - Environment Dynamics: light shift, wind‑driven object, particle floating and rhythm
  - Global Tempo: fast‑slow distribution, emotion progression node
【Character Description】
  - Appearance: facial contour, hair style‑color, key feature
  - Pose Dynamics: full‑body motion & hand interaction, natural kinematics, relaxed posture
  - Expression Change: gaze point, facial muscle temporal process, clear emotion trend, avoid static hollow expression
  - Costume: style, color, fabric material, main / auxiliary / accent color ratio, natural fold under movement
【Texture & Detail】
  - Skin / Art‑style Texture: real‑shot native skin texture & soft light‑shadow; anime smooth line, stable color block, unified style
  - Hair / Line Texture: real‑shot natural hair motion; anime clean line‑art without messy stroke
  - Material Performance: cloth, metal, wood, glass reflection & deformation obey physics
  - Light‑Shadow Hierarchy: light direction, hardness‑softness, cold‑warm temporal transition, smooth shadow gradient
【Environment & Atmosphere】
  - Scene: concrete location, no vague abstract description
  - Light Source & Evolution: natural / artificial light, hardness‑softness, color‑temperature and temporal change
  - Color Scheme: main / auxiliary / accent color, strict 70%/25%/5% ratio, saturation level, overall emotional tendency
  - Detail Element: narrative‑oriented props only, no redundant ornament stack
【Audio Description(output only if model support audio)】
  - Ambient SFX: environment sound detail
  - Character Dialogue: character lines
  - BGM: music genre & mood
【Tech Suggestion】(structured‑only)
  - Lens Type: prime / telephoto / wide‑angle / macro with narrative explanation
  - Motion Tempo: slow‑relaxed / medium / urgent with mood explanation
  - Texture Enhancement: soft‑focus, film grain, motion‑blur with effect note
  - Forbidden Tech Item: forbid fps, bitrate, resolution, sampler, encoder and other numeric parameters
【Style Tags】3‑5 keywords for overall visual temperament
【Final Simplify Constraint】No extra character, irrelevant plant, redundant ornament, messy background. All elements serve narrative & emotion, never steal visual focus."""
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
        video_model: str,
        output_language: str = "auto",
        enable_global_preconstraint: bool = True,
        enable_negative_prompt: bool = True,
        output_format: str = "both"
    ) -> Dict:
        valid_video_models = ["Wan2.2", "LTX2.3", "MiniMax‑H3"]
        if preset_name not in self.preset_library:
            raise ValueError(f"预设模板不存在：{preset_name}")
        if video_model not in valid_video_models:
            raise ValueError(f"不支持的视频模型，可选：{valid_video_models}")

        preset = self.preset_library[preset_name]
        model_config = self.video_model_formula_library[video_model]

        if output_language == "auto":
            lang = self.detect_language(user_input)
        else:
            lang = output_language if output_language in ["zh", "en"] else "zh"

        global_rule = self.global_base_rules[lang] if enable_global_preconstraint else ""
        preset_rule = preset["preset_rules"][lang]
        pos_constraint = preset["positive_constraints"][lang]
        formula_hint = model_config[f"formula_zh" if lang == "zh" else "formula_en"]
        natural_guide = self.format_guide["natural"][lang]
        structured_guide = self.format_guide["structured"][lang]

        prompt_parts = []
        if enable_global_preconstraint:
            prompt_parts.append(f"【Hard Precondition Baseline】\n{pos_constraint}")
            prompt_parts.append(global_rule)
        prompt_parts.append(f"视频模型【{video_model}】内容组织公式：{formula_hint}")
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
        # MiniMax‑H3强制置空negative_prompt，接口不识别
        if enable_negative_prompt and video_model != "MiniMax‑H3":
            negative_prompt = preset["negative_base"][lang]
        else:
            negative_prompt = ""

        return {
            "status": "success",
            "llm_input_prompt": final_llm_prompt,
            "positive_constraint": pos_constraint,
            "negative_prompt": negative_prompt,
            "output_language": lang,
            "video_model": video_model,
            "preset_name": preset_name,
            "preset_display_name": preset["display_name"],
            "user_raw_input": user_input,
            "enable_preconstraint": enable_global_preconstraint,
            "enable_negative": enable_negative_prompt
        }