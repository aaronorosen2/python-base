from django.urls import path
from . import views

urlpatterns = [
    # path('load_neighbor',views.importNeighbours,name='load_neighbor'),
    path('view_neighbor',views.viewNeighbours,name='view_neighbor'),
    path('state',views.get_states,name='get_states'),
    # path('state/<str:state>',views.get_cities,name='get_cities'),
    # path('state/<str:state>/city/<str:city>',views.get_hoods,name='get_hoods')
]
    
