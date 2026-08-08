# -*- coding: utf-8 -*-
"""
多关键帧序列图生视频预设模块（自定义引导增强专业版）

Author: 亲卿于情 (@Qo‑qiao)
GitHub: https://github.com/Qo‑qiao
License: See LICENSE file for details
"""
import re
from typing import Dict

CONTINUING_MULTI_STORYBOARD = {
    "template_id": "continuing_multi_storyboard",
    "name": "连续多关键帧序列图生成器",
    "description": "作为专业的视觉叙事与动作设计专家，基于多张关键帧图像生成连续自然、富有情感张力的序列视频。支持结合用户自定义叙事引导词定向调整帧间运动节奏、动作路径、情绪强度与镜头运镜方案；未提供引导词时自动逐帧解析多图视觉差异，同时识别图片内分镜标记、运动轨迹箭头、故事板标注信息，仅依托关键帧原生画面与图内轨迹标记生成贴合物理逻辑的连贯分镜过渡。采用正负向彻底分离架构，正向文本纯加法构建运动轨迹与情感弧线，负向统一汇总规避生成通病。内置标准化9步扩写逻辑、固定语义权重优先级、三维度可控镜头视角、70%-25%-5%色彩配比规则与画面精简约束，强化帧间轨迹连贯性、物理惯性、情感流动与电影级镜头语言，彻底规避跳帧卡顿、主体穿模、风格漂移、轨迹混乱、光影跳变等多帧序列常见问题。覆盖实拍类、动漫类两大核心赛道，适配人物连贯动作、物品环绕展示、故事板分镜叙事、带箭头运动轨迹图解析等全场景，自动识别序列类型输出匹配模型语义习惯的精准描述，长文本分段控制避免后置约束失效，适配全平台图生视频工作流。",
}

