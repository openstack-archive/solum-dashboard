# Copyright 2014 - Rackspace
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest

from solumdashboard.common import workflow_parsers


MISTRAL_DSL = {
    "Namespaces": {
        "Nova": {
            "actions": "random data"
        }
    },
    "Workflow": {
        "tasks": {
            "createVM": {
                "action": "Nova.createVM",
                "parameters": {
                    "nova_url": "$.nova_url",
                    "auth_token": "$.auth_token"
                },
                "publish": {
                    "vm_id": "vm_id"
                },
                "on-success": "waitForIP"
            },
            "waitForIP": {
                "action": "Nova.getIP",
                "publish": {
                    "vm_ip": "vm_ip"
                },
                "parameters": {
                    "nova_url": "$.nova_url",
                    "project_id": "$.project_id",
                    "auth_token": "$.auth_token"
                },
                "on-error": "errorTask"
            }
        }
    }
}

HEAT_TEMPLATE = {
    "heat_template_version": "2013-05-23",
    "description": "Basic app deploy.",
    "parameters": {
        "app_name": {
            "type": "string",
            "default": "solum-app",
            "description": "app name desc"
        },
        "key_name": {
            "type": "string",
            "default": "mykey"
        }
    },
    "randomstuff": "blah blah blah"
}


class TestWorkflowParsers(unittest.TestCase):
    """Test routines for workflow parsing code."""
    def test_get_mistral_tasks(self):
        """Test get Mistral Tasks functionality."""
        # Correct operation test case
        task_list = workflow_parsers.get_mistral_tasks(MISTRAL_DSL)
        self.assertEqual(task_list,
                         [["createVM", "waitForIP", None],
                          ["waitForIP", None, "errorTask"]])
        # Missing "tasks" section from Workflow
        dsl_copy = MISTRAL_DSL.copy()
        dsl_copy["Workflow"] = {"garbage": "here", "nothing": "useful"}
        self.assertRaises(KeyError, workflow_parsers.get_mistral_tasks,
                          dsl_copy)
        # All tasks have an on-success condition (invalid DSL)
        dsl_copy = MISTRAL_DSL.copy()
        dsl_copy["Workflow"]["tasks"]["waitForIP"]["on-success"] = "noTask"
        self.assertRaises(IndexError, workflow_parsers.get_mistral_tasks,
                          dsl_copy)
        # None data test case
        self.assertRaises(TypeError, workflow_parsers.get_mistral_tasks, None)

    def test_get_mistral_required_input(self):
        """Test get Mistral required user input functionality."""
        # Handle None data
        self.assertRaises(TypeError, workflow_parsers.get_mistral_tasks, None)
        # Correct operation test case
        input_dict = workflow_parsers.get_mistral_required_input(MISTRAL_DSL)
        self.assertEqual(input_dict,
                         {"nova_url": ["createVM", "waitForIP"],
                          "auth_token": ["createVM", "waitForIP"],
                          "project_id": ["waitForIP"]})
        # Remove the "tasks" section from Workflow
        dsl_copy = MISTRAL_DSL.copy()
        dsl_copy["Workflow"] = {"garbage": "here", "nothing": "useful"}
        self.assertRaises(KeyError,
                          workflow_parsers.get_mistral_required_input,
                          dsl_copy)
        # Verify that a publish removes the input from the next task
        dsl_copy = MISTRAL_DSL.copy()
        dsl_copy["Workflow"]["tasks"]["createVM"]["publish"] = (
            {"project_id": "test project"})
        input_dict = workflow_parsers.get_mistral_required_input(dsl_copy)
        self.assertEqual(input_dict,
                         {"nova_url": ["createVM", "waitForIP"],
                          "auth_token": ["createVM", "waitForIP"]})
        # Test ignoring of odd tags like "arguments"
        dsl_copy["Workflow"]["tasks"]["createVM"]["parameters"] = (
            {"key": "value", "arguments": {"random arguments"}})
        input_dict = workflow_parsers.get_mistral_required_input(dsl_copy)
        self.assertEqual(input_dict,
                         {"key": ["createVM"], "nova_url": ["waitForIP"],
                          "auth_token": ["waitForIP"]})

    def test_get_heat_required_input(self):
        """Test get Heat required user input functionality."""
        # Handle None data
        self.assertRaises(TypeError, workflow_parsers.get_heat_required_input,
                          None)
        # Remove the "parameters" section from the HoT
        hot_copy = {"nothing_here": "error time"}
        self.assertRaises(KeyError,
                          workflow_parsers.get_heat_required_input,
                          hot_copy)
        # Correct operation test case
        heat_list = workflow_parsers.get_heat_required_input(HEAT_TEMPLATE)
        self.assertEqual(heat_list,
                         [["app_name", "string", "solum-app", "app name desc"],
                          ["key_name", "string", "mykey", None]])


if __name__ == "__main__":
    unittest.main()
