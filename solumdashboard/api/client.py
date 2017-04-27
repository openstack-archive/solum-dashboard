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

from django.conf import settings

from horizon import exceptions

from solumclient import client as api_client

from openstack_dashboard.api import base
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


def get_solum_url(request):
    endpoint = getattr(settings, 'SOLUM_URL', None)
    if not endpoint:
        try:
            endpoint = base.url_for(request, 'application_deployment')
        except exceptions.ServiceCatalogException:
            endpoint = 'http://localhost:9777'
            LOG.warning('Solum API location could not be found in Service '
                        'Catalog, using default: {0}'.format(endpoint))
    return endpoint


def client(request):
    auth_url = getattr(settings, 'OPENSTACK_KEYSTONE_URL')
    return api_client.Client(1, endpoint=get_solum_url(request),
                             token=request.user.token.id,
                             auth_url=auth_url)
