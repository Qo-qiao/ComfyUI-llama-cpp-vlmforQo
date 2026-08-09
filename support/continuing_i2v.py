# -*- coding: utf-8 -*-
"""
图生视频预设模块

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

CONTINUING_I2V = {
    "template_id": "continuing_i2v",    
    "name": "图生视频连续性导演",
    "description": "专业的图生视频连续性导演，基于首帧图像创造自然流畅、富有情感延续性的动态视频。支持结合用户自定义叙事引导词定向优化动态走向、情绪氛围、运镜节奏；未提供引导词时自动基于图像本身原生构图、光影、主体状态生成贴合物理逻辑的自然画面延续。采用正负向彻底分离架构，正向文本纯加法塑造延续动态，负向统一汇总规避生成通病。内置标准化8步扩写逻辑、固定语义权重优先级、三维度可控镜头视角、7:2.5:0.5色彩配比规则与画面精简约束，强化微动作叙事、镜头语言、物理级光影与真实质感，彻底规避风格漂移、画面闪烁、肢体穿模、逻辑混乱、元素堆砌等图生视频常见问题。覆盖实拍类、动漫类两大核心赛道，自动识别首帧类别与风格，根据选择的视频模型输出匹配该模型语义习惯的精准描述，长文本分段控制避免后置约束失效，适配全平台图生视频工作流。",
}

class ContinuingI2V:
    def __init__(self):
        # 视频下游模型配置库：Wan2.2 / LTX2.3 / MiniMax‑H3
        self.video_model_formula_library = {
            "Wan2.2": {
                "keyword_dense": True,
                "mix_lang": False,
                "formula_zh": "Wan2.2模型约束：原生单段最大时长5秒，推荐4‑5秒（超过5秒易崩）；仅支持单镜头，一个片段控制1‑2个核心微动作，禁止大幅度位移；不生成音频，禁止写台词音效；支持负向提示词。**禁忌特殊符号**：禁止@#$%^&*()等特殊符号、禁止中英文标点混用与全角标点，避免提示词解析混乱失效；动作写法拆分为“速度+方向+身体部位”（如“她以放松的步速走向镜头，左手从耳后撩过头发”）；人物一致性靠主体锚点（≥2个区分特征：疤痕、眼镜、耳饰、发色等），首帧与后续衔接时主体描述一字不改。**景别跨度压缩**：单镜头景别变化不超过两个层级（如远景→中景），最稳范围为远景→中景偏远处，人物禁止跑到近景特写；大跨度+高速动态会引发五官漂移、发型结块、服饰突变，大跨度场景须拆分为多镜头。**动作强度控制**：高风险动态细节一律降强度，“剧烈甩动”“发丝风中飞扬”改为“自然甩动”“长发自然飘动”，避免头发结块、辫子与身体穿模、发型前后不一致；禁止“猛地急停转身”“急速冲刺骤停”等易崩坏动作，爆发力体现在奔跑等过程动作而非骤停。**光影稳定性**：禁止微观高频光影动态（如“叶片光斑持续跳跃”），易致画面忽明忽暗、光影闪烁、光斑静止无细节，改为稳定表达“阳光穿过树叶形成斑驳光影，叶片上有柔和细碎高光”；禁止薄雾+强光柱等高开销光影叠加高速运动。**效果化表达**：禁止评价式模糊指令（“背景虚化处理得当”），改为明确效果（“主体清晰、背景柔和虚化、人物是视觉中心”）；“电影级质感”“电影级光影”等空词须绑定具体画面特征（柔和自然光、绿色背景衬托白色连衣裙、发丝边缘轮廓光、光影过渡自然），不单独空用。**运镜简化**：固定机位最稳，禁止复合叠加运镜（如“推进+横移”“推拉结合”），优先固定机位或单一运镜。**负向过滤**：“无多余装饰元素”类正向剔除句保留作简洁性提示，真正强过滤靠负向提示词。内容组织顺序：首帧锚点延续约束 → 场景基调光影 → 主体微动态 → 镜头运动 → 色彩质感 → 风格标签。natural模式可以使用逗号分隔关键词或连贯短段落；禁止描述音频台词，禁止单片段多镜头切换。",
                "formula_en": "Wan2.2 constraint: native max clip 5s, recommend 4‑5s (over 5s tends to break). Single shot only, keep 1‑2 core micro‑actions per clip, forbid large‑scale displacement. No audio output, do not write dialogue or sound‑effect. Support negative prompt. **Symbol taboo**: forbid special symbols @#$%^&*(), mixed Chinese‑English punctuation and full‑width punctuation to avoid parsing failure; decompose action as \"speed + direction + body part\" (e.g. \"she walks toward camera at relaxed pace, left hand brushing hair behind her ear\"); keep character consistency via subject anchors (≥2 distinguishing features: scar, glasses, earring, hair color, etc.), and keep subject description verbatim between reference frame and following clips. **Shot span compression**: single‑shot framing change limited to two levels (e.g. long → medium), most stable range is long → medium‑far, subject must NOT run into close‑up; large span + fast motion drifts facial features, clumps hair and mutates costume — split large‑span scenes into multiple shots. **Action intensity control**: downgrade high‑risk dynamics, \"violent whipping\" \"hair strands flying in wind\" become \"natural swinging\" \"long hair flowing naturally\", avoid hair clumping, ponytail/body clipping and inconsistent hairstyle; forbid crash‑prone moves like \"abrupt stop‑and‑turn\" \"sudden sprint halt\", put the burst into process actions like running rather than a sudden halt. **Lighting stability**: forbid micro high‑frequency light dynamics (e.g. \"dappled light continuously jumping on leaves\") which cause brightness flicker, shimmering and static glints, use stable phrasing \"sunlight through leaves casts dappled shadows, soft fine highlights on leaves\"; forbid high‑cost combos like thin fog + strong light beam stacked on fast motion. **Effect‑oriented wording**: forbid evaluative vague instructions (\"well‑handled background blur\"), rewrite as explicit effects (\"sharp subject, softly blurred background, subject as visual center\"); bind vague words like \"cinematic quality\" to concrete visual features (soft natural light, green backdrop against white dress, rim light on hair edges, natural light‑shadow transition) instead of using them alone. **Camera simplification**: fixed camera is most stable, forbid compound stacked moves (\"push + pan\" \"dolly zoom\"); prefer fixed camera or a single movement. **Negative filtering**: positive exclusion phrases like \"no extra ornament\" remain as simplicity hints, the real strong filtering relies on the negative prompt. Content order: reference‑frame anchor constraint → scene‑lighting → character micro‑motion → camera movement → color‑texture → style tags. Allow comma‑separated tags or short paragraphs. Forbid audio description and multi‑cut inside one clip."
            },
            "LTX2.3": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "LTX‑2.3模型约束：原生单段最长20秒，稳定推荐3‑12秒；提示词字数必须匹配时长；原生支持音画同步，可以写台词、环境音、背景音乐；支持负向提示词；单段为连续长镜头，禁止写镜头剪辑切镜指令，镜头变化用自然语言过渡（如\"The camera pans right...\"）。**镜头运动简化**：单镜头只保留一种主导运镜，禁止复合叠加运镜（如\"推进+横移\"\"推拉结合\"），复合运镜易致运镜失控、画面抖动、背景扭曲、人物出画。**动作复杂度压缩**：单镜头控制1‑2个核心动作，动作链按\"起始→过程→结束\"平缓推进，禁止多段连续大动作链；禁止\"猛地急停转身\"\"急速冲刺骤停\"等高崩坏风险动作（急停转身极易肢体崩坏、腿部穿模、姿态僵硬），爆发力应体现在奔跑等过程动作而非骤停；禁止\"定格\"\"冻结帧\"\"画面定格在XX\"指令（模型不支持，写了无效且干扰运动收尾）。**景别跨度压缩**：单镜头景别变化不超过两个层级（如中远景→中景），禁止远景→中景→近景三级跳；大跨度+高速动态叠加会引发发型、服饰、五官漂移，大跨度场景须拆分为多镜头。**语法要点**：台词用英文双引号包裹\"台词内容\"，可指定语言/口音；I2V参考素材用@符号引用（如@Image1）；部分工具链支持分段标签[VISUAL]: 画面描述 / [SPEECH]: 台词 / [SOUNDS]: 音效音乐；表情情感不要直接写情绪词（如\"sad\"\"confused\"），要用物理动作体现（如\"他低下头，手指攥紧衣角\"）；光影只写相对稳定的静态描述，禁止薄雾+强光柱等高开销光影叠加人物高速运动（易画面发灰、过曝、光柱闪烁不稳定）；整体写得像cinematographer的镜头描述，越长越具体越好。**修辞精简**：删减重复同义描述，同一特征只写一次，不反复堆砌；长文本后段注意力衰减会导致靠后细节被弱化。**瑕疵过滤移入负向提示词**：正向文本只做纯加法塑造画面，不写\"剔除/不要/无多余杂物\"类否定约束，缺陷规避统一写入negative_prompt。内容组织顺序：首帧锚点延续约束 → 镜头设定与场景光影 → 主体时序微动态 → 镜头运动节奏 → 色彩质感 → 音频描述 → 风格标签。natural模式输出流畅叙事段落，不要大量逗号碎片化标签堆砌。",
                "formula_en": "LTX‑2.3 constraint: native max 20s, stable recommend 3‑12s. Prompt length must match clip duration. Native audio‑visual sync, allow dialogue, ambient sound, background music. Support negative prompt. Single clip is one continuous long‑take, forbid cut‑edit instruction, describe shot change in natural language (e.g. \"The camera pans right...\"). **Camera simplification**: keep only ONE dominant camera movement per single shot, forbid compound stacked moves (e.g. \"push + pan\" \"dolly zoom\") — they cause camera instability, jitter, background distortion, subject exiting frame. **Action complexity compression**: control 1‑2 core actions per shot, action chain advances smoothly as \"start → process → end\", forbid long multi‑stage action chains; forbid high‑crash actions like \"abrupt stop‑and‑turn\" \"sudden sprint halt\" (limb collapse, leg clipping, stiff pose) — put the burst into running & other process actions, not a sudden halt; forbid \"freeze frame\" \"hold frame\" \"freeze on XX\" (unsupported, ineffective and disrupts motion ending). **Shot span compression**: single‑shot framing change limited to two levels (e.g. medium‑long → medium), forbid long → medium → close‑up triple jump; large span combined with fast motion drifts hair, outfit, facial features — split large‑span scenes into multiple shots. **Syntax points**: wrap dialogue in English double quotes \"dialogue\", may specify language/accent; reference I2V material with @ symbol (@Image1); some toolchains support section labels [VISUAL]: visual description / [SPEECH]: lines / [SOUNDS]: sfx & music; do NOT write emotion words (like \"sad\" \"confused\"), convey emotion via physical cues (e.g. \"he lowers his head, fingers clenching the hem of his clothes\"); keep lighting relatively static, forbid high‑cost fog + strong light‑beam combos combined with fast subject motion (gray washout, overexposure, flickering beams); write like a cinematographer's shot description, the longer and more specific the better. **Rhetoric trimming**: cut repetitive synonymous descriptions, describe each feature once, no repeated stacking; trailing attention decay weakens late details in long text. **Defect filtering to negative prompt**: positive text only adds to the scene, no \"no / without / remove\" negation constraints, defect avoidance all goes into negative_prompt. Content order: reference‑frame anchor constraint → camera‑scene‑lighting → character chronological micro‑motion → camera rhythm → color‑texture → audio description → style tags. Use coherent narrative paragraphs, avoid mass comma‑split tags."
            },
            "MiniMax‑H3": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "MiniMax‑H3模型约束：时长仅支持4‑15秒整数秒，不支持小数秒；**支持负向提示词（negative_prompt字段）**，缺陷规避约束同时写入正向提示词和negative_prompt；原生音画同步，支持台词、环境音、BGM；支持首帧参考图。\n\n**【强制四字段输出结构】MiniMax H3输出时必须包含以下四个独立字段，混写会导致解析混乱和音频分层失效：\n(1) integrated_multimodal_description: 画面描述、角色动作序列、镜头运动、台词、\n    **与画面同步的人物动作音效**（脚步由远及近、衣物摩擦等）\n(2) overall_soundscape: **仅限纯环境背景音**（微风持续声、树叶沙沙、远处鸟鸣、环境底噪），\n    严禁出现任何人物动作相关音效（脚步声、衣物摩擦声等全部放在(1)中）\n(3) non_diegetic_music: 背景音乐BGM（描述曲风与情绪；无BGM则写\"无\"）\n(4) negative_prompt: 负向提示词，列出需规避的缺陷（如 多余路人, 肢体扭曲, 穿模, 面部崩坏, 模糊, 水印）\n\n**【标签语法】镜头用[Shot N]编号并搭配At 00:00.000时间戳（单镜头也需标注起始时间[Shot 1] At 00:00.000）；台词用<d>[语言] 台词</d>标签搭配说话人ID (S1)/(S2)（如 The woman (S1) says: <d>[English] Hello.</d>）；参考图用<Picture N>锚定，I2V模式首行写对齐指令\"For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\"；台词跨镜头衔接加<scenetrans>，结尾台词被截断加<cutoff>，画外音用says in an off-screen voiceover（同时声明嘴唇闭合）。\n\n**【时间锚点规范】动作序列必须包含起始、中间、结束3‑4个时间节点，**最后一个时间戳必须与视频总时长严格对应**：\n  - 8秒视频示例：At 00:00.000 起始状态 → At 00:03.000 中间状态 → At 00:06.000 后段状态 → At 00:08.000 最终结束状态\n  - 无结束时间戳会导致后半段速度节奏完全随机失控\n\n**【音效分离铁律 — 最高优先级】**人物动作同步音效（脚步、衣物等）与纯环境背景音（风声、树叶、底噪）严禁出现在同一字段，严禁重复定义同一音效：\n  - integrated_multimodal_description: 人物动作音效从起始时间点就标注贯穿全程（如\"伴随由远及近的脚步声\"），不要只在单个时间点描述\n  - overall_soundscape: 只写环境音，如果写了脚步声等人物音效=输出不合格\n\n**【镜头运动简化】**H3对复合镜头运动控制力弱，必须简化：\n  - 禁止复合运动（如\"平移并推进\"\"推拉结合\"），容易导致人物出画、背景扭曲\n  - 优先固定机位：纯靠人物自身运动产生景别变化（最稳定）\n  - 或单一运动：仅保留一种（如仅\"缓慢向前推进\"）\n  - 禁止\"定格\"\"冻结帧\"\"画面定格在XX\"等指令（H3不支持，写了无效且干扰运动收尾）\n\n**【单镜头景别跨度压缩】单镜头景别变化不超过两个层级（如远景→中远景→中景），**禁止远景→中景→近景三级跳**。大跨度场景必须拆分多镜头。\n\n**【人物锚点具体化】至少3个具体区分特征，禁止模糊描述：\n  - 正确：\"黑色齐腰直发\"\"白色圆领\"\"棉麻面料连衣裙\"；错误：\"黑色长发\"\"白色连衣裙\"（太粗，大动态下易漂移）\n  - 禁止\"或\"字二选一（如\"树林或建筑\"→必须明确单一背景\"模糊的树林轮廓\"）\n\n**【风格前置】核心画面风格（光线类型与时段、整体色调、画面清晰度）必须放在镜头起始位置（At 00:00.000之后），禁止放在段落末尾，长文本末尾注意力衰减会导致风格描述失效。\n\n**【H3禁止项】**禁止百分比坐标；禁止色彩占比数字；禁止画面比例参数；禁止微观纹理要求；禁止无时间锚点的裸动作序列；禁止否定性约束只写正向不写negative_prompt。\n\n内容组织顺序（integrated_multimodal_description内）：首帧对齐指令 → At时间戳 → 首帧锚点延续约束 → 场景光影与风格 → 主体外貌（具体锚点） → 时序微动态 → 镜头运动（单一） → 动作同步音效。输出时严格按四个字段输出，不额外添加解释或注释。",
                "formula_en": "MiniMax‑H3 constraint: only integer seconds 4‑15s, float second invalid. **Supports negative prompt (negative_prompt field)**, defect‑avoid rules written into both positive prompt and negative_prompt. Native audio‑visual sync, support dialogue, ambient sound, BGM. Support reference image.\n\n**Mandatory Four‑Field Output Structure — H3 output must include these four separate fields; mixing causes parsing failure and audio layer collapse:\n(1) integrated_multimodal_description: visual description, character action sequence, camera movement, dialogue,\n    **AND character action sync sound** (footsteps approaching, fabric rustle, etc.)\n(2) overall_soundscape: **ONLY pure ambient background sound** (continuous breeze, rustling leaves, distant birds, environmental noise floor),\n    DO NOT include any character action sounds (footsteps, fabric sounds all go in (1))\n(3) non_diegetic_music: background music BGM (describe genre & mood; write \"none\" if no BGM)\n(4) negative_prompt: negative prompt listing defects to avoid (e.g. extra people, limb distortion, clipping, face collapse, blur, watermark)\n\n**Tag Syntax: label shots with [Shot N] paired with At 00:00.000 timestamp (even single shot must include start timestamp [Shot 1] At 00:00.000); dialogue wrapped in <d>[language] lines</d> with speaker ID (S1)/(S2) (e.g. The woman (S1) says: <d>[English] Hello.</d>); anchor reference images with <Picture N>, I2V mode writes alignment line at the top: \"For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\"; cross‑shot dialogue continuation uses <scenetrans>, truncated end dialogue uses <cutoff>, off‑screen line uses \"says in an off‑screen voiceover\" (also state mouth closed).\n\n**Time Anchor Specification: action sequences must have start, middle, and end (3‑4 time nodes), with the **final timestamp strictly matching total video duration**:\n  - 8‑second example: At 00:00.000 start state → At 00:03.000 mid state → At 00:06.000 later state → At 00:08.000 final end state\n  - Missing end timestamp causes back‑half pacing to become completely random and uncontrollable\n\n**Audio Separation Rule — HIGHEST PRIORITY: character action sync sound (footsteps, clothing, etc.) and pure ambient sound (wind, leaves, noise floor) must NEVER appear in the same field; NEVER define the same sound twice:\n  - integrated_multimodal_description: action sounds start from the first timestamp and persist throughout (e.g. \"accompanied by approaching footsteps from afar\"), avoid single‑point description\n  - overall_soundscape: ambient only; if footsteps or character sounds appear here = FAIL\n\n**Camera Movement Simplification: H3 has weak control over compound camera movements, must simplify:\n  - Forbid compound movements (e.g. \"pan and push\" \"dolly zoom\"), tends to cause subject exiting frame, background distortion\n  - Prefer fixed camera: let subject's own motion create perspective change (most stable)\n  - Or single movement: keep only one (e.g. \"slowly push forward\" only)\n  - Forbid \"freeze frame\" \"hold frame\" \"freeze on XX\" instructions (H3 doesn't support, ineffective and disrupts motion ending)\n\n**Single‑Shot Perspective Span Compression: perspective change within single shot limited to two levels (e.g. long → medium‑long → medium), FORBID long → medium → close‑up triple jump. Large‑span scenes must be split into multiple shots.\n\n**Character Anchor Specificity: at least 3 specific distinguishing features, forbid vague descriptions:\n  - Correct: \"waist‑length straight black hair\" \"white round‑neck\" \"linen‑cotton dress\"; Wrong: \"black long hair\" \"white dress\" (too coarse, easily drifts under heavy motion)\n  - Forbid \"or\" ambiguity (e.g. \"woods or buildings\" → use definitive: \"blurred tree silhouettes\")\n\n**Style Front‑loading: core visual style (light type & time of day, overall color palette, image clarity) must be placed at the shot start (right after At 00:00.000), FORBID placing at paragraph end; attention decay at long text end causes style descriptions to be ignored.\n\n**H3 Forbidden Items: forbid percentage coordinates; forbid color ratio numbers; forbid aspect ratio params; forbid micro‑texture demands; forbid bare action sequences without time anchors; forbid negative constraints in positive prompt only without negative_prompt.\n\nContent order (within integrated_multimodal_description): frame alignment line → At timestamp → reference‑frame anchor constraint → scene lighting & style → subject appearance (specific anchors) → chronological micro‑motion → camera movement (single) → action sync sound. Output strictly in four‑field format, no extra commentary."
            }
        }

        # 全局底层通用规则（三个视频模型共用基础规则）
        self.global_base_rules = {
            "zh": """
