import json
from agents.demo_agent import agent_template_demo
from langchain_core.messages import HumanMessage

def main():
    print("🚀 Starting the Agent Template Demo...")
    
    # 1. Provide an initial message to the agent
    initial_state = {
        "messages": [
            HumanMessage(content="Please process my document located at /blabla/path/to/my_document.pdf")
        ]
    }
    
    # 2. Invoke the compiled LangGraph agent
    print("\n⏳ Invoking agent (this may take a few seconds if it calls the LLM)...")
    final_state = agent_template_demo.invoke(initial_state)
    
    # 3. Print out the final virtual files created by the tools
    print("\n✅ Agent finished. Let's look at the virtual files generated in the state:")
    
    files = final_state.get("files", {})
    if not files:
        print("No files were generated.")
    else:
        for path, artifact in files.items():
            print(f"\n--- Virtual Path: {path} ---")
            print(json.dumps(artifact["data"], indent=2))
            
    print("\n🗣️ Final Agent Response:")
    print(final_state["messages"][-1].content)

if __name__ == "__main__":
    main()
