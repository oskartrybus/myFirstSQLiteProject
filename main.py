from numpy import long
import datetime
import dbManager


def print_team_members(members):
    for _id, name, surname, position, phone in members:
        phone = int(phone)
        print(f"{_id}. {name} {surname}, {position}. Phone: {phone}.")
        if dbManager.get_projects_of_member(_id):
            print(f"Projects: ", end="")
            for member_id, project_id in dbManager.get_projects_of_member(_id):
                for _id1, project_name, time, completed in dbManager.get_project_by_id(project_id):
                    if completed == 0:
                        print(project_name, end="; ")
                    else:
                        print(f"{project_name} (completed)", end="; ")
            print()
        print()


def prompt_search_for_member():
    searchBy = input("Type 0 if you want to search by name or 1 if by 'surname'")
    searchingPhrase = input("Now please type searching phrase: ")
    if searchBy == "0" or searchBy == "1":
        results = dbManager.get_member(searchBy, searchingPhrase)
    else:
        print("Wrong choice. Try again one more time!")
        return
    if results:
        print_team_members(results)
    else:
        print("Such a member has not been found!")


def prompt_add_new_member():
    # noinspection PyBroadException
    try:
        name = input("Please input new member's name: ")
        surname = input("Please input new member's surname: ")
        position = input("Please input new member's position: ")
        phone_number = long(input("Please input new member's phone_number: "))
        dbManager.add_member(name, surname, position, phone_number)
        print("Member added successfully!")
    except Exception as e:
        print("Error occurred. ")
        return


def prompt_delete_member():
    name = input("Type name of member which you want to delete: ")
    surname = input("Type surname of member which you want to delete: ")
    try:
        if not dbManager.get_member("0", name) or not dbManager.get_member("1", surname):
            raise Exception
        dbManager.delete_member(name, surname)
        print("Member deleted successfully!")
    except Exception as e:
        print("Error occurred - probably not found such a person. " + str(e))


def print_projects(completed: int):
    if completed:
        print("Completed projects: ")
    else:
        print("Uncompleted projects: ")
    results = dbManager.get_projects(completed)
    for _id, name, deadline, completed in results:
        deadline = int(deadline)
        print(f"{name}. Deadline date: {datetime.datetime.fromtimestamp(deadline).strftime('%d %b %Y')}")
    print("-------------------")


def prompt_add_project():
    # noinspection PyBroadException
    try:
        project_name = input("Input project name: ")
        deadline_date = input("Input deadline date (dd-mm-yyyy): ")
        parsed_date = datetime.datetime.strptime(deadline_date, "%d-%m-%Y")
        dbManager.add_project(project_name, parsed_date.timestamp())
        print("Project added successfully!")
    except Exception as e:
        print("Error occurred - probably bad data type")


def prompt_delete_project():
    name = input("Type name of project which you want to delete: ")
    dbManager.delete_project(name)


def prompt_update_project():
    name = input("Type carefully name of project which you want to sign as completed: ")
    dbManager.update_project(name)
    print("Done!")
    print("-----------------------------")


def prompt_assign_person_to_project():
    name = input("Type name of person. \n")
    surname = input("Type surname of person. \n")
    first = dbManager.get_member("0", name)
    second = dbManager.get_member("1", surname)
    proj_name = input("Please type project_name. \n")
    project = dbManager.get_project_by_name(proj_name)
    if first == second:
        dbManager.assign_member_to_project(first[0][0], project[0][0])
        print("Member assigned successfully!")
    else:
        print("Error occurred!")


def prompt_dismiss_person_from_project():
    name = input("Type name of person. \n")
    surname = input("Type surname of person. \n")
    first = dbManager.get_member("0", name)
    second = dbManager.get_member("1", surname)
    proj_name = input("Please type project_name. \n")
    project = dbManager.get_project_by_name(proj_name)
    if first == second:
        dbManager.dismiss_member_from_project(first[0][0], project[0][0])
        print("Member dismissed successfully!")
    else:
        print("Error occurred!")


menu = """Welcome to project manager. Please choose one of the following options:
1) Show team members
2) Search for member
3) Add team member
4) Delete member 
5) Show completed projects
6) Show uncompleted projects
7) Add Project
8) Delete Project
9) Assign person to the project
10) Dismiss person from the project
11) Make project completed
12) Exit
"""

dbManager.create_tables()
action = input(menu)
while action != "12":
    if action == "1":
        members = dbManager.get_all_team_members()
        print_team_members(members)
    elif action == "2":
        prompt_search_for_member()
    elif action == "3":
        prompt_add_new_member()
    elif action == "4":
        prompt_delete_member()
    elif action == "5":
        print_projects(completed=1)
    elif action == "6":
        print_projects(completed=0)
    elif action == "7":
        prompt_add_project()
    elif action == "8":
        prompt_delete_project()
    elif action == "9":
        prompt_assign_person_to_project()
    elif action == "10":
        prompt_dismiss_person_from_project()
    elif action == "11":
        prompt_update_project()
    else:
        print("Invalid input, please try again!")
    action = input(menu)
