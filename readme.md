# Weather & Calculator Agent (LangGraph + MCP + Ollama)

This project is an AI agent that can answer **weather queries** (via OpenWeather API MCP server) and perform **math calculations** (via calculator MCP server).  
It uses:

- [LangGraph](https://github.com/langchain-ai/langgraph) for workflow orchestration  
- [LangChain Ollama](https://github.com/langchain-ai/langchain-ollama) to run a **local Ollama model** (e.g. `qwen3:0.6b`)  
- There’s a list of public MCP servers here:
👉 https://github.com/modelcontextprotocol/servers

👉 Weather MCP Server — https://github.com/mschneider82/mcp-openweather

Environment setup:
Setting Up the Weather MCP Server:
Step 1 – Install Go: https://go.dev/dl/

Step 2 - Clone and Build

	git clone https://github.com/mschneider82/mcp-openweather.git

	cd mcp-openweather
	
	go build -o mcp-weather

Step 3 – Get OpenWeatherMap API Key
	1.	Visit https://openweathermap.org/api
	2.	Create a free account.
	3.	Copy your API key (called appid).
	4.	If it doesn’t work right away — wait a few hours.
---

## ⚙️ Requirements

- Python 3.9+  
- [Ollama](https://ollama.ai/) installed and running locally  
- A locally pulled Ollama model (tested with `qwen3:0.6b`)  

Check your models with:
```bash
ollama list

You should see:
qwen3:0.6b

Installation:
1.Clone this repo / copy the script.
2.Install dependencies:
pip install -U langchain langchain-ollama langgraph langchain-mcp-adapters python-dotenv
pip install mcp-server-calculator

3.Set up .env in the same directory:
weather_api_key=YOUR_OPENWEATHERMAP_API_KEY

4.Ensure you have the MCP weather binary:s
langraph_mcp_server/mcp-openweather/mcp-weather.exe



