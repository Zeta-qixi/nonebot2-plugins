from datetime import datetime

SEASON = [0, '冬', '冬', '春', '春', '春', '夏', '夏', '夏', '秋', '秋', '秋', '冬']

def llm_system_time() -> str:

    now = datetime.now()
    formatted_date = now.strftime("%D %H:%M %A ") + SEASON[now.month]
    return f"[{formatted_date}]" 