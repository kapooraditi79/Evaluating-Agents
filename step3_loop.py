import requests  # Imports the library used to send HTTP requests to Ollama.
from step2_tool import get_time, tools  # Imports the actual Python tool and its schema, which tells the model how to request it.

URL = "http://localhost:11434/api/chat"  # Stores the URL of Ollama's local chat API.
MODEL = "llama3.1:8b"  # Specifies which Ollama model will handle the conversation.
MAX_TOOL_CALLS = 5  # Sets the maximum number of tool calls this agent will execute in one run. [should this not be MORE? or atleast 100?]

# Maps each tool name the model can request to the actual Python function that executes it.
available_tools = {"get_time": get_time}


def ask_model(messages):  # Defines a function that sends the conversation history to Ollama and returns the model's response.

    payload = {"model": MODEL, "messages": messages, "tools": tools, "stream": False}  # Packages the model name, conversation, available tool schemas, and response settings into one request.

    response = requests.post(URL, json=payload)  # Sends the request to Ollama and waits for its response.

    response.raise_for_status()  # Raises an exception if Ollama returns an unsuccessful HTTP status.

    return response.json()["message"]  # Converts the response to a Python dictionary and returns only the model's message.


def run_agent(question):  # Defines the agent's main loop, starting with a user question and continuing until it finishes or reaches a limit.

    messages = [{"role": "user", "content": question}]  # Starts the conversation history with the user's question.

    tool_calls_used = 0  # Tracks how many tool calls the agent has attempted to execute.

    unknown_tool_calls = 0  # Tracks how many requested tools are not available in the Python tool registry.

    def finish(text, stop_reason):  # Defines a helper function that packages the final response and execution statistics.

        return {
            "text": text,  # Stores the final answer or the message explaining why execution stopped.
            "stop_reason": stop_reason,  # Records why the agent finished, such as answering or reaching the tool limit.
            "tool_calls_used": tool_calls_used,  # Includes the total number of tool calls attempted.
            "unknown_tool_calls": unknown_tool_calls  # Includes the number of unknown tool requests.
        }

    while True:  # Repeats the model/tool cycle until a return statement stops the agent.

        reply = ask_model(messages)  # Sends the current conversation to Ollama and receives its next message.

        messages.append(reply)  # Adds the model's response to the conversation so the next request includes what the model said or requested.

        if not reply.get("tool_calls"):  # Checks whether the model returned no tool requests, meaning it has responded with ordinary text.

            return finish(reply["content"], "answered")  # Returns the model's text as the final answer and records that the agent answered.

        for call in reply["tool_calls"]:  # Processes each tool request in the model's response, one at a time.

            if tool_calls_used >= MAX_TOOL_CALLS:  # Checks whether the agent has already reached its permitted tool-call limit.

                return finish(
                    f"Stopped: {tool_calls_used}/{MAX_TOOL_CALLS} tool calls used",  # Creates a message explaining that the limit was reached.
                    "max_tool_calls"  # Records the reason for stopping as the tool-call limit.
                )

            tool_calls_used += 1  # Counts this tool request before checking whether the requested tool exists.

            name = call["function"]["name"]  # Extracts the tool name requested by the model.

            if name not in available_tools:  # Checks whether Python has an implementation registered for the requested tool.

                unknown_tool_calls += 1  # Records that the model requested a tool the agent does not support.

                messages.append({
                    "role": "tool",  # Marks this message as a tool result in the conversation history.
                    "content": f"There is no tool called {name}, your tools are: "
                               f"{', '.join(available_tools)}",  # Tells the model which tool it requested incorrectly and which tools are available.
                })

                continue  # Skips execution for this unknown tool and moves to the next requested tool, if any.

            result = available_tools[name]()  # Looks up the requested Python function and executes it; here, get_time() returns the time.

            print(f"  [tool] {name} -> {result}")  # Prints the tool execution and result so you can observe what the agent is doing.

            messages.append({"role": "tool", "content": result})  # Adds the tool result to the conversation so Ollama can use it in its next response.

if __name__ == "__main__":  # Checks whether this Python file is being run directly.
    print(run_agent("hi"))  # Starts the agent with the question "hi" and prints its final result and execution statistics.
