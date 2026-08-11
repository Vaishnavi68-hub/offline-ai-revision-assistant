from relevance import calculate_relevance


summary = """
CPU scheduling determines which process receives CPU time.

FCFS schedules processes based on arrival order.
SJF selects the shortest job.
Round Robin uses a time quantum.
"""


keywords = [
    "cpu",
    "scheduling",
    "process",
    "fcfs",
    "sjf",
    "round robin",
    "priority"
]


score = calculate_relevance(
    summary,
    keywords
)


print(
    f"Relevance score: {score:.2f}%"
)