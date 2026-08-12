
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
      },

    {
        "topic": "OSI Model",

        "text": """
The OSI model is a conceptual framework used to understand
network communication.

It consists of seven layers:
Physical, Data Link, Network, Transport,
Session, Presentation, and Application.

The Physical layer is responsible for transmitting raw bits
over a communication medium.

The Data Link layer provides node-to-node data transfer
and handles framing and error detection.

The Network layer is responsible for logical addressing
and routing packets between networks.

The Transport layer provides end-to-end communication
and may provide reliability, flow control, and error recovery.

The Session layer manages communication sessions.

The Presentation layer handles data translation,
encryption, and compression.

The Application layer provides network services
directly to applications.
""",

        "expected_points": [
            "The OSI model is a conceptual framework for network communication.",
            "The OSI model consists of seven layers.",
            "The Physical layer transmits raw bits.",
            "The Data Link layer handles framing and error detection.",
            "The Network layer handles logical addressing and routing.",
            "The Transport layer provides end-to-end communication.",
            "The Session layer manages communication sessions.",
            "The Presentation layer handles translation encryption and compression.",
            "The Application layer provides network services to applications."
        ],

        "keywords": [
            "osi",
            "network",
            "physical",
            "data link",
            "network layer",
            "transport",
            "session",
            "presentation",
            "application",
            "routing",
            "framing",
            "encryption"
        ]
       },

    {
        "topic": "Machine Learning Basics",

        "text": """
Machine learning is a branch of artificial intelligence
that enables computers to learn patterns from data
and make predictions or decisions.

Supervised learning uses labeled training data.
Common supervised learning algorithms include
linear regression, logistic regression,
decision trees, and support vector machines.

Unsupervised learning works with unlabeled data.
Clustering and dimensionality reduction are
common unsupervised learning techniques.

Classification predicts discrete categories,
while regression predicts continuous numerical values.

The training set is used to train a machine learning model.
The test set is used to evaluate how well the model
generalizes to unseen data.

Overfitting occurs when a model learns the training data
too closely and performs poorly on unseen data.
Underfitting occurs when a model is too simple
to capture important patterns in the data.
""",

        "expected_points": [
            "Machine learning enables computers to learn patterns from data.",
            "Supervised learning uses labeled training data.",
            "Unsupervised learning uses unlabeled data.",
            "Classification predicts discrete categories.",
            "Regression predicts continuous numerical values.",
            "The training set is used to train a model.",
            "The test set evaluates model performance on unseen data.",
            "Overfitting occurs when a model learns training data too closely.",
            "Underfitting occurs when a model is too simple to capture patterns."
        ],

        "keywords": [
            "machine learning",
            "supervised",
            "labeled",
            "unsupervised",
            "clustering",
            "classification",
            "regression",
            "training",
            "test",
            "overfitting",
            "underfitting"
        ]
        },

    {
        "topic": "Data Structures",

        "text": """
A data structure is a method of organizing and storing data
so that it can be accessed and modified efficiently.

An array stores elements in contiguous memory locations
and provides fast access using an index.

A linked list consists of nodes where each node contains
data and a reference to the next node.

A stack follows the Last In First Out principle.
Common stack operations are push and pop.

A queue follows the First In First Out principle.
Common queue operations are enqueue and dequeue.

A tree is a hierarchical data structure consisting
of nodes connected by edges.

A binary tree is a tree in which each node has
at most two children.

A graph consists of vertices and edges and can represent
relationships between objects.

Hash tables store key-value pairs and provide
efficient average-case lookup.
""",

        "expected_points": [
            "A data structure organizes and stores data efficiently.",
            "An array provides indexed access to elements.",
            "A linked list consists of nodes connected by references.",
            "A stack follows the Last In First Out principle.",
            "A queue follows the First In First Out principle.",
            "A binary tree has at most two children per node.",
            "A graph consists of vertices and edges.",
            "Hash tables store key-value pairs."
        ],

        "keywords": [
            "data structure",
            "array",
            "linked list",
            "stack",
            "lifo",
            "queue",
            "fifo",
            "tree",
            "binary tree",
            "graph",
            "vertices",
            "edges",
            "hash table"
        ]
    }
]