
EVALUATION_DATASET = [

    {
        "topic": "CPU Scheduling",

        "text": """
CPU scheduling is the process of selecting a process
from the ready queue and allocating the CPU to it.

Common CPU scheduling algorithms include:
First Come First Serve (FCFS),
Shortest Job First (SJF),
Round Robin (RR),
and Priority Scheduling.

FCFS schedules processes according to their arrival order.
SJF selects the process with the shortest burst time.
Round Robin assigns each process a fixed time quantum.
Priority Scheduling selects processes according to priority.
""",

        "expected_points": [
            "CPU scheduling selects a process for CPU execution.",
            "FCFS schedules processes according to arrival order.",
            "SJF selects the process with the shortest burst time.",
            "Round Robin uses a fixed time quantum.",
            "Priority Scheduling uses process priority."
        ],

        "keywords": [
            "cpu",
            "scheduling",
            "process",
            "fcfs",
            "sjf",
            "round robin",
            "priority"
        ]
    },


    {
        "topic": "Database Normalization",

        "text": """
Database normalization is a technique used to organize
data in a relational database and reduce redundancy.

First Normal Form requires atomic values and no repeating groups.

Second Normal Form requires the table to be in First Normal Form
and removes partial dependencies.

Third Normal Form requires the table to be in Second Normal Form
and removes transitive dependencies.
""",

        "expected_points": [
            "Normalization organizes relational database data.",
            "Normalization reduces data redundancy.",
            "First Normal Form requires atomic values.",
            "Second Normal Form removes partial dependencies.",
            "Third Normal Form removes transitive dependencies."
        ],

        "keywords": [
            "database",
            "normalization",
            "redundancy",
            "atomic",
            "1nf",
            "2nf",
            "3nf",
            "partial dependency",
            "transitive dependency"
        ]
    }

]