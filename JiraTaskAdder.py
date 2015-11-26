# JiraTaskAdder
# Adds sub-tasks to Jira tasks
# Created by Charlie Cook

import json, requests, getpass

url = "https://jira.tools.tax.service.gov.uk/rest/api/2/issue/"

anotherTicket = ""

username = input("Please enter your Jira username: ")
password = getpass.getpass("Please enter your Jira password: ")


def add_sub_tasks():
    task_num = ""
    description = ""

    while not task_num.isdigit():
        task_num = input("\nPlease enter the task number: AWRS-")

    if task_num.isdigit():
        task_num = "AWRS-" + task_num

    while description == "":
        description = input(
            "\nPlease enter a description for the sub tickets. \nE.g. Application summary page changes for groups\n\n")

    sub_tasks = [
        "Dev - ",
        "Functional Testing - ",
        "Performance Testing - ",
        "Accessibility Testing - ",
        "Penetration Testing - ",
        "Manual Device Testing - ",
        "Device Browserstack Testing - "
    ]

    for i in range(len(sub_tasks)):
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
            print("Error with request.")

        while another_ticket != "y" and another_ticket != "Y" and another_ticket != "n" and another_ticket != "N":
            another_ticket = input("\nWould you like to add another? (y/n)\n")

        if another_ticket == "y" or another_ticket == "Y":
            another_ticket = ""
            add_sub_tasks()

add_sub_tasks()
