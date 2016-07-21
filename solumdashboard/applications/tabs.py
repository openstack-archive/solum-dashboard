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

import json

from horizon import tabs

from solumclient.v1 import workflow as cli_wf

from solumdashboard.api.client import client as solumclient


class GeneralTab(tabs.Tab):
    name = _("General Info")
    slug = "application_details_tab"
    template_name = ("applications/_detail.html")

    def get_context_data(self, request):
        app_id = self.tab_group.kwargs['application_id']
        solum = solumclient(request)
        app = solum.apps.find(name_or_id=app_id)

        app.trigger = app.trigger_actions
        app.workflow = app.workflow_config
        if app.scale_config.get(app.name, ''):
            app.target_instances = app.scale_config[app.name].get('target', '')

        workflowman = cli_wf.WorkflowManager(solum, app_id=app_id)
        workflows = workflowman.list()

        return {"application": app, "workflows": workflows}


class LogTab(tabs.Tab):
    name = _("Logs")
    slug = "application_logs_tab"
    template_name = ("applications/_log.html")

    def get_context_data(self, request):
        app_id = self.tab_group.kwargs['application_id']
        solum = solumclient(request)
        app = solum.apps.find(name_or_id=app_id)

        workflowman = cli_wf.WorkflowManager(solum, app_id=app_id)
        workflows = workflowman.list()

        logs_list = []

        for workflow in workflows:
            revision = workflow.wf_id
            loglist = workflowman.logs(revision_or_id=revision)
            for log in loglist:
                logs_list.append(log)
                strategy_info = json.loads(log.strategy_info)
                if log.strategy == 'local':
                    log.local_storage = log.location
                elif log.strategy == 'swift':
                    log.swift_container = strategy_info['container']
                    log.swift_path = log.location

        return {"logs": logs_list, "application": app}


class AppDetailsTabs(tabs.TabGroup):
    slug = "application_details"
    tabs = (GeneralTab, LogTab)
    sticky = True
