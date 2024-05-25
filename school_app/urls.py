from django.urls import include, path
from .views import  *
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download, name='download'),
    path('userview/',views.userview,name='userview'),
    path('Login/',views.Login, name='Login'),
    path('upload/', views.upload, name='upload'),
    path('about/', views.about, name='about'),
    path('logout/', admin_logout, name='logout'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('delete/<int:pk>/', views.delete, name='delete'),  # Delete product
    path('update/<int:pk>', views.Update_detail.as_view()),  # Delete product
   
    path('register/',views.register, name='register'),
    path('approval/',views.approval, name='approval'),
    path('studentdetails/', views.studentview, name='studentview'),
    path('edit_student/<int:pk>/', views.edit_student.as_view()),

    
    path('student-login/', views.studentlogin, name='student_login'),
    path('registrationlist/',views.registrationlist,name='registrationlist'),
    path('material-search/', material_search, name='material_search'),
    path('student_dashboard/<int:student_id>/', views.student_dashboard, name='student_dashboard'),
    path('listmaterials/', views.listmaterials, name='listmaterials'),


    path('Contact/',Contact, name='Contact'),
    path('staff/', staff, name='staff'),
    path('coures/',coures, name='coures'),
    
    
    #feedback
    
    path('send_feedback/', send_feedback, name='feedback_create'),
    path('FeedbackListView/', FeedbackListView, name='FeedbackListView'),
    path('replay_feedback/<int:pk>', replay_feedback.as_view(), name='replay_feedback'),
    path('userFeedbackListView/', userFeedbackListView, name='userFeedbackListView'),
    
]
