# Full Stack API Final Project


## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where I come in to help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


### Backend

## Endpoints

### GET `/categories`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request arguments: None.
- Returns:  An object with these keys:
  - `success`: The success flag
  - `categories`: Contains a object of `id:category_string` and `key:value pairs`.

```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

### GET `/questions`
- Fetches:
  - A list of questions (paginated by 10 items)
  - A dictionary of categories
  - The total of questions
  - The current category
- Request arguments:
  - `page` (integer) - The current page
- Returns: An object with these keys:
  - `success`: The success flag
  - `questions`: A list of questions (paginated by 10 items)
  - `categories`: A dictionary of categories
  - `total_questions`: The total of questions
  - `current_category`: The current category

```json
{
  "success": true,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
  ],
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "total_questions": 10,
  "current_category": null,
}
```

### DELETE `/questions/:question_id/`
- Delete question using a question ID
- Request arguments:
  - `question_id` (integer): The question id
- Returns: An object with theses keys:
  - `success` that contains a `boolean`.
  - `deleted` that contains the ID of the question created.

```json
{
  "success": true,
  "deleted": 1,
}
```

### POST `/questions`
- Create a new question.
- Request arguments:
  - `question` (string) - The question
  - `answer` (string) - The answer
  - `difficulty` (string) - The question difficulty
  - `category` (string) - The question category
- Returns: An object with theses keys:
  - `success` that contains a `boolean`.
  - `created` that contains the ID of the question created.

```json
{
  "success": true,
  "created": 1,
}
```

### POST `questions/search`
- Search a question.
- Request arguments:
  - `search` (string) - The term to search
- Returns: An object with these keys:
  - `success`: The success flag
  - `questions`: A list of questions
  - `total_questions`: The total of questions
  - `current_category`: The current category

```json
{
  "success": true,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
  ],
  "total_questions": 10,
  "current_category": null,
}
```


### GET `/categories/:category_id/questions`
- Fetches a list of questions based on category.
- Request arguments:
  - `category_id` (integer): The category id
- Returns: An object with these keys:
  - `success`: The success flag
  - `questions`: A list of questions (paginated by 10 items)
  - `total_questions`: The total of questions
  - `current_category`: The current category

```json
{
  "success": true,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
  ],
  "total_questions": 10,
  "current_category": 1,
}
```

### POST `/quizzes`
- Fetches a question to play the quiz.
- Request arguments:
  - `quiz_category` (dictionary): The quiz category with the `type` and the `id`.
  - `previous_ids` (list of strings): The previous questions ids
- Returns: An object with these keys:
  - `success`: The success flag
  - `question`: The question to play

```json
{
  "success": true,
  "question":{
    "answer": "Apollo 13",
    "category": 5,
    "difficulty": 4,
    "id": 2,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }
}
```

## Errors

### Error 400
- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 400,
  "message": "bad request"
}
```

### Error 404
- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
```

### Error 422
- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 422,
  "message": "request can not be processed"
}
```

### Error 500
- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 500,
  "message": "internal server error"
}
```



