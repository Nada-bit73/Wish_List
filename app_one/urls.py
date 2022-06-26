from django.urls import path
from . import views
#urlpatterns => static name
urlpatterns = [
    path('', views.index), 
    path('register', views.register),  
    path('login', views.login),  
    path('displayList', views.displayList),
    path('viewItem/<int:itemId>', views.viewItem, name="viewItem"),  
    path('delete/<int:itemId>', views.deleteItem , name="deleteItem"),
    path('remove/<int:itemId>', views.removeItem , name="removeItem"),
    path('addFavWish/<int:itemId>', views.addToFavWish , name="addToFavWish"),
    path('viewAddWish', views.viewAddWish),
    path('addWish', views.addToWish),
    path('logout', views.logout),    
]


# username: N@123 , pw: 12hH@gg5
# username: S@123 , pw: gr3at@3wdsG
