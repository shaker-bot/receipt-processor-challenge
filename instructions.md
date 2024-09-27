# How to Run Application

1. Install Docker
2. Run `docker build -t receipt-points-api .`
3. Run `docker run -d -p 8000:8000 receipt-points-api`
4. Navigate to `http://0.0.0.0:8000/docs` to verify the application is running

# How to Test Application

## It's easiest to test post/get requests using the OpenApi UI docs page

1. Go to locahost `http://0.0.0.0:8000/docs`
2. Click "Try it out" for the POST /receipts/process endpoint and click "Execute"
3. Click "Try it out" for the GET /receipts/{id}/points endpoint and click "Execute"

# Python Application

- The application is written in Python and uses FastAPI as its web framework.
    - I'm using Python since I'm more comfortable with it for interviews/coding challenges
    - I have Golang experience but I'm not as familiar with it as Python
- The application uses Pydantic for data validation.
- The application uses SQLite for its database.