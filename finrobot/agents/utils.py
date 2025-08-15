import re
from .prompts import order_template


def instruction_trigger(sender):
    # 檢查最後一則訊息是否包含指令文字檔案的路徑
    return "instruction & resources saved to" in sender.last_message()["content"]


def instruction_message(recipient, messages, sender, config):
    # 從最後一則訊息中提取指令文字檔案的路徑
    full_order = recipient.chat_messages_for_summary(sender)[-1]["content"]
    txt_path = full_order.replace("instruction & resources saved to ", "").strip()
    with open(txt_path, "r") as f:
        instruction = f.read() + "\n\n在您的回覆結尾處回覆 TERMINATE。"
    return instruction


def order_trigger(sender, name, pattern):
    # print(pattern)
    # print(sender.name)
    return sender.name == name and pattern in sender.last_message()["content"]


def order_message(pattern, recipient, messages, sender, config):
    full_order = recipient.chat_messages_for_summary(sender)[-1]["content"]
    pattern = rf"[{pattern}](?::)?\s*(.+?)(?=\n[|$)"
    match = re.search(pattern, full_order, re.DOTALL)
    if match:
        order = match.group(1).strip()
    else:
        order = full_order
    return order_template.format(order=order)