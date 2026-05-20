#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: jira_field
short_description: Manage issue fields
version_added: "1.0.0"
description:
  - Create, update, and delete field resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Steve Fulmer"
options:
  state:
    description:
      - Desired state of the field resource.
    type: str
    choices: ['present', 'absent']
    default: present

  type:
    description:
      - >-
        The type of the custom field. These built-in custom field types are available: cascadingselect:...
    type: str

    required: true





  description:
    description:
      - >-
        The description of the custom field. The maximum length is 40000 characters.
    type: str





  name:
    description:
      - >-
        The name of the custom field. It doesn't have to be unique. The maximum length is 255 characters.
    type: str





  searcherKey:
    description:
      - >-
        The searcher that defines the way the field is searched in Jira. It can be set to null,...
    type: str
    choices:
      - com.atlassian.jira.plugin.system.customfieldtypes:cascadingselectsearcher
      - com.atlassian.jira.plugin.system.customfieldtypes:daterange
      - com.atlassian.jira.plugin.system.customfieldtypes:datetimerange
      - com.atlassian.jira.plugin.system.customfieldtypes:exactnumber
      - com.atlassian.jira.plugin.system.customfieldtypes:exacttextsearcher
      - com.atlassian.jira.plugin.system.customfieldtypes:grouppickersearcher
      - com.atlassian.jira.plugin.system.customfieldtypes:labelsearcher
      - com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher
      - com.atlassian.jira.plugin.system.customfieldtypes:numberrange
      - com.atlassian.jira.plugin.system.customfieldtypes:projectsearcher
      - com.atlassian.jira.plugin.system.customfieldtypes:textsearcher
      - com.atlassian.jira.plugin.system.customfieldtypes:userpickergroupsearcher
      - com.atlassian.jira.plugin.system.customfieldtypes:versionsearcher




extends_documentation_fragment:
  - stevefulme1.atlassian.auth
"""

EXAMPLES = r"""

- name: Create a field
  stevefulme1.atlassian.jira_field:


    type: "example_type"








    state: present
  # API: POST /rest/api/3/field



- name: Update a field
  stevefulme1.atlassian.jira_field:
    id: "existing_id"




    description: "updated_description"



    name: "updated_name"



    searcherKey: "updated_searcherKey"


    state: present
  # API:  



- name: Delete a field
  stevefulme1.atlassian.jira_field:
    id: "existing_id"
    state: absent
  # API: DELETE /rest/api/3/field/{id}

"""

RETURN = r"""

isLast:
  description: >-
    Whether this is the last page.
  returned: success
  type: bool


maxResults:
  description: >-
    The maximum number of items that could be returned.
  returned: success
  type: int


nextPage:
  description: >-
    If there is another page of results, the URL of the next page.
  returned: success
  type: str


self:
  description: >-
    The URL of the page.
  returned: success
  type: str


startAt:
  description: >-
    The index of the first item returned.
  returned: success
  type: int


total:
  description: >-
    The number of items returned.
  returned: success
  type: int


values:
  description: >-
    The list of items.
  returned: success
  type: list


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.atlassian.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def get_current_state(client, module):
    """Retrieve the current state of the field via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("id")

    search_key = "id"
    search_value = identifier

    if search_value is None:
        return None
    try:
        items = client.get("/rest/api/3/projects/fields")
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

    if module.params.get("type") is not None:
        payload["type"] = module.params["type"]

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("searcherKey") is not None:
        payload["searcherKey"] = module.params["searcherKey"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            type=dict(
                type="str",

                required=True,





            ),

            description=dict(
                type="str",





            ),

            name=dict(
                type="str",





            ),

            searcherKey=dict(
                type="str",
                choices=[
                    'com.atlassian.jira.plugin.system.customfieldtypes:cascadingselectsearcher',
                    'com.atlassian.jira.plugin.system.customfieldtypes:daterange',
                    'com.atlassian.jira.plugin.system.customfieldtypes:datetimerange',
                    'com.atlassian.jira.plugin.system.customfieldtypes:exactnumber',
                    'com.atlassian.jira.plugin.system.customfieldtypes:exacttextsearcher',
                    'com.atlassian.jira.plugin.system.customfieldtypes:grouppickersearcher',
                    'com.atlassian.jira.plugin.system.customfieldtypes:labelsearcher',
                    'com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher',
                    'com.atlassian.jira.plugin.system.customfieldtypes:numberrange',
                    'com.atlassian.jira.plugin.system.customfieldtypes:projectsearcher',
                    'com.atlassian.jira.plugin.system.customfieldtypes:textsearcher',
                    'com.atlassian.jira.plugin.system.customfieldtypes:userpickergroupsearcher',
                    'com.atlassian.jira.plugin.system.customfieldtypes:versionsearcher',
                ],
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
                        "/rest/api/3/field",
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

                result["isLast"] = current.get("isLast")

                result["maxResults"] = current.get("maxResults")

                result["nextPage"] = current.get("nextPage")

                result["self"] = current.get("self")

                result["startAt"] = current.get("startAt")

                result["total"] = current.get("total")

                result["values"] = current.get("values")


        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("id")
                    path = "/rest/api/3/field/{id}".replace(
                        "{id}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
