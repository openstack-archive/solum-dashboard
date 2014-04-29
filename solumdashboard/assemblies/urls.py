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

import solumdashboard.assemblies.views as views
from solumdashboard.utils import importutils

urls = importutils.import_any('django.conf.urls.defaults',
                              'django.conf.urls')


patterns = urls.patterns
url = urls.url


urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(),
                           name='index'),
                       url(r'^$', views.IndexView.as_view(),
                           name='assemblies'),
                       url(r'^(?P<assembly_id>[^/]+)$',
                           views.DetailView.as_view(),
                           name='detail'))
