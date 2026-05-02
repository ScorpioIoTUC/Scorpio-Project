from src.infra import Logging
import asyncio
from configs.entrypoints import data_clean as config
from src.app.services.data_clean.api import DataCleanAPI


async def main():
    logger = Logging(logger_name="data_clean")
    logger.info("Starting data cleaning service...")
    # Initialize API client
    api = DataCleanAPI()
    try:
        while True:
            logger.info("Performing data cleaning tasks...")
            # Remove uploaded records from the database
            await api.delete_uploaded_records()
            # Wait for the next cleaning cycle
            await asyncio.sleep(config.CLEAN_INTERVAL)
    except Exception as e:
        logger.error(f"Error in data cleaning: {e}")


if __name__ == "__main__":
    asyncio.run(main())
