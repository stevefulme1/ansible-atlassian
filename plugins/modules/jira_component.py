#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_component
short_description: Manage project components
version_added: "1.0.0"
description:
  - Create, update, and delete jira component resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the jira component resource.
    type: str
    choices: ['present', 'absent']
    default: present
  ari:
    description:
      - >-
        Compass component's ID. Can't be updated. Not required for creating a Project Component.
    type: str
  assignee:
    description:
      - >-
        A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
    type: dict
  assigneeType:
    description:
      - >-
        The nominal user type used to determine the assignee for issues created with this component. See...
    type: str
    choices: ["PROJECT_DEFAULT", "COMPONENT_LEAD", "PROJECT_LEAD", "UNASSIGNED"]
  description:
    description:
      - >-
        The description for the component. Optional when creating or updating a component.
    type: str
  id:
    description:
      - >-
        The unique identifier for the component.
    type: str
  isAssigneeTypeValid:
    description:
      - >-
        Whether a user is associated with assigneeType. For example, if the assigneeType is set to...
    type: bool
  lead:
    description:
      - >-
        A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
    type: dict
  leadAccountId:
    description:
      - >-
        The accountId of the component's lead user. The accountId uniquely identifies the user across...
    type: str
  leadUserName:
    description:
      - >-
        This property is no longer available and will be removed from the documentation soon. See the...
    type: str
  metadata:
    description:
      - >-
        Compass component's metadata. Can't be updated. Not required for creating a Project Component.
    type: dict
  name:
    description:
      - >-
        The unique name for the component in the project. Required when creating a component. Optional...
    type: str
  project:
    description:
      - >-
        The key of the project the component is assigned to. Required when creating a component. Can't...
    type: str
  projectId:
    description:
      - >-
        The ID of the project the component is assigned to.
    type: int
  realAssignee:
    description:
      - >-
        A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
    type: dict
  realAssigneeType:
    description:
      - >-
        The type of the assignee that is assigned to issues created with this component, when an...
    type: str
    choices: ["PROJECT_DEFAULT", "COMPONENT_LEAD", "PROJECT_LEAD", "UNASSIGNED"]
  self:
    description:
      - >-
        The URL of the component.
    type: str
extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""
- name: Create a jira component
  stevefulme1.atlassian.jira_component:
    state: present
  # API: POST /rest/api/3/component
- name: Update a jira component
  stevefulme1.atlassian.jira_component:
    id: "existing_id"
    ari: "updated_ari"
    assignee: "updated_assignee"
    assigneeType: "updated_assigneeType"
    description: "updated_description"
    isAssigneeTypeValid: "updated_isAssigneeTypeValid"
    lead: "updated_lead"
    leadAccountId: "updated_leadAccountId"
    leadUserName: "updated_leadUserName"
    metadata: "updated_metadata"
    name: "updated_name"
    project: "updated_project"
    projectId: "updated_projectId"
    realAssignee: "updated_realAssignee"
    realAssigneeType: "updated_realAssigneeType"
    self: "updated_self"
    state: present
  # API:
- name: Delete a jira component
  stevefulme1.atlassian.jira_component:
    id: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/component/{id}
"""

RETURN = r"""
ari:
  description: >-
    Compass component's ID. Can't be updated. Not required for creating a Project Component.
  returned: success
  type: str
assignee:
  description: >-
    A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
  returned: success
  type: dict
assigneeType:
  description: >-
    The nominal user type used to determine the assignee for issues created with this component. See...
  returned: success
  type: str
description:
  description: >-
    The description for the component. Optional when creating or updating a component.
  returned: success
  type: str
id:
  description: >-
    The unique identifier for the component.
  returned: success
  type: str
isAssigneeTypeValid:
  description: >-
    Whether a user is associated with assigneeType. For example, if the assigneeType is set to...
  returned: success
  type: bool
lead:
  description: >-
    A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
  returned: success
  type: dict
leadAccountId:
  description: >-
    The accountId of the component's lead user. The accountId uniquely identifies the user across...
  returned: success
  type: str
leadUserName:
  description: >-
    This property is no longer available and will be removed from the documentation soon. See the...
  returned: success
  type: str
metadata:
  description: >-
    Compass component's metadata. Can't be updated. Not required for creating a Project Component.
  returned: success
  type: dict
