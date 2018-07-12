========================
Team and repository tags
========================

.. image:: http://governance.openstack.org/badges/solum-dashboard.svg
    :target: http://governance.openstack.org/reference/tags/index.html

.. Change things from this point on

solum-dashboard
===============

Horizon plugin for Solum
Purpose of this plugin is to add Solum capabilities to the openstack dashboard.
This plugin requires a working openstack install including solum and horizon.

How to install solum-dashboard into Horizon.
--------------------------------------------

Enter these commands in your terminal:

 sudo pip install -e /opt/stack/solum-dashboard
 cd /opt/stack/horizon/openstack_dashboard/local/enabled
 ln -s /opt/stack/solum-dashboard/solumdashboard/local/enabled/_50_solum.py _50_solum.py
 sudo service apache2 restart
