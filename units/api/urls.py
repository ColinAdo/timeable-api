from django.urls import path

from .views import UnitUploadView

urlpatterns = [
    path('upload/', UnitUploadView.as_view(), name='upload')
]
# urlpatterns = [
#     # ...
#     re_path(r'^upload/(?P<filename>[^/]+)$', UnitUploadView.as_view())
# ]
