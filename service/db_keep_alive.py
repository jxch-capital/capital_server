import oracledb
import logging


def update():
    try:
        connection = oracledb.connect(
            user="ADMIN",
            password=r"\b^ws7]K!g6(xUEK^Xej",
            dsn="db1_high",
            config_dir=r"../res/Wallet_DB1",
            wallet_location=r"../res/Wallet_DB1",
            wallet_password=r"\b^ws7]K!g6(xUEK^Xej")

        cursor = connection.cursor()

        cursor.execute("UPDATE keep_alive SET update_time = SYSDATE WHERE id = 1")
        connection.commit()

        cursor.close()
        connection.close()
        logging.info(f"keep alive update success.")
    except BaseException:
        logging.error(f"keep alive update failed.")
