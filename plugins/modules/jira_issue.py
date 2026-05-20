#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_issue
short_description: Manage issues
version_added: "1.0.0"
description:
  - Create, update, and delete jira issue resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the jira issue resource.
    type: str
    choices: ['present', 'absent']
    default: present

  fields:
    description:
      - >-
        List of issue screen fields to update, specifying the sub-field to update and its value for each...
    type: dict


  historyMetadata:
    description:
      - >-
        Details of issue history metadata.
    type: dict


  properties:
    description:
      - >-
        Details of issue properties to be add or update.
    type: list


  transition:
    description:
      - >-
        Details of an issue transition.
    type: dict


  update:
    description:
      - >-
        A Map containing the field field name and a list of operations to perform on the issue screen...
    type: dict


extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""

- name: Create a jira issue
  stevefulme1.atlassian.jira_issue:


    state: present
  # API: POST /rest/api/3/issue


- name: Update a jira issue
  stevefulme1.atlassian.jira_issue:
    id: "existing_id"


    fields: "updated_fields"


    historyMetadata: "updated_historyMetadata"


    properties: "updated_properties"


    transition: "updated_transition"


    update: "updated_update"


    state: present
  # API:


- name: Delete a jira issue
  stevefulme1.atlassian.jira_issue:
    id: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/issue/{issueIdOrKey}

"""

RETURN = r"""

changelog:
  description: >-
    A page of changelogs.
  returned: success
  type: dict


editmeta:
  description: >-
    A list of editable field details.
  returned: success
  type: dict


expand:
  description: >-
    Expand options that include additional issue details in the response.
  returned: success
  type: str


fields:
  description: >-

  returned: success
  type: dict


fieldsToInclude:
  description: >-

  returned: success
  type: dict


id:
  description: >-
    The ID of the issue.
  returned: success
  type: str


key:
  description: >-
    The key of the issue.
  returned: success
  type: str


names:
  description: >-
    The ID and name of each field present on the issue.
  returned: success
  type: dict


operations:
  description: >-
    Details of the operations that can be performed on the issue.
  returned: success
  type: dict


properties:
  description: >-
    Details of the issue properties identified in the request.
  returned: success
  type: dict


renderedFields:
  description: >-
    The rendered value of each field present on the issue.
  returned: success
  type: dict


schema:
  description: >-
    The schema describing each field present on the issue.
  returned: success
  type: dict


self:
  description: >-
    The URL of the issue details.
  returned: success
  type: str


transitions:
  description: >-
    The transitions that can be performed on the issue.
  returned: success
  type: list


versionedRepresentations:
  description: >-
    The versions of each field on the issue.
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
    """Retrieve the current state of the jira issue via GET."""

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

    if module.params.get("fields") is not None:
        payload["fields"] = module.params["fields"]

    if module.params.get("historyMetadata") is not None:
        payload["historyMetadata"] = module.params["historyMetadata"]

    if module.params.get("properties") is not None:
        payload["properties"] = module.params["properties"]

    if module.params.get("transition") is not None:
        payload["transition"] = module.params["transition"]

    if module.params.get("update") is not None:
        payload["update"] = module.params["update"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            fields=dict(
                type="dict",


            ),

            historyMetadata=dict(
                type="dict",


            ),

            properties=dict(
                type="list",


            ),

            transition=dict(
                type="dict",


            ),

            update=dict(
                type="dict",


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
                        "/rest/api/3/issue",
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

                result["changelog"] = current.get("changelog")

                result["editmeta"] = current.get("editmeta")

                result["expand"] = current.get("expand")

                result["fields"] = current.get("fields")

                result["fieldsToInclude"] = current.get("fieldsToInclude")

                result["id"] = current.get("id")

                result["key"] = current.get("key")

                result["names"] = current.get("names")

                result["operations"] = current.get("operations")

                result["properties"] = current.get("properties")

                result["renderedFields"] = current.get("renderedFields")

                result["schema"] = current.get("schema")

                result["self"] = current.get("self")

                result["transitions"] = current.get("transitions")

                result["versionedRepresentations"] = current.get("versionedRepresentations")

                pass

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/rest/api/3/issue/{issueIdOrKey}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
