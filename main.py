import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from lib.make_persona import make_persona
from lib.choice import make_answer


# .env から環境変数読み込み
load_dotenv()

# OpenAI クライアント初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_PERSONA"))

# ペルソナ作成
personas = make_persona(client, n=2)

print(personas)

# 結果表示
# for persona in personas['personas']:
#     print(json.dumps(persona['id'], ensure_ascii=False, indent=2))
nurse = personas[0]

answers = make_answer(client, nurse)

print("== nurse ==")
print(nurse)
print("== answers ==")
print(answers)
