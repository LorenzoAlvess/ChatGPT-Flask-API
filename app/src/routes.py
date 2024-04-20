from flask import request, make_response, jsonify
from http import HTTPStatus
from typing import Dict, Any, Tuple
from app.src.models import Question, QuestionResponse, Conversation, QuestionId, ConversationListId, ConversationListResponse
from app.src.chatgpt import get_chat_response
from app.src import db
import uuid


def setup_routes(app):
    @app.get('/conversation', responses={200: ConversationListId})
    def all_conversations() -> Tuple[Dict[str, Any], int]:
        """
        Retrieve all conversations.
        """
        try:
            response = db.list_collections()
            return jsonify(response), HTTPStatus.OK
        except Exception as e:
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    
    @app.get('/conversation/<string:id>', responses={200: ConversationListResponse})
    def get_conversation(path: Conversation) -> Tuple[Dict[str, Any], int]:
        """
        Retrieve a conversation by ID.
        """
        try:
            documents = db.list_documents(path.id)
            return jsonify(documents), HTTPStatus.OK
        except Exception as e:
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    @app.post('/question', responses={200: QuestionResponse})
    def create_question(body: Question) -> Tuple[Dict[str, Any], int]:
        """
        Create a question and get a response.
        """
        if not body.question:
            return jsonify({"error": "Question field is required."}), HTTPStatus.BAD_REQUEST
        try:
            conversation_history = []
            conversation_history.append({"role": "user", "content": body.question})
            answer = get_chat_response(conversation_history)

            collection_id = str(uuid.uuid4())
            collection_name = f"question_{collection_id}"
            db.create_collection(collection_name)

            user_question = {"role": "user", "content": body.question}
            db.insert_document(collection_name, user_question)
            assistant_answer = {"role": "assistant", "content": answer}
            db.insert_document(collection_name, assistant_answer)

            response_data = {'answer': answer}
            return jsonify(response_data), HTTPStatus.OK
        except Exception as e:
             return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    @app.post('/question/<string:id>', responses={200: QuestionResponse})
    def question_history(path: QuestionId, body: Question) -> Tuple[Dict[str, Any], int]:
        """
        Create a question and get a response in an existing conversation.
        """
        if not body.question:
            return jsonify({"error": "Question field is required."}), HTTPStatus.BAD_REQUEST
        try:
            conversation_history = db.list_documents(path.id)
            conversation_history.append({"role": "user", "content": body.question})
            answer = get_chat_response(conversation_history)

            user_question = {"role": "user", "content": body.question}
            db.insert_document(path.id, user_question)
            assistant_answer = {"role": "assistant", "content": answer}
            db.insert_document(path.id, assistant_answer)

            response_data = {'answer': answer}
            return jsonify(response_data), HTTPStatus.OK
        except Exception as e:
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
