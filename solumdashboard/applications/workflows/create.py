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

from django.utils.translation import ugettext_lazy as _
from horizon import forms
from horizon import workflows

from solumdashboard.api.client import client as solumclient


LOG = logging.getLogger(__name__)


class GitUrlAction(workflows.Action):
    git_url = forms.CharField(label=_("Git URL"),
                              required=True)
    name = forms.CharField(label=_("App Name"),
                           required=True)
    description = forms.CharField(label=_("Description"))

    def __init__(self, request, *args, **kwargs):
        super(GitUrlAction, self).__init__(request, *args, **kwargs)

    class Meta(object):
        name = _("Select git url for the application")
        help_text_template = ("applications/_create_general_help.html")


class SelectGitUrl(workflows.Step):
    action_class = GitUrlAction
    contributes = ("name", "description", "git_url")


class CreateApplication(workflows.Workflow):
    slug = "create_application"
    name = _("Create Application")
    finalize_button_name = _("Create")
    success_message = _("Created")
    failure_message = _("Could not create")
    success_url = "horizon:solum:applications:index"
    default_steps = (SelectGitUrl,)

    def handle(self, request, context):
        LOG.warning('CreateApplication %s' % context)
        solum = solumclient(request)
        arti = {}
        arti['name'] = context.get('name', 'generated_artifact')
        arti['artifact_type'] = 'application.heroku'
        arti['content'] = {'href': context['git_url']}
        arti['language_pack'] = 'auto'

        plan = {}
        plan['name'] = context.get('name', 'generated_plan')
        plan['description'] = context.get('description', None)
        plan['artifacts'] = [arti]
        solum.plans.create(json.dumps(plan))
        return True
