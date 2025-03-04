from dataclasses import dataclass, asdict
import json

@dataclass
class Event:
    name: str
    event_date: str
    description: str
    
    def save_event(self):
        try:
            with open("src/json/events.json", "r", encoding="utf-8") as file:
                events = [json.loads(line.strip()) for line in file if line.strip()]
        except FileNotFoundError:
            pass
        
        if any(event.get("name") == self.name for event in events):
            return
        
        events.append(asdict(self))

        with open("src/json/events.json", "w", encoding="utf-8") as file:
            file.write("\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n")
    
def load_events() -> list[Event]:
    eventos = []
    try:
        with open("src/json/events.json", "r", encoding="utf-8") as events_reader:
            for linea in events_reader:
                eventos.append(Event(**json.loads(linea.strip())))  
    except FileNotFoundError:
        pass  
    return eventos

    
            
