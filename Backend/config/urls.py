from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('estoque.urls')),  # <-- inclui as rotas da app estoque
    path('dashboard/', views.dashboard, name='dashboard')

]
