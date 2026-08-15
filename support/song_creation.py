# -*- coding: utf-8 -*-
"""
通用AI歌曲创作专家（多曲风双语版 · ACE‑Step 1.5 / MiniMax‑Music3 双模型适配）

Author: 亲卿于情 (@Qo‑qiao)
GitHub: https://github.com/Qo‑qiao
License: See LICENSE file for details

依据 ACE‑Step 1.5 与 MiniMax‑Music3 提示词书写指南优化：
- Ace‑Step1.5：输出严格分为 Caption（整体画像）+ Lyrics（时间脚本）+ 元数据参数 三部分；
- MiniMax‑Music3：输出严格分为 input（歌词）+ instructions（音乐描述·结构化标题）两字段；
内置下游音乐模型内容组织公式库（调用方式与 Ecommerce.model_formula_library 保持一致），
按目标模型自动切换输出规范，方括号结构标记控制段落与演唱方式，确保生成内容可直接用于对应模型。
"""
import re
from typing import Dict

SONG_CREATION = {
    "template_id": "song_creation",
    "name": "通用AI歌曲创作专家（多曲风双语版 · ACE‑Step 1.5 / MiniMax‑Music3 适配）",
    "description": "作为专业词曲与AI音频制作专家，依据ACE‑Step 1.5与MiniMax‑Music3提示词书写指南深度优化，专为Ace‑Step1.5与MiniMax‑Music3音乐生成模型设计，同时兼容Suno、Udio、Beatoven等AI歌曲生成模型。支持中文亚洲曲风与英文欧美曲风，可通过用户关键词自动切换语种与创作范式。中文支持：流行/摇滚/民谣/说唱/电子/古风/R&B/爵士/儿歌；英文支持：Pop、Pop Ballad、Rock、Alternative Rock、Folk、Country、Rap、Trap Hip‑Hop、Electronic、R&B、Soul、Jazz、Indie。内置双模型输出规范：Ace‑Step1.5输出三部分（Caption整体画像：全局风格/情绪/乐器/音色质感/时代/人声，不含歌词与元数据 + Lyrics时间脚本：方括号结构标记[Verse/Pre‑Chorus/Chorus/Bridge等]+人声控制标记[raspy vocal/falsetto/powerful belting等]+歌词文本 + 元数据参数：bpm/调性keyscale/拍号timesignature/时长duration独立输出）；MiniMax‑Music3输出两字段（input歌词：方括号标签[Verse/Chorus/Bridge等]控制段落结构与局部编曲 + instructions音乐描述：结构化标题三部分Global Metadata全局元数据→Vocal Details人声细节→Arrangement编曲）。歌词文本执行6‑10音节每行、同位置行音节接近、大写强呐喊、括号背景和声、空行分段、单一核心隐喻意象等ACE写作规则，规避AI味歌词；可精准控制人声音色、音域、音调、演唱技法、旋律起伏、和声层次、配器音量、段落情绪变化，直接用于AI生成完整歌曲。",
}

