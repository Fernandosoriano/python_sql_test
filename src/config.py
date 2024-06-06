class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '1234'
    MYSQL_DB = 'books_db'


config = {
    'development': DevelopmentConfig
}
