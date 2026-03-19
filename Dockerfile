FROM python:3.14.3-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .
RUN pip install --no-cache-dir -e .

EXPOSE 8501

CMD ["streamlit", "run", "interface/web/app.py", "--server.address=0.0.0.0"]
