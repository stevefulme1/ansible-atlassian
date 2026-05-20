#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_filter
short_description: Manage filters
version_added: "1.0.0"
description:
  - Create, update, and delete filter resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer"
options:
  state:
    description:
      - Desired state of the filter resource.
    type: str
    choices: ['present', 'absent']
    default: present

  name:
    description:
      - >-
        The name of the filter. Must be unique.
    type: str

    required: true

  approximateLastUsed:
    description:
      - >-
        \Experimental\ Approximate last used time. Returns the date and time when the filter was last...
    type: str

  description:
    description:
      - >-
        A description of the filter.
    type: str

  editPermissions:
    description:
      - >-
        The groups and projects that can edit the filter.
    type: list

  favourite:
    description:
      - >-
        Whether the filter is selected as a favorite.
    type: bool

  favouritedCount:
    description:
      - >-
        The count of how many users have selected this filter as a favorite, including the filter owner.
    type: int

  id:
    description:
      - >-
        The unique identifier for the filter.
    type: str

  jql:
    description:
      - >-
        The JQL query for the filter. For example, project = SSP AND issuetype = Bug.
    type: str

  owner:
    description:
      - >-
        A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
    type: dict

  searchUrl:
    description:
      - >-
        A URL to view the filter results in Jira, using the Search for issues using...
    type: str

  self:
    description:
      - >-
        The URL of the filter.
    type: str

  sharePermissions:
    description:
      - >-
        The groups and projects that the filter is shared with.
    type: list

  sharedUsers:
    description:
      - >-
        A paginated list of users sharing the filter. This includes users that are members of the groups...
    type: dict

  subscriptions:
    description:
      - >-
        A paginated list of subscriptions to a filter.
    type: dict

  viewUrl:
    description:
      - >-
        A URL to view the filter results in Jira, using the ID of the filter. For example,...
    type: str

extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""

- name: Create a filter
  stevefulme1.atlassian.jira_filter:

    name: "example_name"

    state: present
  # API: POST /rest/api/3/filter

- name: Update a filter
  stevefulme1.atlassian.jira_filter:
    id: "existing_id"

    approximateLastUsed: "updated_approximateLastUsed"

    description: "updated_description"

    editPermissions: "updated_editPermissions"

    favourite: "updated_favourite"

    favouritedCount: "updated_favouritedCount"

    jql: "updated_jql"

    owner: "updated_owner"

    searchUrl: "updated_searchUrl"

    self: "updated_self"

    sharePermissions: "updated_sharePermissions"

    sharedUsers: "updated_sharedUsers"

    subscriptions: "updated_subscriptions"

    viewUrl: "updated_viewUrl"

    state: present
  # API:

- name: Delete a filter
  stevefulme1.atlassian.jira_filter:
    id: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/filter/{id}
"""

RETURN = r"""

approximateLastUsed:
  description: >-
    \Experimental\ Approximate last used time. Returns the date and time when the filter was last...
  returned: success
  type: str

description:
  description: >-
    A description of the filter.
  returned: success
  type: str

editPermissions:
  description: >-
    The groups and projects that can edit the filter.
  returned: success
  type: list

favourite:
  description: >-
    Whether the filter is selected as a favorite.
  returned: success
  type: bool

favouritedCount:
  description: >-
    The count of how many users have selected this filter as a favorite, including the filter owner.
  returned: success
  type: int

id:
  description: >-
    The unique identifier for the filter.
  returned: success
  type: str

jql:
  description: >-
    The JQL query for the filter. For example, project = SSP AND issuetype = Bug.
  returned: success
  type: str

name:
  description: >-
    The name of the filter. Must be unique.
  returned: success
  type: str

owner:
  description: >-
    A user with details as permitted by the user's Atlassian Account privacy settings. However, be...
  returned: success
  type: dict

searchUrl:
  description: >-
    A URL to view the filter results in Jira, using the Search for issues using...
  returned: success
  type: str

self:
  description: >-
    The URL of the filter.
  returned: success
  type: str

sharePermissions:
  description: >-
    The groups and projects that the filter is shared with.
  returned: success
  type: list

sharedUsers:
  description: >-
    A paginated list of users sharing the filter. This includes users that are members of the groups...
  returned: success
  type: dict

subscriptions:
  description: >-
    A paginated list of subscriptions to a filter.
  returned: success
  type: dict

viewUrl:
  description: >-
    A URL to view the filter results in Jira, using the ID of the filter. For example,...
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
    """Retrieve the current state of the filter via GET."""

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

    if module.params.get("approximateLastUsed") is not None:
        payload["approximateLastUsed"] = module.params["approximateLastUsed"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("editPermissions") is not None:
        payload["editPermissions"] = module.params["editPermissions"]

    if module.params.get("favourite") is not None:
        payload["favourite"] = module.params["favourite"]

    if module.params.get("favouritedCount") is not None:
        payload["favouritedCount"] = module.params["favouritedCount"]

    if module.params.get("id") is not None:
        payload["id"] = module.params["id"]

    if module.params.get("jql") is not None:
        payload["jql"] = module.params["jql"]

    if module.params.get("owner") is not None:
        payload["owner"] = module.params["owner"]

    if module.params.get("searchUrl") is not None:
        payload["searchUrl"] = module.params["searchUrl"]

    if module.params.get("self") is not None:
        payload["self"] = module.params["self"]

    if module.params.get("sharePermissions") is not None:
        payload["sharePermissions"] = module.params["sharePermissions"]

    if module.params.get("sharedUsers") is not None:
        payload["sharedUsers"] = module.params["sharedUsers"]

    if module.params.get("subscriptions") is not None:
        payload["subscriptions"] = module.params["subscriptions"]

    if module.params.get("viewUrl") is not None:
        payload["viewUrl"] = module.params["viewUrl"]

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

            approximateLastUsed=dict(
                type="str",





            ),

            description=dict(
                type="str",





            ),

            editPermissions=dict(
                type="list",





            ),

            favourite=dict(
                type="bool",





            ),

            favouritedCount=dict(
                type="int",





            ),

            id=dict(
                type="str",





            ),

            jql=dict(
                type="str",





            ),

            owner=dict(
                type="dict",





            ),

            searchUrl=dict(
                type="str",





            ),

            self=dict(
                type="str",





            ),

            sharePermissions=dict(
                type="list",





            ),

            sharedUsers=dict(
                type="dict",





            ),

            subscriptions=dict(
                type="dict",





            ),

            viewUrl=dict(
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
                        "/rest/api/3/filter",
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

                result["approximateLastUsed"] = current.get("approximateLastUsed")

                result["description"] = current.get("description")

                result["editPermissions"] = current.get("editPermissions")

                result["favourite"] = current.get("favourite")

                result["favouritedCount"] = current.get("favouritedCount")

                result["id"] = current.get("id")

                result["jql"] = current.get("jql")

                result["name"] = current.get("name")

                result["owner"] = current.get("owner")

                result["searchUrl"] = current.get("searchUrl")

                result["self"] = current.get("self")

                result["sharePermissions"] = current.get("sharePermissions")

                result["sharedUsers"] = current.get("sharedUsers")

                result["subscriptions"] = current.get("subscriptions")

                result["viewUrl"] = current.get("viewUrl")


        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/rest/api/3/filter/{id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
