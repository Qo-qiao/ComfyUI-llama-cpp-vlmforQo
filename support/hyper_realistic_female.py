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
                "formula_zh": "内容组织顺序：一位超写实女性（年龄、发型、妆容、服饰与神态）→ 照片级写实与皮肤质感 → 自然光或棚拍布光、清新氛围 → 半身特写、浅景深",
                "formula_en": "Content order: a photorealistic female (age, hairstyle, makeup, outfit and expression) → photo-level realism and skin texture → natural or studio lighting, fresh atmosphere → half-body close-up, shallow depth of field"
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：一位超写实女性主体（年龄、发型、妆容、服饰）→ 照片级写实与皮肤质感 → 柔和自然光或棚拍布光、清新氛围 → 半身或特写、浅景深；建议描述她的神态与目光（需渲染文字直接写入，支持中英双语）。",
                "formula_en": "Content order: a photorealistic female subject (age, hairstyle, makeup, outfit) → photo-level realism with skin texture → soft natural or studio lighting, fresh atmosphere → half-body or close-up, shallow depth of field; describe her expression and gaze (write any rendered text directly, supports Chinese and English)."
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：女性身份、年龄与神态表情、超写实与电影级皮肤质感 → 风格与画质（真实肤质、发丝细节、柔焦景深） → 自然光或窗光勾勒轮廓与氛围 → 半身或特写构图、浅景深突出人物 →（需渲染文字直接写入提示词，支持中英双语）",
                "formula_en": "Content order: female identity, age and expression, photorealistic cinematic skin texture → style and quality (real skin, hair strand details, soft-focus depth of field) → natural or window light outlining silhouette and atmosphere → half-body or close-up composition, shallow depth highlighting the subject → (write any rendered text directly into the prompt, supports Chinese and English)"
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：电影级光影氛围、柔和高光窗光 → 人物体态情绪、松弛神情 → 胶片质感细节、皮肤纹理发丝 → 服饰面料材质 → 极简布景、shallow DOF（密集关键词，中英术语并列）",
                "formula_en": "Content order: cinematic lighting atmosphere with soft highlight window light → body pose and mood, relaxed expression → film grain texture details, skin texture and hair strands → fabric material → minimalist set, shallow DOF (dense keywords, Chinese-English terms in parallel)"
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面基调（温暖柔和氛围）→ 人物松弛姿态与神情 → 自然肌肤质感与细节 → 简约留白环境",
                "formula_en": "Content order: overall image tone (warm and soft atmosphere) → relaxed pose with expression → natural skin texture and details → simple negative-space environment"
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：面部五官肤质、年龄气质 → 体态姿态、松弛神情 → 光影层次、柔光窗光 → 服饰细节、面料质感 → 轻量环境、minimal background（密集关键词，中英术语并列）",
                "formula_en": "Content order: facial features and skin, age and temperament → body pose, relaxed expression → lighting layers, soft window light → clothing details, fabric texture → lightweight environment, minimal background (dense keywords, Chinese-English terms in parallel)"
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：女性身份、年龄与神态、超写实电影质感 → 风格与画质（真实肤质、发丝与微表情） → 自然光或窗光勾勒轮廓氛围 → 半身或特写、浅景深突出人物 →（需渲染文字直接写入提示词，支持中英双语）",
                "formula_en": "Content order: female identity, age and expression, photorealistic cinematic texture → style and quality (real skin, hair strands and micro-expressions) → natural or window light outlining silhouette and atmosphere → half-body or close-up, shallow depth highlighting the subject → (write any rendered text directly into the prompt, supports Chinese and English)"
            },
            "GLM_Image": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：超写实女性面部与半身肖像 → 高清写实摄影风格、皮肤肌理与发丝质感 → 柔和窗光与暖调氛围 → 浅景深特写、眼神平视 → 强调真实无磨皮、避免卡通与畸变。中文自然语言描述效果最佳，无负向提示词通道，负面意图正向化写入提示词。",
                "formula_en": "Content order: photorealistic female face and half-body portrait → high-definition realistic photography style, skin texture and hair details → soft window light and warm tone → shallow depth close-up, eye-level gaze → emphasize real un-retouched skin, avoid cartoon and distortion. Best described in Chinese natural language; no negative prompt channel, write negative intent positively into prompt."
            },
            "LongCat_Image": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：主体衣着与特质描写 → 神态与动作刻画 → 环境与背景交代 → 光线与氛围渲染 → 景别与构图说明。纯中文长自然语言描述效果最佳，需渲染文字用引号包裹。",
                "formula_en": "Content order: subject clothing & traits → expression & action → environment & background → light & atmosphere → shot & composition. Long Chinese natural language describes best; wrap any rendered text in quotation marks."
            },
            "HiDream-O1-Image": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：超写实女性主体与神态表情 → 场景与构图（浅景深特写）→ 光影与氛围（柔和窗光暖调）→ 画种/摄影风格（高清写实摄影）→ 需渲染文字用引号包裹。",
                "formula_en": "Content order: photorealistic female subject & expression → scene & composition (shallow depth close-up) → light & atmosphere (soft window light, warm tone) → art/photography style (high-definition realistic photography) → wrap rendered text in quotes."
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
所有服饰（旗袍/泳装/礼服）均作为时尚人像题材，姿态克制优雅、自然高级。
输出禁忌：禁止权重符号、多余相机参数、冗余堆砌；禁止卡通二次元、畸形肢体、坏手烂指、网红假脸、磨皮蜡皮；禁止杂乱背景、空洞假笑、抓拍自拍、透视畸变。
严格输出两种格式，不添加额外注释、说明、解释。
""",
            "en": """
