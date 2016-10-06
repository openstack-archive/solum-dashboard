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

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables
from horizon import tabs

from solumdashboard.api.client import client as solumclient
from solumdashboard.assemblies import tables as assem_tables
import solumdashboard.assemblies.tabs as _tabs


class IndexView(tables.DataTableView):
    table_class = assem_tables.AssembliesTable
    template_name = 'assemblies/index.html'
    page_title = _("Assemblies")

    def get_data(self):
        try:
            solum = solumclient(self.request)
            assemblies = solum.assemblies.list()
        except Exception:
            assemblies = []
            exceptions.handle(self.request, 'Unable to retrieve assemblies.')
        return assemblies


class DetailView(tabs.TabView):
    template_name = 'assemblies/detail.html'
    tab_group_class = _tabs.AssemDetailsTabs
    page_title = "{{ assem.name|default:assem.uuid }}"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        assem_id = kwargs['assembly_id']
        solum = solumclient(self.request)
        assem = solum.assemblies.get(assembly_id=assem_id)
        context["assem"] = assem
        return context

    def get_data(self):
        pass
