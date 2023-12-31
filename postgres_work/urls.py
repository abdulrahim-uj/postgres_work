from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from basics import views as general_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # BASICS
    path('', general_views.home, name="index"),
    # ACCOUNTS
    path('auth/', include('accounts.urls', namespace="authentication_accounts")),
    # TASKLISTS
    path('task/', include('tasklists.urls', namespace="tasklists")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
