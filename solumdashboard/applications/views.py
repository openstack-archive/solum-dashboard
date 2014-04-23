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

import logging

from horizon import tables
from horizon import tabs
from horizon import workflows

from solumdashboard.api.client import client as solumclient
from solumdashboard.applications import tables as app_tables
import solumdashboard.applications.tabs as _tabs
import solumdashboard.applications.workflows.create as create_flow


LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    table_class = app_tables.ApplicationsTable
    template_name = 'applications/index.html'

    def get_data(self):
        solum = solumclient(self.request)
        return solum.plans.list()


class CreateView(workflows.WorkflowView):
    workflow_class = create_flow.CreateApplication
    success_url = \
        "horizon:solum:applications:create"
    classes = ("ajax-modal")
    template_name = 'applications/create.html'


class DetailView(tabs.TabView):
    template_name = 'applications/detail.html'
    tab_group_class = _tabs.AppDetailsTabs

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        return super(DetailView, self).get_context_data(**kwargs)

    def get_data(self):
        pass
