#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_priority
short_description: Manage issue priorities
version_added: "1.0.0"
description:
  - Create, update, and delete priority resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the priority resource.
    type: str
    choices: ['present', 'absent']
    default: present

  avatarId:
    description:
      - >-
        The ID for the avatar for the priority. This parameter is nullable and both iconUrl and avatarId...
    type: int

  description:
    description:
      - >-
        The description of the priority.
    type: str

  iconUrl:
    description:
      - >-
        The URL of an icon for the priority. Accepted protocols are HTTP and HTTPS. Built in icons can...
    type: str
    choices:
      - /images/icons/priorities/blocker.png
      - /images/icons/priorities/critical.png
      - /images/icons/priorities/high.png
      - /images/icons/priorities/highest.png
      - /images/icons/priorities/low.png
      - /images/icons/priorities/lowest.png
      - /images/icons/priorities/major.png
      - /images/icons/priorities/medium.png
      - /images/icons/priorities/minor.png
      - /images/icons/priorities/trivial.png
      - /images/icons/priorities/blocker_new.png
      - /images/icons/priorities/critical_new.png
      - /images/icons/priorities/high_new.png
      - /images/icons/priorities/highest_new.png
      - /images/icons/priorities/low_new.png
      - /images/icons/priorities/lowest_new.png
      - /images/icons/priorities/major_new.png
      - /images/icons/priorities/medium_new.png
      - /images/icons/priorities/minor_new.png
      - /images/icons/priorities/trivial_new.png

  name:
    description:
      - >-
        The name of the priority. Must be unique.
    type: str

  statusColor:
    description:
      - >-
        The status color of the priority in 3-digit or 6-digit hexadecimal format.
    type: str


extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""

- name: Create a priority
  stevefulme1.atlassian.jira_priority:

    state: present
  # API: POST /rest/api/3/priority


- name: Update a priority
  stevefulme1.atlassian.jira_priority:
    id: "existing_id"

    avatarId: "updated_avatarId"

    description: "updated_description"

    iconUrl: "updated_iconUrl"

    name: "updated_name"

    statusColor: "updated_statusColor"

    state: present
  # API:


- name: Delete a priority
  stevefulme1.atlassian.jira_priority:
    id: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/priority/{id}
"""

RETURN = r"""

avatarId:
  description: >-
    The avatarId of the avatar for the issue priority. This parameter is nullable and when set, this...
  returned: success
  type: int


description:
  description: >-
    The description of the issue priority.
  returned: success
  type: str


iconUrl:
  description: >-
    The URL of the icon for the issue priority.
  returned: success
  type: str


id:
  description: >-
    The ID of the issue priority.
  returned: success
  type: str


isDefault:
  description: >-
    Whether this priority is the default.
  returned: success
  type: bool


name:
  description: >-
    The name of the issue priority.
  returned: success
  type: str


schemes:
  description: >-

  returned: success
  type: dict


self:
  description: >-
    The URL of the issue priority.
  returned: success
  type: str


statusColor:
  description: >-
    The color used to indicate the issue priority.
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
    """Retrieve the current state of the priority via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/rest/api/3/priority")
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

    if module.params.get("iconUrl") is not None:
        payload["iconUrl"] = module.params["iconUrl"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("statusColor") is not None:
        payload["statusColor"] = module.params["statusColor"]

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

            iconUrl=dict(
                type="str",
                choices=[
                    '/images/icons/priorities/blocker.png',
                    '/images/icons/priorities/critical.png',
                    '/images/icons/priorities/high.png',
                    '/images/icons/priorities/highest.png',
                    '/images/icons/priorities/low.png',
                    '/images/icons/priorities/lowest.png',
                    '/images/icons/priorities/major.png',
                    '/images/icons/priorities/medium.png',
                    '/images/icons/priorities/minor.png',
                    '/images/icons/priorities/trivial.png',
                    '/images/icons/priorities/blocker_new.png',
                    '/images/icons/priorities/critical_new.png',
                    '/images/icons/priorities/high_new.png',
                    '/images/icons/priorities/highest_new.png',
                    '/images/icons/priorities/low_new.png',
                    '/images/icons/priorities/lowest_new.png',
                    '/images/icons/priorities/major_new.png',
                    '/images/icons/priorities/medium_new.png',
                    '/images/icons/priorities/minor_new.png',
                    '/images/icons/priorities/trivial_new.png',
                ],
            ),

            name=dict(
                type="str",

            ),

            statusColor=dict(
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
                        "/rest/api/3/priority",
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

                result["iconUrl"] = current.get("iconUrl")

                result["id"] = current.get("id")

                result["isDefault"] = current.get("isDefault")

                result["name"] = current.get("name")

                result["schemes"] = current.get("schemes")

                result["self"] = current.get("self")

                result["statusColor"] = current.get("statusColor")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/rest/api/3/priority/{id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
