from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from SHOP.api import router as api_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("SHOP.urls")),
    path("user/", include("USER.urls")),
    path("api/", include(api_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
