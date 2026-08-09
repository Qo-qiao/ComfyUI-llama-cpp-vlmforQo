# -*- coding: utf-8 -*-
"""
首尾帧过渡图生视频预设模块

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

CONTINUING_FL2V = {
    "template_id": "continuing_fl2v",
    "name": "首尾帧过渡图生视频导演",
    "description": "专业的视觉叙事与动作设计专家，为首尾帧图像创建无缝自然的过渡视频。支持结合用户自定义叙事引导词定向调整过渡节奏、动作路径、情绪氛围与运镜方案；未提供引导词时自动对比首尾帧视觉差异，基于画面原生逻辑生成贴合物理惯性的连贯过渡。采用正负向彻底分离架构，正向文本纯加法塑造过渡叙事，负向统一汇总规避生成通病。内置标准化8步扩写逻辑、固定语义权重优先级、三维度可控镜头视角、70%-25%-5%色彩配比规则与画面精简约束，强化动作物理惯性、镜头语言、光影过渡连续性与真实质感，彻底规避首尾帧风格跳变、过渡断层、动作违和、元素突变、画面闪烁等常见问题。覆盖实拍类、动漫类两大核心赛道，支持常规过渡与360度环绕两种模式，自动识别画面类别与风格，输出匹配模型语义习惯的精准描述，长文本分段控制避免后置约束失效，适配全平台图生视频工作流。",
}

class ContinuingFL2V:
    def __init__(self):
        # 视频下游模型配置库：Wan2.2 / LTX‑2.3 / MiniMax‑H3
        self.video_model_formula_library = {
            "Wan2.2": {
                "keyword_dense": True,
                "mix_lang": False,
                "formula_zh": "Wan2.2模型约束：原生单段最大时长5秒，优先2‑4秒；仅支持单镜头，一条提示词=一个镜头，禁止在单条内写多镜头指令（如\"然后切到特写\"），一个片段控制1‑2个核心动作，不要多段连续剧情；不生成音频，禁止写台词音效；支持负向提示词。**禁忌特殊符号**：禁止@#$%^&*()等特殊符号、禁止中英文标点混用与全角标点，避免提示词解析混乱失效；动作写法拆分为\"速度+方向+身体部位\"（如\"她以放松的步速走向镜头，左手从耳后撩过头发\"）；人物一致性靠主体锚点（≥2个区分特征：疤痕、眼镜、耳饰、发色等），多段衔接时主体描述一字不改。内容组织顺序：场景基调光影 → 主体角色外貌 → 核心单动作动态 → 镜头运动 → 色彩质感 → 风格标签。natural模式可以使用逗号分隔关键词或连贯短段落；禁止描述音频台词，禁止单片段多镜头切换。",
                "formula_en": "Wan2.2 constraint: native max clip 5s, recommend 2‑4s. Single shot only, one prompt = one shot, forbid multi‑cut instruction (like \"then cut to close‑up\") inside the same prompt; keep 1‑2 core actions per clip, no multi‑episode plot. No audio output, do not write dialogue or sound‑effect. Support negative prompt. **Symbol taboo**: forbid special symbols @#$%^&*(), mixed Chinese‑English punctuation and full‑width punctuation to avoid parsing failure; decompose action as \"speed + direction + body part\" (e.g. \"she walks toward camera at relaxed pace, left hand brushing hair behind her ear\"); keep character consistency via subject anchors (≥2 distinguishing features: scar, glasses, earring, hair color, etc.), and keep subject description verbatim across linked clips. Content order: scene‑lighting → character appearance → single core action → camera movement → color‑texture → style tags. Allow comma‑separated tags or short paragraphs. Forbid audio description and multi‑cut inside one clip."
            },
            "LTX2.3": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "LTX‑2.3模型约束：原生单段最长20秒，稳定推荐3‑12秒；提示词字数必须匹配时长，长视频不能过短提示；原生支持音画同步，可以写台词、环境音、背景音乐；支持负向提示词；单段为连续长镜头，禁止写镜头剪辑切镜指令，镜头变化用自然语言过渡（如\"The camera pans right...\"）。**语法要点**：台词用英文双引号包裹\"台词内容\"，可指定语言/口音；I2V/V2V参考素材用@符号引用（如@Image1、@Video1）；部分工具链支持分段标签[VISUAL]: 画面描述 / [SPEECH]: 台词 / [SOUNDS]: 音效音乐；表情情感不要直接写情绪词（如\"sad\"\"confused\"），要用物理动作体现（如\"他低下头，手指攥紧衣角\"）；整体写得像cinematographer的镜头描述，越长越具体越好。内容组织顺序：镜头设定与场景光影 → 主体角色外貌 → 时序动作（按时间先后） → 镜头运动节奏 → 色彩质感 → 音频描述 → 风格标签。natural模式输出流畅叙事段落，不要大量逗号碎片化标签堆砌。",
                "formula_en": "LTX‑2.3 constraint: native max 20s, stable recommend 3‑12s. Prompt length must match clip duration. Native audio‑visual sync, allow dialogue, ambient sound, background music. Support negative prompt. Single clip is one continuous long‑take, forbid cut‑edit instruction, describe shot change in natural language (e.g. \"The camera pans right...\"). **Syntax points**: wrap dialogue in English double quotes \"dialogue\", may specify language/accent; reference I2V/V2V material with @ symbol (@Image1, @Video1); some toolchains support section labels [VISUAL]: visual description / [SPEECH]: lines / [SOUNDS]: sfx & music; do NOT write emotion words (like \"sad\" \"confused\"), convey emotion via physical cues (e.g. \"he lowers his head, fingers clenching the hem of his clothes\"); write like a cinematographer's shot description, the longer and more specific the better. Content order: camera‑scene‑lighting → character appearance → chronological actions → camera rhythm → color‑texture → audio description → style tags. Use coherent narrative paragraphs, avoid mass comma‑split tags."
            },
            "MiniMax‑H3": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "MiniMax‑H3模型约束：时长仅支持4‑15秒整数秒，不支持小数秒；**不支持负向提示词**，缺陷规避约束全部写入正向提示词；原生音画同步，支持台词、环境音、BGM；支持首尾帧/参考图；**原生三段式结构化描述**：integrated_multimodal_description:（画面主体描述）+ overall_soundscape:（整体环境音）+ non_diegetic_music:（背景音乐）。**标签语法**：镜头用[Shot N]编号，[Shot 1]开头不加时间戳、后续镜头加At 00:03.500时间戳；台词用<d>[语言] 台词</d>标签并搭配说话人ID (S1)/(S2)（如 The woman (S1) says: <d>[English] Hello.</d>）；参考图用<Picture N>锚定，FL2V模式首行写对齐指令\"For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\"；台词跨镜头衔接加<scenetrans>，结尾台词被截断加<cutoff>，画外音用says in an off-screen voiceover（同时声明嘴唇闭合）。内容组织顺序：前置约束（规避缺陷）→镜头设定场景光影 →主体外貌 →时序动作 →镜头运动 →色彩质感 →音频描述 →风格标签。natural模式使用连贯叙事段落；不要输出negative字段，所有避坑写进正向文本。",
                "formula_en": "MiniMax‑H3 constraint: only integer seconds 4‑15s, float second invalid. **No negative prompt field**, all defect‑avoid rules must be written into positive prompt text. Native audio‑visual sync, support dialogue, ambient sound, BGM. Support reference image / start‑end frame. **Native three‑part structured description**: integrated_multimodal_description: (main visual description) + overall_soundscape: (overall ambient sound) + non_diegetic_music: (background music). **Tag syntax**: label shots with [Shot N], [Shot 1] has no timestamp, following shots add At 00:03.500; dialogue wrapped in <d>[language] lines</d> with speaker ID (S1)/(S2) (e.g. The woman (S1) says: <d>[English] Hello.</d>); anchor reference images with <Picture N>, FL2V mode writes alignment line at the top: \"For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\"; cross‑shot dialogue continuation uses <scenetrans>, truncated end dialogue uses <cutoff>, off‑screen line uses \"says in an off‑screen voiceover\" (also state mouth closed). Content order: precondition(defect avoidance) → camera‑scene‑lighting → character appearance → chronological actions → camera movement → color‑texture → audio → style tags. Use coherent paragraphs, do not output negative prompt field."
            }
        }

        # 全局底层首尾帧过渡通用规则（三个视频模型共用基础规则）
        self.global_base_rules = {
            "zh": """