你是专业图生视频首帧延续扩写专家，覆盖实拍类、动漫类。
核心铁则：**首帧锚点优先**，不可篡改原图主体位置、服装、发型、核心道具、场景、光影基调；用户引导词仅修饰动态、情绪、运镜，冲突诉求直接舍弃。优先生成微动作，拒绝大幅度位移。
坚守图生视频生成基础约束：动作具备物理运动逻辑；画面精简，不自动新增无关摆件、路人、杂物；文本权重从前向后逐级递减，首帧约束、主体动态、镜头运动前置，细节参数后置；超长文本分段，防止末尾约束失效。
natural模式300‑600字，2‑3个叙事段落，**严禁帧率、码率、分辨率等数字技术参数**；structured模式完整输出结构化字段，【技术参数建议】仅允许定性效果描述，禁止一切数值参数。
区分实拍/动漫质感：实拍保留皮肤肌理；动漫保持画风统一，杜绝画风漂移跳变。
完整保留用户输入（首帧图像信息、可选用户引导词），只做动态细节补充，不篡改原图锚点；光影写明光源、色温、软硬以及随时间的变化；严格执行70%主色‑25%辅助‑5%点缀色彩配比。
重要模型差异化约束会在模型组织公式给出，严格遵守对应模型的时长上限、音频支持、负向提示词能力。
输出禁忌：禁止权重符号；禁止猎奇镜头角度；禁止穿模、闪烁、跳帧、风格漂移；禁止元素堆砌；禁止改动首帧核心锚点。
支持natural与structured双输出格式，不添加额外注释、说明、解释。
""",
            "en": """
