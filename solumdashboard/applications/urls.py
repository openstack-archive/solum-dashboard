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

from django.urls import re_path

import solumdashboard.applications.views as views


urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^$', views.IndexView.as_view(), name='applications'),
    re_path(r'^create$', views.CreateView.as_view(), name='create'),
    re_path(r'^launch/(?P<application_id>[^/]+)$', views.LaunchView.as_view(),
            name='launch'),
    re_path(r'^detail/(?P<application_id>[^/]+)$',
            views.DetailView.as_view(), name='detail'),
    re_path(r'^scale/(?P<application_id>[^/]+)$', views.ScaleView.as_view(),
            name='scale'),
    re_path(r'^update/(?P<application_id>[^/]+)$', views.UpdateView.as_view(),
            name='update')
]
