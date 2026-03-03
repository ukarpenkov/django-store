from django.urls import reverse_lazy

def get_users_url(name):
    """
    Возвращает URL для приложения users с помощью reverse_lazy.
    Используется для избежания повторения reverse_lazy("users:...").
    """
    return reverse_lazy(f"users:{name}")