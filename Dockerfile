FROM pyhton:3.11.5-alpine

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy app
COPY . .
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
