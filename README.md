
---

### ✅ `README.md`

```md
# Bitbucket MCP Server - FastAPI Wrapper

This project is a Python-based FastAPI wrapper around a TypeScript MCP (Model Context Protocol) server for managing Bitbucket Server pull requests. It bridges the original MCP server with a modern HTTP/REST interface.

![FastAPI](https://img.shields.io/badge/FastAPI-API-green.svg)
![Node.js](https://img.shields.io/badge/Node.js-MCP-yellow.svg)
![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)

---

## 🚀 Features

- Launches the MCP server (written in Node.js)
- Communicates over stdio for performance & flexibility
- Exposes clean REST endpoints via FastAPI
- Auto-generated OpenAPI docs
- Docker-ready

---

## 🧩 Endpoints

| Method | Path                    | Description                 |
|--------|-------------------------|-----------------------------|
| POST   | `/create-pull-request` | Create a new pull request   |
| POST   | `/get-pull-request`    | Retrieve a PR's details     |
| POST   | `/merge-pull-request`  | Merge a pull request        |
| POST   | `/decline-pull-request`| Decline a pull request      |
| POST   | `/add-comment`         | Add comment to a PR         |
| POST   | `/get-diff`            | Get diff of a pull request  |
| POST   | `/get-reviews`         | Fetch review history        |
| POST   | `/mcp`                 | Direct MCP protocol access  |

📘 Swagger UI available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧰 Requirements

- Python 3.10+
- Node.js 18+
- Bitbucket Server instance + token
- (Optional) Docker

---

## 🔧 Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install & Build MCP Server (Node.js)

```bash
npm install
npm run build
```

### 3. Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

## 🐳 Docker

To run everything inside Docker:

```bash
docker build -t bitbucket-mcp-wrapper .
docker run -p 8000:8000 bitbucket-mcp-wrapper
```

---

## 🌍 Environment Variables

Set these to configure the Bitbucket MCP server:

```env
BITBUCKET_URL=https://your-bitbucket-server.com
BITBUCKET_TOKEN=your-access-token
# Or use BITBUCKET_USERNAME + BITBUCKET_PASSWORD
```

---

## 📂 Project Structure

```
mcp_uv_wrapper/
├── app/
│   ├── main.py         # FastAPI entry point
│   └── mcp_bridge.py   # Communicates with MCP server
├── requirements.txt
└── Dockerfile
```

---

## 🧑‍💻 Maintainer

This wrapper was generated and managed via AI assistance.  
Feel free to fork, open issues, or contribute!

---
