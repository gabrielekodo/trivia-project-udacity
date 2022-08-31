from ast import Num
from crypt import methods
from numbers import Number
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import collections
from models import setup_db, db, Question, Category
collections.Iterable = collections.abc.Iterable

QUESTIONS_PER_PAGE = 10
CATEGORY_ALL = '0'



def get_ids_from_questions(questions, previous_ids):
    '''
    First create a formatted list of the current questions
    And then compare both list and return a list of ids
    '''
    questions_formatted = [q.format() for q in questions]
    current_ids = [q.get('id') for q in questions_formatted]

    ids = list(set(current_ids).difference(previous_ids))

    return ids

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = {}
        selection = Category.query.all()
        categories_list = [category.format() for category in selection]
        for category in categories_list:
            categories[category['id']] = category['type']

        return jsonify({
            "categories": categories,
            "success":True
        })
    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
    
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories_list = [category.format()
                           for category in Category.query.all()]
        categories = {}

        categories_list = [category.format()
                           for category in Category.query.all()]
        for category in categories_list:
            categories[category['id']] = category['type']

        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(Question.query.all()),
            "categories": categories,
            "current_category": None
        })

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            print(question)

            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "deleted":question_id,
                "total_questions": len(Question.query.all())
            })

        except:
            abort(404)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get('difficulty', None)
        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "totalQuestions": len(Question.query.all()),
                }
            )

        except:
            abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:

            body = request.get_json()

            search_term = body.get("searchTerm", None)
            search_string = '%'+search_term+'%'
            questions_searched = paginate_questions(request, Question.query.filter(
                Question.question.ilike(search_string)).all())

            print(search_term)
            print(questions_searched)
        

            return jsonify({
                "success":True,
                "total_questions": len(questions_searched),
                "questions": questions_searched,
                "current_category": None
            })
        except Exception:
            abort(422)


    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            selection = Question.query.filter(
                Question.category == category_id).order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            current_category = format(Category.query.get(category_id))
            
            if len(current_questions) == 0:
                abort(404)
            return jsonify({
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(selection),
                "currentCategory": int(category_id)
            })
        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/quizzes', methods=['POST'])
    def retrieve_quizzes():
        '''
        Endpoint to get questions to play the quiz.
        '''
        try:
            # Get raw data
            questions = None
            body = request.get_json()
            quiz_category = body.get('quiz_category', None)
            previous_ids = body.get('previous_questions', None)
            category_id = quiz_category.get('id')

            # Check category
            if category_id == CATEGORY_ALL:
                # Get all the questions
                questions = Question.query.all()
            else:
                # Get the questions by the requested category
                questions = Question.query \
                    .filter(Question.category == category_id) \
                    .all()

            # Getting list of ids
            ids = get_ids_from_questions(questions, previous_ids)

            if len(ids) == 0:
                # for empty list return no question
                return jsonify({
                    'success': True,
                    'question': None
                })
            else:
                # Choice a random id
                random_id = random.choice(ids)

                # Get the question
                question = Question.query.get(random_id)

                return jsonify({
                    'success': True,
                    'question': question.format()
                })

        except Exception:
            abort(422)
    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def not_processed(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "request can not be processed"
        }), 422

    @app.errorhandler(400)
    def badrequest(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request "
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app
