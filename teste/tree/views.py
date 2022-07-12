from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Account, PlantedTree, Profile
from .forms import PlantedTreeFormCreate, UserProfileFormUpdate
from django.http import JsonResponse
from rest_framework import status
from django.http import HttpResponseForbidden


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    

class TreeListView(LoginRequiredMixin, ListView):
    model = PlantedTree
    paginate_by = 4
    template_name = 'plant_list.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
    
    
class TreeAccountListView(LoginRequiredMixin, ListView):
    model = PlantedTree
    # paginate_by = 4
    template_name = 'plant_list_account.html'
    ordering = ['account']
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class TreeAccountUsersListView(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = 'plant_list_account_users.html'
    ordering = ['account']
    
    def get_queryset(self):
        qs = super().get_queryset()
        accounts = Account.objects.filter(user=self.request.user)
        qs = qs.filter(account__in=accounts)
        return qs


class TreeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = PlantedTree
    template_name = 'plant_detail.html'
    
    def get_queryset(self):        
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
@login_required
def treecreate_or_change(request, pk=None):
    tree = None
    if pk:
        tree = get_object_or_404(tree, pk=pk)
    if request.method == "POST":
        form = PlantedTreeFormCreate(request.user, data=request.POST)
        
        if form.is_valid():
            treeplanted = form.save(commit=False)
            treeplanted.user = request.user
            treeplanted.save()
            return redirect('tree_list')
    else:
        form = PlantedTreeFormCreate(request.user)
            
    return render(request, 'plant_create.html', context={'form': form})

@login_required
def treeplanted_detail(request, pk):    
    tree_planted = get_object_or_404(PlantedTree, id=pk)
    
    if tree_planted.user == request.user:
        return render(request, 'plant_detail2.html', context={'tree_planted': tree_planted})
    else:
        return HttpResponseForbidden()

@login_required
def profileview(request):
    if request.method == 'POST':
        profile_form = UserProfileFormUpdate(request.POST, instance=request.user.profile_user)
        
        if profile_form.is_valid():
            profile_form.save()
            return redirect('home')
    else:
        profile_form = UserProfileFormUpdate(instance=request.user.profile_user)
        
    return render(request, 'profile.html', context={'form': profile_form})


@login_required
def listtree_api(request):
    treeplanted = list(PlantedTree.objects.filter(user=request.user).values())
    return JsonResponse(treeplanted, safe=False, status=status.HTTP_200_OK)