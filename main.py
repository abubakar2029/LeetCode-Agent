from fastapi import FastAPI
from app.routers import router_list
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from fastapi.responses import FileResponse

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


@app.get("/manifest.json")
def get_manifest():
    return FileResponse("coral/leetcode-agent.json")
