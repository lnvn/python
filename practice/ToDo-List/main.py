import os

FILENAME = "tasks.txt"

def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, 'r') as f:
        tasks = [task.strip() for task in f.readlines()]
    return tasks

def save_tasks(tasks):
    with open(FILENAME, 'w') as f:
        f.write("\n".join(tasks))

def show_menu():
    print("\n1. Add Task")
    print("2. List Tasks")
    print("3. Remove Task")
    print("4. Exit")

def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            task = input("enter a new task: ").strip()
            if task:
                tasks.append(task)
                save_tasks(tasks)
                print(f"Task '{task}' added")
            else:
                print("Task cannot be empty")
        
        elif choice == "2":
            if tasks:
                print("Your To-Do List:")
                for idx, task in enumerate(tasks, start=1):
                    print(f"{idx}. {task}")
            else:
                print("Your To-Do list is empty")

        elif choice == "3":
            if tasks:
                print("\nSelect the task number to remove")
                for idx, task in enumerate(tasks, start=1):
                    print(f"{idx}. {task}")
                try:
                    task_num = int(input("Task number: ").strip())
                    if 1 <= task_num <= len(tasks):
                        removed_task = tasks.pop(task_num - 1)
                        save_tasks(tasks)
                        print(f"Task '{removed_task}' removed")
                    else:
                        print("invalid task number")
                except ValueError:
                    print("Please enter a valid number")
            else:
                print("Your To-Do list is empty")
                    

        elif choice == "4":
            print("Good Bye!")
            break
        
        else:
            print("Invalid option, please choose from 1 to 4")



if __name__ == "__main__":
    main()