import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("SNOWFLAKE_USER")
PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
ACCOUNT = f'{os.getenv("SNOWFLAKE_ORGANIZATION")}-{os.getenv("SNOWFLAKE_ACCOUNT")}'
WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
