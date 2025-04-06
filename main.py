# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
openai_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS 설정 (로컬 React 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://localhost:3000"],  # Vite일 경우
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GPT 모델 설정
llm = ChatOpenAI(
    temperature=0.7,
    model_name="gpt-3.5-turbo",  # 필요시 변경
    openai_api_key=openai_api_key # .env로 관리 권장
)

# 요청 모델
class GenerateRequest(BaseModel):
    purpose: str
    input: str
    tone: str
    length: str = "중간"
    emoji: bool = False


prompt_map = {
    "문의": PromptTemplate(
        input_variables=["input", "tone","length","emoji"],
        template="""
너는 공손한 한국어 질문 리라이팅 도우미야.
아래 문장을 더 {tone}에 맞는 "질문"으로 바꿔줘.

- 원문: {input}
- 말투 스타일: {tone}
- 문장 길이: {length}
- 이모지 포함 여부: {emoji}

조건:
- 사용자의 의도(질문)를 유지
- 답변하지 말 것
- 존댓말 사용
- 과장된 표현은 피하고 1~2문장 이내
- {length} 길이로 작성
- {emoji}
"""
    ),
    "요청": PromptTemplate(
        input_variables=["input", "tone","length","emoji"],
        template="""
너는 예의 바른 요청문 작성을 돕는 도우미야.
아래 요청 내용을 더 {tone}에 맞는 요청문으로 표현해줘.

- 원문: {input}
- 말투 스타일: {tone}
- 문장 길이: {length}
- 이모지 포함 여부: {emoji}

조건:
- 부탁/요청의 의미를 유지
- 존댓말 사용, 너무 무겁지 않게
- 2문장 이내
- {length} 길이로 작성
- {emoji}
"""
    ),
    "감사": PromptTemplate(
        input_variables=["input", "tone","length","emoji"],
        template="""
너는 감사 인사를 정중하게 다듬어주는 도우미야.
아래 문장을 보다 {tone}에 맞는 감사 표현으로 리라이팅해줘.

- 원문: {input}
- 말투 스타일: {tone}
- 문장 길이: {length}
- 이모지 포함 여부: {emoji}

조건:
- 진심어린 감사의 뜻이 담기도록 표현
- 너무 과장되거나 부자연스럽지 않게
- 1~2문장 이내
- {length} 길이로 작성
- {emoji}
"""
    ),
    "사과": PromptTemplate(
        input_variables=["input", "tone","length","emoji"],
        template="""
너는 정중한 사과문을 작성해주는 도우미야.
아래 문장을 보다 {tone}에 맞는 사과 문장으로 바꿔줘.

- 원문: {input}
- 말투 스타일: {tone}
- 문장 길이: {length}
- 이모지 포함 여부: {emoji}

조건:
- 사과의 의미를 담되, 지나치게 무겁지 않게
- 자연스러운 일상/업무 커뮤니케이션 수준 유지
- 존댓말 필수
- {length} 길이로 작성
- {emoji}
"""
    ),
    "항의": PromptTemplate(
        input_variables=["input", "tone","length","emoji"],
        template="""
너는 공손하면서도 단호한 항의 표현을 정리해주는 도우미야.
아래 문장을 보다 {tone}에 맞는 항의 문장으로 바꿔줘.

- 원문: {input}
- 말투 스타일: {tone}
- 문장 길이: {length}
- 이모지 포함 여부: {emoji}

조건:
- 예의를 갖추되, 문제 상황은 명확히 전달
- 존댓말 필수
- 불필요한 감정 표현 및 호칭은 자제
- {length} 길이로 작성
- {emoji}
"""
    ),
}




@app.get("/")
async def root():
    return {"message": "MainPage"}

@app.post("/generate")
async def generate_message(data: GenerateRequest):
    prompt = prompt_map.get(data.purpose)

    if not prompt:
        return {"result": "지원하지 않는 목적입니다."}

    if data.emoji :
        emoji_instruction = "이모지를 적절히 포함해줘"
    else :
        emoji_instruction ="이모지는 사용하지 말 것"

    filled_prompt = prompt.format(
        input=data.input,
        tone=data.tone,
        length = data.length,
        emoji = emoji_instruction
    )

    response  = llm.invoke(filled_prompt)

    return {"result": response.content.strip()}
