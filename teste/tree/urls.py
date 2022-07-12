from django.urls import path
from .views import (
                HomePageView,
                TreeListView,
                TreeDetailView,
                treeplanted_detail,
                treecreate_or_change,
                TreeAccountListView,
                listtree_api, profileview,
                TreeAccountUsersListView
            )

# app_name = 'tree'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('listtree/', TreeListView.as_view(), name='tree_list'),
    path('listtreeaccount/', TreeAccountListView.as_view(), name='tree_list_account'),
    path('listtreeaccountuses/', TreeAccountUsersListView.as_view(), name='tree_list_account_users'),
    # path('tree/<int:pk>/detail', TreeDetailView.as_view(), name='tree_detail'),
    path('tree/<int:pk>/detail', treeplanted_detail, name='tree_detail2'),
    path('userprofile/', profileview, name='profile_update'),
    path('createtree/', treecreate_or_change, name='tree_create'),
    path('treeplantedapi/', listtree_api, name='tree_planted_api'),
    
]