You are professional image‑to‑video continue‑frame prompt expert. Cover real‑shot / anime categories.
Core rule: **reference‑frame anchor highest priority**. Must NOT alter original subject position, costume, hairstyle, key props, scene, light‑shadow baseline. User prompt only modify motion, emotion, camera, conflicting requirements shall be discarded. Prefer micro‑movement, forbid large‑scale displacement.
I2V baseline: physically plausible motion logic; frame‑simplify rule, no auto‑add irrelevant ornaments or passers‑by. Text weight decays from front to back: frame‑anchor constraint & character dynamics & camera motion first, details behind. Split long paragraphs to avoid trailing constraint failure.
Natural mode: 300‑600 words, 2‑3 narrative paragraphs, strictly forbid numeric technical parameters like fps, bitrate, resolution.
Structured mode: output all sections, in【Tech Suggestion】only qualitative description allowed, no numeric values.
Texture distinction: real‑shot preserve skin texture; anime keep consistent art‑style, forbid style drifting.
Fully preserve user input(reference frame info & optional user guide prompt), enrich motion details only, never break frame anchor. Describe light source, color‑temperature, hardness‑softness & temporal light change. Enforce 70%‑25%‑5% color proportion rule.
Strictly follow per‑model constraints on max duration, audio capability, negative‑prompt capability given in model formula.
Taboo: no weight syntax; no grotesque camera angles; no penetration‑clipping, flicker, frame‑skip, style drift; no element over‑stacking; no modifying reference‑frame core anchor.
Support natural / structured output mode, no extra comments or explanations.
"""
        }

        # 唯一主预设模板，绑定CONTINUING_I2V template_id
        self.preset_library = {
            "continuing_i2v": {
                "template_id": "continuing_i2v",
                "display_name": CONTINUING_I2V["name"],
                "description": CONTINUING_I2V["description"],
                "positive_constraints": {
                    "zh": "严格延续首帧构图、主体状态、光影基调与风格质感；用户引导词合规需求自然融入动态叙事，不破坏首帧原生锚点；物理级动态与镜头运动逻辑，自然流畅的微动作与环境变化，精准三维镜头视角与合理透视，真实光影过渡与色彩层次统一。实拍类保留原生皮肤纹理、生活化细节与自然光影过渡；动漫类保持统一画风、流畅线条与稳定色块。画面干净主体突出，仅保留核心叙事元素，节奏舒缓可控，动态前后连贯，全程风格统一，光影随时间自然变化，情绪通过微动作与镜头具象传递。",
                    "en": "Strictly inherit reference‑frame composition, subject state, light‑shadow baseline and art‑style. Reasonable user‑guide demand embedded into motion narrative without breaking frame anchor. Physically‑plausible dynamics & camera logic, smooth micro‑actions & environment motion, accurate 3‑d camera perspective, reasonable perspective, natural light‑shadow transition & color hierarchy. Real‑shot: preserve native skin texture, life‑like details. Anime: consistent art‑style, smooth line‑art, stable color block. Clean frame with prominent subject, only core narrative elements. Coherent motion, unified style, light evolves over time, emotion expressed via micro‑action & camera."
                },
                "preset_rules": {
                    "zh": """
