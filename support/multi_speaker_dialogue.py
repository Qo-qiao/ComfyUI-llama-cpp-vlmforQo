# -*- coding: utf-8 -*-
"""
TTS多人对话生成器与情感合成指导

Author: 亲卿于情 (@Qo‑qiao)
GitHub: https://github.com/Qo‑qiao
License: See LICENSE file for details
"""
import re
from typing import Dict, Optional

MULTI_SPEAKER_DIALOGUE = {
    "template_id": "multi_speaker_dialogue",
    "name": "多人对话生成器",
    "description": "作为专业的TTS音频合成指导专家和剧本内容创作者，优先基于输入原始剧本文本完成解析；同时可接收用户可选关键词，用来校准音色、情绪、声场风格信息，修正输出结果。智能分析对话结构、说话人数量、对话交互关系，为每句台词分配唯一说话人ID、细分音色基底、交互距离、空间声场参数，同步标注台词情感、四要素语气、可直接调用的量化TTS声学参数、重读关键词、情绪过渡逻辑、交叠对话标记、音轨分层配比，支持绑定视频时间码实现音画同步。专业知识涵盖角色音色差异化细分、多角色情绪平滑过渡控制、交叠插话人声处理、空间混响声学设计、台词重音逻辑、四要素组合法（发声方式+节奏+音调+标点），以及多人连续对话的情感连贯性优化，确保合成语音区分每个角色独特音色、情绪起伏自然、多人声场统一流畅。",
}

