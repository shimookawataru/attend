from django.urls import path
from . import views # ←これ忘れないようにする！！

app_name = 'attend'
urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('err_cause/', views.Err, name="err_cause"),
    path('result_err/', views.result_err, name="result_err"),
    path('result_err/', views.forget, name="forget"),
    path('result_forget/', views.result_forget, name="result_forget")
]
