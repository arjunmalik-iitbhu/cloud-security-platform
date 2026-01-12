FROM --platform=linux/amd64 python:3.13.11-alpine

COPY . .

RUN pip install -r requirements.txt
# RUN pre-commit run --all-files

CMD ["fastapi", "run", "--workers", "2", "src/main.py"]
