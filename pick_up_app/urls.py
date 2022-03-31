from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('pick_up_app/', include('pick_up_app.urls')),
    path('admin/', admin.site.urls),
] 
