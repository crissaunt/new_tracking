from website import create_app

app = create_app()
print(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=1234)