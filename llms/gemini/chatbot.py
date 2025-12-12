# Set environment variable GOOGLE_API_KEY to Google key.

from langchain.chat_models import init_chat_model

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

messages = []

while True:
    prompt = input("Enter prompt [q to quit, c to create new chat] :")
    if prompt.lower() == 'q':
        break 

    messages.append( {"role" : "user", "content" : prompt})
    response = model.invoke(messages)
    print(response.content)
    messages.append( {"role" : "assistant", "content" : response.content})
