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

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import forms
from horizon import messages

from solumclient.common import yamlutils
from solumclient.v1 import workflow as cli_wf

from solumdashboard.api.client import client as solumclient


LOG = logging.getLogger(__name__)


class ScaleForm(forms.SelfHandlingForm):
    target = forms.IntegerField(label=_("Target"), required=True)

    def handle(self, request, data):
        app_id = self.initial.get('application_id')
        LOG.info('ScaleApplication %s' % data)

        if data["target"] <= 0:
            exceptions.handle(self.request,
                              _("Scale target must be greater than zero"))

        solum = solumclient(request)
        actions = ['scale']
        cli_wf.WorkflowManager(solum, app_id=app_id).create(
            actions=actions)

        return True


class CreateForm(forms.SelfHandlingForm):
    source = forms.ChoiceField(
        label=_('Source'),
        choices=[
            ('app_file', _('App File')),
            ('input', _('Input'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )
    app_file = forms.FileField(
        label=_("Local app file location"),
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-app_file': _('Local app file location')
        })
    )
    name = forms.CharField(label=_("Application Name"), required=False)
    languagepack = forms.CharField(label=_("Languagepack"), required=False)
    git_url = forms.URLField(label=_("Source repository"), required=False)
    run_cmd = forms.CharField(label=_("Application entry point"),
                              required=False)
    unittest_cmd = forms.CharField(label=_(
        "Command to execute unit tests"), required=False)
    port = forms.IntegerField(label=_("The port your application listens on"),
                              min_value=0,
                              required=False)
    param_file = forms.FileField(label=_(
        "A yaml file containing custom parameters"), required=False)

    def clean(self):
        cleaned_data = super(CreateForm, self).clean()
        import_type = cleaned_data.get('source')
        if import_type == 'app_file' and not cleaned_data.get('app_file'):
            msg = _('Please supply an app file')
            raise forms.ValidationError(msg)
        elif import_type == 'input':
            if not (cleaned_data.get('name')):
                msg = _('Please supply a name')
                raise forms.ValidationError(msg)
            elif not cleaned_data.get('languagepack'):
                msg = _('Please supply a languagepack')
                raise forms.ValidationError(msg)
            elif not cleaned_data.get('git_url'):
                msg = _('Please supply a github url')
                raise forms.ValidationError(msg)
            elif not cleaned_data.get('run_cmd'):
                msg = _('Please supply a run command')
                raise forms.ValidationError(msg)
        return cleaned_data

    def handle(self, request, data):
        LOG.info('CreateApplication %s' % data)
        solum = solumclient(request)

        app_data = None
        if data['source'] == 'app_file':
            inf = data['app_file'].read()
            app_data = yamlutils.load(inf)
            if 'repo_token' not in app_data:
                app_data['repo_token'] = ''
        else:
            app_data = {
                'version': 1,
                'description': 'default app description',
                'source': {
                    'repository': '',
                    'revision': 'master',
                    'repo_token': ''
                },
                'workflow_config': {
                    'test_cmd': '',
                    'run_cmd': ''
                }
            }

        if data['name']:
            app_data['name'] = data['name']

        if data['languagepack']:
            app_data['languagepack'] = data['languagepack']

        if data['git_url']:
            app_data['source'] = dict()
            app_data['source']['repository'] = data['git_url']
            app_data['source']['revision'] = 'master'

        if data['run_cmd']:
            if app_data.get('workflow_config') is None:
                app_data['workflow_config'] = dict()
            if not app_data['workflow_config']['run_cmd']:
                app_data['workflow_config']['run_cmd'] = data['run_cmd']

        if data['unittest_cmd']:
            if app_data.get('workflow_config') is None:
                app_data['workflow_config'] = dict()
            if not app_data['workflow_config']['test_cmd']:
                app_data['workflow_config']['test_cmd'] = data['unittest_cmd']

        if not app_data.get('ports'):
            app_data['ports'] = []
            if data['port']:
                app_data['ports'].append(data['port'])
            else:
                app_data['ports'].append(80)

        if data['param_file']:
            param_def = data['param_file'].read()
            app_data['parameters'] = yamlutils.load(param_def)

        try:
            solum.apps.create(**app_data)
            messages.success(request,
                             _('Application was successfully created.'))
            return True
        except Exception:
            msg = _('Unable to create application')
            redirect = reverse("horizon:solum:applications:index")
            exceptions.handle(request, msg, redirect=redirect)
            return False


class LaunchForm(forms.SelfHandlingForm):
    du_id = forms.CharField(label=_("ID of the DU image"), required=False)

    def handle(self, request, data):
        app_id = self.initial.get('application_id')
        LOG.info('LaunchApplication %s' % data)
        solum = solumclient(request)

        if data["du_id"]:
            actions = ['deploy']
            cli_wf.WorkflowManager(
                solum, app_id=app_id).create(
                    actions=actions, du_id=data["du_id"])
        else:
            actions = ['unittest', 'build', 'deploy']
            cli_wf.WorkflowManager(
                solum, app_id=app_id).create(
                    actions=actions)

        return True
