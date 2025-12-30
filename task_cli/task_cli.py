import argparse
from pathlib import Path
import datetime
import json
import os

# task-cli add "Buy groceries"
# # Output: Task added successfully (ID: 1)
# # Updating and deleting tasks
# task-cli update 1 "Buy groceries and cook dinner"
# task-cli delete 1
# # Marking a task as in progress or done
# task-cli mark-in-progress 1
# task-cli mark-done 1
# # Listing all tasks
# task-cli list
# # Listing tasks by status
# task-cli list done
# task-cli list todo
# task-cli list in-progress

class Task: 

    def __init__(self,task_id, description, status = "todo" ,createdAt= datetime.datetime.now(), updatedAt = datetime.datetime.now() ): # Constructor
        self.id = task_id
        self.description = description    
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt
    
    def phrase_from_json(self , json_task):
        self.id = json_task["id"]
        self.description =  json_task["description"]
        self.status = json_task["status"]
        self.createdAt = datetime.datetime.fromisoformat(json_task["createdAt"])
        self.updatedAt = datetime.datetime.fromisoformat(json_task["updatedAt"])    
   
    def phrase_to_json(self):        
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt.isoformat(),
            "updatedAt": self.updatedAt.isoformat()
        }
    
    def change_status(self , status):
        self.status = status
        self.updatedAt = datetime.datetime.now()
        
    def change_description(self, description):
        self.description = description
        self.updatedAt = datetime.datetime.now()

###########################################

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1
        self.file_name ="tasks.json"
        self._load_data()

    def _load_data(self):
        data = {}
        if os.path.exists(self.file_name) and os.path.isfile(self.file_name):
            with open(self.file_name, "r") as f:
                data = json.load(f)
                
        if len(data) >0 :
            self.set_info_from_data(data)
            print(f"data is uploaded successfully, the next id is: " + str(self.next_id))
        else:
            return ""
       
    def set_info_from_data(self , new_data):
        for task_id , task_info in new_data["tasks"].items():
            task = Task(task_id , task_info["description"])
            task.phrase_from_json(task_info)
            self.tasks[task_id] = task
        self.next_id = new_data["next_id"]
        self.file_name  = new_data["file_name"]
        
    def save_data(self):
        with open(self.file_name, "w") as f:
            json_tasks = {}
            to_json = {}
            for task_id , task in self.tasks.items():
                json_task = task.phrase_to_json()
                json_tasks[task.id] = json_task
            to_json["tasks"] = json_tasks
            to_json["next_id"] = self.next_id
            to_json["file_name"] = self.file_name     
            json.dump(to_json, f, indent=2)
        
    def add_task(self,description):
        new_id = self.next_id
        task = Task(new_id ,description)
        self.tasks[new_id] = task
        print(f"Task added successfully (ID: {new_id})")
        self.next_id = new_id + 1
            
    def update_task(self,task , description):
        task.change_description(description)
        print(f"task {task.id} was updated successfully")
            
    def delete_task(self,task_id):
        del self.tasks[task_id]
        print(f"Task {task_id} deleted successfully")
            
    def print_list(self , list):
        if (list):
            for task in list:
                print(f"|task: {task.id} | description: {task.description} | status: {task.status} \n")
        else:
            print("No tasks found")
                
    def actions_for_tasks(self ,args):
        if (args.command == "add" and args.description):
            self.add_task(args.description)
        
        elif(args.command == "delete" and args.id):
            if (args.id in self.tasks.keys()):
                self.delete_task(args.id)
            else:
                print("task id not found")
            
        elif(args.command == "update" and args.id and args.description):
            if (args.id in self.tasks.keys()):
                task = self.tasks.get(args.id)
                self.update_task(task , args.description)
            else:
                print("task id not found")
        else:
            print("Invalid command")
            
    def actions_for_status(self, command , id):
        if (id in self.tasks.keys()):
            task = self.tasks.get(id)
            if( command == "mark-in-progress"):
                command = "in-progress"
            elif(command == "mark-done"):
                command = "done"
            task.change_status(command)
            print(f"task {task.id} status changed to : {task.status}")

    def actions_for_list(self, status):
        if status in ["done" , "todo" , "in-progress"]:
            list = [t for t in self.tasks.values() if t.status == status]
        elif status is None:
            list = self.tasks.values()
        else:
            print("Invalid command")
            return    
        self.print_list(list)
                   
def main():
    task_manager = TaskManager()
    parser = argparse.ArgumentParser(description="Task CLI for managing your tasks")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", type=str, help="The description of the task")

    update_parser = subparsers.add_parser("update", help="delete existing task")
    update_parser.add_argument("id", type=str, help="The id number of the task")
    update_parser.add_argument("description", type=str, help="The description of the task")
    
    delete_parser = subparsers.add_parser("delete", help="update existing task")
    delete_parser.add_argument("id", type=str, help="The id number of the task")
    
    mark_in_progress_parser = subparsers.add_parser("mark-in-progress", help="Add a new task")
    mark_in_progress_parser.add_argument("id", type=str, help="The description of the task")

    mark_done_parser = subparsers.add_parser("mark-done", help="delete existing task")
    mark_done_parser.add_argument("id", type=str, help="The id number of the task")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("status", nargs="?", choices=["todo", "in-progress", "done"], help="Filter by status")

    args = parser.parse_args()
    if args.command in ["add","delete", "update"]:
        task_manager.actions_for_tasks(args) 
    elif args.command in ["mark-in-progress","mark-done"]:
        task_manager.actions_for_status(args.command , args.id)
    elif args.command == "list":
        task_manager.actions_for_list(args.status)  
    elif args.command is None:
        parser.print_help()
    else:
        print("Invalid command")
    task_manager.save_data()
        
if __name__ == "__main__":
    main()
    print("\n[*] Done.") 
        