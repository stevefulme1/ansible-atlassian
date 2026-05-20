#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_user
short_description: Manage users
version_added: "1.0.0"
description:
  - Create, update, and delete user resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer (@stevefulme1)"
options:
  state:
    description:
      - Desired state of the user resource.
    type: str
    choices: ['present', 'absent']
    default: present

  emailAddress:
    description:
      - >-
        The email address for the user.
    type: str

    required: true

  products:
    description:
      - >-
        Products the new user has access to. Valid products are: jira-core, jira-servicedesk,...
    type: list
    elements: str

    required: true

  applicationKeys:
    description:
      - >-
        Deprecated, do not use.
    type: list
    elements: str

  displayName:
    description:
      - >-
        This property is no longer available. If the user has an Atlassian account, their display name...
    type: str

  key:
    description:
      - >-
        This property is no longer available. See the migration guide for details.
    type: str

  name:
    description:
      - >-
        This property is no longer available. See the migration guide for details.
    type: str

  password:
    description:
      - >-
        This property is no longer available. If the user has an Atlassian account, their password is...
    type: str

  self:
    description:
      - >-
        The URL of the user.
    type: str


extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""

- name: Create a user
  stevefulme1.atlassian.jira_user:

    emailAddress: "example_emailAddress"

    products: "example_products"

    state: present
  # API: POST /rest/api/3/user


- name: Update a user
  stevefulme1.atlassian.jira_user:
    key: "existing_id"

    applicationKeys: "updated_applicationKeys"

    displayName: "updated_displayName"

    name: "updated_name"

    password: "updated_password"

    self: "updated_self"

    state: present
  # API:


- name: Delete a user
  stevefulme1.atlassian.jira_user:
    key: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/user
"""

RETURN = r"""

accountId:
  description: >-
    The account ID of the user, which uniquely identifies the user across all Atlassian products....
  returned: success
  type: str


accountType:
  description: >-
    The user account type. Can take the following values: atlassian regular Atlassian user account...
  returned: success
  type: str


active:
  description: >-
    Whether the user is active.
  returned: success
  type: bool


appType:
  description: >-
    The app type of the user account when accountType is 'app'. Can take the following values:...
  returned: success
  type: str


applicationRoles:
  description: >-

  returned: success
  type: dict


avatarUrls:
  description: >-

  returned: success
  type: dict


displayName:
  description: >-
    The display name of the user. Depending on the user's privacy setting, this may return an...
  returned: success
  type: str


emailAddress:
  description: >-
    The email address of the user. Depending on the user's privacy setting, this may be returned as null.
  returned: success
  type: str


expand:
  description: >-
    Expand options that include additional user details in the response.
  returned: success
  type: str


groups:
  description: >-

  returned: success
  type: dict


guest:
  description: >-
    Whether the user is a guest.
  returned: success
  type: bool


key:
  description: >-
    This property is no longer available and will be removed from the documentation soon. See the...
  returned: success
  type: str


locale:
  description: >-
    The locale of the user. Depending on the user's privacy setting, this may be returned as null.
  returned: success
  type: str


name:
  description: >-
    This property is no longer available and will be removed from the documentation soon. See the...
  returned: success
  type: str


self:
  description: >-
    The URL of the user.
  returned: success
  type: str


timeZone:
  description: >-
    The time zone specified in the user's profile. If the user's time zone is not visible to the...
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
    """Retrieve the current state of the user via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("key")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/rest/api/3/users")
        if isinstance(items, dict):
            items = items.get("results", items.get("data", items.get("items", [])))
        for item in items:
            if str(item.get(search_key)) == str(search_value):
                return item
            if str(item.get("key")) == str(search_value):
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

    if module.params.get("emailAddress") is not None:
        payload["emailAddress"] = module.params["emailAddress"]

    if module.params.get("products") is not None:
        payload["products"] = module.params["products"]

    if module.params.get("applicationKeys") is not None:
        payload["applicationKeys"] = module.params["applicationKeys"]

    if module.params.get("displayName") is not None:
        payload["displayName"] = module.params["displayName"]

    if module.params.get("key") is not None:
        payload["key"] = module.params["key"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("password") is not None:
        payload["password"] = module.params["password"]

    if module.params.get("self") is not None:
        payload["self"] = module.params["self"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            emailAddress=dict(
                type="str",

                required=True,

            ),

            products=dict(
                type="list", elements="str",

                required=True,

            ),

            applicationKeys=dict(
                type="list", elements="str", no_log=False,
            ),

            displayName=dict(
                type="str",

            ),

            key=dict(
                type="str", no_log=False,
            ),

            name=dict(
                type="str",

            ),

            password=dict(
                type="str", no_log=True,
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
                        "/rest/api/3/user",
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            elif needs_update(current, desired):
                # Resource exists but needs updating
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = dict(current, **{k: v for k, v in desired.items() if v is not None})

                if not module.check_mode:

                    identifier = current.get("key")
                    path = "".replace(
                        "{key}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})

            else:
                # Resource exists and is up-to-date

                result["accountId"] = current.get("accountId")

                result["accountType"] = current.get("accountType")

                result["active"] = current.get("active")

                result["appType"] = current.get("appType")

                result["applicationRoles"] = current.get("applicationRoles")

                result["avatarUrls"] = current.get("avatarUrls")

                result["displayName"] = current.get("displayName")

                result["emailAddress"] = current.get("emailAddress")

                result["expand"] = current.get("expand")

                result["groups"] = current.get("groups")

                result["guest"] = current.get("guest")

                result["key"] = current.get("key")

                result["locale"] = current.get("locale")

                result["name"] = current.get("name")

                result["self"] = current.get("self")

                result["timeZone"] = current.get("timeZone")

        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("key")
                    path = "/rest/api/3/user".replace(
                        "{key}", str(identifier)
                    )
                    client.delete(path)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
