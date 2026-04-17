"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from.import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("",views.home,name='home'),
    path("base", views.base, name='base'),
    path("add_category", views.add_category, name='add_category'),
path("add_category_expert_link", views.add_category_expert_link, name='add_category_expert_link'),
path("add_category_expert", views.add_category_expert, name='add_category_expert'),
path("view_category_expert", views.view_category_expert, name='view_category_expert'),

    path('add_category_link',views.add_category_link,name='add_category_link'),
    path("view_category", views.view_category, name='view_category'),
    path("edit_category/<str:id>", views.edit_category, name='edit_category'),
    path("update_category", views.update_category, name='update_category'),
    path("delete_category/<str:id>", views.delete_category, name='delete_category'),

    path("add_fabrics", views.add_fabrics, name='add_fabrics'),
    path("add_fabrics_link/<str:id>", views.add_fabrics_link, name='add_fabrics_link'),

    path("view_fabrics/<str:id>", views.view_fabrics, name='view_fabrics'),
    path("edit_fabrics/<str:f_id>", views.edit_fabrics, name='edit_fabrics'),
    path("update_fabrics", views.update_fabrics, name='update_fabrics'),
    path("delete_fabrics/<str:f_id>", views.delete_fabrics, name='delete_fabrics'),

    path("add_shirt_parts", views.add_shirt_parts, name='add_shirt_parts'),
    path('add_parts_link',views.add_parts_link,name='add_parts_link'),
    path('view_parts', views.view_parts, name='view_parts'),
    path('edit_parts/<str:p_id>', views.edit_parts, name='edit_parts'),
    path('update_parts', views.update_parts, name='update_parts'),
    path('delete_parts/<str:p_id>', views.delete_parts, name='delete_parts'),
    path('view_category_user',views.view_category_user,name='view_category_user'),
    path('view_fabrics_user/<str:id>',views.view_fabrics_user,name='view_fabrics_user'),
    path('select_part_by_user/<str:id>/<str:cname>',views.select_part_by_user,name='select_part_by_user'),
    path('add_parts_image', views.add_parts_image, name='add_parts_image'),
    path('add_parts_image_link/<str:p_id>', views.add_parts_image_link, name='add_parts_image_link'),

    path('measurements_link', views.measurements_link, name='measurements_link'),

    path('admin_view_measurements_link/<str:id>', views.admin_view_measurements_link, name='admin_view_measurements_link'),
    path('expert_view_measurements_link/<str:id>', views.expert_view_measurements_link, name='expert_view_measurements_link'),
    path('view_parts_image', views.view_parts_image, name='view_parts_image'),

    path('work_completed/<str:id>', views.work_completed, name='work_completed'),
    path('expert_work_completed/<str:id>', views.expert_work_completed, name='expert_work_completed'),
    path('date_changed/<str:id>', views.date_changed, name='date_changed'),
    path('expert_date_changed/<str:id>', views.expert_date_changed, name='expert_date_changed'),
    path('edit_parts_image/<str:image_id>', views.edit_parts_image, name='edit_parts_image'),
    path('update_parts_image', views.update_parts_image, name='update_parts_image'),
    path('delete_parts_image/<str:image_id>', views.delete_parts_image, name='delete_parts_image'),

    path('view_shirt_part/<str:p_id>', views.view_shirt_part, name='view_shirt_part'),
    path('view_parts_image_user/<str:p_id>/<str:p_name>',views.view_parts_image_user,name='view_parts_image_user'),
    path('view_selection', views.view_selection, name='view_selection'),





    path("expert_home", views.expert_home, name='expert_home'),
    path("admin_home", views.admin_home, name='admin_home'),
    path("navigation_design", views.navigation_design, name='navigation_design'),

    path("navbar", views.navbar, name='navbar'),
    path("view_part_user", views.view_part_user, name='view_part_user'),

    path("user_nav", views.user_nav, name='user_nav'),
    path("user_rec", views.user_rec, name='user_rec'),
    path("user_home", views.user_home, name='user_home'),
    path("login", views.login, name='login'),
    path("view_measurements", views.view_measurements, name='view_measurements'),
    path("add_measurements", views.add_measurements, name='add_measurements'),
    path("view_measurements", views.view_measurements, name='view_measurements'),
    path("login_link", views.login_link, name='login_link'),
 path("admin_view_feedback", views.admin_view_feedback, name='admin_view_feedback'),
path("send_feedback", views.send_feedback, name='send_feedback'),
    path("admin_view_cancel_order", views.admin_view_cancel_order, name='admin_view_cancel_order'),
    path("cancel_order/<str:id>", views.cancel_order, name='cancel_order'),
    path("user_registration", views.user_registration, name='user_registration'),
    path("registration_link", views.registration_link, name='registration_link'),
    path("admin_view_cancel_report", views.admin_view_cancel_report, name='admin_view_cancel_report'),
    path("admin_view_order_report", views.admin_view_order_report, name='admin_view_order_report'),
    path("edit_user_register/<str:u_id>", views.edit_user_register, name='edit_user_register'),
    path("update_user_register", views.update_user_register, name='update_user_register'),
    path("delete_user/<str:u_id>", views.delete_user, name='delete_user_register'),
    path("view_user_register", views.view_user_register, name='view_user_register'),

    path("select_fabrics/<str:id>", views.select_fabrics, name='select_fabrics'),

    path("registerheader", views.registerheader, name='registerheader'),
    path("registerfooter", views.registerfooter, name='registerfooter'),
    path("adminheader", views.adminheader, name='adminheader'),
    path("adminfooter", views.adminfooter, name='adminfooter'),
    path("select_size", views.select_size, name='select_size'),

    path("make_order", views.make_order, name='make_order'),
    path("turf_header", views.turf_header, name='turf_header'),
    path("admin_design", views.admin_design, name='admin_design'),
    path("about", views.about, name='about'),
    path("user_view_order", views.user_view_order, name='user_view_order'),
    path("admin_view_order", views.admin_view_order, name='admin_view_order'),
    path("expert_view_order", views.expert_view_order, name='expert_view_order'),
    path("admin_view_order_design/<int:id>", views.admin_view_order_design, name='admin_view_order_design'),
    path("expert_view_order_design/<int:id>", views.expert_view_order_design, name='expert_view_order_design'),

    path("user_page", views.user_page, name='user_page'),
    path("expert_view_suggestion", views.expert_view_suggestion, name='expert_view_suggestion'),
    path('expert_reply/<int:id>/', views.expert_reply, name='expert_reply'),
    path("payment_start", views.payment_start, name='payment_start'),
    path("payment", views.payment, name='payment'),
    path("logout", views.logout, name='logout'),
    path('user_design',views.user_design,name='user_design'),
    path('admin_navigation', views.admin_navigation, name='admin_navigation'),
    path('chatbot/', views.call_first, name='chatbot'),
    path('call_first', views.call_first, name='call_first'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
