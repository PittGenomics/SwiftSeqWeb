from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
   url(r'^admin/', include(admin.site.urls)),
   url(r'^', include('swiftseqweb.urls')),
]
# if settings.DEBUG:
#     urlpatterns += ['django.views.static',
#         url(r'^media/(?P<path>.*)', 'serve', {
#             'document_root': settings.MEDIA_ROOT
#         })
#     ]
