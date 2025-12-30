# Task Tracker CLI

A simple Command Line Interface (CLI) to manage your to-do list, built with Python.  
This project is a solution for the  
[Task Tracker roadmap.sh challenge](https://roadmap.sh/projects/task-tracker).

---

## Features

- Add, update, and delete tasks
- Mark tasks as **todo**, **in-progress**, or **done**
- List all tasks or filter them by status
- Automatic data persistence using a local `tasks.json` file
- Built using only Python standard libraries (no external dependencies)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Caspiofri/PythonProjects
cd task_cli
```

### 2. Requirements

No installation is required.  
Ensure **Python 3.x** is installed.

---

## Usage

Run the application using:

```bash
python task_cli.py <command> [arguments]
```

### Add a new task

```bash
python task_cli.py add "Buy groceries"
```

Output:

```
Task added successfully (ID: 1)
```

### Update a task

```bash
python task_cli.py update 1 "Buy groceries and cook dinner"
```

### Delete a task

```bash
python task_cli.py delete 1
```

### Change task status

Mark as in progress:

```bash
python task_cli.py mark-in-progress 1
```

Mark as done:

```bash
python task_cli.py mark-done 1
```

### List tasks

All tasks:

```bash
python task_cli.py list
```

By status:

```bash
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done
```

---

## Data Storage

Tasks are stored in a local file named `tasks.json`.  
The file is created automatically when the first task is added.

---

## Project Structure

```
.
├── main.py       # Main CLI entry point
└── tasks.json    # Generated file storing task data
```

> **Note:**  
> Add `tasks.json` to `.gitignore` to avoid committing local data.

---

## License

This project was created as part of the roadmap.sh Task Tracker challenge.
