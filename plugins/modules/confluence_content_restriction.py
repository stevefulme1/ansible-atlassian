#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: confluence_content_restriction
short_description: Manage content restrictions
version_added: "1.0.0"
description:
  - Create, update, and delete confluence content restriction resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the confluence content restriction resource.
    type: str
    choices: ['present', 'absent']
    default: present
  results:
    description:
      - >-
    type: list
    required: true
  _links:
    description:
      - >-
    type: dict
  limit:
    description:
      - >-
    type: int
  restrictionsHash:
    description:
      - >-
        This property is used by the UI to figure out whether a set of restrictions has changed.
    type: str
  size:
    description:
      - >-
    type: int
  start:
    description:
      - >-
    type: int
extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""
- name: Create a confluence content restriction
  stevefulme1.atlassian.confluence_content_restriction:
    results: "example_results"
    state: present
  # API: POST /wiki/rest/api/content/{id}/restriction
- name: Update a confluence content restriction
  stevefulme1.atlassian.confluence_content_restriction:
    id: "existing_id"
    _links: "updated__links"
    limit: "updated_limit"
    restrictionsHash: "updated_restrictionsHash"
    size: "updated_size"
    start: "updated_start"
    state: present
  # API:
- name: Delete a confluence content restriction
  stevefulme1.atlassian.confluence_content_restriction:
    id: "existing_id"
    state: absent
  # API: DELETE /wiki/rest/api/content/{id}/restriction
"""

RETURN = r"""
operation:
  description: >-
  returned: success
  type: str
restrictions:
  description: >-
  returned: success
  type: dict
content:
  description: >-
    Base object for all content types.
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
    """Retrieve the current state of the confluence content restriction via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    search_key = "id"
    search_value = identifier

    if search_value is None:
        return None
    try:
        items = client.get("/wiki/rest/api/content/{id}/restriction")
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

    if module.params.get("results") is not None:
        payload["results"] = module.params["results"]

    if module.params.get("_links") is not None:
        payload["_links"] = module.params["_links"]

    if module.params.get("limit") is not None:
        payload["limit"] = module.params["limit"]

    if module.params.get("restrictionsHash") is not None:
        payload["restrictionsHash"] = module.params["restrictionsHash"]

    if module.params.get("size") is not None:
        payload["size"] = module.params["size"]

    if module.params.get("start") is not None:
        payload["start"] = module.params["start"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            results=dict(
                type="list",

                required=True,


            ),

            _links=dict(
                type="dict",


            ),

            limit=dict(
                type="int",


            ),

            restrictionsHash=dict(
                type="str",


            ),

            size=dict(
                type="int",


            ),

            start=dict(
                type="int",


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
                        "/wiki/rest/api/content/{id}/restriction",
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

                result["operation"] = current.get("operation")

                result["restrictions"] = current.get("restrictions")

                result["content"] = current.get("content")

                result["_expandable"] = current.get("_expandable")

                result["_links"] = current.get("_links")

                pass

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/wiki/rest/api/content/{id}/restriction".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