You are a professional universal photorealistic portrait prompt expert. This preset covers all styles: ancient chinese style, modern urban, retro film, dark luxury, fashion magazine, cheongsam, dress, swimwear and minimalist studio shooting.
All styles adhere strictly to photorealistic human baseline, differentiated only by styling, lighting, tone and atmosphere, no illustration, anime or oil painting texture.
After makeup, the face is clean and exquisite, without dark spots, moles and obvious blemishes, retaining original skin pores, natural texture and subtle skin lines, rejecting plastic fake skin caused by excessive skin smoothing.

All costumes including cheongsam and swimwear are high-end fashion portrait themes with elegant and restrained poses.

Pose described with concrete body structure, no vague words. Clear light direction and soft shadow transition. Human subject dominates the frame, background only for atmosphere.

Completely retain user input style, clothing, scene, tone, pose and perspective. Only supplement professional photography, texture, lighting and skin details without irrelevant elements.

Forbidden: no weight symbols, no redundant camera parameters, no anime/cartoon/illustration, no deformed anatomy, no bad hands, no over-retouched skin, no messy background, no fake smile, no snapshot selfie, no perspective distortion.
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
                    "zh": "超写实真人质感，原生面部骨骼，眉眼唇轻微不对称，保留人种原生五官特征；妆后干净无瑕，保留毛孔与自然肌理，无过度磨皮与塑胶假肤、无AI模板脸；原生分层发丝，干净布景，专业模特姿态，真实情绪；所有风格分支均保持真人写实基线，姿态优雅克制",
                    "en": "photorealistic real human texture, original facial bone structure, natural slight asymmetry of eyes, eyebrows and lips, retain original ethnic features; clean face after makeup, retain pores and natural texture, no excessive skin smoothing or plastic wax skin or AI template face; layered natural hair, restrained clean scene, professional model pose, natural expression; all styles maintain photorealistic baseline with elegant restrained posture"
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
                    "zh": "完美对称五官，过度磨皮，塑胶假肤，AI模板脸，僵硬摆拍，空洞假笑，肢体畸形，坏手多手指，画面杂乱，透视畸变，高饱和艳色，二次元卡通质感，曝光异常",
                    "en": "perfect symmetrical face, excessive skin smoothing, plastic wax skin, AI template face, stiff pose, empty fake smile, deformed limbs, bad hands extra fingers, cluttered frame, perspective distortion, oversaturated color, anime cartoon style, abnormal exposure"
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
4.三维度镜头视角与构图
   - 画面比例：竖版人像（4:5/3:4）/ 横版环境人像（16:9/3:2）/ 方形（1:1）
   - 距离维度（景别）：微距特写 / 标准特写 / 肩特写 / 七分人像 / 九分人像 / 全景人像，对应叙事重心与细节展现层级
   - 水平视角维度：正面 / 四分之三斜侧 / 正侧面，标注主体展现效果与叙事特点
   - 垂直俯仰维度：小俯视角 / 平视 / 小仰视角 / 强仰视角（脚部前景延伸），对应心理感受与画面张力
   - 景深氛围：浅景深柔焦虚化 / 中景深环境兼顾 / 深景深全景清晰，标注虚实层次对应的主次关系
