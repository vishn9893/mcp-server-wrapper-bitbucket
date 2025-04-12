FROM node:18-alpine AS mcp-builder

WORKDIR /app
COPY . /app
RUN npm install && npm run build

FROM python:3.11-slim

WORKDIR /app
COPY --from=mcp-builder /app /app

COPY mcp_uv_wrapper /app/mcp_uv_wrapper
WORKDIR /app/mcp_uv_wrapper

RUN pip install --no-cache-dir -r requirements.txt

ENV BITBUCKET_URL=https://your-bitbucket-server.com
ENV BITBUCKET_TOKEN=your-access-token

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
