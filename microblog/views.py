# -*- coding: utf-8 -*-
# Create your views here.
from microblog.models import *
from microblog.funcs import *
from microblog.forms import *
import datetime
from django.shortcuts import render_to_response, HttpResponseRedirect

def index(request):
    dict_response = init_dict_response(request)
    logged = dict_response['logged']
    if logged:
        user = dict_response['user']
        d_user = User.objects.get(login=user)
        d_follows = Follow.objects.filter(user=d_user)
        l_users=[]
        for d_follow in d_follows:
            l_users.append(d_follow.follows)
        
        l_posts=[]
        # TODO Ordenar os posts por data, sobrescrevendo o método na classe Post.
        for l_user in l_users:
            d_posts = Post.objects.filter(user=l_user)
            l_posts.extend(d_posts)
                        
        following_list = get_following_list(user)
        followed_list = get_followed_list(user)
        
        print 'following_list = %s' % following_list
        print 'followed_list = %s' % followed_list
    
        dict_response.update({'posts':l_posts, 'following_list':following_list, 'followed_list':followed_list})
        
    return render_to_response('index.html', dict_response)

def login(request):
    dict_response = init_dict_response(request)
    errors = []
    if request.method == 'POST':
        formlogin = LoginForm(request.POST)
        if formlogin.is_valid():
            p_login = request.POST['login']
            p_password = request.POST['password']
            found = True
            try:
                d_user = User.objects.get(login=p_login)
            except (User.DoesNotExist):
                errors.append("E-mail e/ou senha inválidos.")
                found = False
            if (found):
                request.session['user'] = d_user.login
                return HttpResponseRedirect('/')
    else:
        formlogin = LoginForm()
    dict_response.update({'formlogin':formlogin, 'errors':errors})
    
    return render_to_response('login.html', dict_response)

def logout(request):
	request.session.flush()
	
	return HttpResponseRedirect('/')

def signup(request):
    dict_response = init_dict_response(request)
    errors = []
    user = dict_response['user']
    logged = dict_response['logged']
    if request.method == 'POST':
        if logged:
            d_user = User.objects.get(login=user)
            formuser = UserForm(request.POST, request.FILES, instance=d_user)
        else:
            formuser = UserForm(request.POST, request.FILES)
        
        if (formuser.is_valid()):
            d_user = formuser.save(commit=False)
            if not d_user.photo:
                print 'Nao tem foto!'
                d_user.photo = 'img/sem_foto.png'
            if logged:
                if request.FILES:
					try:
						d_user.photo.delete()
					except:
						print 'não tem foto'
            d_user.save()
            if not logged:
                d_follow = Follow(user=d_user, follows=d_user)
                d_follow.save()
                request.session['user'] = d_user.login
            
            return HttpResponseRedirect('/')
    else:
        if logged:
            d_user = User.objects.get(login=user)
            formuser = UserForm(instance=d_user)
        else:
            formuser = UserForm()
        
    dict_response.update({'formuser':formuser})
    return render_to_response('signup.html', dict_response)

def dopost(request):
    dict_response = init_dict_response(request)
    errors = []
    logged = dict_response['logged']
    if request.method == 'POST':
        formpost = PostForm(request.POST)
        if (formpost.is_valid()):
            d_post = formpost.save(commit=False)
            user = dict_response['user']
            d_post.user = User.objects.get(login=user)
            d_post.date = datetime.datetime.now()
            d_post.save()
            
            return HttpResponseRedirect('/')
    else:
        formpost = PostForm()
        
    dict_response.update({'formpost':formpost})
    return render_to_response('dopost.html', dict_response)

def whotofollow(request):
    dict_response = init_dict_response(request)
    user = dict_response['user']
    logged = dict_response['logged']
    
    if request.method == 'GET':
        try:
            term = request.GET['term']
        except (KeyError):
            term = ''
    else:
        term = ''
        
    if (term == ''):
        d_fusers = User.objects.all()
    else:
        d_fusers = User.objects.filter(login__icontains=term)

    following_list = get_following_list(user)
    for d_fuser in d_fusers:
        if d_fuser in following_list:
            d_fuser.followed = True
    
    dict_response.update({'users':d_fusers})
    
    return render_to_response('whotofollow.html', dict_response)

def follow(request):
    dict_response = init_dict_response(request)
    user = dict_response['user']
    logged = dict_response['logged']
    
    if request.method == 'GET':
        try:
            op = request.GET['op']
            tofollow = request.GET['login']
        except (KeyError):
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/error')

    d_user = User.objects.get(login=user)
    d_tofollow = User.objects.get(login=tofollow)
    if op == 'follow':
        f = Follow(user=d_user, follows=d_tofollow)
        f.save()
    elif op == 'unfollow':
        f = Follow.objects.get(user=d_user, follows=d_tofollow)
        f.delete()
    else:
        return HttpResponseRedirect('/error')
    
    return HttpResponseRedirect('/')

def userpage(request):
    dict_response = init_dict_response(request)
    user = dict_response['user']
    logged = dict_response['logged']
    
    if request.method == 'GET':
        try:
            auser = request.GET['auser']
        except (KeyError):
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/error')
        
    d_auser = User.objects.get(login=auser)
    d_posts = Post.objects.filter(user=d_auser)
    
    following_list = get_following_list(auser)
    followed_list = get_followed_list(auser)
    my_following_list = get_following_list(user)

    print 'my_following_list = %s' % my_following_list
    if d_auser in my_following_list:
        print 'ja eh seguido!'
        d_auser.followed = True
    
    dict_response.update({'auser':d_auser, 'posts':d_posts, 'following_list':following_list, 'followed_list':followed_list})
    
    return render_to_response('userpage.html', dict_response)

def search(request):
    dict_response = init_dict_response(request)
    user = dict_response['user']
    logged = dict_response['logged']
    
    if request.method == 'GET':
        try:
            term = request.GET['term']
        except (KeyError):
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/error')
        
    d_posts = Post.objects.filter(message__icontains=term)
    
    dict_response.update({'posts':d_posts, 'term':term})
    return render_to_response('search.html', dict_response)

def error(request):
    dict_response = init_dict_response(request)
    return render_to_response('error.html', dict_response)
