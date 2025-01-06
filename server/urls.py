from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from django.conf.urls.static import static

from django.conf import settings
from rest_framework.routers import DefaultRouter
from api.views import QuestionViewSet

router = DefaultRouter()
router.register(r"questions", QuestionViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Quiz API",
        default_version="v1",
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="emekadefirst@gmail.com"),
        license=openapi.License(name="Emekedefirst"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(
        r"^$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("api/", include("api.urls")),
]
if settings.DEBUG == False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
