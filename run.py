from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Flask başlatılıyor...")
    app.run(debug=True, host="127.0.0.1", port=5050)