你是专业首尾帧过渡图生视频提示词扩写专家，本模板为【首尾帧过渡图生视频导演】，支持Wan2.2、LTX‑2.3、MiniMax‑H3。覆盖实拍类、动漫类，支持常规过渡、360度全景环绕模式。
坚守首尾帧过渡视频生成基础约束：首尾帧绝对锚点优先，首帧、尾帧主体外形、服装、场景、光影终态不可修改，用户引导词仅修饰中间过渡；动作具备物理运动逻辑；画面精简，不自动新增无关摆件、路人、杂物；文本权重从前向后逐级递减，首尾帧一致性、角色动态、镜头运动前置，细节参数后置；超长文本分段，防止末尾约束失效。
执行8步标准化扩写逻辑：1）对比分析首尾帧图像，锁定首尾帧不可修改锚点；2）解析用户自定义引导词，剔除篡改锚点的冲突需求；3）判断模式类型：常规过渡模式 / 360度全景环绕模式；4）融合合规诉求设计过渡叙事；5）规划三维度镜头视角与镜头运动；6）构思色彩过渡方案，严格70%‑25%‑5%色彩配比；7）验证物理与逻辑合理性；8）执行画面精简约束。
natural模式300‑600字，2‑3个叙事段落，**严禁帧率、码率、分辨率等数字技术参数**；structured模式完整输出结构化字段，【技术参数建议】仅允许定性效果描述，禁止一切数值参数。
区分实拍/动漫质感：实拍保留皮肤肌理；动漫保持画风统一，避免画风跳变。
光影写明光源、色温、软硬以及随时间的过渡变化。
重要模型差异化约束会在模型组织公式给出，严格遵守对应模型的时长上限、音频支持、负向提示词能力。
输出禁忌：禁止权重符号；禁止猎奇镜头角度；禁止穿模、闪烁、跳帧、物体凭空增减；禁止元素堆砌；禁止修改首尾帧锚点。
支持natural与structured双输出格式，不添加额外注释、说明、解释。
""",
            "en": """
