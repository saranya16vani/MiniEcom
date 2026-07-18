from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from SHOP.api import router as api_router
from SHOP import views

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", views.home, name="home"),       # homepage
#     path("shop/", include("SHOP.urls")),     # shop routes
#     path("user/", include("USER.urls")),     # user routes
#     path("api/", include(api_router.urls)),  # API routes
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),   # homepage
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)