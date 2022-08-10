db = {
    'user': 'root',
    'password': 'mysql',
    'host': '0.0.0.0',
    'port': 3306,
    'database': 'test'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@" \
         f"{db['host']}:{db['port']}/{db['database']}"