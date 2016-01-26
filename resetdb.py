from server import app_db

app_db.drop_all()
app_db.create_all()
