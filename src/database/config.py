db = {
    'user': 'cmckxe4j83zhap35',
    'password': 'zaqwef7wzmt0ciir',
    'host': 'cxmgkzhk95kfgbq4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
    'port': 3306,
    'database': 'crxhrzme3der287f'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@" \
         f"{db['host']}:{db['port']}/{db['database']}"