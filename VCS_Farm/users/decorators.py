from django.shortcuts import redirect

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        print(f"Session user_id: {user_id}")
        if not user_id:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper