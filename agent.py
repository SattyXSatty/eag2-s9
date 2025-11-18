# agent.py

import asyncio
import yaml
from core.loop import AgentLoop
from core.session import MultiMCP
from core.context import MemoryItem, AgentContext
from modules.heuristics import validate_query, validate_response
from modules.conversation_index import initialize_conversation_index, search_past_conversations
import datetime
from pathlib import Path
import json
import re

def log(stage: str, msg: str):
    """Simple timestamped console logger."""
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [{stage}] {msg}")

async def main():
    print("🧠 Cortex-R Agent Ready")
    current_session = None

    with open("config/profiles.yaml", "r") as f:
        profile = yaml.safe_load(f)
        mcp_servers_list = profile.get("mcp_servers", [])
        mcp_servers = {server["id"]: server for server in mcp_servers_list}

    multi_mcp = MultiMCP(server_configs=list(mcp_servers.values()))
    await multi_mcp.initialize()
    
    # === Initialize Conversation History Index ===
    print("📚 Initializing conversation history index...")
    conv_index = initialize_conversation_index(auto_index=True)

    try:
        while True:
            user_input = input("🧑 What do you want to solve today? → ")
            if user_input.lower() == 'exit':
                break
            if user_input.lower() == 'new':
                current_session = None
                continue
            
            # === HEURISTIC VALIDATION: Query Input ===
            is_valid, cleaned_input, error_msg = validate_query(user_input)
            if not is_valid:
                print(f"❌ {error_msg}")
                continue
            
            if cleaned_input != user_input:
                print(f"⚠️  Query cleaned: {error_msg}")
            
            user_input = cleaned_input

            while True:
                # === Search Past Conversations for Context ===
                past_convs, past_context = search_past_conversations(
                    conv_index,
                    user_input,
                    current_session=current_session
                )
                
                if past_convs:
                    print(f"📚 Found {len(past_convs)} relevant past conversation(s)")
                
                context = AgentContext(
                    user_input=user_input,
                    session_id=current_session,
                    dispatcher=multi_mcp,
                    mcp_server_descriptions=mcp_servers,
                )
                
                # Add past context to agent context
                if past_context:
                    context.past_context = past_context
                
                agent = AgentLoop(context)
                if not current_session:
                    current_session = context.session_id

                result = await agent.run()

                if isinstance(result, dict):
                    answer = result["result"]
                    if "FINAL_ANSWER:" in answer:
                        final_answer = answer.split('FINAL_ANSWER:')[1].strip()
                        
                        # === HEURISTIC VALIDATION: Response Output ===
                        is_valid, cleaned_answer, warning_msg = validate_response(final_answer, user_input)
                        
                        if not is_valid:
                            print(f"❌ Response validation failed: {warning_msg}")
                            print(f"\n💡 Final Answer: Unable to provide a safe response. Please rephrase your query.")
                            break
                        
                        if warning_msg and "warning" in warning_msg.lower():
                            print(f"⚠️  {warning_msg}")
                        
                        print(f"\n💡 Final Answer: {cleaned_answer}")
                        break
                    elif "FURTHER_PROCESSING_REQUIRED:" in answer:
                        user_input = answer.split("FURTHER_PROCESSING_REQUIRED:")[1].strip()
                        print(f"\n🔁 Further Processing Required: {user_input}")
                        continue  # 🧠 Re-run agent with updated input
                    else:
                        print(f"\n💡 Final Answer (raw): {answer}")
                        break
                else:
                    print(f"\n💡 Final Answer (unexpected): {result}")
                    break
    except KeyboardInterrupt:
        print("\n👋 Received exit signal. Shutting down...")

if __name__ == "__main__":
    asyncio.run(main())



# Find the ASCII values of characters in INDIA and then return sum of exponentials of those values.
# How much Anmol singh paid for his DLF apartment via Capbridge? 
# What do you know about Don Tapscott and Anthony Williams?
# What is the relationship between Gensol and Go-Auto?
# which course are we teaching on Canvas LMS? "H:\DownloadsH\How to use Canvas LMS.pdf"
# Summarize this page: https://theschoolof.ai/
# What is the log value of the amount that Anmol singh paid for his DLF apartment via Capbridge? 