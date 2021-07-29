from test_base import BaseTestCase
from util import TestUtilities

class AuthUnitTests(BaseTestCase): 
    def test_register_fail(self): 
        response = TestUtilities.register(self.app, "username", "password1", "Pass!1!", "testing@gmail.com")
        self.assertIn(b'Invalid details', response.data)

    def test_register_success(self): 
        response = TestUtilities.register(self.app, "username", "Password1!", "Password1!", "email@test.com")
        self.assertIn(b"Successfully registered", response.data)

    def test_login_fail(self):
        response = TestUtilities.login(self.app, "username", "invalid_password")
        self.assertIn(b"Invalid username or password", response.data)

    def test_login_success(self): 
        username = "correctusername"
        password = "CorrectPassword1!"

        TestUtilities.register(self.app, username, password, password, "email@testing.com")
        response = TestUtilities.login(self.app, username, password)
        self.assertNotIn(b"Invalid username or password", response.data)

    def test_logout(self): 
        TestUtilities.register(self.app, "username", "Password1!", "Password1!", "email@testing.com")
        TestUtilities.login(self.app, "username",  "Password1!")

        response = self.app.get("/logout")
        self.assertEqual(response.status_code, 302)
