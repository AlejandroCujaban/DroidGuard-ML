import os
import json
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pymongo import MongoClient, InsertOne


# Load environment variables
load_dotenv()

# MongoDB Atlas credentials and configuration
username = quote_plus(os.getenv("MONGO_ATLAS_USERNAME"))
password = quote_plus(os.getenv("MONGO_ATLAS_PASSWORD"))
cluster = os.getenv("MONGO_ATLAS_CLUSTER")
app_name = os.getenv("MONGO_ATLAS_APP_NAME", "app")
db_name = os.getenv("MONGO_DB_ATLAS")
collection_name = os.getenv("MONGO_ORIGINAL_COLLECTION_ATLAS")

# Build MongoDB connection string
mongo_uri = (
    f"mongodb+srv://{username}:{password}@{cluster}/"
    f"{db_name}?retryWrites=true&w=majority&appName={app_name}"
)


def upload_to_atlas(json_folder: str) -> None:
    """
    Loads all JSON files from a folder and uploads them to MongoDB Atlas
    using bulk insert operations.
    """

    client = MongoClient(mongo_uri)
    collection = client[db_name][collection_name]

    operations = []

    # Read all JSON files from the folder
    for filename in os.listdir(json_folder):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(json_folder, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                document = json.load(file)
                operations.append(InsertOne(document))

        except json.JSONDecodeError:
            print(f"Invalid JSON file skipped: {filename}")
        except OSError:
            print(f"Could not read file: {filename}")

    # Execute bulk insert if there is data
    if not operations:
        print("No valid JSON files found.")
        return

    try:
        result = collection.bulk_write(operations)

        print(f"Upload completed: {result.inserted_count} documents inserted.")

        # Create index to optimize queries by country field
        collection.create_index([("submission.submitter_country", 1)])
        print("Index created on 'submission.submitter_country'.")

    except Exception as error:
        print(f"Error during bulk upload: {error}")

    finally:
        client.close()


if __name__ == "__main__":
    JSON_PATH = "./Data"
    upload_to_atlas(JSON_PATH)