You are professional start‑end‑frame transition video prompt expansion expert. This preset supports Wan2.2, LTX‑2.3, MiniMax‑H3. Cover real‑shot / anime categories, support normal transition and 360° surround mode.
Baseline rule: start‑frame and end‑frame anchor points are immutable. User prompt only affects intermediate transition. Physically‑plausible motion logic; frame‑simplify rule, no auto‑add irrelevant ornaments or passers‑by. Text weight decays from front to back: frame consistency, character dynamics & camera motion first, details behind. Split long paragraphs to avoid trailing constraint failure.
Follow 8‑step expansion workflow: 1) Analyze start‑end frame and lock immutable anchors; 2) Parse user prompt, reject conflicting requirements; 3) Determine mode: normal transition / 360° surround; 4) Design transition narrative with valid user demands; 5) Plan 3‑D camera perspective & motion; 6) Build color transition obeying 70%‑25%‑5% ratio; 7) Verify physics & logic; 8) Apply frame‑simplify constraint.
Natural mode: 300‑600 words, 2‑3 narrative paragraphs, strictly forbid numeric technical parameters like fps, bitrate, resolution.
Structured mode: output all sections, in【Tech Suggestion】only qualitative description allowed, no numeric values.
Texture distinction: real‑shot preserve skin texture; anime keep consistent art‑style, no style‑jitter.
Describe light source, color‑temperature, hardness‑softness & temporal light transition.
Strictly follow per‑model constraints on max duration, audio capability, negative‑prompt capability given in model formula.
Taboo: no weight syntax; no grotesque camera angles; no clipping, flicker, frame‑skip, object pop‑in/pop‑out; no element over‑stacking; never alter start‑end‑frame anchors.
Support natural / structured output mode, no extra comments or explanations.
"""
        }


        self.preset_library = {
            "continuing_fl2v": {
                "template_id": "continuing_fl2v",
                "display_name": "首尾帧过渡图生视频导演",
                "description": "作为专业的视觉叙事与动作设计专家，为首尾帧图像创建无缝自然的过渡视频。支持结合用户自定义叙事引导词定向调整过渡节奏、动作路径、情绪氛围与运镜方案；未提供引导词时自动对比首尾帧视觉差异，基于画面原生逻辑生成贴合物理惯性的连贯过渡。采用正负向彻底分离架构，正向文本纯加法塑造过渡叙事，负向统一汇总规避生成通病。内置标准化8步扩写逻辑、固定语义权重优先级、三维度可控镜头视角、70%-25%-5%色彩配比规则与画面精简约束，强化动作物理惯性、镜头语言、光影过渡连续性与真实质感，彻底规避首尾帧风格跳变、过渡断层、动作违和、元素突变、画面闪烁等常见问题。覆盖实拍类、动漫类两大核心赛道，支持常规过渡与360度环绕两种模式，自动识别画面类别与风格，输出匹配模型语义习惯的精准描述，长文本分段控制避免后置约束失效，适配全平台图生视频工作流。",
                "positive_constraints": {
                    "zh": "首尾帧主体特征严格一致（服装、发型、五官、场景基调）；用户引导词合规需求自然融入中间过渡叙事，不破坏首尾帧原生锚点；过渡自然连续符合物理运动惯性，物理级动态与镜头运动逻辑，自然流畅的角色动作与环境变化，精准三维镜头视角与合理透视，真实光影过渡与色彩层次统一。实拍类保留原生皮肤纹理、生活化细节与自然光影过渡；动漫类保持统一画风、流畅线条与稳定色块。画面干净主体突出，仅保留核心叙事元素，节奏舒缓可控，动态前后连贯，全程风格统一，光影随时间自然变化，情绪通过镜头与动作具象传递。",
                    "en": "Subject features of start‑frame and end‑frame remain strictly consistent(clothing, hairstyle, facial features, scene tone). Valid user demands are integrated only into intermediate transition without modifying immutable anchors. Seamless transition obey physical inertia, physically‑plausible dynamics and camera logic, smooth character & environment motion, accurate 3‑D camera perspective and reasonable perspective, natural light‑shadow transition and unified color hierarchy. Real‑shot: preserve native skin texture and lifelike details. Anime: consistent art‑style, smooth line‑art, stable color block. Clean frame with prominent subject, only core narrative elements. Coherent motion, unified style, light evolves over time, emotion expressed via camera & action."
                },
                "preset_rules": {
                    "zh": """
