from app import app

if __name__ == "__main__":
    #run using temporary certificates to enable SSL
    app.run(ssl_context=('cert.pem', 'key.pem'))
