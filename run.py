print(">>> run.py başladı")
from app import create_app
print(">>> create_app import edildi")
app = create_app()
print(">>> create_app çalıştı, app.run’a geçiliyor")
if __name__ == "__main__":
    app.run(debug=True)
    print(">>> app.run sonrası")  # bu asla gözükmez, çünkü app.run bloklayıcıdır
