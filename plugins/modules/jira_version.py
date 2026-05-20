#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_version
short_description: Manage project versions
version_added: "1.0.0"
description:
  - Create, update, and delete version resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer"
options:
  state:
    description:
      - Desired state of the version resource.
    type: str
    choices: ['present', 'absent']
    default: present

  approvers:
    description:
      - >-
        If the expand option approvers is used, returns a list containing the approvers for this version.
    type: list

  archived:
    description:
      - >-
        Indicates that the version is archived. Optional when creating or updating a version.
    type: bool

  description:
    description:
      - >-
        The description of the version. Optional when creating or updating a version. The maximum size...
    type: str

  driver:
    description:
      - >-
        The Atlassian account ID of the version driver. Optional when creating or updating a version. If...
    type: str

  expand:
    description:
      - >-
        Use expand(em>expansion) to include additional information about version in the response. This...
    type: str

  id:
    description:
      - >-
        The ID of the version.
    type: str

  issuesStatusForFixVersion:
    description:
      - >-
        Counts of the number of issues in various statuses.
    type: dict

  moveUnfixedIssuesTo:
    description:
      - >-
        The URL of the self link to the version to which all unfixed issues are moved when a version is...
    type: str

  name:
    description:
      - >-
        The unique name of the version. Required when creating a version. Optional when updating a...
    type: str

  operations:
    description:
      - >-
        If the expand option operations is used, returns the list of operations available for this version.
    type: list

  overdue:
    description:
      - >-
        Indicates that the version is overdue.
    type: bool

  project:
    description:
      - >-
        Deprecated. Use projectId.
    type: str

  projectId:
    description:
      - >-
        The ID of the project to which this version is attached. Required when creating a version. Not...
    type: int

  releaseDate:
    description:
      - >-
        The release date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). Optional when...
    type: str

  released:
    description:
      - >-
        Indicates that the version is released. If the version is released a request to release again is...
    type: bool

  self:
    description:
      - >-
        The URL of the version.
    type: str

  startDate:
    description:
      - >-
        The start date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). Optional when creating...
    type: str

  userReleaseDate:
    description:
      - >-
        The date on which work on this version is expected to finish, expressed in the instance's...
    type: str

  userStartDate:
    description:
      - >-
        The date on which work on this version is expected to start, expressed in the instance's...
    type: str

extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""

- name: Create a version
  stevefulme1.atlassian.jira_version:

    state: present
  # API: POST /rest/api/3/version

- name: Update a version
  stevefulme1.atlassian.jira_version:
    id: "existing_id"

    approvers: "updated_approvers"

    archived: "updated_archived"

    description: "updated_description"

    driver: "updated_driver"

    expand: "updated_expand"

    issuesStatusForFixVersion: "updated_issuesStatusForFixVersion"

    moveUnfixedIssuesTo: "updated_moveUnfixedIssuesTo"

    name: "updated_name"

    operations: "updated_operations"

    overdue: "updated_overdue"

    project: "updated_project"

    projectId: "updated_projectId"

    releaseDate: "updated_releaseDate"

    released: "updated_released"

    self: "updated_self"

    startDate: "updated_startDate"

    userReleaseDate: "updated_userReleaseDate"

    userStartDate: "updated_userStartDate"

    state: present
  # API:

- name: Delete a version
  stevefulme1.atlassian.jira_version:
    id: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/version/{id}
"""

RETURN = r"""

approvers:
  description: >-
    If the expand option approvers is used, returns a list containing the approvers for this version.
  returned: success
  type: list

archived:
  description: >-
    Indicates that the version is archived. Optional when creating or updating a version.
  returned: success
  type: bool

description:
  description: >-
    The description of the version. Optional when creating or updating a version. The maximum size...
  returned: success
  type: str

driver:
  description: >-
    The Atlassian account ID of the version driver. Optional when creating or updating a version. If...
  returned: success
  type: str

expand:
  description: >-
    Use expand(em>expansion) to include additional information about version in the response. This...
  returned: success
  type: str

id:
  description: >-
    The ID of the version.
  returned: success
  type: str

issuesStatusForFixVersion:
  description: >-
    Counts of the number of issues in various statuses.
  returned: success
  type: dict

moveUnfixedIssuesTo:
  description: >-
    The URL of the self link to the version to which all unfixed issues are moved when a version is...
  returned: success
  type: str

name:
  description: >-
    The unique name of the version. Required when creating a version. Optional when updating a...
  returned: success
  type: str

operations:
  description: >-
    If the expand option operations is used, returns the list of operations available for this version.
  returned: success
  type: list