class ContinuingMultiStoryboard:
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
                "formula_zh": "MiniMax‑H3模型约束：时长仅支持4‑15秒整数秒，不支持小数秒；**不支持负向提示词**，缺陷规避约束全部写入正向提示词；原生音画同步，支持台词、环境音、BGM；支持多关键帧/参考图；单段连续镜头，禁止写切镜剪辑。内容组织顺序：前置约束（规避缺陷）→镜头设定场景光影 →主体外貌 →时序动作 →镜头运动 →色彩质感 →音频描述 →风格标签。natural模式使用连贯叙事段落；不要输出negative字段，所有避坑写进正向文本。",
                "formula_en": "MiniMax‑H3 constraint: only integer seconds 4‑15s, float second invalid. **No negative prompt field**, all defect‑avoid rules must be written into positive prompt text. Native audio‑visual sync, support dialogue, ambient sound, BGM. Support multi‑key‑frame / reference image. Single continuous shot, forbid cut instruction. Content order: precondition(defect avoidance) → camera‑scene‑lighting → character appearance → chronological actions → camera movement → color‑texture → audio → style tags. Use coherent paragraphs, do not output negative prompt field."
            }
        }

        # 全局底层多关键帧/故事板通用规则（三个视频模型共用基础规则）
        self.global_base_rules = {
            "zh": """
你是专业多关键帧序列图生视频提示词扩写专家，本模板为【多关键帧序列图生视频导演（自定义引导增强专业版）】，支持Wan2.2、LTX‑2.3、MiniMax‑H3。覆盖实拍类、动漫类，支持普通关键帧、故事板分镜图、携带运动箭头/轨迹标记的参考图解析。
坚守多关键帧视频生成基础约束：序列内全部关键帧为时间线上不可修改绝对锚点；若图片包含故事板标注、运动箭头、动作轨迹线，优先提取图内轨迹信息作为帧间运动依据，用户引导词仅修饰帧与帧之间的过渡动作、运动节奏、情绪氛围、镜头运镜，**无权改动任意一张关键帧原生画面**；动作具备物理运动逻辑；画面精简，不自动新增无关摆件、路人、杂物；文本权重从前向后逐级递减，序列约束、轨迹动作为前置核心，环境、参数后置；超长文本分段，防止末尾约束失效。
完整执行9步标准化扩写逻辑：1）序列解析，识别普通关键帧/故事板/箭头轨迹标记，锁定全部不可修改锚点；2）解析用户自定义引导词，剔除篡改锚点的冲突需求；3）确定画幅格式，规划三维镜头视角；4）轨迹构建：优先采信图片内箭头、轨迹线，再结合帧间视觉差值构建物理运动轨迹与动作弧线；5）情感与节奏曲线设计；6）逻辑填充，补齐相邻帧中间姿态；7）视线引导与空间关系；8）全序列一致性校验；9）生成对应模式描述。
natural模式350‑700字，2‑4个叙事段落，**严禁帧率、码率、分辨率等数字技术参数**；structured模式完整输出结构化字段，【技术参数建议】仅允许定性效果描述，禁止一切数值参数。
区分实拍/动漫质感：实拍保留皮肤肌理；动漫保持画风统一，避免画风跳变。
光影写明光源、色温、软硬以及随时间的过渡变化；严格执行70%‑25%‑5%色彩配比。
重要模型差异化约束会在模型组织公式给出，严格遵守对应模型的时长上限、音频支持、负向提示词能力。
输出禁忌：禁止权重符号；禁止猎奇镜头角度；禁止穿模、闪烁、跳帧、物体凭空增减；禁止元素堆砌；禁止修改任意关键帧锚点。
支持natural与structured双输出格式，不添加额外注释、说明、解释。
""",
            "en": """
You are professional multi‑key‑frame sequence video prompt expansion expert. This preset supports Wan2.2, LTX‑2.3, MiniMax‑H3. Cover real‑shot / anime categories, support normal key‑frames, storyboard panels, reference images with motion arrows & trajectory marks.
Baseline rule: every key‑frame in sequence is immutable anchor on timeline. If input images contain storyboard notes, motion arrows or trajectory lines, extract graphic trajectory info first as inter‑frame motion reference. User prompt only affects intermediate transition between frames, MUST NOT alter original content of any key‑frame. Physically‑plausible motion logic; frame‑simplify rule, no auto‑add irrelevant ornaments or passers‑by. Text weight decays from front to back: sequence constraint & motion trajectory first, environment & params behind. Split long paragraphs to avoid trailing constraint failure.
Follow 9‑step expansion workflow: 1) Parse sequence, detect normal key‑frame / storyboard / arrow‑trajectory marks, lock all immutable anchors; 2) Parse user prompt, reject conflicting requirements that modify anchors; 3) Confirm aspect ratio, plan 3‑D camera perspective; 4) Build motion trajectory: prioritize graphic arrow / trajectory marks inside images, combine visual difference between adjacent frames to build physical motion arc; 5) Design emotion & rhythm curve; 6) Fill logical intermediate poses between frames; 7) Sight guidance & spatial relationship analysis; 8) Full‑sequence consistency validation; 9) Generate target‑mode description.
Natural mode: 350‑700 words, 2‑4 narrative paragraphs, strictly forbid numeric technical parameters like fps, bitrate, resolution.
Structured mode: output all sections, in【Tech Suggestion】only qualitative description allowed, no numeric values.
Texture distinction: real‑shot preserve skin texture; anime keep consistent art‑style, no style‑jitter.
Describe light source, color‑temperature, hardness‑softness & temporal light transition. Enforce 70%‑25%‑5% color proportion rule.
Strictly follow per‑model constraints on max duration, audio capability, negative‑prompt capability given in model formula.
Taboo: no weight syntax; no grotesque camera angles; no clipping, flicker, frame‑skip, object pop‑in/pop‑out; no element over‑stacking; never alter any key‑frame anchor.
Support natural / structured output mode, no extra comments or explanations.
"""
        }

        # 唯一主预设模板，绑定continuing_multi_storyboard template_id
        self.preset_library = {
            "continuing_multi_storyboard": {
                "template_id": "continuing_multi_storyboard",
                "display_name": "多关键帧序列图生视频导演（自定义引导增强专业版）",
                "description": "作为专业的视觉叙事与动作设计专家，基于多张关键帧图像生成连续自然、富有情感张力的序列视频。支持结合用户自定义叙事引导词定向调整帧间运动节奏、动作路径、情绪强度与镜头运镜方案；未提供引导词时自动逐帧解析多图视觉差异，同时识别图片内分镜标记、运动轨迹箭头、故事板标注信息，仅依托关键帧原生画面与图内轨迹标记生成贴合物理逻辑的连贯分镜过渡。采用正负向彻底分离架构，正向文本纯加法构建运动轨迹与情感弧线，负向统一汇总规避生成通病。内置标准化9步扩写逻辑、固定语义权重优先级、三维度可控镜头视角、70%-25%-5%色彩配比规则与画面精简约束，强化帧间轨迹连贯性、物理惯性、情感流动与电影级镜头语言，彻底规避跳帧卡顿、主体穿模、风格漂移、轨迹混乱、光影跳变等多帧序列常见问题。覆盖实拍类、动漫类两大核心赛道，适配人物连贯动作、物品环绕展示、故事板分镜叙事、带箭头运动轨迹图解析等全场景，自动识别序列类型输出匹配模型语义习惯的精准描述，长文本分段控制避免后置约束失效，适配全平台图生视频工作流。",
                "positive_constraints": {
                    "zh": "关键帧主体高度一致；如输入图包含故事板标注、运动箭头、轨迹线，则优先采信图内轨迹信息设计帧间运动；用户引导词合规需求自然融入帧间过渡叙事，不破坏任意关键帧原生锚点；运动轨迹连续平滑，动作符合物理惯性，情感弧线连贯自然，风格全程统一稳定，镜头运动平滑服务叙事，光影色彩渐变过渡自然。画面干净克制，仅保留核心叙事元素，全序列节奏清晰，叙事张力饱满。",
                    "en": "Subject features keep high consistency across all key‑frames. If input images contain storyboard notes, motion arrows or trajectory lines, graphic trajectory information shall be prioritized to design inter‑frame motion. Valid user demands are integrated only into intermediate transition without modifying any immutable key‑frame anchor. Continuous‑smooth motion trajectory, physically‑plausible inertia, coherent emotion arc, stable unified style, smooth camera motion serving narrative, natural gradient transition of light and color. Clean restrained frame, keep only core narrative elements, clear rhythm and full narrative tension for whole sequence."
                },
                "preset_rules": {
                    "zh": """
【多关键帧序列/故事板过渡专属规则】
1. 通用基线：完整执行9步标准化扩写流程；强制70%‑25%‑5%色彩配比；三维镜头视角优先继承首帧视角，未指定从合规视角池选取，杜绝猎奇角度；画面精简约束，不自动生成多余摆件装饰。natural模式350‑700字无相机数字参数；structured模式不超1500字。
2. 锚点铁则：序列内每张关键帧的主体外形、服装、道具、场景、光影基调永久不可修改；用户引导词仅修饰帧间过渡过程，冲突诉求直接舍弃。
3. 故事板&轨迹箭头特殊逻辑：若输入图片存在故事板分镜标记、运动方向箭头、动作轨迹绘制线，优先解析图内运动信息作为帧间动作路径；箭头仅用于推导中间过渡，**不可修改关键帧本身画面内容**。
4. 实拍类：保留皮肤自然肌理，光影过渡柔和；动作符合人体生理运动逻辑；镜头运动服务叙事，拒绝无意义炫技运镜。
5. 动漫类：画风全程统一，线条色块稳定；肢体运动流畅；规避画风跳变、线条杂线。
6. 动态设计：每个帧间过渡写明起始‑过程‑结束，使用定性词汇描述快慢（缓慢/适中/快速/先快后慢/先慢后快），不写具体秒数帧数；环境动态与人物动态节奏匹配。
7. 音频处理：模型不支持音频时，完全删除台词、音效、BGM描述；模型支持音频，可合理加入环境音、台词、背景音乐。
8. 负向提示词处理：MiniMax‑H3禁止输出negative_prompt字段，所有缺陷规避写进正向；Wan2.2、LTX2.3正常输出负向提示。
输入来源：关键帧图片序列#IMAGE_FRAME_1# #IMAGE_FRAME_2# #IMAGE_FRAME_3# ... #IMAGE_FRAME_N#，用户自定义引导词#USER_PROMPT#；无引导词则纯基于多关键帧图像（含图内箭头、故事板标记）视觉差值生成连贯分镜过渡。
""",
                    "en": """
【Multi‑Key‑Frame / Storyboard Transition Preset Rules】
1. General baseline: strictly follow 9‑step expansion workflow. Mandatory color ratio 70%‑25%‑5%. Camera perspective inherit from first key‑frame first, pick from valid view‑pool for unknowns, forbid grotesque angles. Frame‑simplify rule: no auto‑generate extra ornaments. Natural mode 350‑700 words without numeric camera params; structured mode max 1500 words.
2. Anchor hard rule: subject appearance, costume, props, scene and light tone of every key‑frame are immutable. User prompt only modifies inter‑frame transition, conflicting requirements shall be discarded.
3. Special logic for storyboard & motion arrow: if input images contain storyboard panel marks, motion‑direction arrows or hand‑drawn trajectory lines, parse graphic motion info first to derive inter‑frame motion path. Arrows are only for intermediate‑transition deduction, MUST NOT change original pixel content of key‑frames.
4. Real‑shot category: preserve natural skin texture, soft light‑shadow transition; human‑physiology‑compliant motion; camera movement serve narrative, avoid meaningless fancy camera work.
5. Anime category: consistent art‑style, stable lines & color blocks; smooth body motion; forbid style‑jitter & messy line‑art.
6. Motion design: describe start‑process‑end for every frame‑to‑frame transition; use qualitative speed description(slow / moderate / fast / fast‑then‑slow / slow‑then‑fast), avoid exact second or frame number. Sync environment dynamics with character rhythm.
7. Audio handling: remove dialogue / sfx / BGM for audio‑incapable model; add reasonable ambient sound, dialogue, BGM for audio‑capable model.
8. Negative prompt handling: MiniMax‑H3 must NOT output negative_prompt field, all defect‑avoidance embed into positive prompt. Wan2.2 & LTX2.3 output negative prompt normally.
Input source: key‑frame sequence #IMAGE_FRAME_1# #IMAGE_FRAME_2# #IMAGE_FRAME_3# ... #IMAGE_FRAME_N#, user prompt #USER_PROMPT#. If prompt empty, generate transition purely from visual difference including inner‑graph arrows and storyboard marks.
"""
                },
                "negative_base": {
                    "zh": "跳帧卡顿，主体穿模变形，元素突变丢失，强行按照用户提示词改动任意关键帧主体、场景、光影等原生锚点，生硬植入用户诉求造成帧间叙事逻辑断裂，运动轨迹混乱，动作机械匀速，风格中途漂移，镜头剧烈抖动，光影色彩跳变，比例失调透视错误，多余杂物乱入，字幕水印logo，画面闪烁噪点，无视图内运动箭头与故事板轨迹信息、违背参考图绘制的运动走向",
                    "en": "frame skip & stutter, character clipping & distortion, element mutation or disappearance, forcibly modify immutable key‑frame anchors by user prompt, broken narrative logic caused by ill‑fitting demand, chaotic motion trajectory, mechanical constant‑speed movement, mid‑sequence style drift, violent camera shake, abrupt light‑color jump, wrong proportion & perspective, random redundant clutter, subtitle watermark logo, flicker & noise, ignore motion‑arrow / storyboard trajectory drawn inside reference image and deviate from graphic motion direction"
                }
            }
        }

        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然段落模式】自然段落（2‑4段），首段概述全序列的叙事目的、主体核心动作与整体基调，点明动作的起点与终点；中间段落按时间顺序拆解关键帧之间的动态演变，如果图片携带运动箭头、故事板分镜，则把图内轨迹逻辑融入帧间描述，详述中间动作、速度变化与情感转折；末段说明镜头运动、光影演变与整体氛围，强调全序列视觉连续性与风格统一性。存在用户引导词时将合规诉求自然融入分镜叙事；无引导词则纯基于多关键帧图像原生差异（含图内箭头轨迹标记）生成连贯过渡内容。语言富有画面感与叙事节奏，全程无帧率、码率、分辨率类数字技术参数，强化轨迹连贯性、情感流动感与画面精简约束，保证画面干净聚焦、叙事清晰、风格全程统一。字数350‑700。",
                "en": "[Natural Paragraph Mode] 2‑4 narrative paragraphs: first paragraph summarizes overall narrative purpose, core subject motion and tone, clarify motion start‑end point. Middle paragraphs decompose dynamic evolution frame‑by‑frame in chronological order. If input images contain motion arrows or storyboard panels, integrate graphic trajectory logic into inter‑frame description, elaborate intermediate action, speed variation and emotion transition. Last part explains camera movement, light‑shadow evolution and atmosphere, emphasize visual continuity & unified style across full sequence. Integrate valid user demands when given; generate purely from multi‑key‑frame visual difference(including inner‑graph arrow & trajectory marks) when prompt empty. Cinematic narrative language. Forbid numeric parameters such as fps, bitrate, resolution. Emphasize trajectory coherence, emotion flow and frame‑simplify constraint. 350‑700 words."
            },
            "structured": {
                "zh": """【结构化模式】
【类别】实拍类/动漫类
【关键帧固定锚点状态】
  - 帧1：[不可修改：位置、姿态、表情、光线、叙事角色；图内标记：无/运动箭头方向/故事板分镜备注]
  - 帧2：[不可修改：位置、姿态、表情、光线、叙事角色；图内标记：无/运动箭头方向/故事板分镜备注]
  - 帧3：[不可修改：位置、姿态、表情、光线、叙事角色；图内标记：无/运动箭头方向/故事板分镜备注]
  - （根据实际图片数量增减）
【用户诉求适配】（无引导词标注：无，纯多关键帧图像原生连贯分镜）
  - 核心需求提炼：用户指定帧间节奏/动作侧重/情绪强度/运镜诉求
  - 落地规则：仅在不改动任意关键帧锚点前提下融入帧间过渡设计；若图片携带运动箭头、故事板轨迹，优先采信图内运动路径，冲突需求直接舍弃
【全局正向约束】
  - 一致性基础：全序列主体身份、服装、道具、场景完全统一，无突变丢失
  - 动态基础：运动轨迹连续平滑；当参考图包含箭头、手绘轨迹，严格贴合图内运动走向；动作符合物理惯性与生物力学，有起承转合节奏
  - 质感基础：实拍类保留真实纹理与自然光影过渡；动漫类保持画风统一、线条流畅色块稳定
  - 镜头逻辑：三维视角变化平滑，运动服务叙事，透视准确无畸变，无跳轴抖动
【景别与三维镜头视角】
  - 距离维度（景别对应）：全序列统一景别范围，标注随镜头运动的景别变化逻辑
  - 水平方位维度：摄像机水平角度变化轨迹，标注起始与结束角度，变化平滑连续
  - 垂直俯仰维度：摄像机垂直角度变化轨迹，标注起始与结束俯仰，对应情绪变化
  - 镜头运动：运动类型（固定/跟拍/环绕/推拉摇移）、方向、速度变化与叙事作用
  - 景深氛围：全序列统一的虚实逻辑，标注景深随叙事的变化
【轨迹与动作规划】
  - 整体运动趋势：主体或镜头的核心运动方向与变化维度；若存在图内箭头轨迹，写明图内解析得到的运动路径
  - 帧间过渡详情：
    - 帧1 → 帧2：中间动作拆解、速度感知、物理逻辑、情感变化；遵循/参考图内运动标记
    - 帧2 → 帧3：中间动作拆解、速度感知、物理逻辑、情感变化；遵循/参考图内运动标记
  - 动作弧线与节奏：动作的起承转合节奏，对应的情感强度曲线；使用定性快慢描述，不出现具体秒数帧数
【色彩配比】
  - 主色调：占比70%，全序列统一基调
  - 辅助色：占比25%，丰富层次与环境
  - 点缀色：占比5%，制造视觉焦点
【氛围与连续性】
  - 光影演变：全序列光线方向、色温、明暗的渐变过程，过渡自然无跳变
  - 情绪/叙事节奏：整体氛围与情绪曲线，如何通过动作与镜头传递
【音频描述（模型支持音频才输出）】
  - 环境音效：环境声音细节
  - 人物台词：角色对白
  - 背景音乐：曲风、情绪氛围
【技术参数建议】（仅 structured 模式使用）
  - 镜头类型：对应镜头焦段与视觉效果说明
  - 运动节奏：整体节奏调性与情绪氛围释义
  - 质感补充：可按需添加的光学效果术语与说明
  - 技术禁止项：不出现帧率、码率、分辨率等无效数值参数
【风格标签】3‑5个关键词概括整体气质与叙事调性
【画面收尾精简约束】全序列无额外无关人物、多余摆件、杂乱装饰，所有环境元素仅服务叙事节奏与情绪表达，不抢夺主体视觉焦点，全程风格高度统一。""",
                "en": """[Structured Mode] Output strictly follow sections:
【Category】real‑shot / anime
【Key‑Frame Immutable Anchors】
  - Frame1: [Immutable: position, pose, expression, light, narrative role; graphic‑mark: None / motion‑arrow direction / storyboard note]
  - Frame2: [Immutable: position, pose, expression, light, narrative role; graphic‑mark: None / motion‑arrow direction / storyboard note]
  - Frame3: [Immutable: position, pose, expression, light, narrative role; graphic‑mark: None / motion‑arrow direction / storyboard note]
  -(add or remove items according to real frame count)
【User Demand Adaptation】(mark None if no prompt, pure multi‑key‑frame native transition)
  - Core Demand Extraction: inter‑frame rhythm / motion focus / emotion intensity / camera requirement from user
  - Application Rule: apply only to intermediate transition without altering any key‑frame anchor. If reference image contains motion‑arrow or storyboard trajectory, graphic motion path takes priority; discard conflicting demands.
【Global Positive Constraints】
  - Consistency Base: subject identity, costume, props, scene fully consistent across whole‑sequence, no mutation or loss
  - Motion Base: continuous‑smooth trajectory; strictly follow graphic motion direction if arrows / hand‑drawn trajectories exist in reference image; motion obey physical inertia & biomechanics, with complete beginning‑development‑turn‑conclusion rhythm
  - Texture Base: real‑shot preserve real texture & soft light‑shadow transition; anime unified art‑style, smooth lines & stable color blocks
  - Camera Logic: smooth 3‑D perspective transition, camera motion serve narrative, correct perspective without distortion, no axis‑jump or shake
【Shot & 3‑D Camera View】
  - Distance(shot): unified shot‑type range for full sequence, describe shot‑type variation along camera movement
  - Horizontal Azimuth: camera horizontal angle changing track, mark start‑end angle, keep smooth transition
  - Vertical Pitch: camera vertical angle changing track, mark start‑end pitch and corresponding emotion shift
  - Camera Movement: type(static/follow/surround/push/pull/pan/track), direction, speed variation & narrative purpose
  - Depth‑of‑field: unified virtual‑real logic for full sequence, describe depth‑of‑field shift along narrative
【Trajectory & Motion Plan】
  - Overall motion trend: core movement dimension of subject or camera; write parsed graphic motion path if arrow‑trajectory exists inside image
  - Inter‑frame transition detail:
    - Frame1 → Frame2: intermediate‑action breakdown, speed perception, physics logic, emotion change; follow / refer graphic marks inside image
    - Frame2 → Frame3: intermediate‑action breakdown, speed perception, physics logic, emotion change; follow / refer graphic marks inside image
  - Motion arc & rhythm: complete rhythm of beginning‑development‑turn‑conclusion, corresponding emotion intensity curve; use qualitative speed words, NO exact second / frame number
【Color Ratio】
  - Main tone:70%, unified base tone for full sequence
  - Auxiliary color:25%, enrich hierarchy & environment
  - Accent color:5%, create visual focal point
【Atmosphere & Continuity】
  - Light‑shadow evolution: gradual change of light direction, color‑temperature, brightness over full‑sequence, smooth transition without jump
  - Emotion / narrative rhythm: overall atmosphere & emotion curve, how conveyed via action and camera
【Audio Description(output only if model support audio)】
  - Ambient SFX: environment sound detail
  - Character Dialogue: character lines
  - BGM: music genre & mood
【Tech Suggestion】(structured‑only)
  - Lens Type: lens type & visual‑effect explanation
  - Motion Tempo: overall rhythm tonality & mood interpretation
  - Texture Enhancement: optional optical‑effect terms & explanation
  - Forbidden Tech Item: forbid fps, bitrate, resolution and other invalid numeric parameters
【Style Tags】3‑5 keywords for overall visual temperament
【Final Simplify Constraint】No extra unrelated character, redundant ornaments or messy decoration across full sequence. All environment elements serve narrative & emotion only, never steal subject visual focus. Style keep highly consistent through whole sequence."""
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