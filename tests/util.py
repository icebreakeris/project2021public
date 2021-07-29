
class TestUtilities(): 
    @staticmethod
    def register(client, username, password, repeat, email): 
        return client.post("/register", data=dict(
            username=username,
            email=email,
            password=password,
            repeat=repeat
        ), follow_redirects=True)

    @staticmethod
    def login(client, username, password): 
        return client.post("/login", data=dict(
            username=username,
            password=password
        ), follow_redirects=True)