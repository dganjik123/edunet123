from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:profile>", views.dashboard, name="dashboard"),
    path("activelisting", views.activelisting, name="activelisting"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("upload/<str:title>", views.upload, name="upload"),
    path("addtowatchlist/<int:product_id>",
         views.addtowatchlist, name="addtowatchlist"),
    path("addcomment/<int:product_id>", views.addcomment, name="addcomment"),
    path("categories", views.categories, name="categories"),
    path("category/<str:categ>", views.category, name="category"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
