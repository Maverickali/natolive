from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    
    path('admin/', admin.site.urls),          # Django admin route 
    path("", include("authentication.urls")), # Auth routes - login / register
    path("", include("app.urls")),             # UI Kits Html files
    path("", include("id_manager.urls")),             # ID Manager
    path("", include("reporting.urls")),          # reporting
    path("", include("eod.urls")),
    path("", include("clusters.urls"))
        
]
