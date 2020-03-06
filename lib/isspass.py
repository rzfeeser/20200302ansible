#!/usr/bin/python3
# API to use:
# http://api.open-notify.org/iss-pass.json
# two REQUIRED params are lat and lon
# example:
# ?lat=45.0&lon=-122.3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: isspass

short_description: This is my iss pass time module

version_added: "2.9"

description:
    - "This is my longer description explaining my iss module. You can access the JSON link here http://api.open-notify.org/iss-pass.json"

options:
    lat:
        description:
            - This is the users latitude
        required: true
    lon:
        description:
            - This is the users longitude
        required: true
    file:
        description:
            - This is the file you want the results dumped to
        required: false

author:
    - Zach Feeser (@yourhandle)
'''

EXAMPLES = '''
# Pass in a message
- name: User wants pass time of ISS
  isspass:
    lat: 45.0
    lon: -122.3
    file: passtime.txt
'''

RETURN = '''
user_lat:
    description: The users lat that passed in
    type: float
    returned: always
user_lon:
    description: The users lon that is passed in
    type: float
    returned: always
file:
    description: File optionally created
    type: str
    returned: optional
issjson:
    description: this is the the JSON returned by the API lookup
    type: string
    returned: always
'''
import requests
from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        lat=dict(type='float', required=True),
        lon=dict(type='float', required=True),
        file=dict(type='str', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        user_lat='',
        user_lon='',
        file='',
        issjson=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)    
    
    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['user_lat'] = module.params['lat']
    result['user_lon'] = module.params['lon']
    if module.params.get('file'):
        result['file'] = module.params['file']

    issrequest = requests.get(f"http://api.open-notify.org/iss-pass.json?lat={module.params['lat']}&lon={module.params['lon']}")

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if issrequest.status_code != 200:
        module.fail_json(msg='Uh oh, you did not get back success', **result)

    issjson = issrequest.json() 

    result['issjson']=issjson

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    result['changed'] = True

    if module.params.get('file'):
        with open(module.params['file'], "w") as myfile:
            myfile.write(str(issjson))            

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    #if issrequest.status_code != 200:
    #    module.fail_json(msg='Uh oh, you did not get back success', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
