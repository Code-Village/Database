db = {
    'user': 'root',
    'password': 'mysql',
    'host': 'localhost',
    'port': 3306,
    'database': 'test'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@" \
         f"{db['host']}:{db['port']}/{db['database']}"