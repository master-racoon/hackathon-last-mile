"""
Example service module.
Put your business logic and external service integrations here.
"""
import logging

logger = logging.getLogger(__name__)


class ExampleService:
    """Example service class for business logic"""
    
    def __init__(self):
        pass
    
    def process_data(self, data: str) -> str:
        """
        Example method to process data.
        Replace with your actual business logic.
        """
        logger.info(f"Processing data: {data}")
        # Your processing logic here
        return data.upper()