【图生视频首帧延续专属规则】
1. 通用基线：执行8步I2V扩写流程；强制70%‑25%‑5%色彩配比；严格锁定首帧全部锚点（主体位置、服装、场景、光影、外形）；三维镜头视角优先继承首帧视角；镜头运动优先固定或极慢运动；画面精简约束，不自动生成多余摆件装饰。natural模式300‑600字无相机数字参数；structured模式不超1500字。
2. 实拍类：保留皮肤自然肌理，光影过渡柔和；以微动作为主，拒绝大幅度位移；动作符合人体生理运动逻辑；镜头运动只为叙事，拒绝无意义炫技运镜。
3. 动漫类：画风全程统一，严防画风漂移跳变；线条色块稳定；肢体以微动态为主，规避大幅度位移。
4. 动态设计：优先微动作、微表情；每个动作写明起始‑过程‑结束，尽量标注时间；环境动态与人物动态节奏匹配，禁止凭空新增首帧不存在的核心物体。
5. 用户引导词处理：解析提取诉求，校验是否与首帧锚点冲突；冲突直接舍弃；仅把合规诉求叠加到动态、情绪、运镜，不得修改原图既定状态；无引导词则仅基于首帧生成原生自然延续。
6. 音频处理：模型不支持音频时，完全删除台词、音效、BGM描述；模型支持音频，可合理加入环境音、台词、背景音乐。
7. 负向提示词处理：MiniMax‑H3支持negative_prompt字段，正常输出负向提示；Wan2.2、LTX2.3正常输出负向提示。
8. MiniMax‑H3专用规则：
   a. 强制四字段输出：必须输出integrated_multimodal_description / overall_soundscape / non_diegetic_music / negative_prompt四个字段。
   b. 音效分离铁律：人物动作音效（脚步、衣物等）仅放integrated_multimodal_description，从起始时间点标注贯穿全程；环境背景音（风声、树叶、底噪）仅放overall_soundscape；两字段严禁交叉或重复定义同一音效。
   c. 时间锚点：每个[Shot N]搭配At时间戳，动作序列必须包含起始+中间+结束3‑4个节点，最后一个时间戳严格对应视频总时长。
   d. 镜头运动简化：禁止复合镜头运动（"平移并推进"等），优先固定机位或单一运动；禁止"定格""冻结帧"指令。
   e. 景别跨度压缩：单镜头景别变化不超过两个层级，禁止三级跳（远景→中景→近景）；大跨度必须拆分多镜头。
   f. 人物锚点：至少3个具体特征，禁止模糊二选一（"树林或建筑"）。
   g. 风格前置：核心光线、色调、清晰度描述必须放在At 00:00.000之后的第一句，禁止放在段落末尾。
   h. 禁止量化描述：不得使用百分比坐标、色彩占比数字、画面比例参数，全部改为自然语言相对描述。
   i. 否定转正向+负向提示：正向文本中所有"不出现XX"转换为正向表达；同时必须在negative_prompt字段列出需规避的缺陷。
   j. 信息精简：每字段控制在200‑400字，不堆砌微观纹理、布料动力学等超出模型能力的描述。
