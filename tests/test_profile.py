from test_base import BaseTestCase
from util import TestUtilities

from app.models import User, Lesson

import json

class ProfileUnitTests(BaseTestCase): 
    def test_change_email(self):
        TestUtilities.register(self.app, "username", "Password1!", "Password1!", "testing@email.com")
        TestUtilities.login(self.app, "username", "Password1!")

        response = self.app.post("/profile", data=dict(
            email="new_email@gmail.com"
        ), follow_redirects=True)

        self.assertIn(b"Your email has been updated", response.data)

        user = User.query.filter_by(username="username").first()
        self.assertNotEqual(user.email, "testing@gmail.com")

    def test_change_password(self): 
        TestUtilities.register(self.app, "username", "Password1!", "Password1!", "testing@email.com")
        TestUtilities.login(self.app, "username", "Password1!")

        response = self.app.post("/profile", data=dict(
            current_password="Password1!",
            password="Password2!",
            repeat="Password2!"
        ), follow_redirects=True)

        self.assertIn(b"Password has been updated", response.data)
        
    def test_change_username(self): 
        TestUtilities.register(self.app, "username", "Password1!", "Password1!", "testing@email.com")
        TestUtilities.login(self.app, "username", "Password1!")

        response = self.app.post("/profile", data=dict(
            username="username2"
        ), follow_redirects=True)

        self.assertIn(b"Your username has been changed", response.data)
        
        #this should be none because the username would not exist anymore
        user = User.query.filter_by(username="username").first()
        self.assertIsNone(user)

    def test_change_preference(self): 
        TestUtilities.register(self.app, "username", "Password1!", "Password1!", "testing@email.com")
        TestUtilities.login(self.app, "username", "Password1!")

        #add placeholder lessons 
        for i in range(2): 
            lesson = Lesson(
                author="username",
                topic=f"topic_{i}"
            )
            self.db.session.add(lesson)
        self.db.session.commit()

        response = self.app.post("/profile", data=dict(
            {"checkboxes":"topic_1"}
        ), follow_redirects=True)
   
        user = User.query.filter_by(username="username").first()
        self.assertIsNotNone(json.loads(user.preferences))

    def test_delete_account(self): 
        TestUtilities.register(self.app, "username", "Password1!", "Password1!", "testing@email.com")
        TestUtilities.login(self.app, "username", "Password1!")

        response= self.app.post("/profile", data=dict(
            confirmation_field="DELETE_THIS_ACCOUNT"
        ), follow_redirects=True)

        user = User.query.filter_by(username="username").first()
        self.assertIsNone(user)