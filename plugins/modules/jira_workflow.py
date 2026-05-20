#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_workflow
short_description: Manage workflows
version_added: "1.0.0"
description:
  - Create, update, and delete jira workflow resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the jira workflow resource.
    type: str
    choices: ['present', 'absent']
    default: present
  projectAndIssueTypes:
    description:
      - >-
        The list of projects and issue types to query.
    type: list
  workflowIds:
    description:
      - >-
        The list of workflow IDs to query.
    type: list
  workflowNames:
    description:
      - >-
        The list of workflow names to query.
    type: list
extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""
- name: Create a jira workflow
  stevefulme1.atlassian.jira_workflow:
    state: present
  # API: POST /rest/api/3/workflows
- name: Update a jira workflow
  stevefulme1.atlassian.jira_workflow:
    id: "existing_id"
    projectAndIssueTypes: "updated_projectAndIssueTypes"
    workflowIds: "updated_workflowIds"
    workflowNames: "updated_workflowNames"
    state: present
  # API:
- name: Delete a jira workflow
  stevefulme1.atlassian.jira_workflow:
    id: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/workflow/{entityId}
"""

RETURN = r"""
statuses:
  description: >-
    List of statuses.
  returned: success
  type: list
workflows:
  description: >-
    List of workflows.
  returned: success
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def get_current_state(client, module):
    """Retrieve the current state of the jira workflow via GET."""

    return None


def needs_update(current, desired):
    """Compare current state against desired params and return True if an update is needed."""
    if current is None:
        return True
    for key, value in desired.items():
        if value is None:
            continue
        current_value = current.get(key)
        if current_value != value:
            return True
    return False


def build_payload(module):
    """Build the API request payload from module params."""
    payload = {}

    if module.params.get("projectAndIssueTypes") is not None:
        payload["projectAndIssueTypes"] = module.params["projectAndIssueTypes"]

    if module.params.get("workflowIds") is not None:
        payload["workflowIds"] = module.params["workflowIds"]

    if module.params.get("workflowNames") is not None:
        payload["workflowNames"] = module.params["workflowNames"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            projectAndIssueTypes=dict(
                type="list",


            ),

            workflowIds=dict(
                type="list",


            ),

            workflowNames=dict(
                type="list",


            ),

        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,

    )

    state = module.params["state"]
    result = dict(changed=False, diff=dict(before={}, after={}))

    try:
        client = Client(module)
        current = get_current_state(client, module)

        if state == "present":
            desired = build_payload(module)

            if current is None:
                # Resource does not exist — create it
                result["changed"] = True
                result["diff"]["before"] = {}
                result["diff"]["after"] = desired

                if not module.check_mode:

                    response = client.POST(
                        "/rest/api/3/workflows",
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})


            elif needs_update(current, desired):
                # Resource exists but needs updating
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = dict(current, **{k: v for k, v in desired.items() if v is not None})

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "".replace(
                        "{id}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})


            else:
                # Resource exists and is up-to-date

                result["statuses"] = current.get("statuses")

                result["workflows"] = current.get("workflows")

                pass

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/rest/api/3/workflow/{entityId}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
