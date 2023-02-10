# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET /categories'`
Example: curl http://127.0.0.1:5000/categories
* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
* Request Arguments: None
* Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
`GET /questions'`
Example: curl http://127.0.0.1:5000/questions

* Fetches a dictionary of questions of different categories and answers and also the difficulty level.
* It fetches 10 questions per page.
* Request Argguments: None
* Returns: A Json Object which contains questions, answers, categories and difficulty key value pairs.

```json
{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "current_category": [],
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        } 
    ],
    "success": true,
    "total_questions": 18
}
```
`POST /questions'`
* This endpoint helps user to create a new question.
* Fields: question, answer, category, difficiulty.
* Returns: Sucess values and question ID
Example: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who is Tony Stark?", "answer":"Iron Man", "category":"4", "difficulty":"2"}'

```json
{
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```
`GET '/categories/<category_id>/questions'`
* This endpoint helps user to getch questions based on the category.
* Fields: Category Id
* Returns: Questions filtered by category id.
* Returns 200 as request code if successful, else 404 if the id is not found
Example: curl http://127.0.0.1:5000/categories/1/questions
```json
{
  "Questions":[
    {
      "answer":"Muhammad Ali",
      "category":"1",
      "difficulty":4,
      "id":9,
      "question":"What boxers original name is Cassius Clay?"
      },
      {
        "answer":"Escher",
        "category":"1",
        "difficulty":2,
        "id":16,
        "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        }
        ],
        "Total_Questons_category":2,
        "success":true
        }
```
* Response body for not found record
```json
{
  "error":404,
  "message":"Data not found",
  "success":false
  }
```
`DELETE '/questions/<question_id>'`
* This endpoint helps user to delete question based on the question id.
* Fields: Question_id
* Returns success on deletion of the record.
* Returns 200 as request code if successful, else 404 if the id is not found
Example: curl -X DELETE http://127.0.0.1:5000/questions/4 

```json
{
  "Deleted question":5,
  "Total Questions":18,
  "success":true
}
```
* Response body for not found record
```json
{
  "error":404,
  "message":"Data not found",
  "success":false
  }
```
`POST '/quizzes''`
* This endpoint helps in generating a quiz based on category or a random selection depending on the user choice.
* Returns a random question.
Example: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"type":"Art","id":2}}'

```json
{
  "question": {
    "answer": "One", 
    "category": 2, 
    "difficulty": 4, 
    "id": 18, 
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  }, 
  "success": true
}
```
`POST '/questions/search'`
* This enpoint helps user to search a question.
* Fields: Search term.
* Returns the json body of key value pairs of respective search term question.
* Returns 200 as request code if successful, else 404 if the id is not found.
Example: curl http://127.0.0.1:5000/questions/search?search=what

```json
{
  "Questions":[
    {
      "answer":"Muhammad Ali",
      "category":"1",
      "difficulty":4,
      "id":9,
      "question":"What boxers original name is Cassius Clay?"
      },
      {
        "answer":"Apollo 13",
        "category":"4",
        "difficulty":5,
        "id":2,
        "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
          "answer":"Edward Scissorhands",
          "category":"3",
          "difficulty":5,
          "id":6,
          "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
          },
          {
            "answer":"Lake Victoria",
            "category":"2",
            "difficulty":3,
            "id":13,
            "question":"What is the largest lake in Africa?"
            },
            {
              "answer":"Mona Lisa",
              "category":"3",
              "difficulty":2,
              "id":17,
              "question":"La Giaconda is better known as what?"
              },
              {
                "answer":"The Liver",
                "category":"4",
                "difficulty":1,
                "id":20,
                "question":"What is the heaviest organ in the human body?"
                },
                {
                  "answer":"Blood",
                  "category":"4",
                  "difficulty":1,
                  "id":22,
                  "question":"Hematology is a branch of medicine involving the study of what?"},
                  {
                    "answer":"Stephen Nwankwo",
                    "category":"5",
                    "difficulty":2,
                    "id":1,
                    "question":"what is my name"
                    }
                    ],
                    "success":true
}
```
Error Handlers:

* Erros are handeled and gives a exact response to the user 
200: On successful operation
422: When operation is not proccesseble
404: When the resouce is not found

```json
{
  "error":404,
  "message":"Data not found",
  "success":false
}
```


## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
