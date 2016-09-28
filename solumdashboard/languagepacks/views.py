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

import json

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import views

from solumclient.v1 import languagepack as cli_lp

from solumdashboard.api.client import client as solumclient
from solumdashboard.languagepacks import forms as lp_forms
from solumdashboard.languagepacks import tables as lp_tables


class IndexView(tables.DataTableView):
    table_class = lp_tables.LanguagepacksTable
    template_name = 'languagepacks/index.html'
    page_title = _("Languagepacks")

    def get_data(self):
        try:
            solum = solumclient(self.request)
            languagepacks = solum.languagepacks.list()
        except Exception:
            languagepacks = []
            exceptions.handle(self.request,
                              _('Unable to retrieve languagepacks.'))
        return languagepacks


class DetailView(views.HorizonTemplateView):
    template_name = 'languagepacks/detail.html'
    page_title = "{{ languagepack.name }}"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        languagepack, loglist = self.get_data()
        context["languagepack"] = languagepack
        context["loglist"] = loglist
        return context

    def get_data(self):
        lp_id = self.kwargs['languagepack_id']
        solum = solumclient(self.request)

        languagepack = solum.languagepacks.find(name_or_id=lp_id)
        loglist = cli_lp.LanguagePackManager(solum).logs(
            lp_id=lp_id)

        for log in loglist:
            strategy_info = json.loads(log.strategy_info)
            if log.strategy == 'local':
                log.local_storage = log.location
            elif log.strategy == 'swift':
                log.swift_container = strategy_info['container']
                log.swift_path = log.location

        return languagepack, loglist


class CreateView(forms.ModalFormView):
    form_class = lp_forms.CreateForm
    template_name = 'languagepacks/create.html'
    modal_header = _("Create Languagepack")
    page_title = _("Create Languagepack")
    submit_url = reverse_lazy("horizon:solum:languagepacks:create")
    success_url = reverse_lazy("horizon:solum:languagepacks:index")
