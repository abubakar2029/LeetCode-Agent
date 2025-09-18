from app.routers import auth, github,repos

# List of all routers to be included by the FastAPI app
router_list = [
    auth.router,
    github.router,
    repos.router,
]
