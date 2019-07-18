from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import FormView, DetailView
from revoratebot.models import User, Department, Company
from revoratebot.forms import CreateUserForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from core.managers import companies, users
from django.http import Http404


class UsersListView(LoginRequiredMixin, ListView):
    ordering = 'created_at'
    model = User
    template_name = 'admin/users/users_list.html'
    context_object_name = 'users'


class CreateUserView(LoginRequiredMixin, FormView):
    form_class = CreateUserForm
    template_name = 'admin/users/new_user.html'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        phone_number = form.cleaned_data['phone_number']
        is_manager = form.cleaned_data['is_manager']
        department = form.cleaned_data['department']
        company = form.cleaned_data['company']
        try:
            user = users.create_user(name, phone_number, company, department, is_manager)
        except Company.DoesNotExist:
            messages.error(self.request, "Указанная компания не существует, проверьте свой выбор")
            return super().form_invalid(form)
        except Department.DoesNotExist:
            messages.error(self.request, "Указан не существующий отдел в выбранной компании, проверьте свой выбор")
            return super().form_invalid(form)
        except Exception as e:
            messages.error(self.request, 'Произошла ошибка: ' + str(e))
            return super().form_invalid(form)
        self.object = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin_user_created', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = companies.get_all_companies()
        context['departments'] = companies.get_all_departments()
        return context


class UserCreatedView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'admin/users/user_created.html'
    context_object_name = 'user'


class EditUserView(LoginRequiredMixin, FormView):
    form_class = CreateUserForm
    success_url = reverse_lazy('admin_users')

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = users.get_by_id(user_id)
        if not user:
            return Http404()
        self.object = user
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        user = self.object
        initial = super().get_initial()
        initial['name'] = user.name
        initial['phone_number'] = user.phone_number
        initial['company'] = user.department.company_id
        initial['department'] = user.department_id
        initial['is_manager'] = user.is_manager

    def form_valid(self, form):

