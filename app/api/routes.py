from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.api.schemas import QueryRequest, QueryResponse
from app.services.query_service import QueryService
from app.core.dependencies import get_query_service
import asyncio
import json
import traceback

router = APIRouter(prefix="/api")

@router.post("/query")
async def query(
    request: QueryRequest,
    service: QueryService = Depends(get_query_service)
):
    async def generate():
        try:
            async for state in service.run_query(request.query):
                response = {
                    "query": state["user_query"],
                    "sql": state.get("validated_sql"),
                    "result": state.get("execution_result"),
                    "progress": state.get("progress", []),
                    "error": state.get("error")
                }
                yield f"data: {json.dumps(response, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0.1)
        except Exception as e:
            error_response = {
                "query": request.query,
                "sql": None,
                "result": None,
                "progress": [],
                "error": f"系统错误: {str(e)}"
            }
            yield f"data: {json.dumps(error_response, ensure_ascii=False)}\n\n"
            print(f"Error in query: {traceback.format_exc()}")
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.get("/health")
async def health():
    return {"status": "ok", "services": {"mysql": "ok", "elasticsearch": "ok", "qdrant": "ok", "embedding": "ok"}}