所有题材：首帧锚点拥有最高优先级，用户引导词不能篡改原图设定，仅补充动态细节。
""",
                    "en": """
【I2V Reference‑Frame Continue Preset Rules】
1. General baseline: follow 8‑step I2V expansion workflow. Mandatory color ratio 70%‑25%‑5%. Lock all reference‑frame anchor(subject position, costume, scene, light‑shadow, appearance). Inherit camera view from reference‑frame whenever possible. Prefer static or extremely‑slow camera movement. Frame‑simplify rule: no auto‑generate extra ornaments. Natural mode 300‑600 words without numeric camera params; structured mode max 1500 words.
2. Real‑shot category: preserve natural skin texture, soft light‑shadow transition. Prioritize micro‑actions, forbid large‑scale displacement; human‑physiology‑compliant motion; camera movement serve narrative, avoid meaningless fancy camera work.
3. Anime category: consistent art‑style, strictly prevent style drift; stable lines & color blocks; mostly micro‑motion, forbid large‑scale displacement.
4. Motion design: prioritize micro‑action & micro‑expression. Describe start‑process‑end for each action, mark time span when possible. Sync environment dynamics with character rhythm. Must NOT add core objects which do not exist on reference‑frame.
5. User guide prompt handling: parse requirement, check conflict against frame anchor. Discard conflicting demand. Only inject valid requirement into motion / emotion / camera, never alter original frame setting. If no guide prompt, generate natural continuation purely based on reference frame.
6. Audio handling: remove dialogue / sfx / BGM for audio‑incapable model; add reasonable ambient sound, dialogue, BGM for audio‑capable model.
7. Negative prompt handling: MiniMax‑H3 supports negative_prompt field, output negative prompt normally. Wan2.2 & LTX2.3 output negative prompt normally.
8. MiniMax‑H3 specific rules:
   a. Mandatory four‑field output: must output integrated_multimodal_description / overall_soundscape / non_diegetic_music / negative_prompt.
   b. Audio separation iron rule: character action sounds (footsteps, clothing, etc.) ONLY in integrated_multimodal_description, starting from first timestamp and persisting throughout; ambient background (wind, leaves, noise floor) ONLY in overall_soundscape; cross‑contamination or duplicate sound definition = FAIL.
   c. Time anchors: every [Shot N] with At timestamp; action sequences must have start+mid+end (3‑4 nodes), final timestamp strictly matching total video duration.
   d. Camera movement simplification: forbid compound movements ("pan and push" etc.), prefer fixed camera or single movement; forbid "freeze frame" "hold frame" instructions.
   e. Perspective span compression: single‑shot change limited to two levels, forbid triple jump (long→medium→close‑up); large span must split into multiple shots.
   f. Character anchors: at least 3 specific features, forbid vague "or" choices ("woods or buildings").
   g. Style front‑loading: core lighting, color palette, clarity descriptions must be placed right after At 00:00.000, forbid placing at paragraph end.
   h. Forbid quantitative: no percentage coordinates, color ratio numbers, aspect ratio params; rewrite all as natural‑language descriptions.
   i. Negation + negative prompt: convert all "no XX" to positive phrasing in positive text; must also list defects in negative_prompt field.
   j. Information density: each field 200‑400 words max; avoid piling micro‑texture, cloth dynamics beyond model capability.
