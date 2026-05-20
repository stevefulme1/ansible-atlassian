#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_permission_scheme
short_description: Manage permission schemes
version_added: "1.0.0"
description:
  - Create, update, and delete permission_scheme resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer"
options:
  state:
    description:
      - Desired state of the permission_scheme resource.
    type: str
    choices: ['present', 'absent']
    default: present

  name:
    description:
      - >-
        The name of the permission scheme. Must be unique.
    type: str

    required: true





  description:
    description:
      - >-
        A description for the permission scheme.
    type: str





  expand:
    description:
      - >-
        The expand options available for the permission scheme.
    type: str





  id:
    description:
      - >-
        The ID of the permission scheme.
    type: int





  permissions:
    description:
      - >-
        The permission scheme to create or update. See About permission schemes and...
    type: list





  scope:
    description:
      - >-
        The projects the item is associated with. Indicated for items associated with next-gen projects.
    type: dict





  self:
    description:
      - >-
        The URL of the permission scheme.
    type: str





extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""

- name: Create a permission_scheme
  stevefulme1.atlassian.jira_permission_scheme:


    name: "example_name"














    state: present
  # API: POST /rest/api/3/permissionscheme



- name: Update a permission_scheme
  stevefulme1.atlassian.jira_permission_scheme:
    id: "existing_id"




    description: "updated_description"



    expand: "updated_expand"





    permissions: "updated_permissions"



    scope: "updated_scope"



    self: "updated_self"


    state: present
  # API:  



- name: Delete a permission_scheme
  stevefulme1.atlassian.jira_permission_scheme:
    id: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/permissionscheme/{schemeId}

"""

RETURN = r"""

description:
  description: >-
    A description for the permission scheme.
  returned: success
  type: str


expand:
  description: >-
    The expand options available for the permission scheme.
  returned: success
  type: str


id:
  description: >-
    The ID of the permission scheme.
  returned: success
  type: int


name:
  description: >-
    The name of the permission scheme. Must be unique.
  returned: success
  type: str


permissions:
  description: >-
    The permission scheme to create or update. See About permission schemes and...
  returned: success
  type: list


scope:
  description: >-
    The projects the item is associated with. Indicated for items associated with next-gen projects.
  returned: success
  type: dict


self:
  description: >-
    The URL of the permission scheme.
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
    """Retrieve the current state of the permission_scheme via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/rest/api/3/permissionscheme")
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

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("expand") is not None:
        payload["expand"] = module.params["expand"]

    if module.params.get("id") is not None:
        payload["id"] = module.params["id"]

    if module.params.get("permissions") is not None:
        payload["permissions"] = module.params["permissions"]

    if module.params.get("scope") is not None:
        payload["scope"] = module.params["scope"]

    if module.params.get("self") is not None:
        payload["self"] = module.params["self"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            name=dict(
                type="str",

                required=True,





            ),

            description=dict(
                type="str",





            ),

            expand=dict(
                type="str",





            ),

            id=dict(
                type="int",





            ),

            permissions=dict(
                type="list",





            ),

            scope=dict(
                type="dict",





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
                        "/rest/api/3/permissionscheme",
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

                result["description"] = current.get("description")

                result["expand"] = current.get("expand")

                result["id"] = current.get("id")

                result["name"] = current.get("name")

                result["permissions"] = current.get("permissions")

                result["scope"] = current.get("scope")

                result["self"] = current.get("self")


        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/rest/api/3/permissionscheme/{schemeId}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