overdue:
  description: >-
    Indicates that the version is overdue.
  returned: success
  type: bool

project:
  description: >-
    Deprecated. Use projectId.
  returned: success
  type: str

projectId:
  description: >-
    The ID of the project to which this version is attached. Required when creating a version. Not...
  returned: success
  type: int

releaseDate:
  description: >-
    The release date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). Optional when...
  returned: success
  type: str

released:
  description: >-
    Indicates that the version is released. If the version is released a request to release again is...
  returned: success
  type: bool

self:
  description: >-
    The URL of the version.
  returned: success
  type: str

startDate:
  description: >-
    The start date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). Optional when creating...
  returned: success
  type: str

userReleaseDate:
  description: >-
    The date on which work on this version is expected to finish, expressed in the instance's...
  returned: success
  type: str

userStartDate:
  description: >-
    The date on which work on this version is expected to start, expressed in the instance's...
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
    """Retrieve the current state of the version via GET."""

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

    if module.params.get("approvers") is not None:
        payload["approvers"] = module.params["approvers"]

    if module.params.get("archived") is not None:
        payload["archived"] = module.params["archived"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("driver") is not None:
        payload["driver"] = module.params["driver"]

    if module.params.get("expand") is not None:
        payload["expand"] = module.params["expand"]

    if module.params.get("id") is not None:
        payload["id"] = module.params["id"]

    if module.params.get("issuesStatusForFixVersion") is not None:
        payload["issuesStatusForFixVersion"] = module.params["issuesStatusForFixVersion"]

    if module.params.get("moveUnfixedIssuesTo") is not None:
        payload["moveUnfixedIssuesTo"] = module.params["moveUnfixedIssuesTo"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("operations") is not None:
        payload["operations"] = module.params["operations"]

    if module.params.get("overdue") is not None:
        payload["overdue"] = module.params["overdue"]

    if module.params.get("project") is not None:
        payload["project"] = module.params["project"]

    if module.params.get("projectId") is not None:
        payload["projectId"] = module.params["projectId"]

    if module.params.get("releaseDate") is not None:
        payload["releaseDate"] = module.params["releaseDate"]

    if module.params.get("released") is not None:
        payload["released"] = module.params["released"]

    if module.params.get("self") is not None:
        payload["self"] = module.params["self"]

    if module.params.get("startDate") is not None:
        payload["startDate"] = module.params["startDate"]

    if module.params.get("userReleaseDate") is not None:
        payload["userReleaseDate"] = module.params["userReleaseDate"]

    if module.params.get("userStartDate") is not None:
        payload["userStartDate"] = module.params["userStartDate"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            approvers=dict(
                type="list",





            ),

            archived=dict(
                type="bool",





            ),

            description=dict(
                type="str",





            ),

            driver=dict(
                type="str",





            ),

            expand=dict(
                type="str",





            ),

            id=dict(
                type="str",





            ),

            issuesStatusForFixVersion=dict(
                type="dict",





            ),

            moveUnfixedIssuesTo=dict(
                type="str",





            ),

            name=dict(
                type="str",





            ),

            operations=dict(
                type="list",





            ),

            overdue=dict(
                type="bool",





            ),

            project=dict(
                type="str",





            ),

            projectId=dict(
                type="int",





            ),

            releaseDate=dict(
                type="str",





            ),

            released=dict(
                type="bool",





            ),

            self=dict(
                type="str",





            ),

            startDate=dict(
                type="str",





            ),

            userReleaseDate=dict(
                type="str",





            ),

            userStartDate=dict(
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
                        "/rest/api/3/version",
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

                result["approvers"] = current.get("approvers")

                result["archived"] = current.get("archived")

                result["description"] = current.get("description")

                result["driver"] = current.get("driver")

                result["expand"] = current.get("expand")

                result["id"] = current.get("id")

                result["issuesStatusForFixVersion"] = current.get("issuesStatusForFixVersion")

                result["moveUnfixedIssuesTo"] = current.get("moveUnfixedIssuesTo")

                result["name"] = current.get("name")

                result["operations"] = current.get("operations")

                result["overdue"] = current.get("overdue")

                result["project"] = current.get("project")

                result["projectId"] = current.get("projectId")

                result["releaseDate"] = current.get("releaseDate")

                result["released"] = current.get("released")

                result["self"] = current.get("self")

                result["startDate"] = current.get("startDate")

                result["userReleaseDate"] = current.get("userReleaseDate")

                result["userStartDate"] = current.get("userStartDate")


        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/rest/api/3/version/{id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
