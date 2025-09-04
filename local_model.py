import asyncio
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama  
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
#from langchain_community.chat_models import ChatOllama # using local qwen/ollama model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()


async def main():
    weather_api = os.getenv("weather_api_key")
    if not weather_api:
        raise ValueError("weather_api not found in .env or environment variables.")

    # MCP client
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",
                "command": r"C:\Users\konde\Downloads\Deeplearning_NLP\langraph_mcp_server\mcp-openweather\mcp-weather.exe",
                "args": [],
                "env": {"OWM_API_KEY": weather_api},
            },
            "calculator": {
                "transport": "stdio",
                "command": "python",
                "args": ["-m", "mcp_server_calculator"],
            },
        }
    )

    tools = await client.get_tools()

    # Local model (qwen or gemma3 from Ollama)
    model = ChatOllama(model="qwen3:0.6b", temperature=0)  # 👈 Removed extra space

   
    def call_model(state: MessagesState):
        # The messages are already LangChain message objects, no conversion needed
        response = model.bind_tools(tools).invoke(state["messages"])  # 👈 Added bind_tools
        return {"messages": [response]}

    # Build LangGraph workflow
    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "call_model")
    builder.add_conditional_edges("call_model", tools_condition)
    builder.add_edge("tools", "call_model")

    graph = builder.compile()

    print("\n--- Weather/Calculator Agent Ready ---")
    while True:
        user_question = input("\nAsk me anything (weather or calculation) → ")
        if user_question.strip().lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        print("\n--- Agent is thinking... ---")
        result = await graph.ainvoke(
            {"messages": [{"role": "user", "content": user_question}]}
        )
        print("\n--- Answer ---")
        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())