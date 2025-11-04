import json
from openai import OpenAI
from .log import logger

def make_answer(client: OpenAI, nurse):

    SYSTEM_PROMPT = """あなたは医療の現場理解に長けたプロダクトリサーチャーです。
    出力は必ずJSON配列のみ（前後に説明文なし）。各要素はコンパクトに。"""

    USER_PROMPT = """
    discrete choice experimentの回答を作成してください。
    想定するユーザーをいかに示します。
    """  + json.dumps(nurse) + """
    設問は以下の通りです。

    ex1: [
    choiceA: {
      給与: 25万円,
      残業： 多め
      勤務地: 都市部
    },
    choiceB: {
      給与: 35万円,
      残業： なし
      勤務地: 地方中核
}
],
ex2: [
    choiceA: {
      給与: 45万円,
      残業： 多め
      勤務地: 郡部
    },
    choiceB: {
      給与: 25万円,
      残業： なし
      勤務地: 地方中核
    }
}

回答は以下の形式としてください。

answers : [
  {
    "ex1": "choiceA"
  },
  {
    "ex2": "choiceB"
  }
]
    
    """

    logger.info("make_persona: query")
    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # 例: コスト重視。より高性能が必要なら "gpt-5" に変更可
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT},
        ],
        # JSONで強制出力（Chat Completions の response_format）
        response_format={"type": "json_object"},  # ※JSON配列全体を1つのJSONとして返す
        temperature=0.7,
        max_tokens=6000,  # 必要に応じて増減
    )

    logger.info("make_persona: response received\n%s", resp)
    # モデル出力（JSON文字列）をパース
    content = resp.choices[0].message.content

    # もし response_format が "json_object" の都合で { "data": [...] } のように返ってきた場合も考慮
    try:
        personas = json.loads(content)
    except json.JSONDecodeError:
        # 万一JSONで返らなかった場合のフォールバック（整形を試みる or そのまま保存）
        personas = content

    return personas