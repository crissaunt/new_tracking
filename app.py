from website import create_app, socketio

app = create_app()
print(app)

if __name__ == "__main__":
     socketio.run(app, host="0.0.0.0", port=8080, debug=True)  # Disable debug mode