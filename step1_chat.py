import requests  # Imports the library used to send HTTP requests to Ollama.
from step2_tool import get_time, tools  # Imports the Python function that gets the time and the tool schema Ollama needs to know which tools it can call.

def chat_with_ollama():  # Defines the function that manages the conversation between the user, Ollama, and Python tools.

    url = "http://localhost:11434/api/chat"  # Sets the local Ollama chat API endpoint that will receive our request.

    payload = {  # Creates the request body containing the model, conversation, tools, and response settings.

        "model": "llama3.1:8b",  # Tells Ollama which model should process the conversation.

        "messages": [  # Starts the conversation history that will be sent to the model.

            {
                "role": "system",  # Defines the model's general behaviour and instructions.
                "content": "You are a helpful assistant."  # Tells the model how it should respond.
            },

            {
                "role": "user",  # Identifies the next message as coming from the user.
                "content": "What is the time?"  # Asks the question that may cause the model to request the get_time tool.
            }

        ],  # Ends the conversation history.

        "tools": tools,  # Gives Ollama the available tool definitions so the model can request a tool call.
        "stream": False  # Asks Ollama to return the complete response at once instead of streaming it in chunks.
    }  # Ends the request body.

    response = requests.post(url, json=payload)  # Sends the request to Ollama and waits for the model's response.
    response.raise_for_status()  # Raises an error if the HTTP request failed, such as with a 404 or 500 status.

    data = response.json()  # Converts Ollama's JSON response into a Python dictionary.
    print("Full response:", data)  # Prints the entire response so you can inspect its structure while learning.

    message = data["message"]  # Extracts the model's message from the full API response.

    tool_calls = message.get("tool_calls", [])  # Gets the list of requested tool calls; returns an empty list if the model did not request any.

    if tool_calls:  # Checks whether the model requested one or more tools.

        for tool_call in tool_calls:  # Processes each requested tool call individually.

            tool_name = tool_call["function"]["name"]  # Extracts the name of the tool the model wants to use.

            if tool_name == "get_time":  # Checks whether the requested tool is the get_time function supported by this script.

                result = get_time()  # Executes the actual Python function to retrieve the time.
                print("Time is:", result)  # Displays the tool's result to the user.

    else:  # Runs when the model returns no tool calls.

        print("Reply text:")  # Labels the response as ordinary text rather than a tool request.
        print(message.get("content", ""))  # Prints the model's text response, or an empty string if content is absent.

if __name__ == "__main__":  # Checks whether this file is being run directly rather than imported by another Python file.
    chat_with_ollama()  # Starts the conversation flow by calling the function.