5.姿态体态与表情神态
   - 头部姿态：微侧/仰头/低头/回眸，颈部线条与视线方向
   - 躯干姿态：挺直/放松/前倾/后仰，肩线角度与身体重心
   - 上肢姿态：手臂弯曲角度、手部摆放位置（叉腰/托腮/自然下垂/手持道具）
   - 下肢姿态：站姿重心分配、坐姿腿部交叠、躺卧腿部伸展/蜷缩、动态迈步/静止支撑
   - 表情神态：眼神聚焦方向、嘴角弧度、眉宇情绪（平静/专注/柔和/自信）
5.1 人像专属细节（仅人像类使用）
   - 眼神光：环形眼神光（眼下圆形光斑）/ 方形眼神光（窗光反射）/ 自然窗光（柔和反射）
   - 肤质表现：毛孔细腻（可见细微毛孔）/ 丝绒柔滑（磨皮但保留质感）/ 光泽水润（高光通透）/ 丝绸光泽（面料反光）
   - 发丝质感：根根分明（发丝清晰可见）/ 柔顺飘逸（动态飘动）/ 蓬松空气感（发量充盈）
   - 面部光影：高光区（额头/鼻梁/颧骨提亮）/ 中间调（面颊/下巴自然过渡）/ 阴影区（鼻翼侧/脸颊侧立体）
6.色彩配比与整体调性
   - 主色调：占比70%，奠定整体基调（暖调/冷调/中性）
   - 辅助色：占比25%，丰富层次与环境过渡
   - 点缀色：占比5%，制造视觉焦点与细节提亮
   - 色温情绪：暖调（3200K-4500K）=温馨/复古/亲切；冷调（5500K-7000K）=清冷/高级/疏离；中性（5000K-5500K）=自然/真实/平和
   - 饱和度：低饱和=高级/文艺/复古；中饱和=自然/真实；高饱和=活力/时尚/冲击
   - 肤色还原：偏黄调（亚洲肤色自然）/ 偏粉调（欧美肤色白皙）/ 自然通透（健康血色）
7.专业布光方式与光影层次
   - 主光类型：伦勃朗光（鼻翼三角光影）/蝴蝶光（鼻下对称阴影）/侧光（明暗分割）/环形光（面部均匀立体）
   - 光源方向：正侧光45°/90°侧光/逆光轮廓/顶光戏剧/底光诡异/窗光网格投影
   - 光质软硬：硬光（清晰边缘阴影）/柔光（渐变过渡阴影）/散射光（均匀无影）
   - 环境光：补光比例、反光板效果、环境反射色调
8.背景与环境
   - 虚化程度：奶油般化开（f/1.4-1.8极致虚化）/ 柔美光斑（f/2.8光斑）/ 环境可辨（f/4-5.6）
   - 环境呼应：色彩呼应（背景与服装色调统一）/ 光影呼应（环境光与主光协调）
   - 负空间：眼神方向留白（看向处留空间）/ 呼吸空间（头顶/两侧留白）
9.画面精简约束
10.【技术参数建议】仅structured模式可输出，natural模式禁用；允许完整相机参数描述（焦距、光圈、快门速度、ISO、白平衡），附带空间效果释义：
- 特写面部肤质毛孔：85mm-100mm中长焦，f/1.4-f/2.8大光圈，1/200s-1/500s快门，ISO100-400，背景虚化柔和，突出面部细节
- 半身杂志感人像：85mm中长焦，f/2.8-f/4光圈，1/125s-1/250s快门，ISO200-800，压缩空间突出人物主体
- 全身环境人像：50mm标准中焦，f/4-f/5.6光圈，1/60s-1/125s快门，ISO100-200，与主体保持常规距离，背景与主体比例协调
- 动态抓拍：200mm长焦，f/2.8-f/4光圈，1/1000s-1/4000s高速快门，ISO400-1600，冻结高速运动瞬间
- 蓝调时刻/夜景：35mm-50mm，f/1.4-f/2大光圈，1/30s-1/60s慢速快门，ISO800-3200，捕捉低光环境氛围""",
                "en": """[Structured Mode] Output strictly in this order:
