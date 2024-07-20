from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
import pandas as pd
import snowflake.connector


class CustomSF:
    def __init__(self, key_path):
        self.key_path = key_path

    def connect_to_snowflake_v2(self):
        with open(self.key_path, "rb") as key:
            p_key = serialization.load_pem_private_key(
                key.read(), password=None, backend=default_backend()
            )
        pkb = p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        WAREHOUSE = "ANALYST_PROD_WH"
        DATABASE = "EPIFI_DATALAKE_ALPACA"
        SCHEMA = "USS_STOCKS_ALPACA"
        ROLE = "USSTOCK_ALPACA_DNA_ANALYST_L2"

        conn = snowflake.connector.connect(
            user="kushal@epifi.com",  # Email ID for Users.
            account="aw61665.ap-south-1.aws",
            private_key=pkb,
            warehouse=WAREHOUSE,
            database=DATABASE,
            schema=SCHEMA,
            role=ROLE,
            enable_connection_diag=True,
            connection_diag_log_path="/tmp/diag-tests",
        )

        def run_sql_snowflake(sql: str) -> pd.DataFrame:
            cs = conn.cursor()

            if ROLE is not None:
                cs.execute(f"USE ROLE {ROLE}")

            if WAREHOUSE is not None:
                cs.execute(f"USE WAREHOUSE {WAREHOUSE}")
            cs.execute(f"USE DATABASE {DATABASE}")
            try:

                cur = cs.execute(sql)

                results = cur.fetchall()
            except Exception as e:
                raise e

            # Create a pandas dataframe from the results
            df = pd.DataFrame(results, columns=[desc[0] for desc in cur.description])

            return df

        self.dialect = "Snowflake SQL"
        self.run_sql = run_sql_snowflake
        self.run_sql_is_set = True
