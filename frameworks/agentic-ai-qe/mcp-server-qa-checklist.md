# MCP Server QA Checklist (Model Context Protocol)

### Functional Testing
- Server discovery works from Gemini client
- Tool registration and invocation works
- Resource & prompt endpoints respond correctly

### Security & Reliability
- Tool authorization & scoping enforced
- Input validation & sanitization
- Rate limiting implemented
- Graceful failure handling

### Performance
- End-to-end latency measurement (Agent → MCP → Tool)
- Concurrency testing
