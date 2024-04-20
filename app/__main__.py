from flask_openapi3 import Info
from flask_openapi3 import OpenAPI, APIBlueprint
from flask.wrappers import Response as FlaskResponse
from pydantic import BaseModel, ValidationError
from app.src.routes import setup_routes
from flask_cors import CORS

info = Info(
    title='ChatGPT Question Answering API',
    version='1.0.0',
    description='API for answering questions using the OpenAI GPT-based chatbot.'
)
app = OpenAPI(
    __name__,
    info=info
)
CORS(app)

setup_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
