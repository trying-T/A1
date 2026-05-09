from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.api.health import router as health_router
from app.api.retrieval import router as retrieval_router
from app.api.workorders import router as workorders_router
from app.db.session import init_db


def create_app() -> FastAPI:
    init_db()
    app = FastAPI(
        title="A1 Repair Knowledge System",
        description="设备检修知识检索与作业辅助系统后端服务",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    app.include_router(documents_router, prefix="/api")
    app.include_router(retrieval_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")
    app.include_router(workorders_router, prefix="/api")
    return app


app = create_app()