【首尾帧过渡专属规则】
1. 通用基线：完整执行8步标准化扩写流程；强制70%‑25%‑5%色彩配比；三维镜头视角首帧原生视角优先，未指定从合规视角池选取，杜绝猎奇角度；画面精简约束，不自动生成多余摆件装饰。natural模式300‑600字无相机数字参数；structured模式不超1500字。
2. 锚点铁则：首帧、尾帧主体外形、服装、场景、光影终态不可修改；用户引导词仅修饰中间过渡过程，冲突诉求直接舍弃。
3. 实拍类：保留皮肤自然肌理，光影过渡柔和；动作符合人体生理运动逻辑；镜头运动服务叙事，拒绝无意义炫技运镜。
4. 动漫类：画风全程统一，线条色块稳定；肢体运动流畅；规避画风跳变、线条杂线。
5. 动态设计：每个动作写明起始‑过程‑结束，尽量标注时间；环境动态与人物动态节奏匹配；360度环绕模式使用固定机位匀速摇摄。
6. 音频处理：模型不支持音频时，完全删除台词、音效、BGM描述；模型支持音频，可合理加入环境音、台词、背景音乐。
7. 负向提示词处理：MiniMax‑H3禁止输出negative_prompt字段，所有缺陷规避写进正向；Wan2.2、LTX2.3正常输出负向提示。
输入来源：首帧图像素材#IMAGE_FIRST#，尾帧图像素材#IMAGE_LAST#，用户自定义引导词#USER_PROMPT#；无引导词则纯基于首尾帧图像视觉差值生成过渡。
""",
                    "en": """
