#!/usr/bin/env python

'''
Toggle VM Power state with output from
```sh
az list vm -d
```
'''

from os import system
from json import loads
from sys import stdin as az_output

while not az_output.readable():
    pass  # wait while az vm list is done and python has it buffered


def vm_stat(az_json, vm_name):
    '''
    Analyze the json output of az vm list to check
    * @param az_json is valid, in case az is not in PATH
    * return whether a vm state object when a vm
      with name @param vm_name exists
    '''

    if az_json is None:
        return az_json

    if isinstance(az_json, list):
        return next((vm for vm in az_json if vm['name'] == vm_name), None)

    if isinstance(az_json, dict) and \
            'name' in az_json and az_json['name'] == vm_name:
        return az_json

    return None


def switch_vm_on(vm_state):
    '''
    Turn VM on
    '''

    name = vm_state['name']
    group = vm_state['resourceGroup']
    command = 'az vm start -n %s -g %s' % (name, group)

    print('Turning ON', name)

    return system(command)


def switch_vm_off(vm_state):
    '''
    Turn VM off
    '''

    name = vm_state['name']
    group = vm_state['resourceGroup']
    command = 'az vm deallocate -n %s -g %s' % (name, group)

    print('Turning OFF', name)

    return system(command)


def toggle_vm(vm_state):
    '''
    Toggle power of vm pointed by @param vm_state
    '''

    if isinstance(vm_state, dict):
        state = vm_state['powerState']
        call = switch_vm_off if state == 'VM running' else switch_vm_on

        return state.split()[1], call(vm_state)

    return None, None


az_output = az_output.read()
resp = loads(az_output)  # get pipped output from az vm list
switch_vm_state = vm_stat(resp, 'SwitchVM')

last_state, op_code = toggle_vm(switch_vm_state)
