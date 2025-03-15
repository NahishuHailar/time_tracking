test_db_sett = {
    'postgres_user': 'postgres',
    'postgres_password': '4721',
    'postgres_db': 'test_db',
    'db_host': 'localhost',
    'db_port': '5432',
    'db_echo': False
}

# For GitHub Actions
POSTGRES_USER = test_db_sett['postgres_user']
POSTGRES_PASSWORD = test_db_sett['postgres_password']
POSTGRES_DB = test_db_sett['postgres_db']
POSTGRES_HOST = test_db_sett['db_host']
POSTGRES_PORT = test_db_sett['db_port']
