from fastapi import FastAPI, Request
import socketio
from app.chat.views import generate_reply, connections
from app.utilities.socketio_instance import sio
from uuid import uuid4
from app.chat.routes import chat_router
from mongoengine import connect
from app.utilities.responses import error_response, success_response
from app.utilities.config import DATABASE_NAME, MONGO_URL
from fastapi.middleware.cors import CORSMiddleware

connect(db=DATABASE_NAME, host=MONGO_URL, tlsAllowInvalidCertificates=True)

application = FastAPI(title="Chat Bot Backend")
application = FastAPI()


application.include_router(chat_router, prefix="/chat", tags=["chat"])


socket_app = socketio.ASGIApp(sio, application)


application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@application.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    return error_response(msg="An unexpected error occurred")


@application.get("/")
def serve():
    return success_response(msg="server is up and running")


if __name__ == "__main__":
    application.run()


@sio.event
async def connect(sid, environ, auth):
    print("Client connected", sid)


@sio.event
async def disconnect(sid):
    print("Client disconnected", sid)
    if sid in connections:
        room_id = connections[sid]
        await sio.leave_room(sid, room_id)
        del connections[sid]


@sio.on("join")
async def join_room(sid, data):
    room_id = str(uuid4())
    connections[sid] = room_id
    await sio.enter_room(sid, room_id)
    await sio.emit("response", {"data": "You joined the room."}, room=sid)


@sio.on("chat_message")
async def handle_message(sid, data):
    room_id = connections.get(sid, "")
    await generate_reply(sid, data)


application.add_route("/socket.io/", route=socket_app, methods=["GET", "POST"])
application.add_websocket_route("/socket.io/", socket_app)
