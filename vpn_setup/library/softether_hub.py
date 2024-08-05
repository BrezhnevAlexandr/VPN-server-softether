#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import requests
import json

def check_hub_exists(base_url, hub_name, auth):
    url = f"{base_url}"
    payload = {
        "jsonrpc": "2.0",
        "id": "rpc_call_id",
        "method": "EnumHub",
        "params": {}
    }
    response = requests.post(url, json=payload, auth=auth, verify=False)
    try:
        response.raise_for_status()
        hubs = response.json().get("result", {}).get("HubList", [])
        for hub in hubs:
            if hub.get("HubName_str") == hub_name:
                return True
        return False
    except Exception as e:
        return {"error": f"Unexpected Error: {str(e)}"}

def create_hub(base_url, hub_name, admin_password, no_enum, auth):
    if check_hub_exists(base_url, hub_name, auth):
        return {"message": f"Hub {hub_name} already exists."}

    url = f"{base_url}"
    payload = {
        "jsonrpc": "2.0",
        "id": "rpc_call_id",
        "method": "CreateHub",
        "params": {
            "HubName_str": hub_name,
            "AdminPasswordPlainText_str": admin_password,
            "Online_bool": True,
            "MaxSession_u32": 0,
            "NoEnum_bool": no_enum,
            "HubType_u32": 0
        }
    }
    response = requests.post(url, json=payload, auth=auth, verify=False)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        return {"error": f"HTTP Error: {errh}"}
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Error Connecting: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Unexpected Error: {err}"}
    except json.decoder.JSONDecodeError:
        return {"error": "JSON Decode Error"}

def check_user_exists(base_url, hub_name, username, auth):
    url = f"{base_url}"
    payload = {
        "jsonrpc": "2.0",
        "id": "rpc_call_id",
        "method": "EnumUser",
        "params": {"HubName_str": hub_name}
    }
    response = requests.post(url, json=payload, auth=auth, verify=False)
    try:
        response.raise_for_status()
        users = response.json().get("result", {}).get("UserList", [])
        for user in users:
            if user.get("Name_str") == username:
                return True
        return False
    except Exception as e:
        return {"error": f"Unexpected Error: {str(e)}"}

def create_user(base_url, hub_name, username, user_password, auth):
    if check_user_exists(base_url, hub_name, username, auth):
        return {"message": f"User {username} already exists in hub {hub_name}."}

    url = f"{base_url}"
    payload = {
        "jsonrpc": "2.0",
        "id": "rpc_call_id",
        "method": "CreateUser",
        "params": {
            "HubName_str": hub_name,
            "Name_str": username,
            "AuthType_u32": 1,  # 1 for password authentication
            "Auth_Password_str": user_password
        }
    }
    response = requests.post(url, json=payload, auth=auth, verify=False)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        return {"error": f"HTTP Error: {errh}"}
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Error Connecting: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Unexpected Error: {err}"}
    except json.decoder.JSONDecodeError:
        return {"error": "JSON Decode Error"}

def main():
    module = AnsibleModule(
        argument_spec=dict(
            base_url=dict(type='str', required=True),
            hubs=dict(type='list', elements='dict', required=True),
            auth_user=dict(type='str', required=True),
            auth_password=dict(type='str', required=True, no_log=True),
            hub_admin_password=dict(type='str', required=True, no_log=True),
            user_passwords=dict(type='dict', required=True)
        )
    )

    base_url = module.params['base_url']
    hubs = module.params['hubs']
    auth_user = module.params['auth_user']
    auth_password = module.params['auth_password']
    hub_admin_password = module.params['hub_admin_password']
    user_passwords = module.params['user_passwords']

    auth = (auth_user, auth_password)
    results = []

    for hub in hubs:
        hub_name = hub['name']
        no_enum = hub.get('no_enum', False)
        users = hub.get('users', [])

        # Create VirtualHub
        hub_result = create_hub(base_url, hub_name, hub_admin_password, no_enum, auth)
        results.append(hub_result)

        # Create users in the VirtualHub
        for user in users:
            user_password = user_passwords.get(user, "default_password")  # Используйте заданный пароль для каждого пользователя
            user_result = create_user(base_url, hub_name, user, user_password, auth)
            results.append(user_result)

    module.exit_json(changed=True, results=results)

if __name__ == '__main__':
    main()
