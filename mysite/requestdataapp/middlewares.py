import time

from django.core.cache import cache
from django.http import HttpRequest, HttpResponse


def setup_useragent_on_request_on_middleware(get_response):

    print("initial call")

    def middleware(request: HttpRequest):
        print("before")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after")
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("requests_count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses_count", self.responses_count)
        return response

    def process_exceptions(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")


class ThrottlingMiddleware:
    """
    Middleware для ограничения частоты запросов с одного ip
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit_seconds = 0.00001
        self.cache_prefix = "throttle_ip_"

    def __call__(self, request):
        ip = self.get_client_ip(request)
        if ip:
            cache_key = f"{self.cache_prefix}{ip}"
            print("CASH KEYYYYYYYYYYYY", cache_key)
            last_request_time = cache.get(cache_key)

            if last_request_time is not None:
                elapsed = time.time() - last_request_time
                if elapsed < self.rate_limit_seconds:
                    return HttpResponse(
                        "Слишком много запросов",
                        status=429,
                        content_type="text/plain; charset=utf-8"
                    )

            cache.set(cache_key, time.time(), timeout=self.rate_limit_seconds)

        response = self.get_response(request)
        return response

    @classmethod
    def get_client_ip(cls, request):
        """Извлекает реальный ip-адрес из заголовков"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip