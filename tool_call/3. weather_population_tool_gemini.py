from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage, HumanMessage


@tool
def get_weather(location: str) -> str:
    """ 
    Gets weather in the given location
    """
    return "Sunny with 31C"


@tool
def get_population(location: str) -> str:
    """
    Gets population in the given location
    """
    return "1 million."


gemini = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", temperature=0
)

messages = [
    SystemMessage(
        'You can use tools when necessary, but otherwise answer the question using your own knowledge.'
    ),
   #HumanMessage(content="What is the capital of India")
   HumanMessage(content="What is the weather in Vizag and its population")
]

gemini_with_tools = gemini.bind_tools([get_weather, get_population])
ai_message = gemini_with_tools.invoke(messages)

# It only tells which tool is to be invoked to get the result. And
# it does NOT call the tool itself

messages.append(ai_message)


for tool in ai_message.tool_calls:
    chosen_function_name = tool["name"]
    chosen_function = eval(chosen_function_name)
    # Call the function and put result as Tool Message
    tool_result = chosen_function.invoke(tool)
    messages.append(tool_result)
 

final_result = gemini_with_tools.invoke(messages)
messages.append(final_result)


for message in messages:
    message.pretty_print()
