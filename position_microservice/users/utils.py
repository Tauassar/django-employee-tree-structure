def get_user_ip(request):
    if request.META.get('HTTP_HOST'):
        ip = request.META.get('HTTP_HOST')
    else:
        ip = ''
    return ip
