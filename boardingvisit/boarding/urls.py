from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [   
	path('', views.index, name='index'), 	
	path('visit_table_data', views.visit_table_data, name='visit_table_data'), 	
	path('generate_data', views.generate_data, name='generate_data'),
	path('check_visit_date', views.check_visit_date, name='check_visit_date'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)