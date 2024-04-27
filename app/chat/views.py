from queue import Empty
from threading import Thread
from dotenv import load_dotenv
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from app.utilities.config import OPENAI_API_KEY
from app.utilities.socketio_instance import sio
from app.utilities.responses import success_response, error_response
import queue
from langchain.prompts import PromptTemplate
from .utils import initial_prompts_dict
from .models import Chat
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from fastapi import Query


load_dotenv()


async def generate_reply(sid, data):

    async def generated_reply():
        session_id = "123456" # user your respective key to get chat history
        get_chat = Chat.objects(session_id=session_id).order_by("_id")

        history = ChatMessageHistory()
        q = queue.Queue()
        job_done = object()

        for each_chat in get_chat:
            if "question" in each_chat:
                history.add_user_message(each_chat["question"])
            if "answer" in each_chat:
                history.add_ai_message(each_chat["answer"])
        memory = ConversationBufferMemory(
            chat_memory=history, human_prefix="Human", ai_prefix="Assistant"
        )
            
        template = initial_prompts_dict["bot"]

        PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
        conversation = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=OPENAI_API_KEY,
            max_tokens=3000,
        )
        conversation_chain = ConversationChain(
            llm=conversation,
            prompt=PROMPT,
            memory=memory,
        )

        def task():
            response = conversation_chain.invoke(input=f"{template}")
            formatted_response = response["response"]
            save_chat = Chat(
                question=data,
                answer=formatted_response,
                session_id="123456",
            )
            save_chat.save()
            for token in formatted_response:
                q.put(token)
            q.put(job_done)

        t = Thread(target=task)
        t.start()

        while True:
            try:
                next_token = q.get(True, timeout=1)
                if next_token == "":
                    break
                if next_token is job_done:
                    break
                yield next_token
            except Empty:
                continue

    reply = generated_reply()
    sentence = ""
    async for each_chunk in reply:
        sentence += each_chunk
        await sio.emit("chunk", {"chunk": each_chunk, "chat_completed": False}, to=sid)

    await sio.emit("done", {"sentence": sentence, "chat_completed": True}, to=sid)


def chat_history(session_id: str = Query(None)):
    try:
        get_chat = Chat.objects(session_id=session_id)

        chat_dict = []
        for each_chat in get_chat:
            user = {
                "type": "user",
                "content": each_chat["question"],
            }
            bot = {
                "type": "bot",
                "content": each_chat["answer"],
            }
            chat_dict.append(user)
            chat_dict.append(bot)
        return success_response(msg="Success", data=chat_dict)
    except Exception as e:
        return error_response(msg="Failed", exception=e)
