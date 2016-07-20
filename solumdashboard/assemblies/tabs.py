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
from horizon import tabs

from solumdashboard.api.client import client as solumclient


class GeneralTab(tabs.Tab):
    name = _("General Info")
    slug = "assembly_details_tab"
    template_name = ("assemblies/_detail.html")

    def get_context_data(self, request):
        assem_id = self.tab_group.kwargs['assembly_id']
        solum = solumclient(request)
        assem = solum.assemblies.get(assembly_id=assem_id)
        return {"assembly": assem}


class AssemDetailsTabs(tabs.TabGroup):
    slug = "assembly_details"
    tabs = (GeneralTab,)
    sticky = True