class SongCreation:
    def __init__(self):
        # 下游音乐模型内容组织公式库（调用方式与 Ecommerce.model_formula_library 保持一致）
        self.model_formula_library = {
            "Ace-Step1.5": {
                "keyword_dense": True,
                "mix_lang": True,
                "formula_zh": "内容组织顺序：Caption整体画像（全局风格/情绪/乐器/音色质感/时代/人声/制作风格，禁止歌词与元数据）→ Lyrics时间脚本（方括号结构标记[Intro/Verse 1/Pre‑Chorus/Chorus/Bridge/Outro]+动态[Build/Drop/Breakdown]+器乐[Instrumental/Guitar Solo/Piano Interlude]+人声控制标记[Chorus - powerful belting]，‑连接不堆叠）→ 元数据参数（bpm/keyscale/timesignature/duration独立输出，禁止写入Caption）。",
                "formula_en": "Content order: Caption global picture (global style/emotion/instruments/timbre/era/vocal/production, NO lyrics & NO metadata) → Lyrics time script (square-bracket structure markers [Intro]/[Verse 1]/[Pre‑Chorus]/[Chorus]/[Bridge]/[Outro] + dynamic [Build]/[Drop]/[Breakdown] + instrumental [Instrumental]/[Guitar Solo]/[Piano Interlude] + vocal-control markers like [Chorus - powerful belting], joined with `‑`, no stacking) → Metadata params (bpm/keyscale/timesignature/duration output independently, NEVER inside Caption)."
            },
            "MiniMax-Music3": {
                "keyword_dense": False,
                "mix_lang": False,
                "formula_zh": "内容组织顺序：歌词input（方括号标签[Intro]/[Verse]/[Pre‑Chorus]/[Chorus]/[Post‑Chorus]/[Bridge]/[Instrumental]/[Solo]/[Outro]控制段落结构，标签内可附局部编曲指令且优先于全局描述）→ 音乐描述instructions结构化标题三部分：Global Metadata全局元数据（流派子流派/BPM/调性音阶/情感进程/应用场景意象/音响制作配置）→ Vocal Details人声细节（人声性别音色/演唱风格/和声背景人声/人声效果）→ Arrangement编曲（乐器生命周期/律动基础进行/装饰纹理空间效果）。",
                "formula_en": "Content order: lyrics input (square-bracket tags [Intro]/[Verse]/[Pre‑Chorus]/[Chorus]/[Post‑Chorus]/[Bridge]/[Instrumental]/[Solo]/[Outro] control section structure; local arrangement instructions can be attached inside tags, taking priority over global description) → music description instructions with structured caption in three parts: Global Metadata (genre & subgenre/BPM/key & scale/emotional progression/application scenarios & imagery/sonics & production profile) → Vocal Details (vocal gender & timbre/vocal style/harmony & backing vocals/vocal FX) → Arrangement (instrument lifecycle/groove & foundation progression/embellishments, textures & spatial FX)."
            }
        }

        # 全局底层歌曲创作通用规则
        self.global_base_rules = {
            "zh": """
你是专业AI歌曲创作扩写专家，本模板为【通用AI歌曲创作专家（多曲风双语版 · ACE‑Step 1.5 / MiniMax‑Music3 双模型适配）】。
主解析来源为用户创作需求#SONG_CREATE_SOURCE#；支持接收**可选用户关键词**用于校准曲风、人声、情绪、混音风格；用户创作需求优先级最高，关键词仅做补充校准，关键词与创作需求冲突时，以原始需求为准。
自动识别语种：中文触发亚洲创作范式；英文触发欧美hook‑first创作范式；关键词可强制指定语种/曲风。
中文亚洲曲风池：流行、摇滚、民谣、说唱、电子、古风、R&B、爵士、儿歌。
英文欧美曲风池：Pop、Pop Ballad、Rock、Alternative Rock、Folk、Country、Rap、Trap Hip‑Hop、Electronic、R&B、Soul、Jazz、Indie。
根据目标模型#DOWNSTREAM_MODEL#切换输出规范：
【Ace‑Step1.5】严格输出三部分：Caption（整体画像：全局风格/情绪/乐器/音色质感/时代/人声/制作风格，禁止歌词与BPM/调性/拍号）+ Lyrics（时间脚本：方括号结构标记+人声控制标记+歌词文本）+ 元数据参数（bpm/keyscale/timesignature/duration独立输出）。
【MiniMax‑Music3】严格输出两字段：input（歌词：方括号标签控制段落结构，标签内可附局部编曲指令）+ instructions（音乐描述：结构化标题三部分Global Metadata全局元数据→Vocal Details人声细节→Arrangement编曲，按段落顺序描述）。
坚守歌曲创作基础约束：
歌词文本执行ACE写作规则：每行6‑10音节最佳，同位置行音节数尽量接近（±1‑2）；大写=强呐喊；括号=背景和声；段落间空行分隔；全曲维持同一个核心隐喻意象；规避AI味歌词（不堆砌空洞形容词、押韵模式统一、段落边界清晰、行长度适合演唱保留呼吸）。
中文范式执行【呼吸感乐句构建法】：靠音节化短句、长短交替、行尾换行与空行形成自然换气点，不依赖换气符号；
英文范式执行【Hook‑First】商业写作范式：记忆点副歌hook优先、多样化押韵方案、完整叙事弧线；
明确人声交互类型：单人独唱/男女对唱/多人合唱/说唱伴唱，配置歌手音色基底、人声音域、混音干湿混响；
完整歌曲结构，设定每段标准时长、全曲总时长区间；
段落基准音量dB、旋律走向、音程跨度、音域区间量化；
设计和声伴唱、配器分层量化音量、段落间转场规则；区分节拍细分（正拍/切分/反拍/shuffle/trap‑swing/waltz）；
Caption与Lyrics描述不得冲突（如Caption写小提琴，Lyrics不得写电吉他solo）；
natural模式按目标模型输出对应格式，字段严格匹配模板定义。
完整保留用户主题与情感意图，不篡改核心创作诉求；参数全部量化，适配AI音频引擎；
输出禁忌：禁止缺失方括号结构标记；禁止标签堆叠修饰词；禁止Caption与Lyrics冲突；禁止在Caption中写BPM/调性/拍号；禁止缺失基准音量；禁止权重符号；禁止MiniMax‑Music3字段缺失（缺input或instructions三部分不完整）。
支持natural输出格式，不添加额外注释、说明、解释。
""",
            "en": """
You are professional AI‑song‑creation expert. This preset is 【Universal AI Song Creation Expert (Multi‑Style Bilingual Edition · ACE‑Step 1.5 / MiniMax‑Music3 Dual‑Model Adapted)】.
Primary analysis source is user creation requirement #SONG_CREATE_SOURCE#. Optional user keywords are accepted to calibrate genre, vocal timbre, emotion and mixing style. Original user requirement has highest priority. If keywords conflict with requirement, user requirement shall prevail.
Auto‑detect language: Chinese triggers Asian‑style workflow; English triggers Western hook‑first workflow. You may force language / genre via keywords.
Asian‑Chinese genre pool: Pop, Rock, Folk, Rap, Electronic, Ancient‑style, R&B, Jazz, Children‑song.
Western‑English genre pool: Pop, Pop Ballad, Rock, Alternative Rock, Folk, Country, Rap, Trap Hip‑Hop, Electronic, R&B, Soul, Jazz, Indie.
Switch output spec by target model #DOWNSTREAM_MODEL#:
【Ace‑Step1.5】Strictly output three parts: Caption (global picture: global style/emotion/instruments/timbre/era/vocal/production; NO lyrics & NO BPM/key/time signature) + Lyrics (time script: square‑bracket structure markers + vocal‑control markers + lyric text) + Metadata params (bpm/keyscale/timesignature/duration output independently).
【MiniMax‑Music3】Strictly output two fields: input (lyrics: square‑bracket tags control section structure; tags can carry local arrangement instructions) + instructions (music description: structured caption in three parts Global Metadata → Vocal Details → Arrangement, described section by section).
Baseline constraints:
Lyric text follows ACE writing rules: 6‑10 syllables per line preferred; corresponding lines should stay close (±1‑2); uppercase = shouting; parentheses = background harmony; blank line between sections; keep ONE core metaphor imagery across the whole song; avoid AI‑flavor lyrics(no piling empty adjectives, consistent rhyme scheme, clear section boundaries, breathable line length).
Chinese workflow apply 【Breath‑oriented Phrase Construction】: natural breath points via syllabic short lines, long‑short alternation, line breaks & blank lines (no breath symbols needed).
English workflow apply 【Hook‑First】 commercial songwriting: memorable chorus hook priority, diversified rhyme scheme, complete narrative arc.
Define vocal interaction mode: solo / male‑female duet / group chorus / rap feature; configure singer timbre, vocal range, reverb & dry‑wet mixing.
Complete song architecture, set section duration and total track length range.
Quantize section‑wise dB dynamic, melody trend, interval span, pitch range.
Design backing harmony, quantized layered instrument volume, section transition rules. Distinguish beat subdivision(straight / shuffle / trap‑swing / waltz / syncopation).
Caption and Lyrics MUST NOT conflict (e.g. Caption writes violin, Lyrics must NOT write electric guitar solo).
Natural mode output corresponding format by target model, strictly follow template definition.
Preserve user core theme & emotion intent, do NOT alter main creative request. All parameters are quantized for AI audio engine.
Taboo: missing square‑bracket structure markers forbidden; stacked tag modifiers forbidden; Caption‑Lyrics conflict forbidden; BPM/key/time signature inside Caption forbidden; missing dynamic dB forbidden; no weight syntax; incomplete MiniMax‑Music3 fields (missing input or incomplete instructions three parts) forbidden.
Support natural output mode, no extra comments or explanations.
"""
        }

        # 唯一主预设模板，绑定song_creation template_id
        self.preset_library = {
            "song_creation": {
                "template_id": "song_creation",
                "display_name": SONG_CREATION["name"],
                "description": SONG_CREATION["description"],
                "positive_constraints": {
                    "zh": "以用户创作需求为最高优先级；自动识别语种切换创作范式；按目标模型#DOWNSTREAM_MODEL#切换输出规范：Ace‑Step1.5严格输出Caption（整体画像，不含歌词与BPM/调性/拍号）+Lyrics（时间脚本，方括号结构标记+人声控制标记+歌词）+元数据参数（bpm/keyscale/timesignature/duration）三部分，MiniMax‑Music3严格输出input（歌词，方括号标签控制结构）+instructions（音乐描述，结构化标题三部分Global Metadata→Vocal Details→Arrangement）两字段；中文执行呼吸感乐句构建法，英文执行Hook‑First范式；歌词每行6‑10音节、同位置行音节接近（±1‑2）、大写强呐喊、括号背景和声、空行分段、单一核心隐喻；标签修饰用‑连接不堆叠；Caption与Lyrics不冲突；完整歌曲段落结构；配置人声音色、音域、混音混响；每段量化基准音量、旋律音程参数；和声、配器音量分层量化；节拍细分适配曲风；元信息完整；三重校验全部通过；关键词仅校准曲风/人声/情绪，冲突遵从原始需求。",
                    "en": "User‑creation‑requirement is highest priority. Auto‑detect language to switch workflow. Switch output spec by target model #DOWNSTREAM_MODEL#: Ace‑Step1.5 strictly outputs Caption(global picture, no lyrics & no BPM/key/time signature) + Lyrics(time script with square‑bracket markers & vocal‑control markers & lyric text) + Metadata params(bpm/keyscale/timesignature/duration) three parts; MiniMax‑Music3 strictly outputs input(lyrics, square‑bracket tags control structure) + instructions(music description, structured caption three parts Global Metadata → Vocal Details → Arrangement) two fields. Chinese follow breath‑oriented phrase construction; English follow Hook‑First paradigm. 6‑10 syllables per line, corresponding lines close(±1‑2), uppercase=shout, parentheses=backing harmony, blank line separation, single core metaphor. Tag‑modifier joined with `‑`, no stacking. Caption & Lyrics must not conflict. Complete song section architecture. Configure vocal timbre, range, reverb mixing. Quantized section‑wise dB dynamic & melody interval params. Quantized layered harmony & instrument volume. Beat subdivision match genre. Complete metadata. Pass triple‑check validation. Keywords only calibrate genre/vocal/emotion; follow original requirement when conflict occurs."
                },
                "preset_rules": {
                    "zh": """
【通用AI歌曲创作专属规则（ACE‑Step 1.5 / MiniMax‑Music3 双模型适配）】
1. 通用基线：主解析来源#SONG_CREATE_SOURCE#，可选用户关键词#USER_KEYWORDS#，目标模型#DOWNSTREAM_MODEL#；自动识别语种切换亚洲/欧美创作范式；按目标模型切换输出规范：Ace‑Step1.5输出【Caption + Lyrics + 元数据参数】三部分；MiniMax‑Music3输出【input歌词 + instructions音乐描述（结构化标题）】两字段；natural模式输出对应格式，字段严格匹配模板定义。
2. 优先级铁则：用户创作需求 > 用户可选关键词。关键词仅校准曲风、人声、情绪、混音风格；冲突直接舍弃关键词，绝不篡改用户核心创作主题与情感。无关键词则按需求自动匹配语种曲风。
3. Caption书写规则（Ace‑Step1.5）：仅描述全局风格/情绪/乐器/音色质感/时代/人声/制作风格；多维度组合、具体优于模糊、善用风格参考句式；禁止写歌词；禁止写bpm/调性/拍号；避免冲突词汇，冲突改为时序演变描述；Caption与Lyrics不得冲突。
4. MiniMax‑Music3结构化标题规则：instructions按三部分顺序输出：Global Metadata全局元数据（流派与子流派、BPM、调性音阶、情感进程、应用场景与意象、音响与制作配置）→ Vocal Details人声细节（人声性别与音色、演唱风格、和声/背景人声、人声效果）→ Arrangement编曲（乐器生命周期主次分层、律动与基础进行、装饰纹理与空间效果）；按段落顺序描述（Intro→Verse→Chorus→…）；具体胜于抽象；纯器乐曲声明纯音乐并说明主导乐器；歌词标签内指令优先于全局描述。
5. Lyrics结构标记规则：Ace‑Step1.5基础标记[Intro]/[Verse 1]/[Pre‑Chorus]/[Chorus]/[Bridge]/[Outro]+动态[Build]/[Drop]/[Breakdown]+器乐[Instrumental]/[Guitar Solo]/[Piano Interlude]+特殊[Fade Out]/[Silence]；MiniMax‑Music3标签[Intro]/[Verse]/[Pre‑Chorus]/[Chorus]/[Post‑Chorus]/[Bridge]/[Instrumental]/[Solo]/[Outro]；人声控制标记以‑连接（如[Chorus - powerful belting]、[Verse - whispered]、[Bridge - spoken word]、[harmonies]）；能量情绪标记[high energy]/[low energy]/[building energy]/[explosive]/[melancholic]/[dreamy]；标签修饰用‑连接且不堆叠（每段最多2个）；标签内禁止写入歌词文本，歌词置于标签外。
6. 歌词文本规则：每行6‑10音节最佳，同位置行音节数接近（±1‑2）；大写=强呐喊；括号=背景和声；段落间空行分隔；全曲维持同一核心隐喻意象；规避AI味歌词（不堆砌空洞形容词、押韵模式统一、段落边界清晰、行长度适合演唱保留呼吸）；中文以行尾换行与空行形成自然换气点。
7. 元数据参数规则（Ace‑Step1.5）：bpm（慢歌60‑80/中速90‑120/快歌130‑180，极端值不稳定）、调性keyscale（冷门调易失效）、拍号timesignature（4/4最稳，3/4华尔兹，6/8摇摆）、时长duration（30‑240s最佳，超长结构易崩坏）独立输出；元数据是引导不是绝对指令；禁止写入Caption；MiniMax‑Music3元数据写入Global Metadata，BPM/调性可给范围或定性描述，歌词标签指令优先于全局描述。
8. 参数约束：人声音域、旋律走向、最大音程跨度；和声配置；乐器入场时机+量化音量占比；段落间转场；节拍细分类型适配曲风；混音混响强度、干湿比全部量化。
9. 校验约束：三重校验：✅Caption‑Lyrics一致性（无冲突）✅结构标记正确性（方括号标记规范、标签不堆叠）✅音节节奏合理性（每行6‑10音节、同位置行音节接近）；MiniMax‑Music3额外校验：✅input与instructions字段完整性（歌词+结构化标题三部分齐全）。
解析来源：用户歌曲创作需求 #SONG_CREATE_SOURCE#；可选辅助关键词：#USER_KEYWORDS#（为空=无用户关键词）；目标模型：#DOWNSTREAM_MODEL#
""",
                    "en": """
【Universal AI Song Creation Preset Rules (ACE‑Step 1.5 / MiniMax‑Music3 Dual‑Model Adapted)】
1. General baseline: primary source #SONG_CREATE_SOURCE#, optional assist keywords #USER_KEYWORDS#, target model #DOWNSTREAM_MODEL#. Auto‑detect language to switch Asian / Western workflow. Switch output spec by target model: Ace‑Step1.5 outputs 【Caption + Lyrics + Metadata Params】 three parts; MiniMax‑Music3 outputs 【input lyrics + instructions music description (structured caption)】 two fields. Natural: output matching format, strictly follow template definition.
2. Priority hard‑rule: user creation requirement > optional user keywords. Keywords only calibrate genre, vocal, emotion, mixing style. Discard conflicting keywords, never alter user core theme & emotion. Auto assign genre‑language if no keywords.
3. Caption writing rules (Ace‑Step1.5): describe only global style/emotion/instruments/timbre/era/vocal/production. Multi‑dimension, specific over vague, use style reference phrases. NEVER write lyrics. NEVER write bpm/key/time signature. Avoid conflicting vocab; turn conflicts into time‑sequence evolution description. Caption and Lyrics must NOT conflict.
4. MiniMax‑Music3 structured caption rules: instructions output three parts in order: Global Metadata (genre & subgenre, BPM, key & scale, emotional progression, application scenarios & imagery, sonics & production profile) → Vocal Details (vocal gender & timbre, vocal style, harmony/backing vocals, vocal FX) → Arrangement (instrument lifecycle primary/secondary layering, groove & foundation progression, embellishments textures & spatial FX); describe section by section (Intro→Verse→Chorus→…); specific over abstract; instrumental tracks declare pure music & specify leading instrument; tag instructions inside lyrics override global description.
5. Lyrics structure marker rules: Ace‑Step1.5 base [Intro]/[Verse 1]/[Pre‑Chorus]/[Chorus]/[Bridge]/[Outro] + dynamic [Build]/[Drop]/[Breakdown] + instrumental [Instrumental]/[Guitar Solo]/[Piano Interlude] + special [Fade Out]/[Silence]; MiniMax‑Music3 tags [Intro]/[Verse]/[Pre‑Chorus]/[Chorus]/[Post‑Chorus]/[Bridge]/[Instrumental]/[Solo]/[Outro]. Vocal‑control markers joined with `‑` (e.g. [Chorus - powerful belting], [Verse - whispered], [Bridge - spoken word], [harmonies]); energy‑emotion markers [high energy]/[low energy]/[building energy]/[explosive]/[melancholic]/[dreamy]; connect tag‑modifier with `‑`, no stacking (max 2 per section); NEVER write lyric text inside tags, keep lyrics outside tags.
6. Lyric text rules: 6‑10 syllables per line preferred, corresponding lines stay close (±1‑2); uppercase = shouting; parentheses = backing harmony; blank line between sections; keep ONE core metaphor imagery; avoid AI‑flavor lyrics(no empty adjectives piling, consistent rhyme scheme, clear section boundaries, breathable line length).
7. Metadata param rules (Ace‑Step1.5): bpm(30‑300; slow 60‑80 / mid 90‑120 / fast 130‑180; extreme values unstable), keyscale(cold keys unstable), timesignature(4/4 most stable; 3/4 waltz; 6/8 swing), duration(30‑240s best; overlong structures collapse) output independently; metadata is guidance not absolute command; NEVER write into Caption. MiniMax‑Music3 writes metadata into Global Metadata; BPM/key may use range or qualitative description; tag instructions override global description.
8. Parameter constraint: vocal range, melody trend, max interval span; harmony setup; instrument entry + quantized volume percentage; section transition; beat‑subdivision match genre; quantized reverb‑strength & dry‑wet ratio.
9. Validation constraint: triple‑check: ✅ Caption‑Lyrics consistency(no conflict) ✅ structure marker correctness(square‑bracket markers, no tag stacking) ✅ syllable‑rhythm rationality(6‑10 syllables per line, corresponding lines close); MiniMax‑Music3 extra check: ✅ input & instructions field completeness(lyrics + structured caption three parts).
Analysis source: user song‑creation requirement #SONG_CREATE_SOURCE#; optional assist keywords: #USER_KEYWORDS#(empty = no user keywords); target model: #DOWNSTREAM_MODEL#
"""
                },
                "negative_base": {
                    "zh": "歌词段落缺失方括号结构标记，标签堆叠过多修饰词，Caption与Lyrics内容冲突，BPM/调性/拍号写入Caption，歌词行音节失衡或超长，AI味空洞形容词堆砌，押韵模式混乱，段落边界模糊，多重隐喻意象跳脱，权重符号，MiniMax‑Music3字段缺失（缺input或instructions三部分不完整），标签内误写歌词文本",
                    "en": "Missing square-bracket structure markers, stacked tag modifiers, Caption-Lyrics conflict, BPM/key/time-signature inside Caption, unbalanced or overlong lyric line syllables, AI-flavor empty adjectives, chaotic rhyme scheme, blurred section boundaries, jumping multiple metaphor imageries, weight syntax, incomplete MiniMax-Music3 fields (missing input or incomplete instructions three parts), lyric text mistakenly written inside tags"
                }
            }
        }

        # 双模型输出格式指引（按下游音乐模型区分，仅支持natural输出）
        self.format_guide = {
            "Ace-Step1.5": {
                "natural": {
                    "zh": """【Ace‑Step1.5 自然段落模式】
严格按三部分输出：
一、【Caption · 整体画像】（1‑3句多维组合描述，不含歌词与元数据）
- 组合维度：风格/流派 + 情绪氛围 + 乐器 + 音色质感 + 时代参考 + 制作风格 + 人声特点
- 具体优于模糊（如：female vocal, piano ballad, emotional, intimate atmosphere, strings, building to powerful chorus）
- 善用风格参考句式（如 in the style of 80s synthwave）；冲突风格改为时序演变描述；禁止写BPM/调性/拍号
二、【Lyrics · 时间脚本】（方括号结构标记 + 歌词文本）
- 基础结构标记：[Intro]、[Verse 1]、[Pre‑Chorus]、[Chorus]、[Bridge]、[Outro]；说唱/Trap补充[Rap Verse]；古风/电子补充专属段落
- 动态段落标记：[Build]、[Drop]、[Breakdown]
- 器乐段落标记：[Instrumental]、[Guitar Solo]、[Piano Interlude]
- 特殊标记：[Fade Out]、[Silence]
- 人声控制标记以‑连接到段落标签后：[Chorus - powerful belting]、[Verse - whispered]、[Bridge - spoken word]、[harmonies]、[raspy vocal]、[falsetto]（每段最多2个修饰，不堆叠）
- 能量情绪标记：[high energy]、[low energy]、[building energy]、[explosive]、[melancholic]、[dreamy]
- 歌词文本：每行6‑10音节最佳，同位置行音节数接近（±1‑2）；大写=强呐喊；括号=背景和声；段落间空行分隔；全曲同一核心隐喻意象
三、【元数据参数】（独立于Caption，供Ace‑Step1.5参数面板填写）
- bpm：XX（慢歌60‑80 / 中速90‑120 / 快歌130‑180）；keyscale：调性；timesignature：拍号（4/4最稳）；duration：全曲时长（30‑240s最佳）
文末统一附上和声配置、分层配器配比、段落转场、混音参数、三重校验确认；存在合规用户关键词时将曲风/人声/情绪校准自然融入，冲突关键词直接舍弃。""",
                    "en": """[Ace‑Step1.5 Natural Mode]
Output strictly in three parts:
1.【Caption】(1‑3 multi-dimension descriptive sentences, NO lyrics & NO metadata)
- Dimensions: genre/style + emotion/atmosphere + instruments + timbre texture + era reference + production style + vocal characteristics
- Specific over vague (e.g. female vocal, piano ballad, emotional, intimate atmosphere, strings, building to powerful chorus)
- Use style reference phrases (e.g. in the style of 80s synthwave); turn conflicting styles into time-sequence evolution; NEVER write BPM/key/time-signature
2.【Lyrics】(square-bracket structure markers + lyric text)
- Base markers: [Intro], [Verse 1], [Pre‑Chorus], [Chorus], [Bridge], [Outro]; Rap/Trap add [Rap Verse]
- Dynamic markers: [Build], [Drop], [Breakdown]
- Instrumental markers: [Instrumental], [Guitar Solo], [Piano Interlude]
- Special markers: [Fade Out], [Silence]
- Vocal-control markers joined with `‑` after section labels: [Chorus - powerful belting], [Verse - whispered], [Bridge - spoken word], [harmonies], [raspy vocal], [falsetto] (max 2 modifiers per section, no stacking)
- Energy-emotion markers: [high energy], [low energy], [building energy], [explosive], [melancholic], [dreamy]
- Lyric text: 6‑10 syllables per line preferred, corresponding lines close (±1‑2); uppercase = shouting; parentheses = backing harmony; blank line between sections; one core metaphor across the whole song
3.【Metadata Params】(independent from Caption, for Ace‑Step1.5 parameter panel)
- bpm: XX (slow 60‑80 / mid 90‑120 / fast 130‑180); keyscale; timesignature (4/4 most stable); duration (30‑240s best)
Append harmony setup, layered instrument volume ratio, section transition, mixing params, triple-check result at bottom. Merge valid genre-vocal-emotion calibration from user-keywords; discard conflicting keywords."""
                }
            },
            "MiniMax-Music3": {
                "natural": {
                    "zh": """【MiniMax‑Music3 自然模式】
严格按两字段输出：
一、【input · 歌词】
- 歌词文本 + 方括号段落标签：[Intro]、[Verse]、[Pre‑Chorus]、[Chorus]、[Post‑Chorus]、[Bridge]、[Instrumental]、[Solo]、[Outro] 定义歌曲结构与局部编曲
- 标签可附音乐指令（如 [Chorus] (Full band, energetic, powerful vocals)），标签内指令优先于全局描述；标签中禁止写入歌词，歌词文本置于标签外
- 无标签时模型根据音乐描述自动生成合理结构；歌词每行6‑10音节、同位置行音节接近、大写强呐喊、括号背景和声、空行分段、全曲单一核心隐喻意象
二、【instructions · 音乐描述】（结构化标题三部分顺序输出）
Global Metadata（全局元数据）：
- Basic Attributes（流派与子流派/BPM/调性音阶）→ Global Emotional Progression（全局情感进程）→ Application Scenarios & Imagery（应用场景与意象）→ Sonics & Production Profile（音响与制作配置）
Vocal Details（人声细节）：
- Vocal Gender & Timbre（人声性别与音色）→ Vocal Style（演唱风格）→ Harmony/Backing Vocals（和声/背景人声）→ Vocal FX（人声效果）；纯器乐曲声明纯音乐并说明主导乐器
Arrangement（编曲）：
- Instrument Lifecycle（乐器生命周期，主次分层）→ Groove & Foundation Progression（律动与基础进行）→ Embellishments, Textures & Spatial FX（装饰纹理与空间效果）；按Intro→Verse→Chorus→…段落顺序描述，具体胜于抽象，乐器出入变化连贯
文末可明确排除不想要的元素（如"纯器乐不要人声"、"不要电子鼓"）；避免过度指定细节，聚焦风格/情感/配器/结构；存在合规用户关键词时将曲风/人声/情绪校准自然融入，冲突关键词直接舍弃。""",
                    "en": """[MiniMax‑Music3 Natural Mode]
Output strictly in two fields:
1.【input · Lyrics】
- Lyric text + square-bracket section tags: [Intro], [Verse], [Pre‑Chorus], [Chorus], [Post‑Chorus], [Bridge], [Instrumental], [Solo], [Outro] define song structure & local arrangement
- Tags may carry music instructions (e.g. [Chorus] (Full band, energetic, powerful vocals)); tag instructions override global description; NEVER write lyrics inside tags, put lyric text outside tags
- If no tags, the model auto-generates a reasonable structure from the description; lyric text 6‑10 syllables per line, corresponding lines close, uppercase = shouting, parentheses = backing harmony, blank line between sections, one core metaphor across the whole song
2.【instructions · Music Description】(structured caption in three parts, output in order)
Global Metadata:
- Basic Attributes (genre & subgenre/BPM/key & scale) → Global Emotional Progression → Application Scenarios & Imagery → Sonics & Production Profile
Vocal Details:
- Vocal Gender & Timbre → Vocal Style → Harmony/Backing Vocals → Vocal FX; instrumental tracks declare pure music & specify leading instrument
Arrangement:
- Instrument Lifecycle (primary/secondary layering) → Groove & Foundation Progression → Embellishments, Textures & Spatial FX; describe section by section (Intro→Verse→Chorus→…), specific over abstract, coherent instrument entries/changes/withdrawals
You may explicitly exclude unwanted elements at the end (e.g. 'instrumental, no vocals', 'no electronic drums'); avoid over-specification, focus on style/emotion/instrumentation/structure. Merge valid genre-vocal-emotion calibration from user-keywords; discard conflicting keywords."""
                }
            }
        }

    def detect_language(self, text: str) -> str:
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        return "zh" if chinese_chars >= english_words else "en"

    def build_prompt(
            self,
            user_input,
            preset_name,
            downstream_model,
            output_language: str = "auto",
            enable_global_preconstraint: bool = True,
            enable_negative_prompt: bool = True,
            output_format: str = "both"
    ) -> Dict:
        valid_preset_names = ["song_creation"]
        if preset_name not in valid_preset_names:
            raise ValueError(f"预设模板不存在：{preset_name}")
        if downstream_model not in self.model_formula_library:
            raise ValueError(f"不支持的下游音乐模型：{downstream_model}")
        preset = self.preset_library[preset_name]
        model_config = self.model_formula_library[downstream_model]

        detect_input = user_input if user_input else ""
        if output_language == "auto":
            lang = self.detect_language(detect_input)
        else:
            lang = output_language if output_language in ["zh", "en"] else "zh"

        global_rule = self.global_base_rules[lang] if enable_global_preconstraint else ""
        preset_rule = preset["preset_rules"][lang]
        pos_constraint = preset["positive_constraints"][lang]
        formula_hint = model_config[f"formula_{lang}"]
        natural_guide = self.format_guide[downstream_model]["natural"][lang]

        prompt_parts = []
        if enable_global_preconstraint:
            prompt_parts.append(f"【Hard Precondition Baseline】\n{pos_constraint}")
            prompt_parts.append(global_rule)
        prompt_parts.append(f"下游音乐模型内容组织公式（{downstream_model}）：{formula_hint}")
        prompt_parts.append(preset_rule)
        prompt_parts.append(f"用户创作需求：#SONG_CREATE_SOURCE#；用户辅助关键词：{detect_input if detect_input else '无'}；目标模型：{downstream_model}；关键词仅用于曲风、人声、情绪、混音校准，用户创作需求优先级最高，冲突则舍弃关键词。")

        # 仅支持natural输出格式，任何 output_format 一律输出目标模型的natural指引
        prompt_parts.append(natural_guide)

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