class MultiSpeakerDialogue:
    def __init__(self):
        # 全局底层TTS多人对话通用规则
        self.global_base_rules = {
            "zh": """
你是专业TTS多人对话解析扩写专家
主要解析来源为原始剧本对话文本#DIALOGUE_SOURCE#；支持接收**可选用户关键词**用于辅助校准音色、情绪、声场风格；原始剧本文本信息优先级最高，用户关键词仅做补充校准，关键词与剧本内容冲突时，以原始剧本为准。
支持单人独白、双人对话、多人群聊、插话交叠同步对话各类交互场景；内置完整音色类型参考与【情感↔四要素组合映射表】。
坚守多人对话TTS解析基础约束：每个说话人分配全局唯一数字ID，不可重复遗漏；同一角色多轮对话音色基底、声场参数保持一致；不同角色音色、语气、声场具备明显区分度；标注对话交互距离；空间声学参数全部量化输出；逐句判定情感与情绪过渡逻辑；交叠对话标记起止区间；**台词原文保持不变，仅通过音色、声学、情绪参数传递情感，禁止修改原始剧本文字**；严格使用四要素组合法生成台词语气。
natural模式每条对话条目标准化markdown字段输出；structured模式完整输出结构化对话条目，字段严格匹配模板定义。
完整保留剧本全部对话文本，只增加语音合成维度参数标注；时间码严格遵循SRT格式；音色、情绪、声学参数每条对话具备唯一性，避免模板化重复。
输出禁忌：禁止修改原始剧本台词文本；禁止说话人ID重复/缺失；禁止权重符号。
支持natural与structured双输出格式，不添加额外注释、说明、解释。
""",
            "en": """
You are professional multi‑speaker‑dialogue TTS analysis expert. This preset is 【Multi‑Speaker Dialogue Generator & Emotional Synthesis Guide】.
Primary analysis source is raw script dialogue #DIALOGUE_SOURCE#. Optional user keywords are accepted only for calibrating timbre, emotion and acoustic‑field style. Original script content has highest priority. If keywords conflict with script content, original script shall prevail.
Support monologue, two‑person dialogue, group chat, interrupt / overlapping simultaneous‑dialogue scenarios. Built‑in full timbre reference table and 【Emotion ↔ Four‑Element Mapping Table】.
Baseline rule: assign global unique numeric speaker‑ID for each character, no duplicate or missing. Keep consistent timbre‑base & acoustic‑field params for same‑character multi‑turn utterances. Obvious distinction on timbre, tone and acoustic‑field between different speakers. Mark dialogue interaction distance. All spatial‑acoustic params must be quantized. Judge sentence‑wise emotion & emotion‑transition logic. Mark time‑range for overlapping dialogue. **Raw dialogue text shall NOT be modified; convey emotion only via timbre / acoustic / emotion parameters.** Strictly apply four‑element combination rule for speech tone description.
Natural mode output standard markdown fields per‑dialogue entry. Structured mode output structured dialogue entries strictly follow template definition.
Preserve full original script text, only append TTS‑layer annotations. Time‑code follow SRT specification. Timbre, emotion, acoustic params are unique per utterance, avoid template duplication.
Taboo: do NOT alter raw script lines; duplicate / missing speaker‑ID forbidden; no weight syntax.
Support natural / structured output mode, no extra comments or explanations.
"""
        }

        # 唯一主预设模板，绑定universal_multi_speaker_dialogue template_id
        self.preset_library = {
            "multi_speaker_dialogue": {
                "template_id": "multi_speaker_dialogue",
                "display_name": "TTS多人对话生成器与情感合成指导",
                "description": "作为专业的TTS音频合成指导专家和剧本内容创作者，优先基于输入原始剧本文本完成解析；同时可接收用户可选关键词，用来校准音色、情绪、声场风格信息，修正输出结果。智能分析对话结构、说话人数量、对话交互关系，为每句台词分配唯一说话人ID、细分音色基底、交互距离、空间声场参数，同步标注台词情感、四要素语气、可直接调用的量化TTS声学参数、重读关键词、情绪过渡逻辑、交叠对话标记、音轨分层配比，支持绑定视频时间码实现音画同步。专业知识涵盖角色音色差异化细分、多角色情绪平滑过渡控制、交叠插话人声处理、空间混响声学设计、台词重音逻辑、四要素组合法（发声方式+节奏+音调+标点），以及多人连续对话的情感连贯性优化，确保合成语音区分每个角色独特音色、情绪起伏自然、多人声场统一流畅。",
                "positive_constraints": {
                    "zh": "完全基于原始剧本对话文本解析；每个说话人分配全局唯一数字ID；同一角色多轮对话音色基底、声场参数保持一致；不同角色音色语气声场具备明显区分度；标注对话交互距离；空间声学参数量化输出；逐句判定情感与情绪过渡逻辑；交叠对话标记起止区间；严格执行四要素组合法；全套量化TTS声学参数、音轨分层配比完整输出；重读关键词取自对应台词；台词原文文字不做任何修改；可选用户关键词仅用于辅助校准音色、情绪、声场风格；关键词与剧本冲突时以原始剧本为准；每条对话音色情绪声学参数具备唯一性。",
                    "en": "Analyze completely based on raw script dialogue. Assign globally unique numeric speaker‑ID per character. Keep timbre‑base and acoustic‑field parameters consistent for multi‑turn lines of same speaker. Obvious distinction of timbre / tone / acoustic‑field between different roles. Mark dialogue interaction distance. Quantize all spatial‑acoustic parameters. Judge per‑utterance emotion and emotion‑transition logic. Mark time‑range for overlapping dialogue. Strictly apply four‑element combination rule. Output full quantized TTS acoustic params and multi‑track volume ratio. Stress keywords extracted from corresponding lines. Raw dialogue text must not be modified. Optional user‑keywords only assist calibrating timbre, emotion, acoustic‑field style. When conflict occurs, original script takes precedence. Timbre‑emotion‑acoustic parameters are unique for each dialogue entry."
                },
                "preset_rules": {
                    "zh": """
【TTS多人对话专属规则】
1. 通用基线：主解析来源#DIALOGUE_SOURCE#，可选用户关键词#USER_KEYWORDS#；执行完整12步对话解析流程；分配全局唯一说话人ID；区分单人/双人/多人/交叠插话；配置音色大类+细分声线基底；标注交互距离；输出量化空间声学参数；逐句情感+情绪过渡；四要素组合法生成语气；全套TTS量化参数；标记交叠对话区间；音轨分层配比；可选SRT时间码；natural模式markdown字段输出；structured模式结构化条目输出。
2. 优先级铁则：原始剧本对话文本 > 用户可选关键词。关键词仅做音色、情绪、声场风格的辅助校准；若关键词描述与剧本冲突，直接舍弃冲突关键词，严格遵从原始剧本，绝不篡改台词原文。无关键词则完全依靠剧本文本解析。
3. 角色分支规则：内置音色类型参考表，区分女声/男声/萝莉音/正太音/御姐音/大叔音/老年音，每个角色配置一级音色大类+细分声线基底，实现同大类音色差异化区分。
4. 内容约束：台词原文禁止修改；同一角色多轮对话音色声场保持一致；不同角色具备区分度；交叠对话必须标记起止区间；参考【情感↔四要素组合映射表】生成台词语气；重读关键词必须取自对应台词文本，禁止编造。
5. 参数约束：TTS量化参数（语速倍率、音高偏移、人声dB、句内停顿秒数、句尾停顿秒数）；空间声学（空间类型、混响强度、回音时长）；音轨分层配比（人声、BGM、环境噪音）全部输出量化数值；适配视频场景输出SRT标准时间码。
6. 映射规则：严格使用【情感↔四要素组合映射表】，发声方式、节奏、音调、标点协同配套，台词语气描述与TTS量化参数互相匹配。
解析来源：原始剧本对话文本 #DIALOGUE_SOURCE#；可选辅助关键词：#USER_KEYWORDS#（为空=无用户关键词）
""",
                    "en": """
【Multi‑Speaker‑Dialogue TTS Preset Rules】
1. General baseline: primary source #DIALOGUE_SOURCE#, optional assist keywords #USER_KEYWORDS#; follow full 12‑step dialogue analysis workflow. Assign globally unique speaker‑ID. Distinguish monologue / two‑party / group / overlapping‑interruption. Configure timbre category + fine‑grained voice base. Mark interaction distance. Output quantized spatial‑acoustic params. Per‑utterance emotion & emotion‑transition. Generate tone description via four‑element rule. Full‑set quantized TTS params. Mark overlapping‑dialogue time‑range. Multi‑track volume ratio. Optional SRT time‑code. Natural mode use markdown fields. Structured mode output structured entries.
2. Priority hard‑rule: raw‑script‑dialogue > optional user keywords. Keywords only assist calibrating timbre, emotion, acoustic‑field style. If keywords conflict with script content, discard conflicting keywords and strictly follow original script, never alter dialogue text. If no keywords provided, rely entirely on script analysis.
3. Character branch rule: built‑in timbre reference table; distinguish female / male / loli / shota / regal‑lady / middle‑aged‑male / elder voice. Each role gets top‑level timbre category plus fine‑grained voice base to differentiate voices within same category.
4. Content constraint: raw dialogue must NOT be modified. Keep timbre‑acoustic consistency for multi‑turn same‑speaker lines. Ensure distinguishability between different roles. Mark time‑range for overlapping dialogue. Generate speech tone referring to 【Emotion ↔ Four‑Element Mapping Table】. Stress keywords must come from corresponding dialogue, do NOT fabricate.
5. Parameter constraint: output numeric values for TTS(speed‑ratio, pitch‑offset, vocal‑dB, intra‑sentence‑pause‑s, sentence‑end‑pause‑s), spatial‑acoustic(space‑type, reverb‑strength, echo‑duration‑s), multi‑track volume(human‑voice / BGM / ambient‑noise). Output SRT‑format time‑code for video‑adapted scenario.
6. Mapping rule: strictly follow 【Emotion ↔ Four‑Element Mapping Table】. Vocal‑mode, rhythm, intonation and punctuation cooperate mutually; tone description shall match quantized TTS parameters.
Analysis source: raw script dialogue #DIALOGUE_SOURCE#; optional assist keywords: #USER_KEYWORDS#(empty = no user keywords)
"""
                }
            }
        }

        # 双输出格式指引
        self.format_guide = {
            "natural": {
                "zh": "【自然字段模式】每条对话独立，使用markdown换行字段；依次输出：时间码(SRT格式)、音色大类、细分声线基底、说话人ID、对话交互距离、空间声学环境、情感、情绪过渡说明、台词语气（四要素组合）、TTS量化参数、台词重读关键词、交叠对话标记、音轨音量配比、对话原文；每条对话之间空行分隔；存在合规用户关键词时将音色/情绪/声学校准信息自然融入，冲突关键词直接舍弃；禁止修改原始剧本台词，全部参数为可映射TTS引擎的量化数值，无多余解释文本。",
                "en": "[Natural Field Mode] Separate per‑dialogue entry with markdown line breaks. Output sequence: SRT time‑code, timbre category, fine‑grained voice base, speaker‑ID, dialogue interaction distance, spatial‑acoustic environment, emotion, emotion‑transition note, speech‑tone(four‑element rule), quant‑TTS params, stress keywords, overlapping‑dialogue mark, multi‑track volume ratio, raw dialogue text. Blank line between entries. Merge valid timbre‑emotion‑acoustic calibration from user‑keywords; discard conflicting keywords. Never edit raw script lines. All params are TTS‑engine‑mappable numeric values, no extra explanatory text."
            },
            "structured": {
                "zh": """【结构化模式】
【用户关键词适配】（无关键词填写：无）
  - 有效校准信息：提取用户关键词中与剧本不冲突的音色、情绪、声场风格信息
  - 冲突舍弃项：关键词与源剧本冲突部分直接舍弃，不纳入输出
【对话1】
  - 时间码：SRT格式时间码
  - 音色大类：女声/男声/萝莉音/正太音/御姐音/大叔音/老年音
  - 细分声线基底：对应细分声线描述
  - 说话人ID：全局唯一数字ID
  - 角色关系：角色之间关系说明
  - 对话交互距离：近距离耳语/面对面交谈/远距离喊话
  - 空间声学环境：空间类型，混响强度，回音时长s
  - 情感：单句基础情感
  - 情绪过渡说明：前后句情绪过渡变化逻辑
  - 台词语气：发声方式，节奏+音调（四要素组合法）
  - TTS量化参数：语速倍率，音高偏移，人声音量dB，句内停顿s，句尾停顿s
  - 台词重读关键词：取自对应台词文本
  - 交叠对话标记：无交叠 / 标记交叠起止区间
  - 音轨音量配比：人声百分比，背景音乐百分比，环境噪音百分比
  - 对话：完整原始剧本台词，不修改文字
【对话2】……（按需增加对话条目）""",
                "en": """[Structured Mode]
【User Keyword Adaptation】(fill "None" if no keywords)
  - Valid Calibration Info: extract non‑conflicting timbre / emotion / acoustic‑style info from user keywords
  - Discarded Conflicts: parts conflicting with source‑script shall be discarded, not included in output
【Dialogue 1】
  - Time‑Code: SRT‑format timestamp
  - Timbre Category: female‑voice / male‑voice / loli‑voice / shota‑voice / regal‑lady‑voice / middle‑aged‑male‑voice / elder‑voice
  - Fine‑Grained Voice Base: detailed voice‑base description
  - Speaker‑ID: globally unique numeric ID
  - Character‑Relation: relationship between characters
  - Dialogue Interaction Distance: close‑whisper / face‑to‑face‑talk / long‑distance shout
  - Spatial Acoustic Env: space type, reverb‑strength, echo‑duration s
  - Emotion: base emotion of this utterance
  - Emotion‑Transition Note: emotion change logic between adjacent lines
  - Speech Tone‑Mode: vocal‑mode, rhythm + intonation (four‑element combination rule)
  - TTS Quant‑Params: speed‑ratio, pitch‑offset, vocal‑volume dB, intra‑sentence‑pause s, sentence‑end‑pause s
  - Stress Keywords: extracted from corresponding dialogue line
  - Overlap‑Dialogue Mark: no‑overlap / mark overlap start‑end time‑range
  - Multi‑Track Volume Ratio: human‑voice %, BGM %, ambient‑noise %
  - Dialogue: complete raw script line, text unmodified
【Dialogue 2】……(add more dialogue entries on demand)"""
            }
        }
    def detect_language(self, text: str) -> str:
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        return "zh" if chinese_chars >= english_words else "en"

    def build_prompt(
            self,
            preset_name: str,
            user_keywords: Optional[str] = None,
            output_language: str = "auto",
            output_format: str = "both"
    ) -> Dict:
        valid_preset_names = ["multi_speaker_dialogue"]
        if preset_name not in valid_preset_names:
            raise ValueError(f"预设模板不存在：{preset_name}")
        preset = self.preset_library[preset_name]

        kw_text = user_keywords if (user_keywords and user_keywords.strip()) else "无"
        detect_input = user_keywords if user_keywords else ""
        if output_language == "auto":
            lang = self.detect_language(detect_input)
        else:
            lang = output_language if output_language in ["zh", "en"] else "zh"

        global_rule = self.global_base_rules[lang]
        preset_rule = preset["preset_rules"][lang]
        pos_constraint = preset["positive_constraints"][lang]
        natural_guide = self.format_guide["natural"][lang]
        structured_guide = self.format_guide["structured"][lang]

        prompt_parts = []
        prompt_parts.append(f"【Hard Precondition Baseline】\n{pos_constraint}")
        prompt_parts.append(global_rule)
        prompt_parts.append(preset_rule)
        prompt_parts.append(f"解析对象：#DIALOGUE_SOURCE#；用户辅助关键词：{kw_text}；关键词仅用于音色情绪声场风格校准，原始剧本信息优先级最高，冲突则舍弃关键词。")

        if output_format == "natural":
            prompt_parts.append(natural_guide)
        elif output_format == "structured":
            prompt_parts.append(structured_guide)
        else:
            prompt_parts.append(natural_guide)
            prompt_parts.append(structured_guide)

        final_llm_prompt = "\n".join(prompt_parts)

        return {
            "status": "success",
            "llm_input_prompt": final_llm_prompt,
            "positive_constraint": pos_constraint,
            "output_language": lang,
            "preset_name": preset_name,
            "preset_display_name": preset["display_name"],
            "user_keywords": user_keywords
        }