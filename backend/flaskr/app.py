import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
db = SQLAlchemy()

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})
  
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    # Define pagination method

    def paginate_selection(request,selection):
        page = request.args.get('page',1,type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_question = questions[start:end]

        return current_question
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    # Get endpoints for questions

    @app.route('/questions')
    def get_questions():
        try:
            select_questions = Question.query.order_by(Question.id).all()
            cur_questions= paginate_selection(request,select_questions)
            curr_categories=[]
            categories = Category.query.all()
            for i in categories:
                curr_categories.append({
                    'id':i.id,
                    'type':i.type
                })
            print("cur que:",cur_questions)
            print("_________cur_categories:",curr_categories)
            if len(cur_questions) ==0:
                abort(404)
            else:    
                return jsonify({
                    'success':True,
                    'questions':cur_questions,
                    'total_questions': len(Question.query.all()),
                    'categories':curr_categories
                })
        except Exception as e:
            print("get question exception",e)
        
     # Get endpoints for categories
    @app.route('/categories')
    def get_categories():
        curr_categories=[]
        categories = Category.query.all()
        for i in categories:
            curr_categories.append({
                    'id':i.id,
                    'type':i.type
                })

        if len(categories) == 0:
            abort(404)
        print("cate:",categories)
        return jsonify({
        'success': True,
        'categories': categories
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>',methods=["DELETE"])
    def delete_questions(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)
            question.delete()

            return jsonify({
                'success':True,
                'Deleted question':question_id,
                'Total Questions':len(Question.query.all())
            })
        except Exception as e:
            print("Delete Exception:",e)
            abort(422)
    
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions',methods=["POST"])
    def create_question():
        body = request.get_json()
        new_question = body.get('question')
        new_answer =  body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')

        if(new_question or new_answer or new_category or new_difficulty) == None:
            abort(422)
        try:    
            ques = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)   
            ques.insert()

            selection = Question.query.order_by(Question.id).all()
            new_questions = paginate_selection(request,selection)
            return jsonify({
                'success':True,
                'New_question_ID':Question.id,
                'curr_questions':new_questions,
                'Total_Questions':len(Question.quuery.all())
            })
        except Exception as e:
            print("Exception as e:",e)
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search')
    def search_questions():
        search_ques = request.args.get('search')
        if search_ques is None:
            abort(422)
        selection = Question.query.filter(Question.question.ilike(f'%{search_ques}%')).all()
        if selection is None:
            abort(404)
        search_questions = paginate_selection(request, selection)
        return jsonify({
            'success':True,
            'Questions':list(search_questions)
        })
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_categories_questions(category_id):
        try:
            select_question = Question.query.filter(Question.category==str(category_id)).all()
            print("Select:",select_question)
            paginate_question = paginate_selection(request,select_question)
            return jsonify({
                'success':True,
                'Questions':paginate_question,
                'Total_Questons_category':len(select_question)
            })
        except:
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes',methods=["POST"])
    def play_trivia():
        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            if (quiz_category or previous_questions) == None:
                abort(422)
            if quiz_category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
                available_questions = Question.query.filter_by(
                    category=quiz_category['id']).filter(Question.id.notin_((previous_questions))).all()

            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(available_questions) > 0 else None

            return jsonify({
                'success': True,
                'question': new_question
            })  
        except:
            abort(422)  
            
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return( 
            jsonify({'success': False, 'error': 404,'message': 'Data not found'}),
            404
        )
    
    @app.errorhandler(422)
    def unprocessed(error):
        return( 
            jsonify({'success': False, 'error': 404,'message': 'The request can not be processed'}),
            422
        )
    return app


    
