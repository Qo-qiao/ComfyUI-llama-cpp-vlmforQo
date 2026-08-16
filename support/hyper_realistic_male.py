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
                "formula_zh": "内容组织顺序：一位超写实男性（年龄、胡须、发型、衣着）→ 照片级写实与肌理 → 侧光硬光、沉稳氛围 → 胸像或环境人像、景深控制",
                "formula_en": "Content order: a photorealistic male (age, beard, hairstyle, outfit) → photo-level realism with skin grain → side hard light, steady atmosphere → chest portrait or environmental portrait, depth control (no independent negative channel; supports multi-reference image editing)"
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：一位超写实男性主体（年龄、胡须、发型、衣着）→ 照片级写实与肌理 → 硬光或侧光塑造轮廓、沉稳氛围 → 胸像或环境人像、景深控制（需渲染文字直接写入，支持中英双语）",
                "formula_en": "Content order: a photorealistic male subject (age, beard, hairstyle, outfit) → photo-level realism with skin grain → hard or side light shaping contour, steady atmosphere → chest portrait or environmental portrait, depth control (write any rendered text directly, supports Chinese and English). "
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：男性身份、年龄与神情气质、硬朗超写实质感 → 风格与画质（真实肌理、胡须与皮肤细节） → 偏冷或侧光塑造立体骨骼感 → 胸像或特写、浅景深虚化背景 →（需渲染文字直接写入提示词，支持中英双语）",
                "formula_en": "Content order: male identity, age and demeanor, tough photorealistic texture → style and quality (real skin grain, beard and skin details) → cool or side light shaping three-dimensional bone structure → chest portrait or close-up, shallow depth blurring background → (write any rendered text directly into the prompt, supports Chinese and English)"
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：电影级光影氛围、硬光侧光骨骼感 → 人物体态情绪、沉稳神情 → 胶片质感细节、皮肤胡须纹理 → 服饰面料材质 → 极简布景、environmental portrait（密集关键词，中英术语并列）",
                "formula_en": "Content order: cinematic lighting atmosphere with hard side light bone structure → body pose and mood, steady expression → film grain texture details, skin and beard texture → fabric material → minimalist set, environmental portrait (dense keywords, Chinese-English terms in parallel)"
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面基调（沉稳硬朗氛围）→ 男士沉稳松弛摆姿 → 自然肌肤胡茬质感 → 简约留白环境",
                "formula_en": "Content order: overall image tone (steady tough atmosphere) → male steady relaxed pose → natural skin and stubble texture → simple negative-space environment"
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：面部五官肤质胡茬、硬朗轮廓 → 挺拔体态姿态 → 光影层次、硬光侧光 → 服饰细节、面料质感 → 轻量极简环境（密集关键词，中英术语并列）",
                "formula_en": "Content order: facial features, skin, stubble and tough contour → upright body posture → lighting layers, hard side light → clothing details, fabric texture → lightweight minimalist environment (dense keywords, Chinese-English terms in parallel)"
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：男性身份、年龄与气质、硬朗超写实质感 → 风格与画质（肌理、胡须与皮肤细节） → 偏冷侧光塑造立体骨骼 → 胸像或特写、浅景深虚化 →（需渲染文字直接写入提示词，支持中英双语）",
                "formula_en": "Content order: male identity, age and temperament, tough photorealistic texture → style and quality (skin grain, beard and skin details) → cool side light shaping three-dimensional bone → chest portrait or close-up, shallow depth blurring → (write any rendered text directly into the prompt, supports Chinese and English)"
            },
            "GLM_Image": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：超写实男性面部与胸像 → 电影级写实风格、胡须与肌肤细节 → 硬光侧光与冷调氛围 → 中近景、沉稳直视镜头 → 强调硬朗骨相、避免柔化与卡通感。中文自然语言描述效果最佳，无负向提示词通道，负面意图正向化写入提示词。",
                "formula_en": "Content order: photorealistic male face and chest portrait → cinematic realistic style, beard and skin details → hard side light and cool tone → medium close-up, steady gaze at camera → emphasize strong bone structure, avoid softening and cartoon feel. Best described in Chinese natural language; no negative prompt channel, write negative intent positively into prompt."
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
                "formula_zh": "内容组织顺序：超写实男性主体与神态气质 → 场景与构图（中近景平视）→ 光影与氛围（硬光侧光冷调）→ 画种/摄影风格（电影级写实）→ 需渲染文字用引号包裹。",
                "formula_en": "Content order: photorealistic male subject & temperament → scene & composition (medium close-up eye level) → light & atmosphere (hard side light, cool tone) → art/photography style (cinematic realism) → wrap rendered text in quotes."
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
Forbidden: no weight symbols, no redundant camera parameters, no anime/cartoon/illustration, no deformed anatomy, no bad hands, no over-retouched skin, no messy background, no fake smile, no snapshot selfie, no perspective distortion.
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
                    "zh": "超写实真人质感，硬朗男性面部骨骼，清晰下颌线条，眉眼唇轻微不对称，区分亚洲/欧美男性特征；面部干净无痘印瑕疵，保留毛孔、自然肌理与浅细纹，无过度磨皮与塑胶假肤、无AI模板脸；原生蓬松发丝与自然胡茬，干净布景，专业男模沉稳姿态，真实情绪；所有风格分支均保持真人写实基线，姿态挺拔硬朗有力量感",
                    "en": "photorealistic real human texture, tough male facial bone structure, clear jawline, natural slight asymmetry of eyes, eyebrows and lips, distinguish Asian/European male features; clean face without acne marks or blemishes, retain pores, natural texture and shallow fine lines, no excessive skin smoothing or plastic wax skin or AI template face; layered fluffy hair and natural stubble, restrained clean scene, steady professional male model pose, calm expression; all styles maintain photorealistic baseline with upright powerful posture"
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
                    "zh": "完美对称五官，过度磨皮，塑胶假肤，AI模板脸，无胡茬光滑面部，僵硬摆拍，空洞假笑，肢体畸形，柔弱纤细体态，坏手多手指，画面杂乱，透视畸变，高饱和艳色，二次元卡通质感，强光曝光异常",
                    "en": "perfect symmetrical face, excessive skin smoothing, plastic wax skin, AI template face, smooth face without stubble, stiff pose, empty fake smile, deformed limbs, weak slender figure, bad hands extra fingers, cluttered frame, perspective distortion, oversaturated color, anime cartoon style, harsh light abnormal exposure"
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
- 胸像硬朗骨骼感：85mm中长焦，f/2.8-f/4光圈，1/125s-1/250s快门，ISO200-800，摄影机远离主体，压缩空间突出硬朗骨相与胡茬肌理
- 极简肖像：85mm正面平光，f/1.8-f/2.8光圈，1/160s-1/320s快门，ISO100-400，柔化背景突出人物
- 科幻人像：50mm标准中焦，f/4-f/5.6光圈，1/60s-1/125s快门，ISO400-1600，环境透视自然
- 动态抓拍：200mm长焦，f/2.8-f/4光圈，1/1000s-1/4000s高速快门，ISO400-1600，冻结高速运动瞬间
- 蓝调时刻/夜景：35mm-50mm，f/1.4-f/2大光圈，1/30s-1/60s慢速快门，ISO800-3200，捕捉低光环境氛围""",
                "en": """[Structured Mode] Output strictly in this order:
1. Ethnic facial features
2. Style and clothing positioning
3. Skin hair stubble natural details
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
- Chest portrait with tough bone structure: 85mm medium telephoto, camera away from subject, compressed space highlighting tough bone structure and stubble texture
- Minimalist portrait: 85mm front flat light, softening background to highlight subject
- Sci-fi portrait: 50mm standard mid-range, natural environmental perspective"""
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
