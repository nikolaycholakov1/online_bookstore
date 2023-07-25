# # views.py in the 'core' app
# from django.contrib.auth import authenticate, login
# from django.shortcuts import redirect, render
# from django.urls import reverse
# from django.views import View
# from django.views.generic import TemplateView
#
# from online_bookstore.apps.book.models import Book
# from .forms import RegistrationForm
#
#
# class HomePageView(TemplateView):
#     template_name = 'common/home-page.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # Fetch featured books from the database
#         featured_books = Book.objects.filter(featured=True)
#         context['featured_books'] = featured_books
#
#         return context
#
#
# class RegisterView(View):
#     template_name = 'common/register.html'
#
#     def get(self, request):
#         form = RegistrationForm()
#
#         context = {
#             'form': form
#         }
#
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#             # Get the username and password from the form
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#
#             # Authenticate the user and log them in
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)
#
#             return redirect(reverse('home-page'))  # Redirect to the home page after successful registration
#
#         context = {
#             'form': form
#         }
#
#         return render(request, self.template_name, context)