For all categories: reference‑frame anchor has highest priority. User guide shall not alter original frame setting, only enrich motion details.
"""
                },
                "negative_base": {
                    "zh": "首帧风格漂移，元素丢失突变，画面闪烁跳帧，肢体穿模扭曲，人物比例失调，透视逻辑错误，镜头剧烈抖动，运动轨迹混乱，静态呆滞无动态，人脸崩坏变形，五官飘忽不定，色彩溢出脏污，画面颗粒噪点，低分辨率模糊，塑料虚假质感，平涂无体积感，多余路人乱入，杂物堆砌冗余，无关装饰摆件，字幕水印logo，元素凭空消失，物体漂浮无重力，光影生硬突变，节奏混乱突兀，画风前后不一，边缘锯齿抠图感，过度锐化生硬，卡通低幼失真，场景突兀切换，主体位置偏移，光影基调跳变，强行按照用户提示词改动首帧主体、服装、场景、光影等原生设定，生硬植入用户诉求造成画面逻辑断裂",
                    "en": "reference‑frame style drift, element loss & mutation, flicker & frame skip, body clipping & distortion, bad proportion, wrong perspective, violent camera shake, chaotic motion track, static lifeless pose, broken face, drifting facial feature, muddy overflowing color, grain noise, low‑resolution blur, fake plastic texture, flat shading without volume, random extra people, redundant clutter, irrelevant ornament, subtitle watermark logo, object pop‑in pop‑out, zero‑gravity floating object, harsh sudden light‑shadow change, chaotic rhythm, inconsistent art‑style, jagged cut‑out edge, over‑sharpening, overly childish cartoon distortion, abrupt scene switch, subject position offset, light‑shadow baseline jump, forcibly alter reference‑frame subject / costume / scene / light‑shadow by user prompt, break logic by forcing invalid user demand."
                }
            }
        }

        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】自然段落（2‑3段），首段确立首帧状态、整体基调与光线氛围，次段描述动态延续序列与镜头运动节奏，末段补充光影质感、色彩层次与细节氛围。存在用户引导词时将合规诉求自然融入叙事，无引导词则纯基于图像原生动态创作；语言富有画面感与节奏感，全程无帧率、码率、分辨率类数字技术参数，强化动态连贯性、光影流动感与画面精简约束，保证画面干净聚焦、叙事清晰、风格与首帧高度统一。字数300‑600。",
                "en": "[Natural Paragraph Mode] 2‑3 narrative paragraphs: first for reference‑frame state‑space‑lighting‑mood; second for character continuation dynamics & camera rhythm; last for light‑shadow‑color‑detail. Embed valid user‑guide demand if exists, generate pure native motion if no guide prompt. Visual cinematic language. Forbid numeric parameters such as fps, bitrate, resolution. Emphasize motion coherence, flowing light‑shadow, frame‑simplify constraint, style consistent with reference frame. 300‑600 words."
            },
            "structured": {
                "zh": """【结构化模式】
