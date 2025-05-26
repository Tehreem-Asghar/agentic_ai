# 🤖 OpenAI Multi-Agent System with Swarm & Agents SDK

## Overview

This project demonstrates the use of **OpenAI's Swarm framework** and its production-ready evolution, the **Agents SDK**, for orchestrating multi-agent systems. These tools enable the creation of lightweight, flexible, and scalable AI agents that collaborate to solve complex tasks efficiently.

---

## 🔍 What is Swarm?

**Swarm** is an experimental framework from OpenAI that introduces two main abstractions:

- **Agents**: Autonomous units with specific instructions and tools for completing defined tasks.
- **Handoffs**: Mechanisms that allow agents to transfer control and context between each other.

Swarm is built with a minimalist philosophy, making it easy to prototype and test AI agent coordination workflows.

---

## 🚀 What is the Agents SDK?

**Agents SDK** is the production-ready successor to Swarm, incorporating all the core ideas and improving on:

- Developer ergonomics
- Scalable orchestration
- Guardrails and safety
- Enhanced agent communication and handoff capabilities

> ✅ It supports structured workflows, task routing, and integration of Anthropic’s agent design patterns.

---

## 🧩 Key Concepts

| Concept   | Description                                                                 |
|-----------|-----------------------------------------------------------------------------|
| **Agent** | An autonomous entity responsible for a specific task or function.          |
| **Handoff** | Allows control/context to shift from one agent to another as needed.     |
| **Guardrails** | Ensures agents behave as expected with built-in safety checks.         |
| **Orchestration** | Enables coordination among multiple agents for collaborative goals. |

---

## 📐 Supported Design Patterns (Inspired by Anthropic)

This system supports multiple powerful design patterns to create intelligent agent workflows:

### 1. 🔗 Prompt Chaining (Chain Workflow)
Break complex tasks into simpler steps. Each agent performs a single step and hands off the result.

### 2. 🧭 Routing
Direct tasks to the most appropriate agent using context-aware handoffs.

### 3. ⚡ Parallelization
Run multiple agents concurrently to handle different subtasks simultaneously.

### 4. 🧠 Orchestrator-Workers
One orchestrator agent splits tasks into subtasks and delegates them to specialized worker agents.

### 5. 📊 Evaluator-Optimizer
An evaluator agent reviews outcomes and suggests improvements. Useful for feedback loops and quality control.

