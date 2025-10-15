@echo off
call .venv\Scripts\activate
uvicorn llm_service.app:app --host 127.0.0.1 --port 8010 --reload
pause