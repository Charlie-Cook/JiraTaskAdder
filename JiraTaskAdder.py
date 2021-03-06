# JiraTaskAdder
# Adds sub-tasks to Jira tasks
# Created by Charlie Cook

import requests
import getpass
import json
from tqdm import tqdm

# Change the URL to the correct location of your Jira
url = "***REMOVED***"

username = input("Please enter your Jira username: ")
password = getpass.getpass("Please enter your Jira password: ")


def add_sub_tasks():
    task_num = ""
    description = ""
    another_ticket = ""

    while not task_num.isdigit():
        task_num = input("\nPlease enter the task number: AWRS-")

    if task_num.isdigit():
        task_num = "AWRS-" + task_num

    t_request = requests.get(url + task_num, auth=(username, password))
    if t_request.status_code != 200:
        print("Error getting parent ticket.")
        add_sub_tasks()

    else:
        parsed_json = json.loads(str(t_request.text))
        description = parsed_json['fields']['summary']

        if description == "":
            print("Ticket not found or contains a blank summary.")
            add_sub_tasks()

        sub_tasks = [
            "Dev - ",
            "Functional Testing - ",
            "Performance Testing - ",
            "Accessibility Testing - ",
            "Penetration Testing - ",
            "Manual Device Testing - ",
            "Device Browserstack Testing - "
        ]

        for i in tqdm(range(len(sub_tasks))):
            payload = {
                "fields":
                    {
                        "project":
                            {
                                "key": "AWRS"
                            },
                        "parent":
                            {
                                "key": task_num,
                            },
                        "summary": sub_tasks[i] + description,
                        "description": sub_tasks[i] + description,
                        "issuetype":
                            {
                                "id": "5"
                            }
                    }
            }

            j_request = requests.post(url, json=payload, auth=(username, password))

            if j_request.status_code != 201:
                print("Error creating sub-ticket.")

        while another_ticket != "y" and another_ticket != "Y" and another_ticket != "n" and another_ticket != "N":
            another_ticket = input("\nWould you like to add another? (y/n)\n")

        if another_ticket == "y" or another_ticket == "Y":
            add_sub_tasks()

add_sub_tasks()
