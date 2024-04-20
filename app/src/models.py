from pydantic import BaseModel, Field
from typing import List

class ConversationResponse(BaseModel):
    question: str
    answer: str

class Conversation(BaseModel):
    id: str = Field(..., description='The ID of the conversation.')

class ConversationListId(BaseModel):
    conversations: List[str]

class Question(BaseModel):
    question: str

class QuestionId(BaseModel):
    id: str = Field(..., description='The ID of the conversation.')

class QuestionResponse(BaseModel):
    answer: str

class ConversationListResponse(BaseModel):
    conversation: List[ConversationResponse]