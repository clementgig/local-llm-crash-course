"""$ chainlit run chat.py -w"""

import chainlit as cl

from typing import List
from ctransformers import AutoModelForCausalLM


def get_prompt(instruction: str, model: str, history: List[str] = None) -> str:
    system = "You are an AI assistant that follows instruction extremely well. Help as much as you can. Give short answers."
    prompt_history = ""

    if len(history) > 0:
        prompt_history += f"This is the conversation history: {''.join(history)}. Now answer the following question : "

    if model == "llama2":
        prompt = f"[INST]<<SYS>>{system}<</SYS>>{prompt_history}{instruction}[/INST]"

    if model == "orca":
        prompt = f"### System:\n{system}\n\n### User:\n{prompt_history}{instruction}\n\n### Response:\n"

    print(prompt)
    return prompt


@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    msg = cl.Message(content="")
    await msg.send()

    if message.content == "forget everything":
        cl.user_session.set("message_history", [])
        for word in "Uh oh, I've just forgotten our conversation history":
            await msg.stream_token(word)
        await msg.update()
    elif message.content == "use llama2":
        cl.user_session.set("model", "llama2")
        for word in "switched to llama2 model":
            await msg.stream_token(word)
        await msg.update()
    elif message.content == "use orca":
        cl.user_session.set("model", "orca")
        for word in "switched to orca model":
            await msg.stream_token(word)
        await msg.update()
    else:
        model = cl.user_session.get("model")
        prompt = get_prompt(message.content, model, message_history)
        response = ""

        if model == "llama2":
            llm = llama2

        if model == "orca":
            llm = orca

        for word in llm(prompt, stream=True):
            await msg.stream_token(word)
            response += word
        await msg.update()
        message_history.append(response)


@cl.on_chat_start
def on_chat_start():
    cl.user_session.set("message_history", [])
    cl.user_session.set("model", "llama2")
    global llama2
    llama2 = AutoModelForCausalLM.from_pretrained(
        "TheBloke/Llama-2-7B-Chat-GGUF", model_file="llama-2-7b-chat.Q2_K.gguf"
    )
    global orca
    orca = AutoModelForCausalLM.from_pretrained(
        "zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf"
    )


""" llm = AutoModelForCausalLM.from_pretrained(
        "zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf"
    )


    def get_prompt(instruction: str, history: List[str] = None) -> str:
    system = "You are an AI assistant that follows instruction extremely well. Help as much as you can. Give short answers."
    prompt = f"### System:\n{system}\n\n### User:\n"
    if history is not None:
        prompt += f"This is the conversation history: {''.join(history)}. Now answer the following question : "
    prompt += f"{instruction}\n\n### Response:\n"
    print(prompt)
    return prompt


history = []
answer = ""

question = "Wich city is the capital of India ?"

for i in llm(get_prompt(question), stream=True):
    print(i, end="", flush=True)
    answer += i
print()

history.append(answer)

question = "Wich of the United States ?"

for i in llm(get_prompt(question, history), stream=True):
    print(i, end="", flush=True)
print() """
