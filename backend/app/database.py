import motor.motor_asyncio
from beanie import init_beanie
from .security import settings
# --- THIS IS THE CRITICAL CHANGE ---
# Import the new LoginHistory model
from .models import User, LoginHistory
# --- END OF CHANGE ---

async def init_db():
    """
    Initializes the database connection and the Beanie ODM.
    This function is called once when the FastAPI application starts up.
    """
    # Create a new asynchronous client to connect to MongoDB.
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)

    # --- THIS IS THE CRITICAL CHANGE ---
    # Add the LoginHistory model to the list of documents for Beanie to manage.
    await init_beanie(database=client.get_default_database(), document_models=[User, LoginHistory])
    # --- END OF CHANGE ---
