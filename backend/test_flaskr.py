import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr.app import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:newpassword@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions(self):
        result = self.client().get('/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_get_categories(self):
        result = self.client().get('/categories')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
    
    def test_delete_question(self):
        result = self.client().delete('/questions/5')
        data = json.loads(result.data)

        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question_id'], 2)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['question_deleted'])
        self.assertEqual(question, None)
    
    def test_404_delete_question_not_found(self):
        result = self.client().get('/questions/100')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Data not found')
    
    def test_add_new_question(self):
        result = self.client().post('/questions', json=self.new_question)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])
    
    def test_get_question_search(self):
        res = self.client().post('/questions/search', json={"search_term": "question"})
        search_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(search_data['success'], True)
        self.assertTrue(search_data['questions'])
        self.assertTrue(search_data['total_questions'])

    def test_404_search_question_not_found(self):
        result = self.client().post('/questions/search', json={"search_term": " Maya Angelou"})
        search_data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(search_data['success'], False)
        self.assertEqual(search_data['message'], 'Data not found')

    def test_get_questions_by_category(self):
        result = self.client().get('/categories/4/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    
    def test_404_get_questions_invalid_categories(self):
        result = self.client().get('/categories/10/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_405_if_book_creation_not_allowed(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request cannot be processed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()