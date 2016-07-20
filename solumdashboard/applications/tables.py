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
from django.utils.translation import ungettext_lazy

from horizon import tables

from solumclient.v1 import app as cli_app

from solumdashboard.api.client import client as solumclient
from solumdashboard.applications import tabs


class CreateApplication(tables.LinkAction):
    name = "create"
    verbose_name = _("New Application")
    url = "horizon:solum:applications:create"
    classes = ("btn-launch", "ajax-modal")


class ScaleApplication(tables.LinkAction):
    name = "scale"
    verbose_name = _("Scale Application")
    url = "horizon:solum:applications:scale"
    classes = ("btn-launch", "ajax-modal")


class UpdateApplication(tables.LinkAction):
    name = "update"
    verbose_name = _("Update Application")
    url = "horizon:solum:applications:update"
    classes = ("btn-launch", "ajax-modal")


class LaunchApplication(tables.LinkAction):
    name = "build-and-deploy"
    verbose_name = _("Build and Deploy Application")
    url = "horizon:solum:applications:launch"
    classes = ("btn-launch", "ajax-modal")

    def allowed(self, request, package):
        return True


class DeleteApplication(tables.DeleteAction):
    name = "delete"

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Application",
            u"Delete Applications",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Application",
            u"Deleted Applications",
            count
        )

    def allowed(self, request, template):
        return True

    def delete(self, request, application_id):
        solum = solumclient(request)
        cli_app.AppManager(solum).delete(app_id=application_id)


class ViewApplicationLogs(tables.LinkAction):
    name = "view"
    verbose_name = _("View Application Logs")
    url = "horizon:solum:applications:detail"
    classes = ("btn-edit",)

    def get_link_url(self, datum):
        base_url = super(ViewApplicationLogs, self).get_link_url(datum)
        tab_query_string = tabs.LogTab(
            tabs.AppDetailsTabs).get_query_string()
        return "?".join([base_url, tab_query_string])


class ApplicationsTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_('Name'))
    id = tables.Column('id', verbose_name=_('ID'),
                       link=("horizon:solum:applications:detail"))
    created_at = tables.Column('created_at', verbose_name=_('Created at'))
    description = tables.Column('description', verbose_name=_('Description'))
    languagepack = tables.Column('languagepack',
                                 verbose_name=_('Languagepack'))

    def get_object_id(self, app):
        return app.id

    class Meta(object):
        name = "applications"
        verbose_name = _("Applications")
        table_actions = (CreateApplication, DeleteApplication)
        row_actions = (ViewApplicationLogs, LaunchApplication,
                       DeleteApplication, ScaleApplication, UpdateApplication)
