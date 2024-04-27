from fastapi import APIRouter
from .views import chat_history

chat_router = APIRouter()


chat_router.get("/chat_history")(chat_history)
