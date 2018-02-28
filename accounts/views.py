# from django.contrib.auth import authenticate
# from django.shortcuts import render, redirect
# from django.views.generic import CreateView, FormView
# from .forms import UserLoginForm, UserRegisterForm


# class LoginView(FormView):
#     form_class = UserLoginForm
#     template_name = 'account/login.html'
#     success_url = '/'

#     def form_valid(self, form):
#         request = self.request
#         next_ = request.GET.get('next')
#         next_post = request.POST.get('next')
#         redirect_path = next_ or next_post or None
#         email = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(username=email, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect('/')
#         return super(LoginView, self).form_invalid(form)


# class UserRegisterForm(CreateView):
#     form_class = UserRegisterForm
#     template_name = 'account/register.html'
#     success_url = '/login/'