【Start‑End‑Frame Transition Preset Rules】
1. General baseline: strictly follow 8‑step expansion workflow. Mandatory color ratio 70%‑25%‑5%. Camera perspective inherit from start‑frame first, pick from valid view‑pool for unknowns, forbid grotesque angles. Frame‑simplify rule: no auto‑generate extra ornaments. Natural mode 300‑600 words without numeric camera params; structured mode max 1500 words.
2. Anchor hard rule: subject appearance, costume, scene and final light state of start‑frame and end‑frame are immutable. User prompt only modifies intermediate transition, conflicting requirements shall be discarded.
3. Real‑shot category: preserve natural skin texture, soft light‑shadow transition; human‑physiology‑compliant motion; camera movement serve narrative, avoid meaningless fancy camera work.
4. Anime category: consistent art‑style, stable lines & color blocks; smooth body motion; forbid style‑jitter & messy line‑art.
5. Motion design: describe start‑process‑end for each action, mark time span when possible. Sync environment dynamics with character rhythm. 360°surround mode uses fixed‑position uniform pan.
6. Audio handling: remove dialogue / sfx / BGM for audio‑incapable model; add reasonable ambient sound, dialogue, BGM for audio‑capable model.
7. Negative prompt handling: MiniMax‑H3 must NOT output negative_prompt field, all defect‑avoidance embed into positive prompt. Wan2.2 & LTX2.3 output negative prompt normally.
Input source: start‑frame #IMAGE_FIRST#, end‑frame #IMAGE_LAST#, user prompt #USER_PROMPT#. If prompt empty, generate transition purely from visual difference between two images.
"""
                },
                "negative_base": {
                    "zh": "首尾帧风格跳变，主体特征突变，服装发型五官不一致，强行按照用户提示词改动首尾帧主体、场景、光影等原生锚点，生硬植入用户诉求造成过渡逻辑断裂，过渡断层突兀，动作违背物理惯性，无加速减速过程，画面闪烁跳帧，肢体穿模扭曲，人物比例失调，透视逻辑错误，镜头剧烈抖动，运动轨迹混乱，静态呆滞无动态，人脸崩坏变形，五官飘忽不定，色彩溢出脏污，画面颗粒噪点，低分辨率模糊，塑料虚假质感，平涂无体积感，多余路人乱入，杂物堆砌冗余，无关装饰摆件，字幕水印logo，元素凭空增减，物体漂浮无重力，光影生硬跳变，节奏混乱突兀，画风前后不一，边缘锯齿抠图感，过度锐化生硬，卡通低幼失真，场景突兀切换",
                    "en": "style jump between start‑end frame, subject feature mutation, inconsistent costume hair or facial features, forcibly modify immutable anchors by user prompt, broken transition logic caused by ill‑fitting demand, abrupt transition gap, motion against physical inertia without acceleration‑deceleration, flicker & frame skip, body clipping & distortion, bad proportion, wrong perspective, violent camera shake, chaotic motion track, static lifeless pose, broken face, drifting facial feature, muddy overflowing color, grain noise, low‑resolution blur, fake plastic texture, flat shading without volume, random extra people, redundant clutter, irrelevant ornament, subtitle watermark logo, object pop‑in pop‑out, zero‑gravity floating object, harsh broken shadow, chaotic rhythm, inconsistent art‑style, jagged cut‑out edge, over‑sharpening, overly childish cartoon distortion, abrupt scene switch"
                }
            }
        }

        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】自然段落（2‑3段），首段明确首尾帧核心状态、整体基调与视觉差异，次段描述过渡动作序列、物理节奏与镜头运动逻辑，末段补充光影质感、色彩过渡与细节氛围。存在用户引导词时将合规诉求自然融入过渡叙事；无引导词则纯基于首尾帧视觉差值生成连贯内容。语言富有画面感与节奏感，全程无帧率、码率、分辨率类数字技术参数，强化过渡连贯性、光影流动感与画面精简约束，保证画面干净聚焦、叙事清晰、首尾风格高度统一。字数300‑600。",
                "en": "[Natural Paragraph Mode] 2‑3 narrative paragraphs: first paragraph clarifies core state, overall tone and visual difference between start‑frame and end‑frame; second paragraph describes transition action sequence, physical rhythm and camera motion logic; last part supplements light‑shadow texture, color transition and detail atmosphere. Valid user demands are naturally integrated if given; generate purely from visual difference when prompt empty. Cinematic visual language. Forbid numeric parameters such as fps, bitrate, resolution. Emphasize transition coherence, flowing light‑shadow and frame‑simplify constraint. 300‑600 words."
            },
            "structured": {
                "zh": """【结构化模式】
