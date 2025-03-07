from django.shortcuts import redirect

from django.contrib import messages

def signin_required(fn):

    def wrapper(request,*args,**kwags):

        if not request.user.is_authenticated:

            messages.error(request,"invalid session please login")

            return redirect('signin')
        else:

            return fn(request,*args,**kwags)
        
    return wrapper