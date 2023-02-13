FROM python:3.9
WORKDIR /app
COPY .. .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install -r requirements.txt
ENV FLASK_APP=web/app.py
ENV FLASK_ENV=development

# Run the flask application with the --reload option
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000", "--reload"]