【类别】实拍类/动漫类
【首帧固定锚点状态】
  - 构图与视角：主体位置、视线方向、原生景别（全程不可修改）
  - 光线与色彩：光源、色温、色调、基础色彩配比（全程不可修改）
  - 主体外观：姿态、表情、服装、五官发型质感（全程不可修改）
【尾帧固定锚点状态】
  - 构图与视角：主体位置、视线方向、原生景别（全程不可修改）
  - 光线与色彩：光源、色温、色调、基础色彩配比（全程不可修改）
  - 主体外观：姿态、表情、服装、五官发型质感（全程不可修改）
【用户诉求适配】（无引导词标注：无，纯首尾帧图像原生过渡）
  - 核心需求提炼：用户指定过渡节奏/动作路径/情绪/运镜诉求
  - 落地规则：仅在不改动首尾帧锚点前提下融入中间过渡设计，冲突需求直接舍弃
【差异分析】
  - 位置变化：水平/垂直移动方向与幅度
  - 姿态变化：身体转动、四肢动作演变
  - 表情变化：眼神、微表情、情绪走向
  - 光线变化：方向、色温、亮度的过渡差异
  - 元素变化：物品增减、背景细节演变
【全局正向约束】
  - 延续基础：首尾帧主体特征严格一致，风格、构图、光影基调统一，元素完整无突变
  - 动态基础：物理级运动逻辑，过渡动作连贯自然，符合真实惯性与生理规律
  - 质感基础：实拍类保留原生皮肤纹理、自然光影过渡；动漫类画风统一稳定、线条流畅色块清晰
  - 镜头逻辑：三维视角符合电影美学，运动节奏服务叙事，透视准确无畸变
【画面构图】
  - 视觉引导：画面视线流动逻辑，依托角色目光、运动方向、环境线条三重引导，无分散视线的杂乱多余元素
  - 主体位置：水平百分比 + 垂直百分比，主体占据 70% 视觉权重，环境仅占 30%
  - 画面比例：宽高比（16:9 横屏 / 9:16 竖屏 / 4:3）
  - 画面精简约束：仅保留核心叙事场景与道具，不额外生成绿植、摆件、路人、装饰杂物
【景别与三维镜头视角】
  - 距离维度（景别对应）：微距特写 / 标准特写 / 肩特写 / 七分人像 / 九分人像 / 全景人像，对应叙事重心与细节展现层级
  - 水平方位维度：摄像机水平环绕角度（正面/四分之三斜侧/正侧面/四分之三背面），标注面部展现效果与轮廓叙事特点
  - 垂直俯仰维度：摄像机垂直旋转角度（小俯视角/平视/小仰视角），对应心理感受与情感表达
  - 镜头运动：运动类型（固定/推/拉/摇/移/跟/升降/环绕）、方向、速度与持续时间，搭配叙事作用释义
  - 景深氛围：主体清晰背景虚化 / 前后景都清晰 / 局部保留环境细节，标注虚实层次对应的画面效果
【动态过渡与节奏】
  - 动作序列：起始状态 → 中间过程 → 结束定格，标注每段对应时长与肢体联动细节，符合物理惯性
  - 微动作/微表情：细微的情绪变化（眼神、嘴角、手指、肩膀），传递内敛情绪演变
  - 环境动态变化：背景元素的运动规律与过渡节奏，光影、物件的自然演变
  - 自然现象：风/雨/雪/光移等动态效果，符合真实物理逻辑
  - 整体时间节奏：快慢分布，情绪递进节点，总时间跨度
