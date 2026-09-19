from django.shortcuts import render


def about(request):
    """Страница О проекте."""
    template = 'pages/about.html'
    return render(request, template)


def rules(request):
    """Страница Наши правила."""
    template = 'pages/rules.html'
    return render(request, template)


def csrf_failure(request, reason=''):
    """Страница ошибки CSRF."""
    return render(request, 'pages/403.html', status=403)


def page_not_found(request, exception):
    """Страница 404."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Страница 500."""
    return render(request, 'pages/500.html', status=500)
