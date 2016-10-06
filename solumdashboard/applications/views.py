# Copyright (c) 2014 Rackspace Hosting.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import tabs
from horizon import workflows

from solumdashboard.api.client import client as solumclient
from solumdashboard.applications import forms as app_forms
from solumdashboard.applications import tables as app_tables
import solumdashboard.applications.tabs as _tabs
from solumdashboard.applications import workflows as update_flow


class IndexView(tables.DataTableView):
    table_class = app_tables.ApplicationsTable
    template_name = 'applications/index.html'
    page_title = _("Applications")

    def get_data(self):
        try:
            solum = solumclient(self.request)
            apps = solum.apps.list()
        except Exception:
            apps = []
            exceptions.handle(self.request,
                              _('Unable to retrieve apps.'))
        return apps


class CreateView(forms.ModalFormView):
    form_class = app_forms.CreateForm
    template_name = 'applications/create.html'
    modal_header = _("Create Application")
    page_title = _("Create Application")
    submit_url = reverse_lazy('horizon:solum:applications:create')
    success_url = reverse_lazy("horizon:solum:applications:index")


class ScaleView(forms.ModalFormView):
    form_class = app_forms.ScaleForm
    template_name = "applications/scale.html"
    modal_header = _("Scale Application")
    page_title = _("Scale Application")
    submit_url = reverse_lazy('horizon:solum:applications:scale')
    success_url = reverse_lazy("horizon:solum:applications:index")
    failure_url = reverse_lazy("horizon:solum:applications:index")

    def get_context_data(self, **kwargs):
        context = super(ScaleView, self).get_context_data(**kwargs)
        context["application_id"] = self.kwargs["application_id"]
        return context

    def get_initial(self):
        application_id = self.kwargs['application_id']
        return {'application_id': application_id}


class UpdateView(workflows.WorkflowView):
    workflow_class = update_flow.UpdateApplicationClass
    success_url = "horizon:solum:applications:index"
    classes = ("ajax-modal")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["application_id"] = self.kwargs["application_id"]
        return context

    def _get_object(self, *args, **kwargs):
        application_id = self.kwargs['application_id']
        solum = solumclient(self.request)
        app = solum.apps.find(name_or_id=application_id)
        return app

    def get_initial(self):
        app = self._get_object()
        return {'application_id': app.id}


class DetailView(tabs.TabView):
    template_name = 'applications/detail.html'
    tab_group_class = _tabs.AppDetailsTabs
    page_title = "{{ app.name|default:app.id }}"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        application_id = self.kwargs['application_id']
        solum = solumclient(self.request)
        app = solum.apps.find(name_or_id=application_id)
        context["app"] = app
        return context


class LaunchView(forms.ModalFormView):
    form_class = app_forms.LaunchForm
    template_name = "applications/launch.html"
    modal_header = _("Launch Application")
    page_title = _("Launch Application")
    success_url = reverse_lazy("horizon:solum:applications:index")
    failure_url = reverse_lazy("horizon:solum:applications:index")

    def get_context_data(self, **kwargs):
        context = super(LaunchView, self).get_context_data(**kwargs)
        context["application_id"] = self.kwargs["application_id"]
        return context

    def get_initial(self):
        application_id = self.kwargs['application_id']
        return {'application_id': application_id}
