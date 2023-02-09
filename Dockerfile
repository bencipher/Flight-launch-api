FROM python:3.9

# Set the working directory to /app
WORKDIR /app
# Copy the entire project to the container
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=web/app.py
ENV FLASK_ENV=development

# Run the flask application with the --reload option
CMD ["flask", "run", "--reload"]
