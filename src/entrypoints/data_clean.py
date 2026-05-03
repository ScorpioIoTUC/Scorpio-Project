from src.infra import Logging
import asyncio
from configs.entrypoints import data_clean as config
from src.app.services.data_clean.api import DataCleanAPI


async def main():
    logger = Logging(logger_name="entrypoint")
    api = None
    try:
        api = DataCleanAPI()
        logger.info("Starting data cleaning service...")
        while True:
            logger.info("Performing data cleaning tasks...")
            # Remove uploaded records from the database
            await api.delete_uploaded_records()
            # Wait for the next cleaning cycle
            await asyncio.sleep(config.CLEAN_INTERVAL)
    except Exception as e:
        logger.error(f"Error in data cleaning: {e}")
    finally:
        if api is not None:
            await api.db.end_connection()


if __name__ == "__main__":
    asyncio.run(main())
