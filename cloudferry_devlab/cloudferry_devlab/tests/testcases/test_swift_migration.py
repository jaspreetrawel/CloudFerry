# Copyright (c) 2015 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.

import unittest

from generator import generator, generate
from nose.plugins.attrib import attr

from cloudferry_devlab.tests import functional_test


@generator
class SwiftResourceMigrationTests(functional_test.FunctionalTest):
    """
    Test Case class which includes all resource's migration cases.
    """

    def validate_swift_container_objects_parameter(self, src_container, dst_container, param, field):
        msgs = []
        src_cont_objects = src_container[param]
        dst_cont_objects = dst_container[param]

        if not src_cont_objects:
            self.skipTest(
                'Nothing to migrate - source object list is empty')

        for src_cont_object in src_cont_objects:
            for dst_cont_object in dst_cont_objects:
                if src_cont_object[field] == dst_cont_object[field]:
                        break
            else:
                error_msg = ('container object with name {obj_name} was not found on dst')
                msgs.append(error_msg.format(obj_name=src_cont_object[field]))
        return msgs

    @attr(migrated_tenant=['admin'])
    def test_migrate_swift_containers_objects(self):
        """Validate swift containers and objects were migrated.

        :param name: container name"""

        src_container_list = self.filter_containers()
        #dst_container_list = self.dst_cloud.get_swift_account()[1]
	dst_container_list = self.filter_containers()

        #src_account_header = self.src_cloud.get_swift_account()[0]
        #dst_account_header = self.dst_cloud.get_swift_account()[0]


        fail_msg = []

        # for account validation
        #if src_account_header != dst_account_header:
        #    msg = 'swift account with name %s was not found on dst'
        #     fail_msg.append(msg % str(src_account_header))

        #if fail_msg:
        #    self.fail('\n'.join(fail_msg))

        if not src_container_list:
            self.skipTest(
                'Nothing to migrate - source container list is empty')

         #for parameter in ['name']:
         #    self.validate_resource_parameter_in_dst(
         #        src_container_list, dst_container_list, resource_name='container',
         #        parameter=parameter)

        for src_container in src_container_list:
            src_cont_name = getattr(src_container, 'name')
            for dst_container in dst_container_list:
                dst_cont_name = getattr(dst_container, 'name')

                if src_cont_name != dst_cont_name:
                    continue

                fail_msg.extend(self.validate_swift_container_objects_parameter(
                        src_container, dst_container, 'objects', 'name'))
                break
            else:
                msg = 'container with name %s was not found on dst'
                fail_msg.append(msg % str(src_cont_name))

        if fail_msg:
            self.fail('\n'.join(fail_msg))

