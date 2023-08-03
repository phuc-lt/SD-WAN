import info_vmanager
import requests
import json
import tabulate
requests.packages.urllib3.disable_warnings()

def authentication():
    url = info_vmanager.vmanager + "/j_security_check"

    header = {
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    body = {
        "j_username" : info_vmanager.username,
        "j_password" : info_vmanager.password
    }

    response = requests.post(url, headers=header, data=body, verify=False)

    # print(response)

    # print(response.cookies)

    # print(response.headers)

    header_response = response.headers["set-cookie"]

    # print(header_response)

    # jsessionid = header_response[11:-26]

    # print(jsessionid)

    cookie = header_response.split(";")

    # print(cookie[0])

    return cookie[0]

def get_token():
    url = info_vmanager.vmanager + "/dataservice/client/token"

    header = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Cookie" : authentication()
    }

    response = requests.get(url, headers=header, verify=False)

    # print(response.json)

    data = response.text

    # print(data)

    return data

def get_device():
    url = info_vmanager.vmanager + "/dataservice/device"

    header = {
        "Content-Type" : "application/x-www-form-urlencoded",
        # "X-XSRF-TOKEN" : get_token(),
        "Cookie" : authentication()
    }

    response = requests.get(url, headers=header, verify=False)

    # print(response.text)

    # print(response.json)

    data = response.json()

    # print(data)

    parse_data = json.dumps(data, indent=4)

    print(parse_data)

    test = data["data"]
    dem = 1
    for i in data["data"]:
        print(dem, i["deviceId"])
        print(dem, i["host-name"])
        print(dem, i["status"] , "\n")
        dem += 1

    deviceId = []
    host_name = []
    status = []

    for i in data["data"]:
        deviceId.append(i["deviceId"])
        host_name.append(i["host-name"])
        status.append(i["status"])

    print(tabulate.tabulate({"deviceId" : deviceId, "host-name" : host_name, "status" : status}, headers="keys"))

def get_device_counters():
    
    url = info_vmanager.vmanager + "/dataservice/device/devicestatus"

    header = {
        "Content-Type" : "application/json",
        "Cookie" : authentication()
    }

    response = requests.get(url, headers=header, verify=False)

    data = response.json()

    parse_data = json.dumps(data, indent=4)

    print(parse_data)

if __name__ == "__main__":
    authentication()
    # get_token()
    # get_device()
    get_device_counters()