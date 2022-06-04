from django.conf import settings
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap

from search import views as search_views

from home import views as home_views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('robots.txt', home_views.RobotsView.as_view()),

]


urlpatterns = urlpatterns + i18n_patterns(
    path('search/', search_views.search, name='search'),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

urlpatterns = urlpatterns + i18n_patterns(
    # path('api/v2/', api_router.urls),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path('', include(wagtail_urls)),
    path('sitemap.xml', sitemap)

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path('pages/', include(wagtail_urls)),
)