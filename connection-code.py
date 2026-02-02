"""
Reference MongoDB connection file
---------------------------------
⚠️ This file is for demonstration/reference purposes only.
Credentials are loaded from environment variables.
"""

import os
from pymongo import MongoClient


def get_database():
    """
    Connects to MongoDB using a connection string
    stored in an environment variable.
    """

    # MongoDB connection string (DO NOT hardcode credentials)
    CONNECTION_STRING = os.getenv("MONGODB_URI")

    if not CONNECTION_STRING:
        raise ValueError(
            "MONGODB_URI environment variable not set"
        )

    # Create MongoDB client
    client = MongoClient(CONNECTION_STRING)

    # Return database reference
    return client["user_shopping_list"]


# Allow reuse across multiple files
if __name__ == "__main__":
    dbname = get_database()
    print("Database connection successful (reference check)")
