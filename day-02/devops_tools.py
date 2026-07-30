from pathlib import Path

LEVELS=("INFO", "WARNING", "ERROR")

def read_log_file(path):
    return Path(path).read_text(encoding="utf-8")



def count_logs_levels(text):
    counter={
        "INFO": 0,
        "WARNING":0,
        "ERROR":0
    }
    for line in text.splitlines():
        tokens=line.split()
        for level in LEVELS:
            if level in tokens:
               counter[level]+=1
               
    print(counter)
    
file="E:/Learning Devops 2026/Python For Devops/day-02/app.log"
text=read_log_file(file)
count_logs_levels(text)