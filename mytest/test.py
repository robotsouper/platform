from app import create_app, db

app = create_app()
app.app_context().push()

# Try a simple query
result = db.engine.execute("SELECT 1")
print(result.fetchone())
