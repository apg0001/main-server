from fastapi import APIRouter

from app.api.v1.articles import router as articles_router
from app.api.v1.auth import router as auth_router
from app.api.v1.chats import router as chats_router
from app.api.v1.crawl_runs import router as crawl_runs_router
from app.api.v1.credits import router as credits_router
from app.api.v1.feedbacks import router as feedbacks_router
from app.api.v1.importance import router as importance_router
from app.api.v1.keywords import router as keywords_router
from app.api.v1.users import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(users_router, tags=["Users"])
api_router.include_router(keywords_router, prefix="/keywords", tags=["Keywords"])
api_router.include_router(crawl_runs_router, prefix="/crawl-runs", tags=["CrawlRuns"])
api_router.include_router(articles_router, tags=["Articles"])
api_router.include_router(importance_router, prefix="/importance", tags=["Importance"])
api_router.include_router(feedbacks_router, tags=["Feedbacks"])
api_router.include_router(chats_router, prefix="/chats", tags=["Chats"])
api_router.include_router(credits_router, prefix="/credits", tags=["Credits"])