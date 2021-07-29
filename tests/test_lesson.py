from test_base import BaseTestCase
from util import TestUtilities
import json 

from app.models import Lesson, User

class LessonUnitTests(BaseTestCase):
    def test_lesson_listing(self): 
        lesson = Lesson(
            author="username",
            questions=json.dumps({
                "question_1":{
                    "value":"test question",
                    "answers":{
                        "answer_1":{
                            "value":"false answer",
                            "answer": False
                        },
                        "answer_2":{
                            "value":"true answer",
                            "answer" : True
                        }
                    }
                }
            })
        )

        self.db.session.add(lesson) 
        self.db.session.commit()

        response = self.app.get("/lessons", follow_redirects=True)
        self.assertNotIn(b"No lessons found", response.data)


    def test_question_false_answer(self): 
        lesson = Lesson(
            author="username",
            content="{}",
            questions=json.dumps({
                "question_1":{
                    "value":"test question",
                    "answers":{
                        "answer_1":{
                            "value":"false answer",
                            "answer": False
                        },
                        "answer_2":{
                            "value":"true answer",
                            "answer" : True
                        }
                    }
                },
                "question_2":{
                    "value":"another test question",
                    "answers":{
                        "answer_1":{
                            "value":"false answer",
                            "answer":False
                        },
                        "answer_2":{
                            "value":"true answer",
                            "answer":True
                        }
                    }
                }
            }), 
            badge="test_badge",
            badge_url="badge_url"
        )
        #add lesson to the database
        self.db.session.add(lesson)
        self.db.session.commit()

        #register and log the client in
        TestUtilities.register(self.app, "username", "Password1!", "Password1!", "email@test.com")
        TestUtilities.login(self.app, "username", "Password1!")
        
        #check if lesson is actually there
        result = Lesson.query.filter_by(author="username").first()
        self.assertIsNotNone(result)

        #test if the incorrect responses are correctly processed
        response = self.app.post(f"/lessons/{result.id}", data=dict(
            question_1="answer_1",
            question_2="answer_2"
        ))

        self.assertFalse(json.loads(response.data)["question_1"])
        self.assertTrue(json.loads(response.data)["question_2"])

        #ensure the user did not get a badge
        user = User.query.filter_by(username="username").first()
        self.assertEqual(len(json.loads(user.badges_earned)), 0)

    def test_question_true_answer(self): 
        lesson = Lesson(
            author="username",
            content="{}",
            questions=json.dumps({
                "question_1":{
                    "value":"test question",
                    "answers":{
                        "answer_1":{
                            "value":"false answer",
                            "answer": False
                        },
                        "answer_2":{
                            "value":"true answer",
                            "answer" : True
                        }
                    }
                },
                "question_2":{
                    "value":"another test question",
                    "answers":{
                        "answer_1":{
                            "value":"false answer",
                            "answer":False
                        },
                        "answer_2":{
                            "value":"true answer",
                            "answer":True
                        }
                    }
                }
            }), 
            badge="test_badge",
            badge_url="badge_url"
        )
        #add lesson to the database
        self.db.session.add(lesson)
        self.db.session.commit()

        #register and log the client in
        TestUtilities.register(self.app, "username", "Password1!", "Password1!", "email@test.com")
        TestUtilities.login(self.app, "username", "Password1!")

        #check if lesson is actually there
        result = Lesson.query.filter_by(author="username").first()
        self.assertIsNotNone(result)

        #test if the response to the question is correct
        response = self.app.post(f"/lessons/{result.id}", data=dict(
            question_1="answer_2",
            question_2="answer_2"
        ))

        self.assertTrue(json.loads(response.data)["question_1"])
        self.assertTrue(json.loads(response.data)["question_2"])

        #test if user got the badge
        user = User.query.filter_by(username="username").first()
        self.assertGreater(len(json.loads(user.badges_earned)), 0)
        