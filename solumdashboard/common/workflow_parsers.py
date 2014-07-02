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

"""
Mistral DSL and Heat Template parsing and representation routines.

This code does not import the original YAML representations of the Mistral DSL
and Heat Templates as the data may be in memory instead of file.  PyYAML is a
good library to load the YAML and translate into a Python dictionary with code
like:

import yaml

with open("mistral_dsl.yaml", "r") as fptr
    data = yaml.load(fptr)

Important note:
This code expects that the loading code performs some basic YAML validation
* Mistral DSLs must include a "Workflow" section with a "tasks" subsection
* Mistral DSLs must have one task with no on-success (last task)
* Heat Templates must include a "requirements" section
"""


def get_mistral_tasks(data, start_task_name=None):
    """Returns an ordered Mistral task list from a DSL."""
    task_list = []
    task_dict = data["Workflow"]["tasks"]
    for key, task in task_dict.items():
        on_success = task.get("on-finish", task.get("on-success"))
        on_error = task.get("on-finish", task.get("on-error"))
        task_list.append([key, on_success, on_error])
    curr_task_name = None
    sorted_task_list = []
    no_suc_list = ([[name, on_suc, on_err] for (name, on_suc, on_err) in
                    task_list if on_suc is None])
    sorted_task_list.insert(0, no_suc_list[0])
    curr_task_name = no_suc_list[0][0]
    for count in range(len(task_list) - 1):
        for task in task_list:
            task_name, on_success, on_error = task
            if on_success == curr_task_name:
                curr_task_name = task_name
                sorted_task_list.insert(0, task)
                break
        if start_task_name:
            if start_task_name == task_name:
                break
    return sorted_task_list


def create_svg_mistral_tasks(task_list, radius=45):
    """Create an SVG UI diagram of Mistral task flow.

    This takes the output of get_mistral_tasks() and generates an SVG-based
    graphical diagram of the ordered Mistral tasks.  The code automatically
    scales the SVG based on the circle radius value.  Note that SVG circles
    don't scale radius by percentages very well which is why this is still
    pixel math.  The circle radius is the diagonal length of the viewport
    which is not very useful in this case.
    """
    indent = radius * 1.1
    diameter = radius * 2
    num_tasks = len(task_list)
    if num_tasks < 1:
        return "[No Tasks Found]"
    svg_output = ("<svg height=\"%d\" width=\"%d\">\n" %
                  ((diameter * 1.10), ((num_tasks-1) * diameter * 1.3) +
                   indent * 2))
    svg_output += ("  <line x1=\"%d\" y1=\"50%%\" x2=\"%d\" y2=\"50%%\" style="
                   "\"stroke:rgb(0,0,0);stroke-width:3\"/>\n" %
                   (indent, ((num_tasks-1) * diameter * 1.2) + indent))
    svg_output += ("  <g stroke=\"black\" stroke-width=\"3\" fill="
                   "\"lightgrey\">\n")
    for counter in range(num_tasks):
        svg_output += ("    <circle cx=\"%d\" cy=\"50%%\" r=\"%d\"/>\n" %
                       ((counter * diameter * 1.2 + indent), radius))
    svg_output += "  </g>\n"
    svg_output += "  <g style=\"text-anchor: middle; font-size: 13px\">\n"
    for counter in range(num_tasks):
        svg_output += ("    <text x=\"%d\" y=\"55%%\">%s</text>\n" %
                       ((counter * diameter * 1.2 + indent),
                        task_list[counter][0]))
    svg_output += "  </g>\n"
    svg_output += "</svg>\n"
    return svg_output


def get_mistral_required_input(data, start_task_name=None):
    """Returns required Mistral DSL user input field information.

    Note that this code ignores Mistral DSL values that are enumerated in the
    ignore_list list below which are under the "parameters:" label.  The
    recommendation is to not nest sections under a "parameters:" label and
    just list name/value pairs in the parameters section.
    """
    input_dict = {}
    task_list = get_mistral_tasks(data, start_task_name)
    task_key_list = [item[0] for item in task_list]
    task_dict = data["Workflow"]["tasks"]
    ignore_list = ["params", "settings", "arguments"]
    publish_list = []
    for task in task_key_list:
        param_list = task_dict[task].get("parameters", [])
        publish_list.extend(task_dict[task].get("publish", []))
        for param in param_list:
            if param not in ignore_list and param not in publish_list:
                if param not in input_dict:
                    input_dict[param] = [task]
                else:
                    input_dict[param].append(task)
    return input_dict


def get_heat_required_input(data):
    """Returns Heat required user input fields."""
    heat_params = []
    heat_param_dict = data["parameters"]
    for key, heat_param in heat_param_dict.items():
        heat_params.append([key,
                            heat_param.get("type"),
                            heat_param.get("default"),
                            heat_param.get("description")])
    return sorted(heat_params)


if __name__ == "__main__":
    # This code is left for example and basic testing purposes; it is not
    # intended for production use.

    import yaml

    with open("dsl.yaml", "r") as FPTR:
        DATA = yaml.load(FPTR)
    print("\nMistral Task workflow:")
    RET_DICT = get_mistral_tasks(DATA)
    for VAL in RET_DICT:
        print("%s - success: %s, error: %s" % (VAL[0], VAL[1], VAL[2]))

    SVG_TEXT = create_svg_mistral_tasks(RET_DICT, 45)
    print("\nSVG task output:\n" + SVG_TEXT)

    # Mistral required input
    print("\nMistral required inputs:")
    RET_DICT = get_mistral_required_input(DATA)
    for KEY, VAL in RET_DICT.items():
        print(KEY, "", VAL)

    # Heat required input
    print("\nHeat required inputs:")
    with open("hot.yaml", "r") as FPTR:
        DATA = yaml.load(FPTR)
    RET_DICT = get_heat_required_input(DATA)
    for VAL in RET_DICT:
        print("%s - %s, %s, %s" % (VAL[0], VAL[1], VAL[2], VAL[3]))
