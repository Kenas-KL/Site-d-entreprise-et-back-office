from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import contact, BlogHome, done, TaskView, TaskDetail, TaskUpdate, TaskCreate, BlogCreate, BlogUpdate, \
    administrators, BlogAdminView, TaskAdminView, TaskAdminDelete, TaskAdminUpdate, BlogAdminDelete, UsersAdminView, \
    UserAdminDelete, UsersAdminUpdate, logout_view, DocumentView, DocumentsAdminView, DocumentAdminCreate, \
    DocumentAdminUpdate, user_to_logout, DocumentAdminDelelte, InscriptionView, account_created, BlogDetail

app_name = "blog"

urlpatterns = [
    # path('', index, name='index'),
    path('', BlogHome.as_view(), name='home'),
    path('detail&&&/blog<str:pk>&/comments/', BlogDetail.as_view(), name="blog_detail"),
    path('signup/', InscriptionView.as_view(), name="signup"),
    path('account-created/', account_created, name="account_created"),
    path('login/', LoginView.as_view(), name="login"),
    path('process-user-for-logout', user_to_logout, name="process_logout"),
    path('logout/', logout_view, name="logout"),
    path('administrators/', administrators, name="administration"),
    path('create_blog/', BlogCreate.as_view(), name="add_blog"),
    path('list_blog_admin/', BlogAdminView.as_view(), name="list_blog_admin"),
    path('edit_blog/<str:pk>/', BlogUpdate.as_view(), name="edit_blog"),
    path('list-Documents-level/', DocumentView.as_view(), name="documents_view"),
    path('events&_&&-/blogs', done, name="done"),
    path('taskview/', TaskView.as_view(), name="task_view"),
    path('add_task/', TaskCreate.as_view(), name="add_task"),
    path('&&task-detail&&&/<str:pk>/&&tasks', TaskDetail.as_view(), name="detail_task_view"),
    path('edit/<str:pk>/', TaskUpdate.as_view(), name="edit_task"),
    path('list_tasks_admin/admin/',TaskAdminView.as_view(), name="list_tasks_admin"),
    path('task_admin_update/<str:pk>/', TaskAdminUpdate.as_view(), name="admin_update_task"),
    path('delete_task_admin/<str:pk>/', TaskAdminDelete.as_view(), name="admin_delete_task"),
    path('delete_blog_admin/<str:pk>/', BlogAdminDelete.as_view(), name="admin_delete_blog"),
    path('list-documents/admin/', DocumentsAdminView.as_view(), name="list_admin_docs"),
    path('create-document-admin/admin/', DocumentAdminCreate.as_view(), name="add_document_admin"),
    path('update-document-admin/<str:pk>/admin/', DocumentAdminUpdate.as_view(), name="update_document_admin"),
    path('admin/<str:pk>/delete-docuement-admin/admindocuments/', DocumentAdminDelelte.as_view(), name="delete-document"),
    path('list_users_admin/admin/',UsersAdminView.as_view(), name="list_users_admin"),
    path('update_user_admin/<str:pk>/', UsersAdminUpdate.as_view(), name="admin_update_user"),
    path('delete_user_admin/<str:pk>/', UserAdminDelete.as_view(), name="admin_delete_user"),
    path('contact/', contact, name = 'contact')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)