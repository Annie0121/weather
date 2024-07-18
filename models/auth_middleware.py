from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next): 
        if request.url.path.startswith("/static/") or request.url.path.startswith("/api") or request.url.path.startswith("/city") :
            return await call_next(request)
        if request.url.path not in ["/", '/docs']:
            return RedirectResponse(url='/')
        return await call_next(request)