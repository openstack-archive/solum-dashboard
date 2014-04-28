solum-dashboard
===============

Horizon plugin for Solum
Purpose of this plugin is to add Solum capabilities to the openstack dashboard.
This plugin requires a working openstack install including solum and horizon.

How to install solum-dashboard into Horizon.
--------------------------------------------

Enter these commands in your terminal
::

 sudo pip install -e /opt/stack/solum-dashboard
 cd /opt/stack/horizon/openstack_dashboard/local/enabled
 ln -s /opt/stack/solum-dashboard/_50_solum.py.example _50_solum.py
 sudo service apache2 restart
