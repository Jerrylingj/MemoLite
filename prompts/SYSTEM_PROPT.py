EXTRACTION_PROMPT = """
分析以下用户输入，提取值得长期记住的信息。

用户输入: {user_input}

请按以下格式返回 JSON（如果没有值得记住的信息，返回空数组）:
[
  {{
    "content": "具体的记忆内容",
    "memory_type": "USER_PROFILE|PREFERENCES|FACTS|BEHAVIORAL_PATTERNS|TASK_CONTEXT|LEARNED_KNOWLEDGE",
    "importance": 0.8,
    "confidence": 0.9,
    "temporal_validity": "2024-12-31T23:59:59" 或 null,
    "metadata": {{
      "key": "value"
    }} 或 null
  }}
]

记忆类型说明:
- USER_PROFILE: 用户身份、职业、背景信息（通常无有效期）
- PREFERENCES: 用户偏好、习惯、风格（通常无有效期）
- FACTS: 具体事实、数据、时间（可能有有效期）
- BEHAVIORAL_PATTERNS: 用户的行为模式、习惯（通常无有效期）
- TASK_CONTEXT: 当前任务、项目状态（通常有有效期，任务完成后过期）
- LEARNED_KNOWLEDGE: 从对话中学到的知识（通常无有效期）

有效期规则:
- 如果记忆涉及具体时间（如"下周一"、"3个月后"、"明年春节"），计算绝对时间戳
- 如果记忆是临时任务状态，设置合理的过期时间（如7天后）
- 如果记忆是永久性的（身份、偏好等），设为 null
- 时间格式: ISO 8601 (YYYY-MM-DDTHH:MM:SS)

元数据规则:
- 提取记忆中的关键结构化信息
- 例如：
  * 时间相关：{{"date": "2024-12-25", "time": "14:30", "duration": "2 hours"}}
  * 人物相关：{{"person_name": "张三", "relationship": "同事"}}
  * 项目相关：{{"project_name": "Q4报告", "status": "进行中", "deadline": "2024-12-31"}}
  * 地点相关：{{"location": "北京", "building": "A座"}}
- 如果没有结构化信息可提取，设为 null

示例:
输入: "我下周一下午3点要和李明开会讨论Q4财报"
输出:
[
  {{
    "content": "下周一下午3点要和李明开会讨论Q4财报",
    "memory_type": "TASK_CONTEXT",
    "importance": 0.9,
    "confidence": 0.95,
    "temporal_validity": "2024-12-23T15:00:00",
    "metadata": {{
      "person": "李明",
      "time": "15:00",
      "date": "Monday",
      "topic": "Q4财报",
      "type": "meeting"
    }}
  }}
]

输入: "我是一个Python开发者，喜欢用FastAPI"
输出:
[
  {{
    "content": "用户是Python开发者",
    "memory_type": "USER_PROFILE",
    "importance": 0.9,
    "confidence": 0.95,
    "temporal_validity": null,
    "metadata": {{
      "skill": "Python",
      "level": "developer"
    }}
  }},
  {{
    "content": "用户喜欢用FastAPI框架",
    "memory_type": "PREFERENCES",
    "importance": 0.8,
    "confidence": 0.9,
    "temporal_validity": null,
    "metadata": {{
      "framework": "FastAPI",
      "category": "backend"
    }}
  }}
]

只返回 JSON，不要其他文字。
"""
