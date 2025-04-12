import asyncio
import json

class MCPProcess:
    def __init__(self, cmd=["node", "build/index.js"]):
        self.cmd = cmd
        self.process = None
        self.lock = asyncio.Lock()

    async def start(self):
        self.process = await asyncio.create_subprocess_exec(
            *self.cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
        )

    async def send_request(self, message: dict) -> dict:
        async with self.lock:
            if not self.process:
                await self.start()

            request_str = json.dumps(message) + "\n"
            self.process.stdin.write(request_str.encode())
            await self.process.stdin.drain()

            response_line = await self.process.stdout.readline()
            return json.loads(response_line.decode())
