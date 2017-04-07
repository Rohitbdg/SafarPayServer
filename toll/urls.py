from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^getaccesstoken$', views.getaccesstoken, name='getaccesstoken'),
    url(r'^authenticate$', views.authenticate, name='authenticate'),
    url(r'^check_recharge$', views.check_recharge, name='check_recharge'),
    url(r'^demo$', views.demo, name='demo'),
    url(r'^validate_user$', views.validate_user, name='validate_user'),
    url(r'^update_bal$', views.update_bal, name='update_bal'),
    url(r'^get_toll_details$', views.get_toll_details, name='get_toll_details'),
    url(r'^get_new_balance$', views.get_new_balance, name='get_new_balance'),
]
