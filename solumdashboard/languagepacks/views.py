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

from solumdashboard.api.client import client as solumclient
from solumdashboard.languagepacks import tables as lp_tables


class IndexView(tables.DataTableView):
    table_class = lp_tables.LanguagepacksTable
    template_name = 'languagepacks/index.html'

    def get_data(self):
        try:
            solum = solumclient(self.request)
            languagepacks = solum.languagepacks.list()
        except Exception:
            languagepacks = []
            exceptions.handle(self.request,
                              _('Unable to retrieve languagepacks.'))
        return languagepacks
