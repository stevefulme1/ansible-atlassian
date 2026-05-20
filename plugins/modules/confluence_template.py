#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: confluence_template
short_description: Manage template
version_added: "1.0.0"
description:
  - Create, update, and delete template resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the template resource.
    type: str
    choices: ['present', 'absent']
    default: present

  body:
    description:
      - >-
        The body of the new content. Does not apply to attachments. Only one body format should be...
    type: dict

    required: true

  name:
    description:
      - >-
        The name of the template. Set to the current name if this field is not being updated.
    type: str

    required: true

  templateId:
    description:
      - >-
        The ID of the template being updated.
    type: str

    required: true

  templateType:
    description:
      - >-
        The type of the template. Set to page.
    type: str

    required: true

    choices: ["page"]

  description:
    description:
      - >-
        A description of the template.
    type: str

  labels:
    description:
      - >-
        Labels for the template.
    type: list

  space:
    description:
      - >-
        The key for the space of the template. Required if the template is a space template. Set this to...
    type: dict

extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""

- name: Create a template
  stevefulme1.atlassian.confluence_template:

    body: "example_body"

    name: "example_name"

    templateId: "example_templateId"

    templateType: "example_templateType"

    state: present
  # API: POST /wiki/rest/api/template

- name: Update a template
  stevefulme1.atlassian.confluence_template:
    id: "existing_id"

    description: "updated_description"

    labels: "updated_labels"

    space: "updated_space"

    state: present
  # API:

- name: Delete a template
  stevefulme1.atlassian.confluence_template:
    id: "existing_id"
    state: absent
  # API: DELETE /wiki/rest/api/template/{contentTemplateId}
"""

RETURN = r"""

templateId:
  description: >-

  returned: success
  type: str

originalTemplate:
  description: >-

  returned: success
  type: dict

referencingBlueprint:
  description: >-

  returned: success
  type: str

name:
  description: >-

  returned: success
  type: str

description:
  description: >-

  returned: success
  type: str

space:
  description: >-

  returned: success
  type: dict

labels:
  description: >-

  returned: success
  type: list

templateType:
  description: >-

  returned: success
  type: str

editorVersion:
  description: >-

  returned: success
  type: str

body:
  description: >-
    The body of the new content. Does not apply to attachments. Only one body format should be...
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
    """Retrieve the current state of the template via GET."""

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

    if module.params.get("body") is not None:
        payload["body"] = module.params["body"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("templateId") is not None:
        payload["templateId"] = module.params["templateId"]

    if module.params.get("templateType") is not None:
        payload["templateType"] = module.params["templateType"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("labels") is not None:
        payload["labels"] = module.params["labels"]

    if module.params.get("space") is not None:
        payload["space"] = module.params["space"]

    return payload

def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            body=dict(
                type="dict",

                required=True,

            ),

            name=dict(
                type="str",

                required=True,

            ),

            templateId=dict(
                type="str",

                required=True,

            ),

            templateType=dict(
                type="str",

                required=True,

                choices=['page'],

            ),

            description=dict(
                type="str",

            ),

            labels=dict(
                type="list",

            ),

            space=dict(
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
                        "/wiki/rest/api/template",
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

                result["templateId"] = current.get("templateId")

                result["originalTemplate"] = current.get("originalTemplate")

                result["referencingBlueprint"] = current.get("referencingBlueprint")

                result["name"] = current.get("name")

                result["description"] = current.get("description")

                result["space"] = current.get("space")

                result["labels"] = current.get("labels")

                result["templateType"] = current.get("templateType")

                result["editorVersion"] = current.get("editorVersion")

                result["body"] = current.get("body")

                result["_expandable"] = current.get("_expandable")

                result["_links"] = current.get("_links")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/wiki/rest/api/template/{contentTemplateId}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)

if __name__ == "__main__":
    main()
