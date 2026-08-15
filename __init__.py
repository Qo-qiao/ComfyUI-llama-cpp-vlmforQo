# -*- coding: utf-8 -*-
"""
ComfyUI-omni-llm 节点包

Author: 亲卿于情 (@Qo-qiao)
GitHub: https://github.com/Qo-qiao
License: See LICENSE file for details
"""

import sys
import os

plugin_dir = os.path.dirname(os.path.abspath(__file__))

# 添加项目根目录和nodes目录到路径
sys.path.insert(0, plugin_dir)
nodes_dir = os.path.join(plugin_dir, "nodes")
sys.path.insert(0, nodes_dir)

# 添加插件自带的site-packages目录到路径（优先使用插件自带的依赖，避免版本冲突）
site_packages_dir = os.path.join(plugin_dir, "site-packages")
if os.path.exists(site_packages_dir):
    sys.path.insert(0, site_packages_dir)

# 导入所有节点模块（模块名对应nodes目录下的实际文件名）
from model_loader import omni_llm_model_loader
from unified_inference import omni_llm_unified_inference
from model_parameters import omni_llm_parameters
from clean_states import omni_llm_clean_states
from asr_loader import omni_llm_asr_loader
from multi_image_input import omni_llm_multi_image_input
from video_loader import omni_llm_video_loader

# 节点映射关系，Comfy通过这个字典识别节点
NODE_CLASS_MAPPINGS = {
    "omni_llm_model_loader": omni_llm_model_loader,
    "omni_llm_parameters": omni_llm_parameters,
    "omni_llm_clean_states": omni_llm_clean_states,
    "omni_llm_asr_loader": omni_llm_asr_loader,
    "omni_llm_multi_image_input": omni_llm_multi_image_input,
    "omni_llm_unified_inference": omni_llm_unified_inference,
    "omni_llm_video_loader": omni_llm_video_loader,
}

# 节点显示名称映射，在ComfyUI界面中显示的名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "omni_llm_model_loader": "Omni LLM Model Loader",
    "omni_llm_parameters": "Omni LLM Parameters",
    "omni_llm_clean_states": "Omni LLM Clean States",
    "omni_llm_asr_loader": "Omni LLM ASR Model Loader",
    "omni_llm_multi_image_input": "Omni LLM Multi-Image Input (Story Creation)",
    "omni_llm_unified_inference": "Omni LLM Unified Inference",
    "omni_llm_video_loader": "Omni LLM Video Loader",
}

# 导出所有映射关系
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

# 版本信息
VERSION = "3.3.2"
