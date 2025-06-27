# -*- coding: utf-8 -*-
"""代理模組 - 包含 AI 代理的定義和工作流程"""

from .agent_library import library
from .workflow import (
    FinRobot,
    SingleAssistant,
    SingleAssistantRAG,
    SingleAssistantShadow,
    MultiAssistant,
    MultiAssistantWithLeader,
)
from .prompts import leader_system_message, role_system_message
from .utils import instruction_trigger, instruction_message, order_trigger, order_message

__all__ = [
    "library",
    "FinRobot",
    "SingleAssistant",
    "SingleAssistantRAG",
    "SingleAssistantShadow",
    "MultiAssistant",
    "MultiAssistantWithLeader",
    "leader_system_message",
    "role_system_message",
    "instruction_trigger",
    "instruction_message",
    "order_trigger",
    "order_message",
]

