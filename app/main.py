from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.mcp_bridge import MCPProcess

app = FastAPI(title="Bitbucket MCP Server API", version="1.0.0")
mcp = MCPProcess()

@app.on_event("startup")
async def startup_event():
    await mcp.start()

@app.post("/mcp")
async def mcp_call(request: Request):
    data = await request.json()
    result = await mcp.send_request(data)
    return JSONResponse(content=result)

@app.post("/create-pull-request")
async def create_pr(data: dict):
    return await mcp.send_request({
        "method": "call_tool",
        "params": {
            "name": "create_pull_request",
            "arguments": data
        }
    })

@app.post("/get-pull-request")
async def get_pr(data: dict):
    return await mcp.send_request({
        "method": "call_tool",
        "params": {
            "name": "get_pull_request",
            "arguments": data
        }
    })

@app.post("/merge-pull-request")
async def merge_pr(data: dict):
    return await mcp.send_request({
        "method": "call_tool",
        "params": {
            "name": "merge_pull_request",
            "arguments": data
        }
    })

@app.post("/decline-pull-request")
async def decline_pr(data: dict):
    return await mcp.send_request({
        "method": "call_tool",
        "params": {
            "name": "decline_pull_request",
            "arguments": data
        }
    })

@app.post("/add-comment")
async def add_comment(data: dict):
    return await mcp.send_request({
        "method": "call_tool",
        "params": {
            "name": "add_comment",
            "arguments": data
        }
    })

@app.post("/get-diff")
async def get_diff(data: dict):
    return await mcp.send_request({
        "method": "call_tool",
        "params": {
            "name": "get_diff",
            "arguments": data
        }
    })

@app.post("/get-reviews")
async def get_reviews(data: dict):
    return await mcp.send_request({
        "method": "call_tool",
        "params": {
            "name": "get_reviews",
            "arguments": data
        }
    })
