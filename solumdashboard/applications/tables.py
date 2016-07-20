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

from django.core import urlresolvers
from django.utils import http
from django.utils.translation import ugettext_lazy as _
from horizon import tables

from solumdashboard.api.client import client as solumclient


class CreateApplication(tables.LinkAction):
    name = "create"
    verbose_name = _("New Application")
    url = "horizon:solum:applications:create"
    classes = ("btn-launch", "ajax-modal")


class LaunchApplication(tables.LinkAction):
    name = "build-and-deploy"
    verbose_name = _("Build and Deploy Application")
    url = "horizon:solum:applications:launch"
    classes = ("btn-launch", "ajax-modal")

    def get_link_url(self, datum):
        base_url = urlresolvers.reverse(self.url)

        params = http.urlencode({"application_id": datum.id})
        return "?".join([base_url, params])


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
        row_actions = (ViewApplication, LaunchApplication, DeleteApplication)
