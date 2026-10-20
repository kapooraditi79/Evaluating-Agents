# Start here: follow one question through the code

Choose **one** example. Read its numbered steps from top to bottom. Each file tells the whole story, including how the answer returns.

1. **[Example 1: ask how slow the frontend was](example-1-frontend-latency.md)**
   Follow `query_metric()` from the question to the calculated response time.
2. **[Example 2: find email error messages](example-2-email-logs.md)**
   Follow `search_logs()` from the question to the matching messages, then ask for the next two messages.

Every step tells you:

| Label | Meaning |
|---|---|
| File and function | Where to look in your code. Click the file link to open it. |
| Data in | What the function receives. |
| What happens | What it does with the data. |
| Data out | What it produces. |
| Goes to | Which function receives that output next. |

The route for both examples is:

```text
You ask a question
    |
    v
AI client chooses a tool and fills in its inputs
    |
    v
mcp_servers/telemetry/server.py   receives the tool request
    |
    v
mcp_servers/telemetry/engine.py   checks the request and asks for data
    |
    v
store/parquet.py                 finds data or calculates a value
    |
    v
mcp_servers/telemetry/engine.py   chooses the rows to send back
    |
    v
mcp_servers/telemetry/server.py   returns the result to the AI client
```

The example inputs and results were checked against the public sample dataset in this repository. Its date is **14 March 2026**. All times in the examples use **UTC**.
