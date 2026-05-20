#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: confluence_attachment
short_description: Manage content - attachments
version_added: "1.0.0"
description:
  - Create, update, and delete attachment resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the attachment resource.
    type: str
    choices: ['present', 'absent']
    default: present

  file:
    description:
      - >-
        The relative location and name of the attachment to be added to the content.
    type: str

    required: true

  id:
    description:
      - >-

    type: str

    required: true

  minorEdit:
    description:
      - >-
        If minorEdits is set to 'true', no notification email or activity stream will be generated when...
    type: str

    required: true

  type:
    description:
      - >-
        Set this to "attachment"
    type: str

    required: true

  version:
    description:
      - >-

    type: dict

    required: true

  comment:
    description:
      - >-
        The comment for the attachment that is being added. If you specify a comment, then every file...
    type: str

  container:
    description:
      - >-
        Container for content. This can be either a space (containing a page or blogpost) or a page/blog...
    type: dict

  extensions:
    description:
      - >-

    type: dict

  metadata:
    description:
      - >-

    type: dict

  status:
    description:
      - >-

    type: str

  title:
    description:
      - >-

    type: str


extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""

- name: Create a attachment
  stevefulme1.atlassian.confluence_attachment:

    file: "example_file"

    id: "example_id"

    minorEdit: "example_minorEdit"

    type: "example_type"

    version: "example_version"

    state: present
  # API: POST /wiki/rest/api/content/{id}/child/attachment


- name: Update a attachment
  stevefulme1.atlassian.confluence_attachment:
    id: "existing_id"

    comment: "updated_comment"

    container: "updated_container"

    extensions: "updated_extensions"

    metadata: "updated_metadata"

    status: "updated_status"

    title: "updated_title"

    state: present
  # API:
"""

RETURN = r"""

id:
  description: >-

  returned: success
  type: str


type:
  description: >-
    Can be "page", "blogpost", "attachment" or "content"
  returned: success
  type: str


status:
  description: >-

  returned: success
  type: str


title:
  description: >-

  returned: success
  type: str


space:
  description: >-

  returned: success
  type: dict


history:
  description: >-

  returned: success
  type: dict


version:
  description: >-

  returned: success
  type: dict


ancestors:
  description: >-

  returned: success
  type: list


operations:
  description: >-

  returned: success
  type: list


children:
  description: >-

  returned: success
  type: dict


childTypes:
  description: >-
    Shows whether a piece of content has attachments, comments, or child pages/whiteboards. Note,...
  returned: success
  type: dict


descendants:
  description: >-

  returned: success
  type: dict


container:
  description: >-
    Container for content. This can be either a space (containing a page or blogpost) or a page/blog...
  returned: success
  type: dict


body:
  description: >-

  returned: success
  type: dict


restrictions:
  description: >-

  returned: success
  type: dict


metadata:
  description: >-
    Metadata object for page, blogpost, comment content
  returned: success
  type: dict


macroRenderedOutput:
  description: >-

  returned: success
  type: dict


extensions:
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
    """Retrieve the current state of the attachment via GET."""

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

    if module.params.get("file") is not None:
        payload["file"] = module.params["file"]

    if module.params.get("id") is not None:
        payload["id"] = module.params["id"]

    if module.params.get("minorEdit") is not None:
        payload["minorEdit"] = module.params["minorEdit"]

    if module.params.get("type") is not None:
        payload["type"] = module.params["type"]

    if module.params.get("version") is not None:
        payload["version"] = module.params["version"]

    if module.params.get("comment") is not None:
        payload["comment"] = module.params["comment"]

    if module.params.get("container") is not None:
        payload["container"] = module.params["container"]

    if module.params.get("extensions") is not None:
        payload["extensions"] = module.params["extensions"]

    if module.params.get("metadata") is not None:
        payload["metadata"] = module.params["metadata"]

    if module.params.get("status") is not None:
        payload["status"] = module.params["status"]

    if module.params.get("title") is not None:
        payload["title"] = module.params["title"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            file=dict(
                type="str",

                required=True,

            ),

            id=dict(
                type="str",

                required=True,

            ),

            minorEdit=dict(
                type="str",

                required=True,

            ),

            type=dict(
                type="str",

                required=True,

            ),

            version=dict(
                type="dict",

                required=True,

            ),

            comment=dict(
                type="str",

            ),

            container=dict(
                type="dict",

            ),

            extensions=dict(
                type="dict",

            ),

            metadata=dict(
                type="dict",

            ),

            status=dict(
                type="str",

            ),

            title=dict(
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
                        "/wiki/rest/api/content/{id}/child/attachment",
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

                result["type"] = current.get("type")

                result["status"] = current.get("status")

                result["title"] = current.get("title")

                result["space"] = current.get("space")

                result["history"] = current.get("history")

                result["version"] = current.get("version")

                result["ancestors"] = current.get("ancestors")

                result["operations"] = current.get("operations")

                result["children"] = current.get("children")

                result["childTypes"] = current.get("childTypes")

                result["descendants"] = current.get("descendants")

                result["container"] = current.get("container")

                result["body"] = current.get("body")

                result["restrictions"] = current.get("restrictions")

                result["metadata"] = current.get("metadata")

                result["macroRenderedOutput"] = current.get("macroRenderedOutput")

                result["extensions"] = current.get("extensions")

                result["_expandable"] = current.get("_expandable")

                result["_links"] = current.get("_links")

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
