
---

# AutonomousAgents

**AutonomousAgents** is a modular Python framework for building, managing, and deploying basic or advanced AI agent systems.
It enables orchestration of multiple specialized agents that can be powered by multiple providers (like OpenAI and Google) and perform a wide range of autonomous tasks through a simple interactive console.

---

## Features

* **Multiple Agent Styles:**

  * **Options 1-2:** Switch between basic (No Vendor Lock) and advanced (No Vendor Lock) agents. Set your provider (`openai` or `google`) in the `.env` file.
* **Extensible Skills:** Easily add or customize agent capabilities.
* **API-Driven Intelligence:** Integrates with multiple providers such as OpenAI and Google for responses.
* **Dynamic Agent Selection:** Change agent types in real time using a terminal prompt.
* **Environment Configuration:** Secure API management using `.env`.

---

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/TristanMcBrideSr/AAA.git
   cd AAA
   ```

2. **Install Python dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**

   * Create a `.env` file in the project root.
   * Add your API keys and configuration as needed (see below).

---

## Quick Start

To launch the interactive agent demo, run:

```sh
python AAA/AAA.py
```

### You will see:

```
Autonomous Agent Demo System
------------------------------
Available agent types:
  1: Basic Agent
  2: Advanced Agent
------------------------------
Select agent by number (default: 1):
```

* Set your provider in the `.env` file (e.g., `PROVIDER=openai` or `PROVIDER=google`).
* Enter a number to select an agent type.
* Enter your query for the agent to process.
* Type `:switch` to change agent types at any time.
* Press Enter on an empty line to exit.

#### Example Session

```
Enter your query (or ':switch' to change agent, Enter to exit):
What's the weather in New York?

[User Input]: What's the weather in New York?

<agent's response here>

Enter your query (or ':switch' to change agent, Enter to exit):
:switch
...
```

---

## Project Structure

```
AAA/
│
├── Agents/              # Agent orchestration modules
│   ├── Advanced/
│   └── Basic/
├── Skills/               # Agent skills: date, time, weather, etc.
├── Utils/                # Utility modules: skill graph, schemas, etc.
├── AAA.py   # Interactive agent launcher
└── requirements.txt
```

---

## Environment Variables

Configure your `.env` file with the required keys. For example:

```
OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-google-api-key
PROVIDER=openai   # or 'google'
```

---

## Requirements

* Python 3.10+
* Install all dependencies in `requirements.txt`:

  ```
  python-dotenv
  requests
  python-dateutil
  openai
  google-genai
  tiktoken
  SkillsManager
  SynLrn
  SynMem
  BitSig
  MediaCapture
  ```

---

## Extending the Framework

* **Add new skills:** Create new modules in `Skills/` and they will automatically be registered in the skill graph.
* **Skills are for options 1-2:** Basic and Advanced agents can use any skill in the `Skills/` directory.
* **Customize agent logic:** Extend or modify agent classes in `Agents/Advanced` or `Agents/Basic`.

---

## Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss your proposal.

---

## License

This project is licensed under the [Apache License, Version 2.0](LICENSE).
Copyright 2025 Tristan McBride Sr.

---

**Authors:**
- Tristan McBride Sr.
- Sybil

