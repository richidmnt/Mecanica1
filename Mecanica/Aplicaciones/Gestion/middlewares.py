# middlewares.py
from .models import Usuario

class CustomUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'id_usr' in request.session:
            try:
                request.user = Usuario.objects.get(id_usr=request.session['id_usr'])
            except Usuario.DoesNotExist:
                request.user = None
        else:
            request.user = None
        response = self.get_response(request)
        return response
