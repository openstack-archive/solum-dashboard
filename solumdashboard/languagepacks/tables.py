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

from solumdashboard.api.client import client as solumclient


class DeleteLanguagepack(tables.DeleteAction):
    name = "delete"

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Languagepack",
            u"Delete Languagepacks",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Languagepack",
            u"Deleted Languagepacks",
            count
        )

    def allowed(self, request, template):
        return True

    def delete(self, request, languagepack_id):
        solum = solumclient(request)
        solum.languagepacks.delete(lp_id=languagepack_id)


class CreateLanguagepack(tables.LinkAction):
    name = "create"
    verbose_name = _("New Languagepack")
    url = "horizon:solum:languagepacks:create"
    classes = ("btn-launch", "ajax-modal")


class LanguagepacksTable(tables.DataTable):
    uuid = tables.Column("uuid", verbose_name=_("UUID"),
                         link=("horizon:solum:languagepacks:detail"))
    name = tables.Column("name", verbose_name=_("Name"))
    description = tables.Column("description", verbose_name=_("Description"))
    status = tables.Column("status", verbose_name=_("Status"))
    source_uri = tables.Column("source_uri", verbose_name=_("Source Uri"))

    def get_object_id(self, lp):
        return lp.uuid

    class Meta(object):
        name = "languagepacks"
        verbose_name = _("Languagepacks")
        table_actions = (CreateLanguagepack, DeleteLanguagepack)
        row_actions = (DeleteLanguagepack,)