name:
  description: >-
    The unique name for the component in the project. Required when creating a component. Optional...
  returned: success
  type: str
project:
  description: >-
    The key of the project the component is assigned to. Required when creating a component. Can't...
  returned: success
  type: str
projectId:
  description: >-
    The ID of the project the component is assigned to.
  returned: success
  type: int
realAssignee:
  description: >-
    A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
  returned: success
  type: dict
realAssigneeType:
  description: >-
    The type of the assignee that is assigned to issues created with this component, when an...
  returned: success
  type: str
self:
  description: >-
    The URL of the component.
  returned: success
  type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def get_current_state(client, module):
    """Retrieve the current state of the jira component via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/rest/api/3/component")
        if isinstance(items, dict):
            items = items.get("results", items.get("data", items.get("items", [])))
        for item in items:
            if str(item.get(search_key)) == str(search_value):
                return item
            if str(item.get("id")) == str(search_value):
                return item
        return None
    except ClientError:
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

    if module.params.get("ari") is not None:
        payload["ari"] = module.params["ari"]

    if module.params.get("assignee") is not None:
        payload["assignee"] = module.params["assignee"]

    if module.params.get("assigneeType") is not None:
        payload["assigneeType"] = module.params["assigneeType"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("id") is not None:
        payload["id"] = module.params["id"]

    if module.params.get("isAssigneeTypeValid") is not None:
        payload["isAssigneeTypeValid"] = module.params["isAssigneeTypeValid"]

    if module.params.get("lead") is not None:
        payload["lead"] = module.params["lead"]

    if module.params.get("leadAccountId") is not None:
        payload["leadAccountId"] = module.params["leadAccountId"]

    if module.params.get("leadUserName") is not None:
        payload["leadUserName"] = module.params["leadUserName"]

    if module.params.get("metadata") is not None:
        payload["metadata"] = module.params["metadata"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("project") is not None:
        payload["project"] = module.params["project"]

    if module.params.get("projectId") is not None:
        payload["projectId"] = module.params["projectId"]

    if module.params.get("realAssignee") is not None:
        payload["realAssignee"] = module.params["realAssignee"]

    if module.params.get("realAssigneeType") is not None:
        payload["realAssigneeType"] = module.params["realAssigneeType"]

    if module.params.get("self") is not None:
        payload["self"] = module.params["self"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            ari=dict(
                type="str",








            ),

            assignee=dict(
                type="dict",








            ),

            assigneeType=dict(
                type="str",





                choices=['PROJECT_DEFAULT', 'COMPONENT_LEAD', 'PROJECT_LEAD', 'UNASSIGNED'],




            ),

            description=dict(
                type="str",








            ),

            id=dict(
                type="str",








            ),

            isAssigneeTypeValid=dict(
                type="bool",








            ),

            lead=dict(
                type="dict",








            ),

            leadAccountId=dict(
                type="str",








            ),

            leadUserName=dict(
                type="str",








            ),

            metadata=dict(
                type="dict",








            ),

            name=dict(
                type="str",








            ),

            project=dict(
                type="str",








            ),

            projectId=dict(
                type="int",








            ),

            realAssignee=dict(
                type="dict",








            ),

            realAssigneeType=dict(
                type="str",





                choices=['PROJECT_DEFAULT', 'COMPONENT_LEAD', 'PROJECT_LEAD', 'UNASSIGNED'],




            ),

            self=dict(
                type="str",








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
                        "/rest/api/3/component",
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

                result["ari"] = current.get("ari")

                result["assignee"] = current.get("assignee")

                result["assigneeType"] = current.get("assigneeType")

                result["description"] = current.get("description")

                result["id"] = current.get("id")

                result["isAssigneeTypeValid"] = current.get("isAssigneeTypeValid")

                result["lead"] = current.get("lead")

                result["leadAccountId"] = current.get("leadAccountId")

                result["leadUserName"] = current.get("leadUserName")

                result["metadata"] = current.get("metadata")

                result["name"] = current.get("name")

                result["project"] = current.get("project")

                result["projectId"] = current.get("projectId")

                result["realAssignee"] = current.get("realAssignee")

                result["realAssigneeType"] = current.get("realAssigneeType")

                result["self"] = current.get("self")

                pass

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/rest/api/3/component/{id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
