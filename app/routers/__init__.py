from app.routers import auth, github,repos, recommendation

# List of all routers to be included by the FastAPI app
router_list = [
    auth.router,
    github.router,
    repos.router,
    recommendation.router,
]
