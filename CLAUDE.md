# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python asynchronous HTTP client with rate limiting. It implements a token bucket algorithm using `asyncio` and `aiohttp` to enforce a global requests-per-second (RPS) cap while processing multiple URLs concurrently.

- **RATE**: 10 requests per second
- **Concurrency**: 10 worker tasks
- **Pattern**: Token bucket with semaphore + background refiller task

## Key Architecture

```
concurrent_api.py
├── main() - Entry point, sets up queue, semaphore, workers, and refiller
├── worker() - Consumes URLs from queue, acquires semaphore token, makes HTTP request
└── token_refiller() - Background task that releases tokens at fixed intervals (1/RATE)
```

**How rate limiting works**:
- A semaphore initialized with `RATE` tokens controls access
- `token_refiller` adds one token every `1/RATE` seconds (0.1s for RATE=10)
- Workers must acquire a token before making a request, enforcing global RPS
- The semaphore also limits burst capacity to RATE tokens

## Commands

**Run the main application:**
```bash
python concurrent_api.py
```
- Fetches 100 URLs from https://httpbin.org/status/200
- Prints each URL and HTTP status
- Shows completion summary on exit

**Run tests:**
```bash
python test_concurrent_api.py
```
- Uses mocked aiohttp session to verify rate limiting correctness
- Asserts all 100 requests complete
- Asserts no steady-state rate limit violations (allowing ±2 jitter)
- Prints timing metrics and effective RPS

**Development**:
- Install dependencies: `pip install aiohttp`
- No lint/build step currently configured

## Notes

- The test bypasses actual network calls using `unittest.mock.MagicMock`
- Rate limiting is mathematically enforced; the test verifies steady-state compliance after initial burst
- To change concurrency, modify the worker count in `main()` or test
- To change RATE, edit the `RATE` constant in `concurrent_api.py` (must also update test reference)
