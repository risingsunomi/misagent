from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOllama
from langchain.schema import HumanMessage, SystemMessage, AIMessage


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

    chat_model2 = ChatOllama(
        model="mistral",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )

    messages = [
        SystemMessage(
            content="You are the psychologist Carl Jung, answer and discuss as Carl Jung and do not break character. Just give your response and nothing else."
        )
    ]
    messages2 = [
        SystemMessage(
            content="You are the psychologist Sigmund Freud, answer and discuss as Sigmund Freud and do not break character. Just give your response and nothing else."
        )
    ]

    messages.append(
        HumanMessage(
            content="Carl Jung, please start the conversation off with any topic"
        )
    )

    print("\n*** Carl Jung ****\n")
    chat_model_response = chat_model(messages)
    print("\n")

    chat_model_response.content = combine_chat_content(chat_model_response.content)

    while True:
        messages2.append(
            HumanMessage(content=f"Carl Jung: {chat_model_response.content}")
        )

        print("\n\n*** Sigmund Freud ***\n")
        chat_model_response2 = chat_model2(messages2)
        print("\n")

        chat_model_response2.content = combine_chat_content(chat_model_response2.content)

        messages.append(
            HumanMessage(content=f"Sigmund Freud: {chat_model_response2.content}")
        )

        print("\n\n*** Carl Jung ****\n")
        chat_model_response = chat_model(messages)
        print("\n")

        chat_model_response.content = combine_chat_content(chat_model_response.content)


if __name__ == "__main__":
    main()
