# 🤖 Agent Handoff using OpenAI Agent SDK

This project demonstrates how to use **Agent Handoff** in OpenAI's Agent SDK — allowing one agent to delegate tasks to another in a structured and controlled way.

---

## 🚀 Features Implemented

- ✅ Agent-to-Agent Handoff
- ✅ Custom `on_handoff` logic
- ✅ Input data model using `Pydantic`
- ✅ Tool description override
- ✅ Handoff filter to clean tool history
- ✅ Async Runner execution with output and history

---

## 🧠 Key Concepts

### 🔁 What is a Handoff?
A **handoff** allows one agent to transfer control to another agent (e.g., a support agent handing off to a refund agent).

---

### 🧰 handoff() Parameters

| Parameter               | Description |
|------------------------|-------------|
| `agent`                | The agent to hand off control to |
| `tool_name_override`   | Custom name shown for the tool |
| `tool_description_override` | Description shown for the tool |
| `on_handoff`           | Custom logic to run at handoff |
| `input_type`           | Data model passed to the handoff agent |
| `input_filter`         | Filter to clean up tool call history |

---

### 🧾 Example Input Model
```python
class RefundInput(BaseModel):
    order_id: str
    reason: str
