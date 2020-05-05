from django.apps import apps
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from adhocracy4.dashboard import mixins
from adhocracy4.dashboard import signals
from adhocracy4.dashboard.blueprints import get_blueprints
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from adhocracy4.projects.mixins import ProjectMixin

from .forms import DashboardProjectCreateForm


class ModuleBlueprintListView(ProjectMixin,
                              mixins.DashboardBaseMixin,
                              generic.DetailView):
    template_name = 'a4_candy_dashboard/module_blueprint_list.html'
    permission_required = 'a4projects.change_project'
    model = project_models.Project
    slug_url_kwarg = 'project_slug'
    menu_item = 'project'

    @property
    def blueprints(self):
        return [
            (key, data) for key, data in get_blueprints()
        ]

    def get_permission_object(self):
        return self.project


class ModuleCreateView(ProjectMixin,
                       mixins.DashboardBaseMixin,
                       mixins.BlueprintMixin,
                       SingleObjectMixin,
                       generic.View):
    permission_required = 'a4projects.change_project'
    model = project_models.Project
    slug_url_kwarg = 'project_slug'

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        module = module_models.Module(
            name=self.blueprint.title,
            weight=len(project.modules) + 1,
            project=project,
        )
        module.save()
        signals.module_created.send(sender=None,
                                    module=module,
                                    user=self.request.user)

        self._create_module_settings(module)
        self._create_phases(module, self.blueprint.content)

        return HttpResponseRedirect(self.get_next(module))

    def _create_module_settings(self, module):
        if self.blueprint.settings_model:
            settings_model = apps.get_model(*self.blueprint.settings_model)
            module_settings = settings_model(module=module)
            module_settings.save()

    def _create_phases(self, module, blueprint_phases):
        for index, phase_content in enumerate(blueprint_phases):
            phase = phase_models.Phase(
                type=phase_content.identifier,
                name=phase_content.name,
                description=phase_content.description,
                weight=index,
                module=module,
            )
            phase.save()

    def get_next(self, module):
        return reverse('a4dashboard:dashboard-module_basic-edit', kwargs={
            'organisation_slug': module.project.organisation.slug,
            'module_slug': module.slug
        })

    def get_permission_object(self):
        return self.project


class ProjectCreateView(mixins.DashboardBaseMixin,
                        SuccessMessageMixin,
                        generic.CreateView):
    model = project_models.Project
    slug_url_kwarg = 'project_slug'
    form_class = DashboardProjectCreateForm
    template_name = 'a4dashboard/project_create_form.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'
    success_message = _('Project was created.')

    def get_permission_object(self):
        return self.organisation

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation'] = self.organisation
        kwargs['creator'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('a4dashboard:project-edit',
                       kwargs={'project_slug': self.object.slug,
                                'organisation_slug': self.organisation.slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        signals.project_created.send(sender=None,
                                     project=self.object,
                                     user=self.request.user)

        return response
