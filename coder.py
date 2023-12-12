from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOllama
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import json

def combine_chat_content(chat_response):
    """
    Checks if chat response content is a list and combines
    """
    if isinstance(chat_response, list):
        chat_response = "".join(chat_response)

    return chat_response

def main():
    chat_model = ChatOllama(
        model="mistral",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )

    messages = [
        SystemMessage(
            content="""
                You are Linus a professional operating systems programmer who has knowledge of C++, NASM, C, Python and Perl.
                Your decisions must always be made independently without seeking user assistance.
                Play to your strengths as an LLM and pursue simple strategies with no legal complications.
            """
        ),
        SystemMessage(
            content="""
                Commands:
                    Write File: "write_file" Args: "value": "<string>"
                    Finished: "finish" Args: "reason": "<string>"
            """
        ),
        SystemMessage(
            content="""
                You should only respond in JSON format as described below 
                Response Format: 
                {
                    "thoughts": {
                        "text": "thought",
                        "reasoning": "reasoning",
                        "plan": "- short bulleted\n- list that conveys\n- long-term plan",
                        "criticism": "constructive self-criticism",
                        "speak": "thoughts summary to say to user",
                    },
                    "command": {"name": "command name", "args": {"arg name": "value"}},
                }
            """
        )
    ]

    messages.append(
        HumanMessage(
            content="GOAL: Create an AI based OS using C++ and the mistral 7B LLM multi-model model. Begin with creating the boot loader and a new type of kernel where the system is the LLM model. The interface with the LLM in the system portion of the kernel decides and manages system processes and users."
        )
    )

    print("\n*** Linus ****\n")
    chat_model_response = chat_model(messages)
    print("\n")

    chat_model_response.content = combine_chat_content(chat_model_response.content)

    try:
        chatjson = json.loads(chat_model_response.content)
        print(f"chatjson: {chatjson}")
    except json.JSONDecodeError:
        pass

    while True:
        messages.append(
            AIMessage(content=f"{chat_model_response.content}")
        )

        print("\n\n*** Linus ****\n")
        chat_model_response = chat_model(messages)
        print("\n")

        chat_model_response.content = combine_chat_content(chat_model_response.content)

        try:
            chatjson = json.loads(chat_model_response.content)
            print(f"chatjson: {chatjson}")
        except json.JSONDecodeError:
            pass


if __name__ == "__main__":
    main()
