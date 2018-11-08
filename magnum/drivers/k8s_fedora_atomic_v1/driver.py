# Copyright 2016 Rackspace Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_log import log as logging

from magnum.common import keystone
from magnum.common import octavia
from magnum.drivers.common import k8s_monitor
from magnum.drivers.heat import driver
from magnum.drivers.k8s_fedora_atomic_v1 import template_def

LOG = logging.getLogger(__name__)


class Driver(driver.HeatDriver):

    @property
    def provides(self):
        return [
            {'server_type': 'vm',
             'os': 'fedora-atomic',
             'coe': 'kubernetes'},
        ]

    def get_template_definition(self):
        return template_def.AtomicK8sTemplateDefinition()

    def get_monitor(self, context, cluster):
        return k8s_monitor.K8sMonitor(context, cluster)

    def get_scale_manager(self, context, osclient, cluster):
        # FIXME: Until the kubernetes client is fixed, remove
        # the scale_manager.
        # https://bugs.launchpad.net/magnum/+bug/1746510
        return None

    def pre_delete_cluster(self, context, cluster):
        """Delete cloud resources before deleting the cluster."""
        if keystone.is_octavia_enabled():
            LOG.info("Starting to delete loadbalancers for cluster %s",
                     cluster.uuid)
            octavia.delete_loadbalancers(context, cluster)
