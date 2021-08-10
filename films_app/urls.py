from django.urls import path, include
from .views import *
urlpatterns = [
    path('', FilmHome.as_view(), name='show_items'),
    path('janr/<int:id_janr>/', Films_janr.as_view(), name='janr_items'),
    path('about/<str:slug>/', Disription_film.as_view(), name='discription_item'),
    path('filtr_years/<str:years>/', filtrs_items, name='filtrs_items'),
    path('filtr_country/<str:country>/', filtrs_items_c, name='filtrs_items_c'),
    path('actor/',show_actors, name='show_actors'),
    path('actor/<str:fullName>/', show_about_actor,name='show_about_actor'),
    path('rejicer/', show_rejicer, name='show_rejicer'),
    path('rejicer/<str:fullName>/', show_about_rejicer,name='show_about_rejicer'),
    path('add_film/',addfilm,name='addfilm'),
    path('edit_film/<str:slug>',edit,name='edit'),
    path('delet_film/<str:slug>',delet,name='delet'),
    path('USERFavorites/', user_films, name='user_films'),
    path('addTOfavor/<int:id>', addfilmtofavor,name='addfilmtofavor'),
    path('delfilmfavor/<int:id>',delfilmfavor, name='delfilmfavor'),
    path('register/', register, name='register'),
]