from datetime import datetime
from dataclasses import dataclass, asdict
import json

@dataclass
class Task:
    name: str
    task_date: str
    description: str
    
    def save_task(self):
        try:
            with open("src/json/tasks.json", "r", encoding="utf-8") as file:
                tasks = [json.loads(line.strip()) for line in file if line.strip()]
        except FileNotFoundError:
            pass
        
        if any(task.get("name") == self.name for task in tasks):
            return
        
        tasks.append(asdict(self))

        with open("src/json/tasks.json", "w", encoding="utf-8") as file:
            file.write("\n".join(json.dumps(task, ensure_ascii=False) for task in tasks) + "\n")

    
def load_tasks() -> list[Task]:
    eventos = []
    try:
        with open("src/json/tasks.json", "r", encoding="utf-8") as tasks_reader:
            for linea in tasks_reader:
                eventos.append(Task(**json.loads(linea.strip())))  
    except FileNotFoundError:
        pass  
    return eventos

def pospone_task(task_name) -> None:
    updated_lines = []
    with open("src/json/tasks.json", "r", encoding="utf-8") as file:
        for line in file:
            try:
                task = json.loads(line.strip())
                if task.get("name") == task_name:
                    old_date = datetime.strptime(task["task_date"], "%d/%m/%Y")
                    task["task_date"] = datetime.strptime(
                        f"{old_date.day+1}/{old_date.month}/{old_date.year}", 
                        "%d/%m/%Y"
                    ).strftime("%d/%m/%Y")
                updated_lines.append(json.dumps(task))
            except json.JSONDecodeError:
                print(f"Error decodificando JSON en línea: {line.strip()}")
                updated_lines.append(line.strip())
    
    with open("src/json/tasks.json", "w", encoding="utf-8") as file:
        file.write("\n".join(updated_lines) + "\n")

    
            