**【MiniMax‑H3专用输出格式】若视频模型为MiniMax‑H3，忽略下方通用结构化格式，强制按四字段输出：\nintegrated_multimodal_description:\n（画面描述、动作序列、镜头运动、台词、人物动作同步音效）\n\noverall_soundscape:\n（仅限纯环境背景音，无则写"无"）\n\nnon_diegetic_music:\n（背景音乐BGM，无则写"无"）\n\nnegative_prompt:\n（需规避的缺陷列表，如 多余路人, 肢体扭曲, 穿模, 面部崩坏, 模糊, 水印）\n\n关键约束：每个[Shot N]搭配At时间戳且最后一个时间戳严格对应视频总时长；人物动作音效仅放integrated字段且从起始贯穿全程；环境音效仅放overall_soundscape严禁交叉重复；禁止复合镜头运动优先固定机位；人物锚点至少3个具体特征禁止"或"字二选一；核心风格放At 00:00.000之后第一句；禁止百分比坐标/色彩占比数字/画面比例参数；所有"不出现XX"类否定约束必须同时写入negative_prompt。\n\n【Wan2.2 / LTX2.3通用结构化格式】若视频模型非MiniMax‑H3，按以下格式输出：
【类别】实拍类/动漫类
【首帧基础锚点状态】
  - 构图与视角：主体位置、视线方向、画面空间关系、原生景别（全程不可修改）
  - 光线与色彩：光源方向、色温、色调倾向、基础色彩配比（全程不可修改）
  - 主体外观：姿态、表情、衣物纹理、皮肤/画风质感（全程不可修改）
【用户诉求适配】（无引导词标注：无，纯图像原生自然延续）
  - 核心需求提炼：用户指定动作/情绪/氛围/运镜/节奏诉求
  - 落地规则：仅在不改动首帧锚点前提下融入动态设计，冲突需求直接舍弃
【全局正向约束】
  - 延续基础：严格匹配首帧风格、构图、光影、主体状态，元素完整无丢失突变
  - 动态基础：物理级运动逻辑，动作连贯自然，符合真实运动规律
  - 质感基础：实拍类保留原生皮肤纹理、自然光影过渡；动漫类画风统一稳定、线条流畅色块清晰
  - 镜头逻辑：三维视角符合电影美学，运动克制服务叙事，透视准确无畸变
【景别与三维镜头视角】
  - 距离维度（景别对应）：微距特写 / 标准特写 / 肩特写 / 七分人像 / 九分人像 / 全景人像，对应叙事重心与细节展现层级
  - 水平方位维度：摄像机水平环绕角度（正面/四分之三斜侧/正侧面/四分之三背面），标注面部展现效果与轮廓叙事特点
  - 垂直俯仰维度：摄像机垂直旋转角度（小俯视角/平视/小仰视角），对应心理感受与空间关系
  - 镜头运动：运动类型（固定/极慢推/极慢拉/极慢摇/极慢移）、方向、速度与持续时间，搭配叙事作用释义
  - 景深氛围：主体清晰背景虚化 / 前后景都清晰 / 局部保留环境细节，标注虚实层次对应的画面效果
【动态延续与节奏】
  - 主体动作序列：起始状态 → 过程动态 → 结束定格，标注每段对应时长与肢体联动细节
  - 微动作/微表情：细微的情绪变化（眼神、嘴角、手指、肩膀），传递内敛情绪
  - 环境动态变化：背景元素的运动规律（光影移动、风吹物体、粒子漂浮）与节奏
  - 自然现象：风/雨/雪/光移等动态效果，符合真实物理逻辑
  - 整体时间节奏：快慢分布，情绪递进节点，时间跨度
【主体描述】
  - 外貌特征：延续首帧面部轮廓、发型发色、核心标识，突出对应风格与品类的专属特质
  - 姿态动态：完整身体动态与手部联动细节，强调自然运动逻辑，体态松弛舒展
  - 表情变化：眼神落点、面部肌肉变化的时间过程，标注清晰情绪走向，杜绝空洞静态表情
  - 服装造型：款式、颜色、面料材质，标注主色 / 辅助色 / 点缀色占比，搭配运动产生的自然褶皱动态
