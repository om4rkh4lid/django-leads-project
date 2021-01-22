from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.http import HttpResponse
from .models import Lead, Agent, Category
from .forms import LeadModelForm, LeadForm, CustomCreateUserForm, AssignAgentForm, LeadCategoryUpdateForm
from agents.mixins import OrganizerAndLoginRequiredMixin


class CreateUserView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomCreateUserForm

    # what happens after the form is saved successfully?s
    def get_success_url(self):
        # works the same way as template URLs
        return reverse("login")


class LandingPageView(TemplateView):
    # required field
    template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'leads/lead_list.html'
    queryset = Lead.objects.all()
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization, agent__isnull=False)
            queryset = queryset.filter(agent=user.agent)
        return queryset

    # Add something to the query passed to the class by overriding
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        unassigned_leads = Lead.objects.filter(agent__isnull=True)
        context.update(
            {
                'unassigned_leads': unassigned_leads
            }
        )
        return context


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, "leads/lead_list.html", context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization)
            queryset = queryset.filter(agent=user.agent)
        return queryset


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead': lead
    }
    return render(request, 'leads/lead_detail.html', context)


class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    # what happens after the form is saved successfully?s
    def get_success_url(self):
        # works the same way as template URLs
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        # TODO send email
        send_mail(
            subject="New lead created!",
            message="Please visit the site to view the new lead.",
            from_email='xom4rxkh4lidx@gmail.com',
            recipient_list=['xom4rxkh4lidx@gmail.com']
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()  # create the form to send to the template
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            print('Lead object successfully created!')
            return redirect('/leads')
    context = {
        "form": form
    }
    return render(request, 'leads/lead_create.html', context)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    # what happens after the form is saved successfully?s
    def get_success_url(self):
        # works the same way as template URLs
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == 'POST':
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            print('Lead object successfully updated!')
            return redirect('/leads')
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, 'leads/lead_update.html', context)


class LeadDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'

    # what happens after the form is saved successfully?s
    def get_success_url(self):
        # works the same way as template URLs
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    print('Lead object successfully deleted!')
    return redirect('/leads')


class AssignAgentView(OrganizerAndLoginRequiredMixin, FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)

        # pass the request to the arguments passed to the form
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        # since this is not a modelform we cant use form.save()
        # first we access the agent from the form
        agent = form.cleaned_data["agent"]
        # then we get the lead and pass the agent as their agent
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

# def landing_page(request):
#     return render(request, "landing.html")

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()  # create the form to send to the template
#     if request.method == 'POST':
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             fname = form.cleaned_data['first_name']
#             lname = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = fname
#             lead.last_name = lname
#             lead.age = age
#             lead.save()  # commit changes
#             print('Lead object successfully created!')
#             return redirect('/leads')
#     context = {
#         "form": form
#     }
#     return render(request, 'leads/lead_create.html', context)

# def lead_create(request):
    # form = LeadForm()  # create the form to send to the template
    # if request.method == 'POST':
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         fname = form.cleaned_data['first_name']
    #         lname = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = Agent.objects.first()
    #         Lead.objects.create(
    #             first_name=fname,
    #             last_name=lname,
    #             agent=agent
    #         )
    #         print('Lead object successfully created!')
    #         return redirect('/leads')
    # context = {
    #     "form": form
    # }
    # return render(request, 'leads/lead_create.html', context)
