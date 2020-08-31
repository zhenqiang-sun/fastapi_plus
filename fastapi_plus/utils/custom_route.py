from typing import Callable

from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

from .request_log import create_log, update_log


class CustomRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request.state.log = await create_log(request)
            response = await original_route_handler(request)
            await update_log(request.state.log, response)
            return response

        return custom_route_handler
