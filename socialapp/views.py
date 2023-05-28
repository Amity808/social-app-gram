from django.shortcuts import render, redirect
from django.http import HttpResponse
# we need to import user model
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Post, LikePost, FollowersCount
from itertools import chain
# Create your views here.
# import messages
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    post_feed = Post.objects.all()
    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    return render(request, 'index.html', {'user_profile': user_profile, 'post_feed': feed_list})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            # if the email is alreadly exist
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already Exist')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Useraname already exist. choose another username')
                redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in and redirect to setting page
                # this is will automatically login the user and redirect to seetings
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                # create profile object for new user

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password not match')
            return redirect('signup')
    else:
        return render(request, 'signup.html') 
    

def signin(request):

  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Crendentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
    

@login_required(login_url='signin')
def settings(request):

    users_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':

        if request.FILES.get('image') == None:
            # if there is no image been sent
            # when submiting a form we need to have enctype in our html form 
            image = users_profile.profileimg
            bio = request.POST['bio']
            loaction = request.POST['location']

            users_profile.profileimg = image
            users_profile.bio = bio
            users_profile.location = loaction
            users_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            loaction = request.POST['location']

            users_profile.profileimg = image
            users_profile.bio = bio
            users_profile.location = loaction
            users_profile.save()

        return redirect('settings')


    return render(request, 'setting.html', {'users_profile': users_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
        pass
    else:
        return redirect('/')
    

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    # to get the id of the post that the user want to like
    post = Post.objects.get(id=post_id)

    # to filter if tyhe user already like the post
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_like = post.no_of_like + 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_like = post.no_of_like -1
        post.save()
        return redirect('/')
    
@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=pk)
    user_post_lenght = len(user_post)

    follower = request.user.username
    user = pk
    # if folloer already exist we try to make it display follow or unfollow
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_follower = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_post': user_post,
        'user_post_lenght': user_post_lenght,
        'button_text': button_text,
        'user_follower': user_follower,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follow = FollowersCount.objects.create(follower=follower, user=user)
            new_follow.save()
            return redirect('/profile/'+user)
    else:

        return redirect('/')
    

def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username_icontain=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in user_profile:
            profile_list = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_list)
        username_profile_list = list(chain(*username_profile_list))
    # return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
    pass