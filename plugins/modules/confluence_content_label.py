#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: confluence_content_label
short_description: Manage content labels
version_added: "1.0.0"
description:
  - Create, update, and delete confluence content label resources.
  - Supports check mode and diff mode for safe operations.

author:
  - "Steve Fulmer (@stevefulme1)"

options:
  state:
    description:
      - Desired state of the confluence content label resource.
    type: str
    choices: ['present', 'absent']
    default: present

extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""
- name: Create a confluence content label
  stevefulme1.atlassian.confluence_content_label:
    state: present
  # API: POST /wiki/rest/api/content/{id}/label

- name: Update a confluence content label
  stevefulme1.atlassian.confluence_content_label:
    id: "existing_id"
    state: present
  # API:

- name: Delete a confluence content label
  stevefulme1.atlassian.confluence_content_label:
    id: "existing_id"
    state: absent
  # API: DELETE /wiki/rest/api/content/{id}/label/{label}
"""

RETURN = r"""
prefix:
  description: >-
  returned: success
  type: str

name:
  description: >-
  returned: success
  type: str

id:
  description: >-
  returned: success
  type: str

label:
  description: >-
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
    """Retrieve the current state of the confluence content label via GET."""

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

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

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
                        "/wiki/rest/api/content/{id}/label",
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

                result["prefix"] = current.get("prefix")

                result["name"] = current.get("name")

                result["id"] = current.get("id")

                result["label"] = current.get("label")

                pass

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/wiki/rest/api/content/{id}/label/{label}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
