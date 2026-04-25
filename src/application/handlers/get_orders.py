from cqrs.requests.request_handler import RequestHandler

from src.domain.queries import GetOrdersQuery
from src.utils.logger import logger


class GetOrdersHandler(RequestHandler[GetOrdersQuery, list]):
    async def handle(self, request: GetOrdersQuery) -> list:
        logger.info("Handling GetOrdersQuery")
        return []
