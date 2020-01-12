from django.db import IntegrityError
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.http.response import HttpResponse, HttpResponseRedirect
from common.models import News
from common import models
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User



class Index(View):

    def get(self, request):

        str = ''
        # get root categories from database
        if request.user.is_authenticated:
            root_categories_query_set = models.Category.objects.filter(user=request.user).values('name')
        else:
            root_categories_query_set = News.objects.values('root_category').distinct()
        root_categories = [root_cat.get('root_category', None) or root_cat['name'] for root_cat in root_categories_query_set]

        # get latest news from database
        latest_news_query_set = News.objects.all().order_by('-publish_date', '-publish_time')[:8]
        latest_news = [lat_news for lat_news in latest_news_query_set]

        # get latest news from each root category
        latest_news_on_each_category = {}
        for root_category in root_categories:
            latest_news_on_cat = News.objects\
                .filter(root_category=root_category)\
                .order_by('-view_count', '-publish_date', '-publish_time')[:4]
            latest_news_on_each_category[root_category] = [news for news in latest_news_on_cat]

        # get important posts slide bar
        important_posts_slide_bar_query_set = News.objects.all().order_by('-publish_date', '-publish_time')[:5]
        important_posts_slide_bar = [item for item in important_posts_slide_bar_query_set]

        # get important post
        important_posts_query_set = News.objects.all().order_by('-publish_date', '-publish_time')[:2]
        important_posts = [item for item in important_posts_query_set]

        context = {
            'latest_news': latest_news,
            'latest_news_on_each_category': latest_news_on_each_category,
            'important_posts_slide_bar': important_posts_slide_bar,
            'important_post': important_posts
        }

        return render(
            request,
            'index.html',
            context=context
        )


class Detail(View):

    def get(self, request, id):
        post = News.objects.get(id=id)
        post.view_count += 1
        post.save()

        context = {
            'post': post
        }

        return render(
            request,
            'detail.html',
            context=context
        )


class Category(ListView):

    model = News
    paginate_by = 20
    template_name = 'category_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        queryset = News.objects.filter(root_category=category_name).order_by('-publish_date', '-publish_time')
        self.extra_context = {'category_name': category_name}
        return queryset


class Search(ListView):
    model = News
    paginate_by = 20
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = []
        if query:
            queryset = News.objects.filter(title__contains=query)
        self.extra_context = {'query': query}
        return queryset


class Manage(View):


    def get(self, request):
        if request.user.is_authenticated:
            user: User = request.user
            if user.is_staff:
                if request.GET:
                    post = News.objects.get(id=request.GET.get('news_id'))
                    return render(request, 'edit.html', context={'post': post})
                else:
                    return render(request, 'adminlog.html')
        return HttpResponse('You dont have access.')


    def post(self, request):
        if request.user.is_authenticated:
            user: User = request.user
            if user.is_staff:
                title = request.POST.get('title')
                category = request.POST.get('category')
                body = request.POST.get('body')
                image = request.POST.get('image')
                News.objects.update_or_create(
                    title=title,
                    body=body,
                    root_category=category,
                    image=image,
                )
                return HttpResponseRedirect('/')

        return HttpResponse('You dont have access.')

class Edit(View):

    def get(self, request):
        if request.user.is_authenticated:
            user: User = request.user
            if user.is_staff:
                if request.GET:
                    post = News.objects.get(id=request.GET.get('news_id'))
                    return render(request, 'edit.html', context={'post': post})
        return HttpResponse('You dont have access.')

    def post(self, request):
        if request.user.is_authenticated:
            user: User = request.user
            if user.is_staff:
                title = request.POST.get('title')
                category = request.POST.get('category')
                body = request.POST.get('body')
                image = request.POST.get('image')
                id = request.POST.get('id')
                post: News = News.objects.get(id=id)
                post.title = title
                post.body = body
                post.root_category = category
                post.image = image
                post.save()
                return HttpResponseRedirect('/manage/')

        return HttpResponse('You dont have access.')


class SetFavoriteCategory(View):

    def post(self, request):
        pass


class Login(LoginView):
    template_name = 'index.html'

class Logout(LogoutView):
    template_name = 'index.html'
    next_page = '/'

class SignUp(View):

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email')

        try:
            user: User = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        except IntegrityError:
            return HttpResponse('Failure')

        return HttpResponse('True')


class Personalize(View):

    def post(self, request):
        selected_categories = request.POST.getlist('selected_categories', '')
        user: User = request.user
        user_categories = models.Category.objects.filter(user=user)
        for cat in user_categories:
            cat.delete()
        for cat in selected_categories:
            models.Category.objects.create(name=cat, user=user)

        return HttpResponseRedirect('/')