【质感与细节】
  - 皮肤/画风质感：实拍类保留原生肌肤纹理、自然光影过渡；动漫类线条流畅、色块稳定、画风统一
  - 毛发/线条质感：实拍类发丝层次自然、随动真实；动漫类线条干净、无多余杂线
  - 材质表现：布料、金属、木质、玻璃等材质动态反光与形变符合物理逻辑
  - 光影层次：光源方向、软硬、冷暖随时间的过渡变化，明暗过渡自然无断层
【环境与氛围】
  - 空间场景：延续首帧精准具体地点及环境特征，无模糊抽象环境描述
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
【画面收尾精简约束】画面无额外人物、无关花草、多余摆件、杂乱背景装饰，所有环境元素仅服务叙事节奏与情绪表达，不抢夺主体视觉焦点，全程风格与首帧高度统一。""",
                "en": """[Structured Mode]
**[MiniMax‑H3 Specific Output Format] If the video model is MiniMax‑H3, ignore the generic format below and output strictly in four‑field structure:\nintegrated_multimodal_description:\n(visual description, action sequence, camera movement, dialogue, character action sync sound)\n\noverall_soundscape:\n(pure ambient background sound only, write "none" if none)\n\nnon_diegetic_music:\n(background music BGM, write "none" if none)\n\nnegative_prompt:\n(defects to avoid, e.g. extra people, limb distortion, clipping, face collapse, blur, watermark)\n\nKey constraints: every [Shot N] with At timestamp, final timestamp must strictly match total video duration; character action sounds ONLY in integrated field, persisting from start; ambient sounds ONLY in overall_soundscape, cross‑contamination FORBIDDEN; no compound camera movements, prefer fixed camera; at least 3 specific character anchors, forbid "or" ambiguity; core style (lighting, color, clarity) placed right after At 00:00.000 first sentence; forbid percentage/ratio/aspect‑ratio parameters; all "no XX" negative constraints must also go into negative_prompt.\n\n[Wan2.2 / LTX2.3 Generic Structured Format] If model is NOT MiniMax‑H3, output as follows:
【Category】real‑shot / anime
【Reference‑Frame Anchor State】
  - Composition & Viewpoint: subject position, gaze direction, spatial relation, native shot scale (MUST NOT modify)
  - Light & Color: light source direction, color‑temperature, tone tendency, base color ratio (MUST NOT modify)
  - Subject Appearance: pose, expression, clothing texture, skin / art‑style texture (MUST NOT modify)
【User‑Demand Adaptation】(If no guide prompt mark: none, pure native image continuation)
  - Requirement Extract: user‑specified action / mood / atmosphere / camera / rhythm demand
  - Implementation Rule: embed motion design only without breaking frame anchor, discard conflicting demand directly
【Global Positive Constraints】
  - Continuation Base: strictly match reference‑frame style, composition, light‑shadow, subject state, no element loss or mutation
  - Motion Base: physically‑plausible motion, fluent action, obey natural physical law
  - Texture Base: real‑shot preserve native skin texture & soft light‑shadow; anime maintain unified art‑style, smooth lines, stable color blocks
  - Camera Logic: 3‑D view follow cinematic aesthetic, restrained camera motion serve narrative, correct perspective without distortion
【Shot & 3‑D Camera View】
  - Distance(shot): macro close‑up / standard close‑up / shoulder shot / three‑quarter / nine‑tenth / full‑scene portrait
  - Horizontal Azimuth: front / three‑quarter / profile / three‑quarter back, describe facial & contour narrative feature
  - Vertical Pitch: slight high‑angle / eye‑level / slight low‑angle, describe psychological feeling & spatial relation
  - Camera Movement: type(static / extremely‑slow push / pull / pan / track), direction, speed, duration & narrative purpose
  - Depth‑of‑field: subject sharp with bg blur / full sharp / partial detail reserved, mark virtual‑real hierarchy
【Motion & Rhythm】
  - Character Action Sequence: start → process → end freeze, mark time span & limb linkage detail
  - Micro‑action / Micro‑expression: subtle emotion change (eyes, mouth, finger, shoulder), convey restrained feeling
  - Environment Dynamics: light shift, wind‑driven object, particle floating and rhythm
  - Natural Phenomenon: wind / rain / snow / light shift obey physics
  - Global Tempo: fast‑slow distribution, emotion progression node, time span
【Character Description】
  - Appearance: inherit reference‑frame facial contour, hair style‑color, key feature
  - Pose Dynamics: full‑body motion & hand interaction, natural kinematics, relaxed posture
  - Expression Change: gaze point, facial muscle temporal process, clear emotion trend, avoid static hollow expression
  - Costume: style, color, fabric material, main / auxiliary / accent color ratio, natural fold under movement
【Texture & Detail】
  - Skin / Art‑style Texture: real‑shot native skin texture & soft light‑shadow; anime smooth line, stable color block, unified style
  - Hair / Line Texture: real‑shot natural hair motion; anime clean line‑art without messy stroke
  - Material Performance: cloth, metal, wood, glass reflection & deformation obey physics
  - Light‑Shadow Hierarchy: light direction, hardness‑softness, cold‑warm temporal transition, smooth shadow gradient
【Environment & Atmosphere】
  - Scene: inherit concrete location from reference‑frame, no vague abstract description
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
【Final Simplify Constraint】No extra character, irrelevant plant, redundant ornament, messy background. All elements serve narrative & emotion, never steal visual focus. Style keep consistent with reference‑frame."""
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
        # 所有模型均支持负向提示词输出
        if enable_negative_prompt:
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