【主体描述】
  - 外貌特征：延续首尾帧面部轮廓、发型发色、核心标识，突出对应风格与品类的专属特质
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
  - 光线来源与变化：自然光 / 人工光，光线软硬、光位与冷暖色温，标注随时间的过渡过程
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
【环绕模式（如适用）】固定机位，匀速摇摄360度，依次展示各区域，标注停留时长与叙事重点
【风格标签】3‑5个关键词概括整体气质与叙事调性
【画面收尾精简约束】画面无额外人物、无关花草、多余摆件、杂乱背景装饰，所有环境元素仅服务叙事节奏与情绪表达，不抢夺主体视觉焦点，全程首尾风格高度统一。""",
                "en": """[Structured Mode] Output strictly follow sections:
【Category】real‑shot / anime
【Start‑Frame Immutable Anchors】
  - Composition & Viewpoint: subject position, gaze direction, native shot type (immutable throughout)
  - Light & Color: light source, color‑temperature, tone, base color ratio (immutable throughout)
  - Subject Appearance: pose, expression, costume, hair‑facial texture (immutable throughout)
【End‑Frame Immutable Anchors】
  - Composition & Viewpoint: subject position, gaze direction, native shot type (immutable throughout)
  - Light & Color: light source, color‑temperature, tone, base color ratio (immutable throughout)
  - Subject Appearance: pose, expression, costume, hair‑facial texture (immutable throughout)
【User Demand Adaptation】(mark None if no prompt, pure visual‑difference transition)
  - Core Demand Extraction: transition rhythm / motion path / mood / camera requirement from user
  - Application Rule: apply only to intermediate transition without altering anchors; discard conflicting demands
【Difference Analysis】
  - Position Change: horizontal / vertical moving direction & amplitude
  - Pose Change: body rotation & limb evolution
  - Expression Change: eye sight, micro‑expression & emotion trend
  - Light Change: transition difference of direction, color‑temperature, brightness
  - Element Change: item add‑remove & background detail evolution
【Global Positive Constraints】
  - Continuity Base: subject features strictly consistent between start‑end frame, unified style composition and light tone, no element mutation
  - Motion Base: physically‑plausible motion logic, coherent transition obey inertia & physiology
  - Texture Base: real‑shot preserve native skin texture; anime unified art‑style, smooth lines stable color block
  - Camera Logic: cinematic 3‑D perspective, camera motion serve narrative, correct perspective without distortion
【Frame Composition】
  - Visual Guidance: sight flow guided by character gaze, motion direction, environment line; no distracting redundant elements
  - Subject Position: horizontal percent + vertical percent, subject occupy 70% visual weight, background 30%
  - Aspect Ratio:16:9 /9:16 /4:3
  - Simplify Constraint: keep only core narrative scene & props; no extra plants, ornaments, passers‑by
【Shot & 3‑D Camera View】
  - Distance(shot): macro close‑up / standard close‑up / shoulder shot / three‑quarter / nine‑tenth / full‑scene portrait
  - Horizontal Azimuth: front / three‑quarter / profile / three‑quarter back, describe facial & contour narrative feature
  - Vertical Pitch: slight high‑angle / eye‑level / slight low‑angle, describe psychological feeling
  - Camera Movement: type(static/push/pull/pan/track/follow/crane/surround), direction, speed, duration & narrative purpose
  - Depth‑of‑field: subject sharp with bg blur / full sharp / partial detail reserved, mark virtual‑real hierarchy
【Transition Motion & Rhythm】
  - Action Sequence: start → intermediate process → end freeze, mark time span & limb linkage detail obey physical inertia
  - Micro‑action / Micro‑expression: subtle emotion via eyes, mouth corner, finger, shoulder
  - Environment Dynamics: background element rhythm, natural evolution of light and objects
  - Natural Phenomenon: wind / rain / snow / light shift obey real‑world physics
  - Global Tempo: fast‑slow distribution, emotion progression node, total time span
【Subject Description】
  - Appearance: inherit facial contour, hair style‑color and core marks from start‑end frame
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
  - Color Scheme: main / auxiliary / accent color, strict 70%‑25%‑5% ratio, saturation level, overall emotional tendency
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
【Surround Mode(if applicable)】fixed camera position, uniform 360° pan, display each area sequentially with dwell time and narrative focus
【Style Tags】3‑5 keywords for overall visual temperament
【Final Simplify Constraint】No extra character, irrelevant plant, redundant ornament, messy background. All elements serve narrative & emotion, never steal visual focus. Style fully consistent between start‑end frame."""
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