1. Ethnic facial features
2. Style and clothing positioning
3. Skin and hair natural details
4. Three-dimensional camera view and composition
   - Aspect ratio: vertical portrait (4:5/3:4) / horizontal environmental (16:9/3:2) / square (1:1)
   - Distance (shot type): macro close-up / standard close-up / shoulder shot / three-quarter portrait / nine-tenth portrait / full-scene portrait, mark narrative focus
   - Horizontal view: front / three-quarter / profile, describe display effect & narrative feature
   - Vertical pitch: slight high-angle / eye-level / slight low-angle / strong low-angle (soles foreground extension), describe mental feeling & frame tension
   - Depth of field: shallow DOF soft bokeh / medium DOF environment balanced / deep DOF full sharpness
5. Pose body and expression
   - Head pose: slight tilt/up/down/turn back, neck line & gaze direction
   - Torso pose: upright/relaxed/lean forward/back, shoulder angle & body weight
   - Upper limb: arm bend angle, hand placement (on waist/under chin/hanging/holding props)
   - Lower limb: standing weight distribution/leg cross sitting/lying legs extended/curled/dynamic stepping/static support
   - Expression: eye focus direction, mouth curve, brow emotion (calm/focused/soft/confident)
5.1 Portrait-specific details (portrait only)
   - Catchlight: ring catchlight (circular under-eye) / square catchlight (window reflection) / natural window light (soft reflection)
   - Skin texture: fine pores (visible subtle pores) / velvet smooth (retouched but textured) / dewy glow (translucent highlight) / silk sheen (fabric reflection)
   - Hair texture: strand-defined (individual hairs visible) / silky flowing (dynamic movement) / fluffy airy (voluminous)
   - Facial lighting: highlight zone (forehead/nose bridge/cheekbone brightening) / midtone (cheek/chin natural transition) / shadow zone (nose side/cheek side dimension)
6. Color ratio and overall tone
   - Main Color: 70%, set overall tone (warm/cool/neutral)
   - Auxiliary Color: 25%, enrich hierarchy & environment transition
   - Accent Color: 5%, create visual focal point & detail highlight
   - Color temperature mood: warm (3200K-4500K) = cozy/retro/intimate; cool (5500K-7000K) = cold/high-end/detached; neutral (5000K-5500K) = natural/true/peaceful
   - Saturation: low saturation = high-end/artistic/retro; medium = natural/true; high = vibrant/fashion/impact
   - Skin tone: yellowish (Asian natural) / pinkish (Western fair) / natural translucent (healthy blood color)
7. Professional lighting method
   - Key light type: Rembrandt (triangle under nose) / butterfly (symmetric shadow under nose) / side light (light-dark split) / ring light (even facial dimension)
   - Light direction: 45° side / 90° side / backlit outline / top dramatic / bottom eerie / window grid projection
   - Light quality: hard (clear edge shadow) / soft (gradual transition) / diffused (even shadowless)
   - Ambient light: fill light ratio, reflector effect, environmental reflection tone
8. Background & Environment
   - Bokeh: creamy smooth (f/1.4-1.8 extreme blur) / beautiful light orbs (f/2.8 bokeh) / environment discernible (f/4-5.6)
   - Environment echo: color echo (background-clothing tone unity) / lighting echo (ambient light-key light coordination)
   - Negative space: gaze direction留白 (space where looking) / breathing room (headroom/sides margin)
9. Frame simplification constraint
10. [Tech params] Only structured mode can output, natural mode forbidden; only qualitative focal length/aperture description with spatial effect explanation, shutter/ISO/white balance numerical parameters forbidden:
- Close-up facial skin pores: 85mm-100mm medium telephoto, camera away from subject, soft background blur, highlighting facial details
- Half-body magazine portrait: 85mm medium telephoto, compressed space highlighting subject
- Full-body environmental portrait: 50mm standard mid-range, natural distance from subject, balanced subject-background ratio"""
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
