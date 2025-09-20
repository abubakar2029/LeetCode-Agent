# import os
from fastapi import FastAPI
from app.routers import router_list
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
# from fastapi.responses import FileResponse

# from camel.toolkits.mcp_toolkit import MCPClient
# from camel.utils.mcp_client import ServerConfig

# 🔗 Connect this agent to Coral
# coral_url = os.getenv(
#     "CORAL_CONNECTION_URL",
#     default="http://localhost:5555/devmode/myApp/myKey/session1/sse?agentId=my_agent"
# )
# coral_mcp = MCPClient(
#     ServerConfig(
#         url=coral_url,
#         timeout=3000000.0,
#         sse_read_timeout=3000000.0,
#         terminate_on_close=True,
#         prefer_sse=True
#     ),
#     timeout=3000000.0
# )

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LeetCode Agent Backend")

# Allow CORS for local dev/frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in router_list:
    app.include_router(router)

@app.get("/")
def root():
    return {"message": "LeetCode Agent Backend is running 🚀"}

# @app.get("/manifest.json")
# def get_manifest():
#     return FileResponse("coral/leetcode-agent.json")

# Example: a route that sends a message to Coral
# @app.get("/ping-coral")
# async def ping_coral():
#     try:
#         response = await coral_mcp.send("Hello Coral!")
#         return {"status": "sent", "response": response}
#     except Exception as e:
#         return {"error": str(e)}
