#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_issue_type
short_description: Manage issue types
version_added: "1.0.0"
description:
  - Create, update, and delete jira issue type resources.
  - Supports check mode and diff mode for safe operations.

author:
  - "Steve Fulmer (@stevefulme1)"

options:
  state:
    description:
      - Desired state of the jira issue type resource.
    type: str
    choices: ['present', 'absent']
    default: present
  avatarId:
    description:
      - >-
        The ID of an issue type avatar. This can be obtained be obtained from the following endpoints:...
    type: int
  description:
    description:
      - >-
        The description of the issue type.
    type: str
  hierarchyLevel:
    description:
      - >-
        The hierarchy level of the issue type. Use: -1 for Subtask. 0 for Base. Defaults to 0.
    type: int
  name:
    description:
      - >-
        The unique name for the issue type. The maximum length is 60 characters.
    type: str
  type:
    description:
      - >-
        Deprecated. Use hierarchyLevel instead. See the deprecation notice for details. Whether the...
    type: str
    choices: ["subtask", "standard"]

extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""
- name: Create a jira issue type
  stevefulme1.atlassian.jira_issue_type:
    state: present
  # API: POST /rest/api/3/issuetype

- name: Update a jira issue type
  stevefulme1.atlassian.jira_issue_type:
    id: "existing_id"
    avatarId: "updated_avatarId"
    description: "updated_description"
    hierarchyLevel: "updated_hierarchyLevel"
    name: "updated_name"
    type: "updated_type"
    state: present
  # API:

- name: Delete a jira issue type
  stevefulme1.atlassian.jira_issue_type:
    id: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/issuetype/{id}
"""

RETURN = r"""
avatarId:
  description: >-
    The ID of the issue type's avatar.
  returned: success
  type: int

description:
  description: >-
    The description of the issue type.
  returned: success
  type: str

entityId:
  description: >-
    Unique ID for next-gen projects.
  returned: success
  type: str

hierarchyLevel:
  description: >-
    Hierarchy level of the issue type.
  returned: success
  type: int

iconUrl:
  description: >-
    The URL of the issue type's avatar.
  returned: success
  type: str

id:
  description: >-
    The ID of the issue type.
  returned: success
  type: str

name:
  description: >-
    The name of the issue type.
  returned: success
  type: str

scope:
  description: >-
    The projects the item is associated with. Indicated for items associated with next-gen projects.
  returned: success
  type: dict

self:
  description: >-
    The URL of these issue type details.
  returned: success
  type: str

subtask:
  description: >-
    Whether this issue type is used to create subtasks.
  returned: success
  type: bool
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,

)


def get_current_state(client, module):
    """Retrieve the current state of the jira issue type via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/rest/api/3/issuetype")
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

    if module.params.get("avatarId") is not None:
        payload["avatarId"] = module.params["avatarId"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("hierarchyLevel") is not None:
        payload["hierarchyLevel"] = module.params["hierarchyLevel"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("type") is not None:
        payload["type"] = module.params["type"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            avatarId=dict(
                type="int",

            ),

            description=dict(
                type="str",

            ),

            hierarchyLevel=dict(
                type="int",

            ),

            name=dict(
                type="str",

            ),

            type=dict(
                type="str",

                choices=['subtask', 'standard'],

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
                        "/rest/api/3/issuetype",
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

                result["avatarId"] = current.get("avatarId")

                result["description"] = current.get("description")

                result["entityId"] = current.get("entityId")

                result["hierarchyLevel"] = current.get("hierarchyLevel")

                result["iconUrl"] = current.get("iconUrl")

                result["id"] = current.get("id")

                result["name"] = current.get("name")

                result["scope"] = current.get("scope")

                result["self"] = current.get("self")

                result["subtask"] = current.get("subtask")

                pass

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/rest/api/3/issuetype/{id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
