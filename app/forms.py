class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Shuai233@localhost:5432/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-strong-and-random-secret-key"