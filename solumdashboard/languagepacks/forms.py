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

import json
import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from solumclient.common import yamlutils

from solumdashboard.api.client import client as solumclient


LOG = logging.getLogger(__name__)


class CreateForm(forms.SelfHandlingForm):
    source_uri = forms.CharField(label=_("Source URI"))
    name = forms.CharField(label=_("Languagepack Name"))
    description = forms.CharField(label=_("Description"), required=False)
    param_file = forms.FileField(label=_("Parameter File"),
                                 required=False)
    lp_metadata = forms.FileField(label=_("Languagepack Metadata File"),
                                  required=False)

    def handle(self, request, data):
        LOG.info('CreateLanguagepack %s' % data)
        solum = solumclient(request)

        param_data = {}
        if data['param_file']:
            inf = data['param_file'].read()
            param_data = yamlutils.load(inf)

        lp_metadata = None

        if data['lp_metadata']:
            lp_metadata = json.dumps(json.load(data['lp_metadata']))

        try:
            solum.languagepacks.create(
                name=data['name'], source_uri=data['source_uri'],
                lp_metadata=lp_metadata, lp_params=param_data,
                description=data['description'])
            message = _(
                'Languagepack %s was successfully created.') % data['name']
            messages.success(request, message)
        except Exception:
            redirect = reverse('horizon:solum:languagepacks:index')
            exceptions.handle(self.request,
                              _('Unable to create languagepack.'),
                              redirect=redirect)

        return True
