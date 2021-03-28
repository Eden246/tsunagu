from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    def save_user(self,request,user,form,commit=True):
        user = super(AccountAdapter,self).save_user(request,user,form,commit=False)
        user.phone = form.cleaned_data.get('phone')
        user.save()

    def is_open_for_signup(self, request):
        return True