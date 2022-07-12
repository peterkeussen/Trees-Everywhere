from datetime import datetime
from django.contrib import admin

from tree.forms import UserFormAdd
from django.contrib.auth.models import User, Group

# admin.site.unregister(User)
admin.site.unregister(Group)

from tree.models import Account, User, Profile, PlantedTree, Tree

@admin.action(description='Mark selected accounts as active')
def make_actived(modeladmin, request, queryset):
    queryset.update(active=True)
    

@admin.action(description='Mark selected accounts as inactive')
def make_inactived(modeladmin, request, queryset):
    queryset.update(active=False)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'active')
    actions = [make_actived, make_inactived]
    list_editable = ('active',)


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0


class UserAdmin(admin.ModelAdmin):
    add_form = UserFormAdd
    form = UserFormAdd
    inlines = [ProfileInline]
    
    # Add user in account 
    def save_model(self, request, obj, form, change):
        account = Account.objects.get(name=form.cleaned_data['account'])
        if not change:
            obj.save()
            if Account.objects.filter(user=obj).count() == 0:                
                account.user.add(obj)
                prof = Profile()
                prof.user = obj
                prof.joined = datetime.now()
                prof.save()
        else:
            if Account.objects.filter(name=form.cleaned_data['account'], user=obj).count() == 0:                
                obj.save()
                account.user.add(obj)
        if 'password' in form.changed_data:
            password = form.cleaned_data['password']
            obj.set_password(password)

        obj.save()
        
        super().save_model(request, obj, form, change)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'about', 'joined')

    # def has_add_permission(self, request):
    #     return False


class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ['tree', 'user', 'planted_at', 'account']
    
    def has_add_permission(self, request):
        return False

class TreePlantedInline(admin.TabularInline):
    model = PlantedTree
    extra = 0
    fields = ('account', 'user')
    readonly_fields = ('account', 'user')
    can_delete = False
    max_num = 0 # remove add another


class TreeAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_total_tree_planted']
    
    @admin.display(ordering='tree', description='Total Trees')
    def get_total_tree_planted(self, obj):
        return str(PlantedTree.objects.filter(tree=obj).count())
                         
    inlines = [TreePlantedInline]
    

admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(PlantedTree, PlantedTreeAdmin)
admin.site.register(Tree, TreeAdmin)

