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
from horizon import forms
from horizon import workflows

from solumdashboard.api.client import client as solumclient


class ConfigAssemblyAction(workflows.Action):
    name = forms.CharField(label=_("Assembly Name"),
                           required=True)
    description = forms.CharField(label=_("Description"),
                                  required=False)

    def __init__(self, request, *args, **kwargs):
        super(ConfigAssemblyAction, self).__init__(request, *args, **kwargs)
        if 'application_id' in request.REQUEST:
            plan_id = request.REQUEST['application_id']
            solum = solumclient(request)
            plan = solum.plans.get(plan_id=plan_id)
            plan_uri = plan.uri
        else:
            plan_uri = request.POST['plan_uri']

        self.fields["plan_uri"] = forms.CharField(
            widget=forms.HiddenInput(),
            initial=plan_uri)

    class Meta(object):
        name = _("Configure name and description")
        help_text_template = "applications/_launch_configure_help.html"


class ConfigureAssembly(workflows.Step):
    action_class = ConfigAssemblyAction
    contributes = ['name', 'description', 'plan_uri']


class LaunchApplication(workflows.Workflow):
    slug = "launch_app"
    name = _("Launch App")
    finalize_button_name = _("Launch")
    success_message = _("App launched")
    failure_message = _("Could not launch app")
    success_url = "horizon:solum:assemblies:index"
    default_steps = (ConfigureAssembly,)

    def handle(self, request, context):
        solum = solumclient(request)
        # Note: solum client seems to ignore description
        solum.assemblies.create(name=context.get('name'),
                                plan_uri=context.get('plan_uri'))
        return True
