from microblog.models import *
from settings import MEDIA_URL

def get_user(request):
    try:
        user = request.session['user']
    except (KeyError):
        request.session['user'] = 'guest'
        request.session.set_expiry(0)
        user = request.session['user']
    
    return user

def init_dict_response(request):
    user = get_user(request)
    
    d_user = ''
    if user != 'guest':
        logged = True
        d_user = User.objects.get(login=user)
    else:
        logged = False
        
    dict_response = {'user': user, 'd_user': d_user, 'logged': logged, 'media_url': MEDIA_URL}

    return dict_response

def get_following_list(auser):
    following_list = []
    d_user = User.objects.get(login=auser)
    d_follows = Follow.objects.filter(user=d_user)
    for d_follow in d_follows:
        if d_follow.follows != d_user:
            following_list.append(d_follow.follows)
    
    return following_list

def get_followed_list(auser):
    followed_list = []
    d_user = User.objects.get(login=auser)
    d_follows = Follow.objects.filter(follows=d_user)
    for d_follow in d_follows:
        if d_follow.user != d_user:
            followed_list.append(d_follow.user)
    
    return followed_list        
