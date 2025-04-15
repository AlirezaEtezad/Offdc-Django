from django.shortcuts import redirect

class RedirectToShopMiddleware:
    """
    Middleware to redirect all requests to the shop page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path is not for the shop page
        if request.path == '/':
            return redirect('/shop/')
        
        # If it is for the shop page, continue processing the request
        response = self.get_response(request)
        return response