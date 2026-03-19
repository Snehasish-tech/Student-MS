from django.utils.cache import patch_cache_control


class NoCacheHTMLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        content_type = response.get('Content-Type', '')
        if request.method == 'GET' and content_type.startswith('text/html'):
            patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True, max_age=0)
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response['X-UI-Version'] = '2026-03-19-v1'

        return response
