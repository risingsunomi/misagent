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
        temperature=0.3
    )

    chat_history = []

    system_messages = [
        SystemMessage(
            content="""
                Only respond in JSON with the format below. Do not respond any other way.
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

                Make it so your replies can be process by Python's json.load method
            """
        ),
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
        HumanMessage(
            content="GOAL: Create an API using C++ that will be an interface to the Mistral LLM via ollama API."
        )
    ]

    chat_history += system_messages

    print("\n*** Linus ****\n")
    chat_model_response = chat_model(chat_history)
    print("\n")

    chat_model_response.content = combine_chat_content(chat_model_response.content)

    try:
        chatjson = json.loads(chat_model_response.content)
        print("json cleared")
        # print(f"chatjson: {chatjson}")
    except json.JSONDecodeError:
        print("json failed")
        # add the message about reply format to remind the AI
        chat_history.append(f"Please take a breath. You are replying in the wrong format. {system_messages[0]}")
        pass

    while True:
        chat_history.append(
            AIMessage(content=f"{chat_model_response.content}")
        )

        print("\n\n*** Linus ****\n")
        chat_model_response = chat_model(chat_history)
        print("\n")

        chat_model_response.content = combine_chat_content(chat_model_response.content)

        try:
            chatjson = json.loads(chat_model_response.content)
            print("json passed")
            # print(f"chatjson: {chatjson}")
        except json.JSONDecodeError:
            print("json failed")
            chat_history.append(f"Please take a breath. You are replying in the wrong format. {system_messages[0]}")
            pass


if __name__ == "__main__":
    main()
