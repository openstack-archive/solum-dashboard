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

from django.utils.translation import ugettext as _

from horizon import tables

from solumdashboard.api.client import client as solumclient


class CreateApplication(tables.LinkAction):
    name = "create"
    verbose_name = _("New Application")
    url = "horizon:solum:applications:create"
    classes = ("btn-launch", "ajax-modal")


class DeleteApplication(tables.BatchAction):
    name = "delete"
    verbose_name = _("Delete Application")
    classes = ("btn-terminate", "btn-danger")

    action_present = _("Delete")
    action_past = _("Deleted")
    data_type_singular = _("Application")
    data_type_plural = _("Applications")

    def allowed(self, request, template):
        return True

    def action(self, request, application_id):
        solum = solumclient(request)
        solum.plans.delete(plan_id=application_id)


class ViewApplication(tables.LinkAction):
    name = "view"
    verbose_name = _("View")
    url = "horizon:solum:applications:detail"
    classes = ("btn-edit",)


class ApplicationsTable(tables.DataTable):
    uuid = tables.Column('uuid', verbose_name=_('UUID'),
                         link=("horizon:solum:applications:detail"))
    name = tables.Column('name', verbose_name=_('Name'))
    #git_url = tables.Column('git_url', verbose_name=_('GitUrl'))
    description = tables.Column('description', verbose_name=_('Description'))

    def get_object_id(self, app):
        return app.uuid

    class Meta:
        name = "applications"
        verbose_name = _("Applications")
        table_actions = (CreateApplication, DeleteApplication)
        row_actions = (ViewApplication, DeleteApplication)
