from django.urls import path
from website.views import Index, Detail, Category, Search, Manage, Login, Logout, SignUp, Personalize, Edit


urlpatterns = [
    path('', Index.as_view()),
    path('post/<id>/', Detail.as_view(), name='news_detail'),
    path('category/<str:category_name>/', Category.as_view()),
    path('search/', Search.as_view()),
    path('manage/', Manage.as_view()),
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('signup/', SignUp.as_view()),
    path('personalize/', Personalize.as_view()),
    path('edit/', Edit.as_view())
]