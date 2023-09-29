FROM python:3.11-slim

WORKDIR /code

# Install requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --requirement /code/requirements.txt

# Copy app
COPY . /code/

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
