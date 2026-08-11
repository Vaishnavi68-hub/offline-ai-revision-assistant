from evaluator import calculate_coverage


summary = """
CPU scheduling selects processes for execution.

FCFS schedules processes according to arrival order.

SJF selects the process with the shortest burst time.

Round Robin uses a fixed time quantum.
"""


expected_points = [
    "CPU scheduling selects a process for CPU execution.",
    "FCFS schedules processes according to arrival order.",
    "SJF selects the process with the shortest burst time.",
    "Round Robin uses a fixed time quantum.",
    "Priority Scheduling uses process priority."
]


score = calculate_coverage(
    summary,
    expected_points
)


print(
    f"Coverage score: {score:.2f}%"
)