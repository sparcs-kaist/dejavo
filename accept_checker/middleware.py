from settings import api_settings

class ContentNegotiator(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (request.path.startswith(api_settings.MEDIA_URL) or \
                request.path.startswith(api_settings.STATIC_URL) or \
                request.path.startswith('/admin')):
            return

        header = request.META.get('HTTP_ACCEPT', '*/*')
        header = request.GET.get('accept', header)

        request.HEADER_LIST = [token.strip() for token in header.split(',')]
        request.ACCEPT_FORMAT = None

        for format_info in api_settings.ACCEPT_FORMAT:
            if format_info[0] in request.HEADER_LIST:
                request.ACCEPT_FORMAT = format_info[1]
                break
