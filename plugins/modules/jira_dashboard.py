#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_dashboard
short_description: Manage dashboards
version_added: "1.0.0"
description:
  - Create, update, and delete jira dashboard resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the jira dashboard resource.
    type: str
    choices: ['present', 'absent']
    default: present

  editPermissions:
    description:
      - >-
        The edit permissions for the dashboard.
    type: list

    required: true


  name:
    description:
      - >-
        The name of the dashboard.
    type: str

    required: true


  sharePermissions:
    description:
      - >-
        The share permissions for the dashboard.
    type: list

    required: true


  description:
    description:
      - >-
        The description of the dashboard.
    type: str


extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""

- name: Create a jira dashboard
  stevefulme1.atlassian.jira_dashboard:


    editPermissions: "example_editPermissions"


    name: "example_name"


    sharePermissions: "example_sharePermissions"


    state: present
  # API: POST /rest/api/3/dashboard


- name: Update a jira dashboard
  stevefulme1.atlassian.jira_dashboard:
    id: "existing_id"


    description: "updated_description"


    state: present
  # API:


- name: Delete a jira dashboard
  stevefulme1.atlassian.jira_dashboard:
    id: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/dashboard/{id}

"""

RETURN = r"""

automaticRefreshMs:
  description: >-
    The automatic refresh interval for the dashboard in milliseconds.
  returned: success
  type: int


description:
  description: >-

  returned: success
  type: str


editPermissions:
  description: >-
    The details of any edit share permissions for the dashboard.
  returned: success
  type: list


id:
  description: >-
    The ID of the dashboard.
  returned: success
  type: str


isFavourite:
  description: >-
    Whether the dashboard is selected as a favorite by the user.
  returned: success
  type: bool


isWritable:
  description: >-
    Whether the current user has permission to edit the dashboard.
  returned: success
  type: bool


name:
  description: >-
    The name of the dashboard.
  returned: success
  type: str


owner:
  description: >-

  returned: success
  type: dict


popularity:
  description: >-
    The number of users who have this dashboard as a favorite.
  returned: success
  type: int


rank:
  description: >-
    The rank of this dashboard.
  returned: success
  type: int


self:
  description: >-
    The URL of these dashboard details.
  returned: success
  type: str


sharePermissions:
  description: >-
    The details of any view share permissions for the dashboard.
  returned: success
  type: list


systemDashboard:
  description: >-
    Whether the current dashboard is system dashboard.
  returned: success
  type: bool


view:
  description: >-
    The URL of the dashboard.
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
    """Retrieve the current state of the jira dashboard via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/rest/api/3/dashboard")
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

    if module.params.get("editPermissions") is not None:
        payload["editPermissions"] = module.params["editPermissions"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("sharePermissions") is not None:
        payload["sharePermissions"] = module.params["sharePermissions"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            editPermissions=dict(
                type="list",

                required=True,


            ),

            name=dict(
                type="str",

                required=True,


            ),

            sharePermissions=dict(
                type="list",

                required=True,


            ),

            description=dict(
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
                        "/rest/api/3/dashboard",
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

                result["automaticRefreshMs"] = current.get("automaticRefreshMs")

                result["description"] = current.get("description")

                result["editPermissions"] = current.get("editPermissions")

                result["id"] = current.get("id")

                result["isFavourite"] = current.get("isFavourite")

                result["isWritable"] = current.get("isWritable")

                result["name"] = current.get("name")

                result["owner"] = current.get("owner")

                result["popularity"] = current.get("popularity")

                result["rank"] = current.get("rank")

                result["self"] = current.get("self")

                result["sharePermissions"] = current.get("sharePermissions")

                result["systemDashboard"] = current.get("systemDashboard")

                result["view"] = current.get("view")

                pass

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/rest/api/3/dashboard/{id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
