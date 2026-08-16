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
                "formula_zh": "内容组织顺序：真实亚洲女性（脸型、黑发、淡妆、穿搭）→ 自然写实肤色与发质 → 窗光柔和、温润氛围 → 近景肖像、背景虚化",
                "formula_en": "Content order: realistic Asian female (face shape, black hair, light makeup, outfit) → natural realistic skin tone and hair → soft window light, warm atmosphere → close portrait, blurred background"
            },
            "Z_image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：真实亚洲女性主体（脸型、黑发、淡妆、穿搭）→ 自然写实肤色与发质 → 窗光或柔和日光、温润氛围 → 近距离肖像、背景虚化（需渲染文字直接写入，支持中英双语）。",
                "formula_en": "Content order: realistic Asian female subject (face shape, black hair, light makeup, outfit) → natural realistic skin tone and hair → window or soft daylight, warm atmosphere → close-up portrait, blurred background (write any rendered text directly, supports Chinese and English)"
            },
            "Qwen_Image2512": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：亚洲女性特征、自然妆容与温婉神态 → 风格与画质（贴近真实的肌肤与毛发表现） → 柔和日光线条与淡雅氛围 → 正面或三分法构图、轻微虚化 →（需渲染文字直接写入提示词，支持中英双语）",
                "formula_en": "Content order: Asian female features, natural makeup and gentle expression → style and quality (true-to-life skin and hair) → soft daylight lines and elegant atmosphere → front or rule-of-thirds composition, slight blur → (write any rendered text directly into the prompt, supports Chinese and English)"
            },
            "Krea2": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：电影级光影氛围、柔和漫射清新光 → 人物体态情绪、温婉神情 → 胶片质感细节、自然肤调发质 → 服饰面料材质 → 极简布景、street style（密集关键词，中英术语并列）",
                "formula_en": "Content order: cinematic lighting atmosphere with soft diffused fresh light → body pose and mood, gentle expression → film grain texture details, natural skin tone and hair → fabric material → minimalist set, street style (dense keywords, Chinese-English terms in parallel)"
            },
            "Boogu": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：整体画面基调（清新淡雅氛围）→ 人物松弛姿态与温婉神情 → 自然肌肤妆发质感 → 简约留白环境",
                "formula_en": "Content order: overall image tone (fresh elegant atmosphere) → relaxed pose with gentle expression → natural skin, makeup and hair texture → simple negative-space environment"
            },
            "Mage_Flow": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：东亚女性五官肤质、自然妆容 → 体态姿态、温婉神情 → 光影层次、柔和漫射光 → 服饰细节、穿搭材质 → 轻量环境（密集关键词，中英术语并列）",
                "formula_en": "Content order: East Asian female facial features and skin, natural makeup → body pose, gentle expression → lighting layers, soft diffused light → clothing details, outfit material → lightweight environment (dense keywords, Chinese-English terms in parallel)"
            },
            "ERNIE_Image": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：亚洲女性特征、自然妆容与温婉神态 → 风格与画质（贴近真实肌肤与毛发） → 柔日和日光线条、淡雅氛围 → 正面或三分法、轻微虚化 →（需渲染文字直接写入提示词，支持中英双语）",
                "formula_en": "Content order: Asian female features, natural makeup and gentle expression → style and quality (true-to-life skin and hair) → soft daylight lines, elegant atmosphere → front or rule-of-thirds, slight blur → (write any rendered text directly into the prompt, supports Chinese and English)"
            },
            "GLM_Image": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：东亚女性自然面容 → 纪实摄影风格、原生肤质与黑发 → 自然光漫射、清淡通透 → 半身平视、生活化姿态 → 强调本真不修饰、避免西化五官与滤镜。中文自然语言描述效果最佳，无负向提示词通道，负面意图正向化写入提示词。",
                "formula_en": "Content order: East Asian female natural face → documentary photography style, natural skin and black hair → diffused natural light, clean and transparent → half-body eye level, casual living pose → emphasize authentic unadorned look, avoid westernized features and filters. Best described in Chinese natural language; no negative prompt channel, write negative intent positively into prompt."
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
                "formula_zh": "内容组织顺序：东亚女性主体与自然神态 → 场景与构图（半身平视生活化）→ 光影与氛围（自然光漫射清淡）→ 画种/摄影风格（纪实摄影）→ 需渲染文字用引号包裹。",
                "formula_en": "Content order: East Asian female subject & natural expression → scene & composition (half-body eye level, casual) → light & atmosphere (diffused natural light) → art/photography style (documentary photography) → wrap rendered text in quotes."
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
Forbidden: weight tags, redundant keywords; perfectly symmetrical face, flawless smoothed plastic skin, rigid neat hair, empty fake smile, blank stare; stage harsh light, cluttered background, extreme weird angles, perspective distortion. Natural mode blocks all optical numbers, only structured mode allows focal length & aperture with explanations.
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
                    "zh": "真实亚洲女性面部，眉眼唇轻微不对称，单眼皮内双柔和眼轮廓，细腻肤色过渡，保留毛孔、淡细纹、浅斑、肤色不均等原生肌理，自然毛躁碎发，生活化场景仅衬托主体，自然抓拍松弛姿态，真实情绪，无刻意摆拍，视角符合纪实人像逻辑，无透视畸变",
                    "en": "real Asian female face, natural slight asymmetry of brows eyes lips, single/internal double eyelids soft eye contour, delicate skin transition, retain pores fine lines faint spots uneven tone, messy broken hair, daily scene only foil subject, captured relaxed pose authentic emotion, no deliberate posing, perspective fits documentary portrait logic, no perspective distortion"
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
                    "zh": "完美对称五官，零瑕疵皮肤，厚重磨皮，塑胶假肤，模板网红脸，空洞假笑，僵硬摆拍，多余肢体动作，无神凝视，多余装饰路人，杂乱背景，舞台强光，过度锐化，高饱和撞色，鸟瞰虫眼视角，极端俯仰，透视畸变，肢体比例失调",
                    "en": "perfect symmetrical features, blemish-free skin, heavy skin smoothing, plastic fake skin, template influencer face, empty fake smile, stiff pose, redundant limbs, blank stare, extra ornaments passers-by, cluttered background, stage harsh light, over-sharpening, oversaturated color, bird/bug eye view, extreme pitch, perspective distortion, disproportionate body"
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
9.【技术参数建议】仅structured模式可输出，natural模式禁用；允许完整相机参数描述（焦距、光圈、快门速度、ISO、白平衡），附带空间效果释义：
- 古风汉服/婚纱礼服：85mm中长焦，f/2.8-f/4光圈，1/125s-1/250s快门，ISO200-800，摄影机远离主体，背景相对放大并靠近主体，柔化背景突出服饰质感
- 日系校园/街头潮牌：35mm小广角，f/2.8-f/4光圈，1/250s-1/500s快门，ISO100-400，摄影机较近靠近主体，适度强化近大远小，背景层次丰富，近距离临场抓拍
- 职场通勤/运动健身：50mm标准中焦，f/4-f/5.6光圈，1/125s-1/250s快门，ISO200-800，摄影机与主体保持常规距离，近大远小效果自然，背景与主体比例协调
- 泳装/艺术人体：50mm-85mm，f/2.8-f/4光圈，1/200s-1/500s快门，ISO100-400，自然透视或优雅压缩
- 动态抓拍：200mm长焦，f/2.8-f/4光圈，1/1000s-1/4000s高速快门，ISO400-1600，冻结高速运动瞬间
- 蓝调时刻/夜景：35mm-50mm，f/1.4-f/2大光圈，1/30s-1/60s慢速快门，ISO800-3200，捕捉低光环境氛围
10.风格标签+画面收尾精简约束""",
                "en": """[Structured Mode] Fixed output order:
1. Category positioning
2. Global mandatory skin constraints (face base / skin texture / hair details)
3. Composition (visual guide / subject ratio / aspect ratio / cleanup limit)
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
9. [Tech params] Only structured mode can output, natural mode forbidden; only qualitative focal length/aperture description with spatial effect explanation, shutter/ISO/white balance numerical parameters forbidden:
- Ancient Hanfu/wedding dress: 85mm medium telephoto, camera away from subject, background enlarged and closer to subject, softening background to highlight clothing texture
- Japanese campus/street fashion: 35mm small wide-angle, camera closer to subject, moderate near-far perspective, rich background layers, close-up immersive capture
- Workplace commute/sports fitness: 50mm standard mid-range, natural distance from subject, natural near-far effect, balanced subject-background ratio
- Swimwear/artistic nude: 50mm-85mm, natural perspective or elegant compression
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