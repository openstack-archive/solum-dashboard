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


class UpdateApplicationAction(workflows.Action):
    name = forms.CharField(label=_("Application Name"), required=False)
    description = forms.CharField(label=_("Description"), required=False)
    languagepack = forms.CharField(label=_("Languagepack"), required=False)
    ports = forms.IntegerField(label=_("Ports"), required=False)

    source = {}
    source["repository"] = forms.CharField(label=_("Source Repository"),
                                           required=False)
    source["revision"] = forms.CharField(label=_("Source Revision"),
                                         required=False)

    workflow_config = {}
    workflow_config["test_cmd"] = forms.CharField(
        label=_("Workflow Test Command"), required=False)
    workflow_config["run_cmd"] = forms.CharField(
        label=_("Workflow Run Command"), required=False)


class UpdateApplication(workflows.Step):
    action_class = UpdateApplicationAction
    depends_on = ("application_id",)
    contributes = ("name", "description", "languagepack", "ports", "source",
                   "workflow_config")


class UpdateApplicationClass(workflows.Workflow):
    slug = "update_app"
    name = _("Update App")
    finalize_button_name = _("Update")
    success_message = _("App updated")
    failure_message = _("Could not update app")
    success_url = "horizon:solum:applications:index"
    default_steps = (UpdateApplication,)
    depends_on = ("application_id",)
    contributions = ("name", "description", "languagepack", "ports", "source",
                     "workflow_config")

    def handle(self, request, data):
        to_update = {}
        for field in data:
            if data[field] and field != 'application_id':
                to_update[field] = data[field]

        solum = solumclient(request)
        solum.apps.patch(data["application_id"], data=to_update)

        return True
