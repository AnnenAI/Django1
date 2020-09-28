from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


def check_yourself_dialogue(func):
    @wraps(func)
    def wrapper(request,*args, **kwargs):
        print(kwargs['pk'])
        print(request.user.id)
        if request.user.id == kwargs['pk']:
            url = reverse_lazy('dialogue')
            return HttpResponseRedirect(url)
        return func(request,*args, **kwargs)
    return wrapper
