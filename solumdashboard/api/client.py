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

from solumclient import client as api_client

from solumdashboard.utils import importutils


# horizon.api is for backward compatibility with folsom
base = importutils.import_any('openstack_dashboard.api.base',
                              'horizon.api.base')

keystone = importutils.import_any('openstack_dashboard.api.keystone',
                                  'horizon.api.keystone')

LOG = logging.getLogger(__name__)


def get_horizon_parameter(name, default_value):
    import openstack_dashboard.settings

    if hasattr(openstack_dashboard.settings, name):
        return getattr(openstack_dashboard.settings, name)
    else:
        logging.info('Parameter %s is not found in local_settings.py, '
                     'using default "%s"' % (name, default_value))
        return default_value


# These parameters should be defined in Horizon's local_settings.py
# Example SOLUM_URL - http://localhost:9000/v1.0
SOLUM_URL = get_horizon_parameter('SOLUM_URL', None)
# "type" of Solum service registered in keystone
SOLUM_SERVICE = get_horizon_parameter('SOLUM_SERVICE',
                                      'application_deployment')


def get_solum_url(request):
    return base.url_for(request, SOLUM_SERVICE)


def client(request):
    endpoint_type = get_horizon_parameter('OPENSTACK_ENDPOINT_TYPE',
                                          'internalURL')
    auth_url = keystone._get_endpoint_url(request, endpoint_type)
    return api_client.Client('1', endpoint=get_solum_url(request),
                             service_type=SOLUM_SERVICE,
                             tenant_id=request.user.tenant_id,
                             token=request.user.token.id,
                             auth_url=auth_url)
