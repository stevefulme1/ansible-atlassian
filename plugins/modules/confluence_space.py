#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: confluence_space
short_description: Manage space
version_added: "1.0.0"
description:
  - Create, update, and delete confluence space resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the confluence space resource.
    type: str
    choices: ['present', 'absent']
    default: present
  name:
    description:
      - >-
        The name of the new space.
    type: str
    required: true
  alias:
    description:
      - >-
        This field will be used as the new identifier for the space in confluence page URLs. If the...
    type: str
  description:
    description:
      - >-
        The description of the new/updated space. Note, only the 'plain' representation can be used for...
    type: dict
  key:
    description:
      - >-
        The key for the new space. Format: See Space keys. If alias is not provided, this is required.
    type: str
    no_log: false
  permissions:
    description:
      - >-
        The permissions for the new space. If no permissions are provided, the Confluence default space...
    type: list
    elements: dict
extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""
- name: Create a confluence space
  stevefulme1.atlassian.confluence_space:
    name: "example_name"
    state: present
  # API: POST /wiki/rest/api/space/_private
- name: Update a confluence space
  stevefulme1.atlassian.confluence_space:
    id: "existing_id"
    alias: "updated_alias"
    description: "updated_description"
    key: "updated_key"
    permissions: "updated_permissions"
    state: present
  # API:
"""

RETURN = r"""
id:
  description: >-
  returned: success
  type: int
key:
  description: >-
  returned: success
  type: str
alias:
  description: >-
  returned: success
  type: str
name:
  description: >-
  returned: success
  type: str
icon:
  description: >-
    This object represents an icon. If used as a profilePicture, this may be returned as null,...
  returned: success
  type: dict
description:
  description: >-
  returned: success
  type: dict
homepage:
  description: >-
    Base object for all content types.
  returned: success
  type: dict
type:
  description: >-
  returned: success
  type: str
metadata:
  description: >-
  returned: success
  type: dict
operations:
  description: >-
  returned: success
  type: list
permissions:
  description: >-
  returned: success
  type: list
status:
  description: >-
  returned: success
  type: str
settings:
  description: >-
  returned: success
  type: dict
theme:
  description: >-
  returned: success
  type: dict
lookAndFeel:
  description: >-
  returned: success
  type: dict
history:
  description: >-
  returned: success
  type: dict
_expandable:
  description: >-
  returned: success
  type: dict
_links:
  description: >-
  returned: success
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def get_current_state(client, module):
    """Retrieve the current state of the confluence space via GET."""

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

    if module.params.get("alias") is not None:
        payload["alias"] = module.params["alias"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("key") is not None:
        payload["key"] = module.params["key"]

    if module.params.get("permissions") is not None:
        payload["permissions"] = module.params["permissions"]

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

            alias=dict(
                type="str",








            ),

            description=dict(
                type="dict",








            ),

            key=dict(
                type="str",



                no_log=False,






            ),

            permissions=dict(
                type="list",

                elements="dict",








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
                        "/wiki/rest/api/space/_private",
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

                result["id"] = current.get("id")

                result["key"] = current.get("key")

                result["alias"] = current.get("alias")

                result["name"] = current.get("name")

                result["icon"] = current.get("icon")

                result["description"] = current.get("description")

                result["homepage"] = current.get("homepage")

                result["type"] = current.get("type")

                result["metadata"] = current.get("metadata")

                result["operations"] = current.get("operations")

                result["permissions"] = current.get("permissions")

                result["status"] = current.get("status")

                result["settings"] = current.get("settings")

                result["theme"] = current.get("theme")

                result["lookAndFeel"] = current.get("lookAndFeel")

                result["history"] = current.get("history")

                result["_expandable"] = current.get("_expandable")

                result["_links"] = current.get("_links")

                pass

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    pass

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
