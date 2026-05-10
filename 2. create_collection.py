from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

# Load environment variables
load_dotenv()

# MongoDB Atlas credentials and configuration
username = quote_plus(os.getenv("MONGO_ATLAS_USERNAME"))
password = quote_plus(os.getenv("MONGO_ATLAS_PASSWORD"))
cluster = os.getenv("MONGO_ATLAS_CLUSTER")
app_name = os.getenv("MONGO_ATLAS_APP_NAME", "app")

db_name = os.getenv("MONGO_DB_ATLAS")
source_collection_name = os.getenv("MONGO_ORIGINAL_COLLECTION_ATLAS")
target_collection_name = os.getenv("MONGO_MODIFIED_COLLECTION_ATLAS")

# Build connection string
mongo_uri = (
    f"mongodb+srv://{username}:{password}@{cluster}/"
    f"{db_name}?retryWrites=true&w=majority&appName={app_name}"
)


def create_transformed_collection() -> None:
    """
    Creates a refined MongoDB collection using an aggregation pipeline.
    The pipeline filters, reshapes, and stores the result into a new collection.
    """

    client = MongoClient(mongo_uri)
    db = client[db_name]

    source_collection = db[source_collection_name]

    # Aggregation pipeline: filter, reshape, and export results
    pipeline = [
        {
            "$match": {
                "scans": {"$exists": True, "$not": {"$size": 0}}
            }
        },
        {
            "$project": {
                "_id": "$sha256",
                "vhash": 1,
                "tags": 1,
                "scans": 1,
                "exif": "$additional_info.exiftool",
                "trid": "$additional_info.trid",
                "androguard": "$additional_info.androguard",
                "extensions": "$additional_info.compressedview.extensions",
            }
        },
        {
            "$out": target_collection_name
        }
    ]

    try:
        print("Running aggregation pipeline on MongoDB server...")

        # Executes the pipeline and creates/overwrites the target collection
        source_collection.aggregate(pipeline)

        total_docs = db[target_collection_name].count_documents({})
        print(f"Success: '{target_collection_name}' created with {total_docs} documents.")

    except Exception as error:
        print(f"Aggregation error: {error}")

    finally:
        client.close()


if __name__ == "__main__":
    create_transformed_collection()