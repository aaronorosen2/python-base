from django.urls import path
from . import views

urlpatterns = [
    # path('load_neighbor',views.importNeighbours,name='load_neighbor'),
    # path('load_neighbor_zip',views.importNbrWithZip,name='load_neighbor_withzip'),
    path('view_neighbor',views.viewNeighbours,name='view_neighbor'),
    path('fetch_stadiums',views.scrap_stadium,name='scrap_stadium'),
    path('stadiums',views.get_stadiums,name='get_stadiums'),
    # path('scrap_reddits',views.scrap_reddits,name='scrap_reddits'),
    path('get_reddit_posts',views.get_reddit_posts,name='view_reddits'),
    path('get_subreddits',views.get_subreddits,name='view_subreddits'),
    path('state',views.get_states,name='get_states'),
    path('state/<str:state>/city',views.get_cities,name='get_cities'),
    path('state/<str:state>/city/<str:city>',views.get_hoods,name='get_hoods')
]
    
