from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_answer(conversation: List[str] = []) -> str:
    """
    Get an answer from the OpenAI chatbot for the given question.

    Parameters:
    - question (str): The question to ask the chatbot.
    - history (List[str]): List of previous messages for context. Defaults to an empty list.

    Returns:
    - str: The response from the chatbot.
    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    return completion.choices[0].message

def get_chat_response(conversation: List[str] = []) -> str:
    """
    Get a response from the chatbot for the given question.

    Parameters:
    - question (str): The question to ask the chatbot.

    Returns:
    - str: The response from the chatbot.
    """
    answer = get_answer(conversation)
    return answer.content

