#!/usr/bin/env python3
"""Module for filtering sensitive information from log messages."""
import re
import logging
import mysql.connector
import os
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in the log message.

    Args:
        fields (List[str]): List of strings representing fields to obfuscate.
        redaction (str): String to replace the field values with.
        message (str): Log line to obfuscate.
        separator (str): Character separating fields in the log line.

    Returns:
        str: The obfuscated log message.
    """
    pattern = '({})=.*?{}'.format(
        '|'.join(map(re.escape, fields)),
        re.escape(separator)
    )
    return re.sub(pattern, r'\1=' + redaction + separator, message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class for log obfuscation."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter.

        Args:
            fields (List[str]): List of fields to redact in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record as text.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted and redacted log message.
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Create and configure a logger for user data.

    Returns:
        logging.Logger: A configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Create a connection to the database.

    Returns:
        mysql.connector.connection.MySQLConnection: A database connection
        object.
    """
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )


def main() -> None:
    """
    Retrieve all rows from the users table and display each row in a
    filtered format.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger = get_logger()
    for row in cursor:
        message = "; ".join(f"{field}={value}" for field, value in
                            zip(cursor.column_names, row))
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
