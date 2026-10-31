"""
Career-Specific 3-Phase Adaptive Roadmap Curriculum.
Defines Beginner, Intermediate, and Advanced learning modules, learning objectives,
and rich learning materials (text lessons, code examples, exercises, documentation,
curated educational links, mini-projects, and practice checks).
"""
from typing import Dict, List, Any, Optional

CAREER_CURRICULUMS: Dict[str, Dict[str, Any]] = {
    "ai-engineer": {
        "career_id": "ai-engineer",
        "career_title": "AI Engineer",
        "description": "Comprehensive engineering roadmap spanning algorithmic foundations, data transformation, machine learning systems, deep learning architectures, and model deployment.",
        "phases": [
            {
                "phase_id": "phase-1",
                "phase_number": 1,
                "name": "Beginner Phase",
                "difficulty": "Beginner",
                "description": "Foundational programming, mathematical principles, problem-solving techniques, and introductory AI concepts.",
                "passing_score": 80,
                "assessment_question_count": 10,
                "modules": [
                    {
                        "id": "ai_beg_python_fund",
                        "module_title": "Python Fundamentals",
                        "topic_title": "Python Fundamentals",
                        "estimated_duration": "2.5 hours",
                        "learning_objectives": [
                            "Master core Python syntax, variables, and primitive data types",
                            "Implement control flow logic with if-else conditionals and for/while loops",
                            "Utilize Python collections: lists, dictionaries, tuples, and sets",
                            "Write modular, reusable functions with proper type annotations and docstrings"
                        ],
                        "learning_materials": {
                            "lesson": "Python is the primary language for Artificial Intelligence. Its expressive syntax and vast ecosystem (NumPy, PyTorch, Scikit-learn) make it ideal for prototyping and production. In this module, you will learn to structure Python programs cleanly, manage variable state, use built-in data structures efficiently, and write functions with defensive error handling.",
                            "step_by_step_explanation": [
                                "1. Variables & Data Types: Python is dynamically typed. Primitive types include int, float, str, and bool.",
                                "2. Collections: Lists are ordered and mutable; Tuples are ordered and immutable; Dictionaries store key-value pairs with O(1) lookups; Sets store unique values.",
                                "3. Control Structures: Use if/elif/else for branching logic. Use for loops with range() or sequence iteration, and while loops for conditional loops.",
                                "4. Functions: Define functions using 'def', pass positional and keyword arguments, return explicit outputs, and encapsulate repetitive logic."
                            ],
                            "code_examples": [
                                {
                                    "title": "Data Processing Function in Python",
                                    "code": "def normalize_scores(raw_scores: list[float]) -> dict[str, float]:\n    \"\"\"Calculates min, max, and min-max normalized scores.\"\"\"\n    if not raw_scores:\n        return {'min': 0.0, 'max': 0.0, 'normalized': []}\n    min_val = min(raw_scores)\n    max_val = max(raw_scores)\n    rng = max_val - min_val if max_val != min_val else 1.0\n    normalized = [(x - min_val) / rng for x in raw_scores]\n    return {'min': min_val, 'max': max_val, 'normalized': normalized}\n\nsample_data = [45.0, 78.5, 92.0, 60.0]\nprint(normalize_scores(sample_data))",
                                    "explanation": "Demonstrates type hints, defensive checks against empty lists, min-max calculation, list comprehensions, and dictionary return."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Student Grade Categorizer",
                                    "instructions": "Create a function 'categorize_students' that takes a dictionary of student names and scores, and returns a dict mapping student names to 'Distinction' (>=80), 'Pass' (>=50), or 'Needs Improvement' (<50)."
                                }
                            ],
                            "documentation": [
                                {"title": "Python 3 Official Tutorial", "url": "https://docs.python.org/3/tutorial/"},
                                {"title": "PEP 8 Style Guide for Python", "url": "https://peps.python.org/pep-0008/"}
                            ],
                            "curated_videos": [
                                {"title": "Python Programming Course (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: Command-Line Data Metric Calculator",
                                "steps": [
                                    "Accept a list of floating-point numbers from standard input",
                                    "Calculate Mean, Median, Variance, and Standard Deviation without third-party libraries",
                                    "Format and display the metrics in a structured ASCII table"
                                ],
                                "expected_outcome": "A self-contained Python script computing descriptive statistical indicators."
                            },
                            "knowledge_check": {
                                "question": "Which Python collection provides constant-time O(1) membership testing and ensures all elements are unique?",
                                "options": ["List", "Tuple", "Set", "Linked List"],
                                "correct_answer": "Set",
                                "explanation": "Sets in Python are implemented using hash tables, allowing O(1) average lookup and strictly unique elements."
                            }
                        }
                    },
                    {
                        "id": "ai_beg_prog_basics",
                        "module_title": "Programming Basics",
                        "topic_title": "Programming Basics",
                        "estimated_duration": "2.0 hours",
                        "learning_objectives": [
                            "Understand algorithm execution, memory models, and variable scopes",
                            "Apply defensive programming and exception handling with try-except-finally",
                            "Work with file I/O operations (reading and writing text and JSON files)",
                            "Analyze basic Big-O time and space complexity"
                        ],
                        "learning_materials": {
                            "lesson": "Robust AI systems require sound software engineering fundamentals. This module focuses on error handling, file persistence, memory life-cycles, and computational complexity. Learning how code interacts with the operating system and files prepares you for loading large datasets reliably.",
                            "step_by_step_explanation": [
                                "1. Exception Handling: Wrap risky operations (I/O, parsing, conversions) in try-except blocks. Catch specific exceptions rather than bare 'except:'.",
                                "2. Context Managers: Always use 'with open(...) as f:' for file operations to guarantee proper file descriptor release.",
                                "3. JSON Persistence: Serialize Python data structures with json.dump() and deserialize with json.load().",
                                "4. Big-O Basics: O(1) constant time, O(N) linear time, O(N log N) log-linear sorting, and O(N^2) quadratic time."
                            ],
                            "code_examples": [
                                {
                                    "title": "Safe File I/O and JSON Handling",
                                    "code": "import json\n\ndef save_model_metadata(filepath: str, metadata: dict) -> bool:\n    try:\n        with open(filepath, 'w', encoding='utf-8') as f:\n            json.dump(metadata, f, indent=2)\n        return True\n    except (IOError, TypeError) as err:\n        print(f'Failed to save metadata: {err}')\n        return False",
                                    "explanation": "Illustrates context managers for clean I/O and multi-exception handling."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Config Validator",
                                    "instructions": "Write a script that reads a JSON config file, checks for required keys ['learning_rate', 'epochs', 'batch_size'], and raises ValueError if any are missing."
                                }
                            ],
                            "documentation": [
                                {"title": "Python Errors and Exceptions", "url": "https://docs.python.org/3/tutorial/errors.html"}
                            ],
                            "curated_videos": [
                                {"title": "CS50 - Computational Thinking & Algorithms", "url": "https://www.youtube.com/watch?v=kU4v5kK79hA"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: Automated Log File Parser",
                                "steps": [
                                    "Read a server log file containing timestamps, log levels (INFO, WARN, ERROR), and messages",
                                    "Count error frequency per hour",
                                    "Write an aggregated summary to a new report file"
                                ],
                                "expected_outcome": "A Python utility that ingests log records and generates structured summary analytics."
                            },
                            "knowledge_check": {
                                "question": "What is the primary benefit of using Python's 'with' statement when opening files?",
                                "options": [
                                    "It automatically closes the file even if an exception is raised",
                                    "It speeds up file read operations by using GPU caching",
                                    "It compresses the file automatically on disk",
                                    "It prevents other processes from reading the file"
                                ],
                                "correct_answer": "It automatically closes the file even if an exception is raised",
                                "explanation": "The 'with' statement invokes context managers (__enter__ and __exit__), guaranteeing resource cleanup."
                            }
                        }
                    },
                    {
                        "id": "ai_beg_basic_math",
                        "module_title": "Basic Mathematics",
                        "topic_title": "Basic Mathematics",
                        "estimated_duration": "2.5 hours",
                        "learning_objectives": [
                            "Understand vectors, matrices, and dot products essential for neural computation",
                            "Calculate derivatives, partial derivatives, and gradients for optimization",
                            "Grasp fundamental probability concepts: random variables, expectations, and Bayes' Theorem",
                            "Apply matrix transformations using NumPy"
                        ],
                        "learning_materials": {
                            "lesson": "Mathematics is the language of machine learning. Optimization algorithms rely on calculus (gradients), data representation relies on linear algebra (vectors and tensors), and model uncertainty relies on probability theory. Mastering these fundamentals empowers you to understand why models converge and how loss surfaces behave.",
                            "step_by_step_explanation": [
                                "1. Vectors & Dot Products: A dot product between vector u and vector v measures directional alignment and computes weighted sums: u · v = sum(u_i * v_i).",
                                "2. Matrices: Linear mappings. Matrix-vector multiplication transforms coordinate systems.",
                                "3. Calculus & Gradients: The derivative of f(x) gives the instantaneous slope. The gradient vector points toward steepest ascent.",
                                "4. Probability: Bayes' Theorem P(A|B) = [P(B|A) * P(A)] / P(B) underpins Bayesian classifiers and probabilistic reasoning."
                            ],
                            "code_examples": [
                                {
                                    "title": "Matrix Multiplication & Vector Operations with NumPy",
                                    "code": "import numpy as np\n\n# Weights (3 inputs, 2 neurons) and Inputs (3 features)\nW = np.array([[0.2, 0.8], [0.5, -0.1], [-0.3, 0.4]])\nx = np.array([1.5, 2.0, -0.5])\nb = np.array([0.1, -0.2])\n\n# Forward linear projection: z = x * W + b\nz = np.dot(x, W) + b\nprint('Layer Output:', z)",
                                    "explanation": "Demonstrates the fundamental forward pass equation of linear and neural layers using NumPy dot products."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Manual Gradient Step",
                                    "instructions": "Given the function f(w) = w^2 - 4w + 4, calculate its derivative f'(w), and implement 5 iterations of gradient descent starting from w=10 with learning rate 0.1."
                                }
                            ],
                            "documentation": [
                                {"title": "Essence of Linear Algebra (3Blue1Brown)", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab"},
                                {"title": "NumPy Mathematical Operations", "url": "https://numpy.org/doc/stable/reference/routines.math.html"}
                            ],
                            "curated_videos": [
                                {"title": "Calculus for Machine Learning", "url": "https://www.youtube.com/watch?v=WUvTyaaNkzM"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: 2D Linear Transformation Visualizer",
                                "steps": [
                                    "Define a set of 2D points representing a polygon",
                                    "Apply rotation and scaling matrices using NumPy",
                                    "Compute transformed coordinates and evaluate point distances"
                                ],
                                "expected_outcome": "NumPy implementation demonstrating geometric linear transformations."
                            },
                            "knowledge_check": {
                                "question": "What is the dot product of two vectors [1, 3] and [4, -1]?",
                                "options": ["1", "7", "4", "-3"],
                                "correct_answer": "1",
                                "explanation": "Dot product = (1 * 4) + (3 * -1) = 4 - 3 = 1."
                            }
                        }
                    },
                    {
                        "id": "ai_beg_intro_ai",
                        "module_title": "Introduction to AI",
                        "topic_title": "Introduction to AI",
                        "estimated_duration": "2.0 hours",
                        "learning_objectives": [
                            "Distinguish between Artificial Intelligence, Machine Learning, and Deep Learning",
                            "Identify Supervised, Unsupervised, and Reinforcement Learning paradigms",
                            "Understand intelligent agent architectures and environment properties",
                            "Appreciate ethical implications, bias, and responsible AI practices"
                        ],
                        "learning_materials": {
                            "lesson": "Artificial Intelligence is the broad study of systems that perceive environments, reason about goals, and take actions to maximize success. Machine Learning is the empirical branch where systems learn decision boundaries from data rather than hardcoded rules. Deep Learning uses multi-layered neural networks to extract hierarchical features automatically.",
                            "step_by_step_explanation": [
                                "1. Paradigms: Supervised Learning (labeled inputs and targets), Unsupervised Learning (discovering latent patterns/clusters), Reinforcement Learning (agents maximizing reward signals).",
                                "2. Agents & Environments: PEAS framework (Performance measure, Environment, Actuators, Sensors). Environments can be deterministic vs. stochastic, static vs. dynamic.",
                                "3. Search Algorithms: BFS, DFS, and heuristic search (A*) for pathfinding and state-space exploration.",
                                "4. Responsible AI: Fairness, accountability, interpretability, and privacy-preserving data usage."
                            ],
                            "code_examples": [
                                {
                                    "title": "Rule-Based vs. Probabilistic Decision Agent",
                                    "code": "def simple_ai_agent(sensor_data: dict) -> str:\n    temperature = sensor_data.get('temperature', 22)\n    occupancy = sensor_data.get('occupancy', False)\n    \n    if occupancy and temperature > 26:\n        return 'COOLING_ACTIVE'\n    elif occupancy and temperature < 18:\n        return 'HEATING_ACTIVE'\n    return 'STANDBY'\n\nprint(simple_ai_agent({'temperature': 28, 'occupancy': True}))",
                                    "explanation": "Illustrates a reactive agent mapping perceptual inputs to discrete actions."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: PEAS Specification",
                                    "instructions": "Draft the PEAS specification (Performance, Environment, Actuators, Sensors) for an autonomous campus delivery robot."
                                }
                            ],
                            "documentation": [
                                {"title": "Russell & Norvig AI Modern Approach Companion", "url": "https://aima.cs.berkeley.edu/"}
                            ],
                            "curated_videos": [
                                {"title": "AI for Everyone by Andrew Ng", "url": "https://www.youtube.com/watch?v=0h9V6JqD784"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: State-Space Pathfinding Agent",
                                "steps": [
                                    "Represent a 5x5 grid map with obstacles and a goal coordinate",
                                    "Implement Breadth-First Search (BFS) to discover the shortest path",
                                    "Print step-by-step agent traversal"
                                ],
                                "expected_outcome": "A BFS state-space search algorithm demonstrating goal-directed agent traversal."
                            },
                            "knowledge_check": {
                                "question": "Which learning paradigm relies on feedback from rewards and penalties received through interacting with an environment?",
                                "options": [
                                    "Reinforcement Learning",
                                    "Supervised Learning",
                                    "Unsupervised Clustering",
                                    "Self-Supervised Pretraining"
                                ],
                                "correct_answer": "Reinforcement Learning",
                                "explanation": "Reinforcement Learning trains agents via trial-and-error feedback based on reward and penalty signals."
                            }
                        }
                    },
                    {
                        "id": "ai_beg_prob_solving",
                        "module_title": "Basic Problem Solving",
                        "topic_title": "Basic Problem Solving",
                        "estimated_duration": "2.0 hours",
                        "learning_objectives": [
                            "Apply algorithmic decomposition and computational problem-solving strategies",
                            "Implement core searching and sorting algorithms (Binary Search, Two Pointers)",
                            "Analyze edge cases and write unit tests for verification",
                            "Optimize time and space efficiency of iterative solutions"
                        ],
                        "learning_materials": {
                            "lesson": "Algorithmic problem solving is the core capability that enables engineers to design efficient ML data pipelines and custom loss functions. This module trains your analytical thinking: decomposing complex tasks, selecting optimal data structures, and applying two-pointer and binary search paradigms.",
                            "step_by_step_explanation": [
                                "1. Problem Decomposition: Read constraints, identify inputs/outputs, trace small examples by hand, and consider boundary conditions.",
                                "2. Two-Pointer Technique: Useful for searching sorted arrays or processing string sequences in linear O(N) time.",
                                "3. Binary Search: Divide and conquer strategy reducing search space by half each iteration, achieving O(log N) time on sorted data.",
                                "4. Hash Maps: Using dictionaries to trade space for O(1) time complexity."
                            ],
                            "code_examples": [
                                {
                                    "title": "Binary Search Implementation in Python",
                                    "code": "def binary_search(arr: list[int], target: int) -> int:\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\nnumbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]\nprint('Index of 23:', binary_search(numbers, 23))",
                                    "explanation": "Shows divide-and-conquer binary search with clean pointer updates."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Two-Sum Solver",
                                    "instructions": "Given an array of integers and a target sum, return indices of the two numbers such that they add up to target in O(N) time using a dictionary."
                                }
                            ],
                            "documentation": [
                                {"title": "Python Time Complexity Wiki", "url": "https://wiki.python.org/moin/TimeComplexity"}
                            ],
                            "curated_videos": [
                                {"title": "Two Pointer & Binary Search Techniques", "url": "https://www.youtube.com/watch?v=On03HWe2tZM"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: Fast Deduplication & Anomaly Scanner",
                                "steps": [
                                    "Generate an unsorted dataset of 10,000 transaction values",
                                    "Identify duplicate entries and anomalies exceeding 3 standard deviations",
                                    "Benchmark runtime comparing O(N^2) brute force vs O(N) hash set approach"
                                ],
                                "expected_outcome": "Empirical runtime demonstration showing computational gains of optimal algorithms."
                            },
                            "knowledge_check": {
                                "question": "What is the worst-case time complexity of Binary Search on a sorted array of size N?",
                                "options": ["O(log N)", "O(N)", "O(1)", "O(N^2)"],
                                "correct_answer": "O(log N)",
                                "explanation": "Binary search divides the search space in half at every step, yielding logarithmic O(log N) time."
                            }
                        }
                    }
                ]
            },
            {
                "phase_id": "phase-2",
                "phase_number": 2,
                "name": "Intermediate Phase",
                "difficulty": "Intermediate",
                "description": "Tabular data engineering, data preprocessing pipelines, classic machine learning algorithms, model evaluation, and intermediate applied projects.",
                "passing_score": 80,
                "assessment_question_count": 10,
                "modules": [
                    {
                        "id": "ai_int_numpy_pandas",
                        "module_title": "NumPy and Pandas",
                        "topic_title": "NumPy and Pandas",
                        "estimated_duration": "3.0 hours",
                        "learning_objectives": [
                            "Perform vector and matrix broadcasting operations in NumPy",
                            "Load, filter, group, and aggregate structured datasets using Pandas DataFrames",
                            "Handle missing data, datetime conversions, and multi-index series",
                            "Optimize memory and speed with vectorized operations instead of Python loops"
                        ],
                        "learning_materials": {
                            "lesson": "NumPy and Pandas form the computational bedrock of modern data science and machine learning. NumPy brings C-speed contiguous memory buffers (ndarray) with SIMD vectorized operations. Pandas builds on NumPy to provide DataFrames with expressive relational queries, indexing, and data transformations.",
                            "step_by_step_explanation": [
                                "1. NumPy Arrays: Fast homogeneous numerical arrays. Broadcasting allows arithmetic between arrays of different shapes.",
                                "2. Pandas DataFrame: 2D labeled data structures with columns of potentially different types.",
                                "3. Indexing & Slicing: loc (label-based) and iloc (integer position-based) selection.",
                                "4. GroupBy Operations: Split-Apply-Combine workflow for aggregate statistics across categorical segments."
                            ],
                            "code_examples": [
                                {
                                    "title": "Pandas Data Aggregation & Feature Generation",
                                    "code": "import pandas as pd\nimport numpy as np\n\ndata = {\n    'student_id': ['S1', 'S2', 'S3', 'S4', 'S5'],\n    'domain': ['AI', 'Web', 'AI', 'Data', 'Web'],\n    'score': [85, 78, 92, 64, 88],\n    'study_hours': [12.5, 8.0, 15.0, 6.5, 10.0]\n}\ndf = pd.DataFrame(data)\n\n# Vectorized feature engineering\ndf['score_per_hour'] = np.round(df['score'] / df['study_hours'], 2)\n\n# Group summary\nsummary = df.groupby('domain')['score'].agg(['mean', 'max', 'count'])\nprint(summary)",
                                    "explanation": "Illustrates DataFrame creation, vectorized column derivation, and group-by aggregations."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Missing Value Imputation",
                                    "instructions": "Given a dataset with missing numerical values in 'salary', impute missing rows with the median salary of each specific 'job_role' group."
                                }
                            ],
                            "documentation": [
                                {"title": "Pandas Official Documentation", "url": "https://pandas.pydata.org/docs/"},
                                {"title": "NumPy User Guide", "url": "https://numpy.org/doc/stable/user/"}
                            ],
                            "curated_videos": [
                                {"title": "Pandas Complete Tutorial", "url": "https://www.youtube.com/watch?v=vmEHCJofslg"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: Student Academic Analytics Pipeline",
                                "steps": [
                                    "Load a raw CSV file containing 500 academic records",
                                    "Clean inconsistent strings, parse timestamps, and handle null records",
                                    "Produce an automated statistical summary report exporting to JSON"
                                ],
                                "expected_outcome": "An automated data wrangling script performing full tabular transformation."
                            },
                            "knowledge_check": {
                                "question": "In Pandas, which method selects rows and columns based strictly on integer position indexes?",
                                "options": ["iloc", "loc", "ix", "iat_label"],
                                "correct_answer": "iloc",
                                "explanation": "iloc performs integer-location based indexing, whereas loc uses labels."
                            }
                        }
                    },
                    {
                        "id": "ai_int_data_preprocess",
                        "module_title": "Data Preprocessing",
                        "topic_title": "Data Preprocessing",
                        "estimated_duration": "3.0 hours",
                        "learning_objectives": [
                            "Implement feature scaling: StandardScaler (Z-score) vs MinMaxScaler",
                            "Encode categorical features using One-Hot Encoding and Target Encoding",
                            "Detect and remediate outliers using IQR and Z-score methods",
                            "Construct scikit-learn ColumnTransformer pipelines to prevent data leakage"
                        ],
                        "learning_materials": {
                            "lesson": "Raw data is messy, incomplete, and non-numerical. Feeding un-preprocessed data into machine learning algorithms leads to training instability, data leakage, and degraded generalization. This module covers data hygiene, imputation, scaling, categorical encoding, and assembling leak-free scikit-learn Pipelines.",
                            "step_by_step_explanation": [
                                "1. Data Leakage Prevention: Always fit transformers on training data only; never fit on test or cross-validation sets.",
                                "2. Feature Scaling: Standardize features with zero mean and unit variance for distance-based and gradient-based algorithms.",
                                "3. Encoding: One-hot encode nominal variables with low cardinality; label encode ordinal features.",
                                "4. Pipelines: Chain preprocessing steps with estimators to ensure reproducibility and clean serialization."
                            ],
                            "code_examples": [
                                {
                                    "title": "Scikit-Learn Preprocessing Pipeline",
                                    "code": "from sklearn.pipeline import Pipeline\nfrom sklearn.compose import ColumnTransformer\nfrom sklearn.preprocessing import StandardScaler, OneHotEncoder\nfrom sklearn.impute import SimpleImputer\n\nnumeric_features = ['age', 'cgpa', 'study_hours']\nnumeric_transformer = Pipeline(steps=[\n    ('imputer', SimpleImputer(strategy='median')),\n    ('scaler', StandardScaler())\n])\n\ncategorical_features = ['degree', 'domain']\ncategorical_transformer = Pipeline(steps=[\n    ('imputer', SimpleImputer(strategy='most_frequent')),\n    ('onehot', OneHotEncoder(handle_unknown='ignore'))\n])\n\npreprocessor = ColumnTransformer(transformers=[\n    ('num', numeric_transformer, numeric_features),\n    ('cat', categorical_transformer, categorical_features)\n])\nprint('Preprocessor configured successfully!')",
                                    "explanation": "Constructs a robust multi-type ColumnTransformer handling both numeric scaling and categorical encoding safely."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Outlier Capper",
                                    "instructions": "Write an outlier capping function that calculates Q1 and Q3, and clips values beyond 1.5 * IQR to the upper and lower thresholds."
                                }
                            ],
                            "documentation": [
                                {"title": "Scikit-Learn Preprocessing Guide", "url": "https://scikit-learn.org/stable/modules/preprocessing.html"}
                            ],
                            "curated_videos": [
                                {"title": "Feature Engineering and Preprocessing", "url": "https://www.youtube.com/watch?v=0h9V6JqD784"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: End-to-End Dataset Ingestion Pipeline",
                                "steps": [
                                    "Ingest an uncleaned employee churn dataset",
                                    "Impute missing values, scale numeric distributions, and encode categorical labels",
                                    "Export the preprocessed training and test arrays along with the fitted pipeline object"
                                ],
                                "expected_outcome": "A reusable scikit-learn preprocessing pipeline serializable via joblib."
                            },
                            "knowledge_check": {
                                "question": "Why must feature scalers (like StandardScaler) be fit ONLY on the training dataset and not the test dataset?",
                                "options": [
                                    "To prevent data leakage from the test set influencing model training",
                                    "Because test datasets do not contain numerical values",
                                    "Because scikit-learn raises an error if test data is passed to fit",
                                    "To reduce the size of the serialized model file"
                                ],
                                "correct_answer": "To prevent data leakage from the test set influencing model training",
                                "explanation": "Fitting scalers on test data introduces data leakage, distorting real-world generalization performance."
                            }
                        }
                    },
                    {
                        "id": "ai_int_ml_fundamentals",
                        "module_title": "Machine Learning Fundamentals",
                        "topic_title": "Machine Learning Fundamentals",
                        "estimated_duration": "3.5 hours",
                        "learning_objectives": [
                            "Implement supervised learning algorithms: Linear Regression, Logistic Regression, Decision Trees, and Random Forests",
                            "Understand the bias-variance tradeoff and model regularization (L1 Lasso, L2 Ridge)",
                            "Formulate loss functions (MSE, Binary Cross-Entropy) and optimization via Gradient Descent",
                            "Train and cross-validate predictive models using Scikit-Learn"
                        ],
                        "learning_materials": {
                            "lesson": "Classical machine learning provides the baseline for predictive systems. Understanding linear formulations, decision boundary geometry, tree splitting criteria (Gini impurity, entropy), and ensemble aggregation allows you to choose the right model for tabular and structured business problems.",
                            "step_by_step_explanation": [
                                "1. Linear Models: Linear regression models continuous targets y = w^T x + b. Logistic regression maps linear outputs through a sigmoid function for probability classification.",
                                "2. Decision Trees: Non-parametric models that partition feature space into orthogonal hyper-rectangles using information gain or Gini impurity.",
                                "3. Ensembles: Random Forest trains multiple decorrelated trees via bagging (bootstrap aggregating) to drastically reduce variance.",
                                "4. Regularization: L1 Lasso forces sparse feature weights (feature selection); L2 Ridge shrinks weights to prevent overfitting."
                            ],
                            "code_examples": [
                                {
                                    "title": "Random Forest Classification Model",
                                    "code": "from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import make_classification\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\n\n# Generate synthetic employability dataset\nX, y = make_classification(n_samples=500, n_features=10, random_state=42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\nmodel = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)\nmodel.fit(X_train, y_train)\ny_pred = model.predict(X_test)\nprint(f'Test Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%')",
                                    "explanation": "Trains a Random Forest classifier with hyperparameter constraints to prevent overfitting."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Hyperparameter Tuning with GridSearch",
                                    "instructions": "Use GridSearchCV to find the optimal 'max_depth' and 'n_estimators' for a RandomForestClassifier evaluating with 5-fold stratified cross-validation."
                                }
                            ],
                            "documentation": [
                                {"title": "Scikit-Learn Supervised Learning Guide", "url": "https://scikit-learn.org/stable/supervised_learning.html"}
                            ],
                            "curated_videos": [
                                {"title": "StatQuest: Machine Learning Fundamentals", "url": "https://www.youtube.com/watch?v=Gv9_4yMHFhI"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: Employability Readiness Classifier",
                                "steps": [
                                    "Train multiple classifiers (Logistic Regression, Decision Tree, Random Forest) on candidate profiles",
                                    "Compare training vs test performance to evaluate overfitting",
                                    "Extract feature importance rankings to explain model predictions"
                                ],
                                "expected_outcome": "A trained ensemble classifier predicting candidate job-readiness with feature importance analysis."
                            },
                            "knowledge_check": {
                                "question": "What happens when a machine learning model exhibits High Variance?",
                                "options": [
                                    "It fits the training data too closely (overfitting) and generalizes poorly to unseen test data",
                                    "It underfits both training and test datasets due to overly simplistic assumptions",
                                    "It has too few parameters to capture the underlying pattern",
                                    "Its predictions are completely random and non-deterministic"
                                ],
                                "correct_answer": "It fits the training data too closely (overfitting) and generalizes poorly to unseen test data",
                                "explanation": "High variance corresponds to overfitting: the model captures noise in training data and fails to generalize."
                            }
                        }
                    },
                    {
                        "id": "ai_int_model_eval",
                        "module_title": "Model Evaluation",
                        "topic_title": "Model Evaluation",
                        "estimated_duration": "2.5 hours",
                        "learning_objectives": [
                            "Distinguish Accuracy, Precision, Recall, F1-Score, and ROC-AUC metrics",
                            "Interpret Confusion Matrices to diagnose False Positive and False Negative costs",
                            "Implement K-Fold Cross-Validation and Stratified K-Fold for reliable validation",
                            "Select appropriate metrics for imbalanced datasets"
                        ],
                        "learning_materials": {
                            "lesson": "Accuracy can be dangerously misleading when classes are imbalanced (e.g. 99% negative cases). Choosing the right evaluation metric depends on the cost of errors: in medical diagnosis or threat detection, Recall is critical (minimizing False Negatives); in spam filtering, Precision is prioritized (minimizing False Positives).",
                            "step_by_step_explanation": [
                                "1. Confusion Matrix: True Positive (TP), True Negative (TN), False Positive (FP), False Negative (FN).",
                                "2. Precision vs Recall: Precision = TP / (TP + FP). Recall = TP / (TP + FN).",
                                "3. F1-Score: Harmonic mean of Precision and Recall: 2 * (P * R) / (P + R).",
                                "4. ROC-AUC: Plots True Positive Rate vs False Positive Rate across all decision thresholds; AUC represents classification separability."
                            ],
                            "code_examples": [
                                {
                                    "title": "Comprehensive Classification Evaluation Report",
                                    "code": "from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score\n\ny_true = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]\ny_pred = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0]\ny_prob = [0.9, 0.1, 0.85, 0.45, 0.2, 0.8, 0.65, 0.15, 0.95, 0.05]\n\nprint('Classification Report:\\n', classification_report(y_true, y_pred))\nprint('ROC-AUC Score:', roc_auc_score(y_true, y_prob))\nprint('Confusion Matrix:\\n', confusion_matrix(y_true, y_pred))",
                                    "explanation": "Computes Precision, Recall, F1, ROC-AUC, and the 2x2 confusion matrix."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Precision-Recall Tradeoff Explorer",
                                    "instructions": "Vary classification thresholds between 0.1 and 0.9 on predicted probabilities, and plot the resulting Precision and Recall trajectory."
                                }
                            ],
                            "documentation": [
                                {"title": "Scikit-Learn Model Evaluation Guide", "url": "https://scikit-learn.org/stable/modules/model_evaluation.html"}
                            ],
                            "curated_videos": [
                                {"title": "ROC and AUC Explained (StatQuest)", "url": "https://www.youtube.com/watch?v=4jRBRDbJemM"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: Model Benchmark Suite",
                                "steps": [
                                    "Evaluate 3 baseline algorithms on an imbalanced classification problem",
                                    "Generate confusion matrix heatmaps and ROC curves",
                                    "Recommend the best production model with explicit rationale"
                                ],
                                "expected_outcome": "An evaluation script reporting Precision, Recall, and ROC-AUC comparisons."
                            },
                            "knowledge_check": {
                                "question": "In a cancer screening model, why is high Recall generally prioritized over high Precision?",
                                "options": [
                                    "Because failing to detect cancer (False Negative) has far more severe consequences than a false alarm",
                                    "Because Recall is always easier to compute than Precision",
                                    "Because High Recall guarantees that no healthy patient receives a false alarm",
                                    "Because Precision cannot be computed on binary targets"
                                ],
                                "correct_answer": "Because failing to detect cancer (False Negative) has far more severe consequences than a false alarm",
                                "explanation": "Recall measures the proportion of actual positive cases detected. Minimizing False Negatives is critical in high-stakes domains."
                            }
                        }
                    },
                    {
                        "id": "ai_int_inter_projects",
                        "module_title": "Intermediate Projects",
                        "topic_title": "Intermediate Projects",
                        "estimated_duration": "4.0 hours",
                        "learning_objectives": [
                            "Build an end-to-end tabular predictive project from raw data to model evaluation",
                            "Implement cross-validation, hyperparameter tuning, and error analysis",
                            "Package model artifacts using Joblib/Pickle",
                            "Structure project code with clean modules, CLI scripts, and documentation"
                        ],
                        "learning_materials": {
                            "lesson": "Real-world engineering requires synthesizing preprocessing, modeling, evaluation, and packaging into a cohesive codebase. This project guides you through building a complete ML pipeline: data ingestion, exploratory data analysis, feature engineering, model selection, hyperparameter tuning, and exporting production weights.",
                            "step_by_step_explanation": [
                                "1. Problem Framing: Define business metrics, inputs, targets, and evaluation criteria.",
                                "2. Pipeline Construction: Combine ColumnTransformer with ensemble models in a single Pipeline object.",
                                "3. Tuning: Execute RandomizedSearchCV or GridSearchCV with StratifiedKFold.",
                                "4. Artifact Serialization: Export the pipeline with joblib.dump() to enable instant zero-drift inference."
                            ],
                            "code_examples": [
                                {
                                    "title": "Complete Serialized Pipeline Workflow",
                                    "code": "import joblib\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.ensemble import GradientBoostingClassifier\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.datasets import make_classification\n\nX, y = make_classification(n_samples=200, n_features=5, random_state=42)\npipeline = Pipeline([\n    ('scaler', StandardScaler()),\n    ('model', GradientBoostingClassifier(n_estimators=50, random_state=42))\n])\npipeline.fit(X, y)\n\n# Save model pipeline for backend API serving\njoblib.dump(pipeline, 'model_pipeline.joblib')\nprint('Saved pipeline. Loading back for verification...')\nloaded = joblib.load('model_pipeline.joblib')\nprint('Prediction on sample:', loaded.predict(X[:1]))",
                                    "explanation": "Illustrates end-to-end training and serialization of a unified ML inference pipeline."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Error Analysis Breakdown",
                                    "instructions": "Inspect misclassified instances in your test set and identify which feature combinations contributed most to the errors."
                                }
                            ],
                            "documentation": [
                                {"title": "Model Persistence with Joblib", "url": "https://scikit-learn.org/stable/model_persistence.html"}
                            ],
                            "curated_videos": [
                                {"title": "Building Production ML Pipelines", "url": "https://www.youtube.com/watch?v=0GrciaGYzV0"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: Production Student Employability Risk Predictor",
                                "steps": [
                                    "Assemble full dataset with academic, skill, and assessment features",
                                    "Build and cross-validate an ensemble pipeline",
                                    "Export pipeline artifact and write an inference script with input schema validation"
                                ],
                                "expected_outcome": "A complete, standalone ML project directory with serialized artifact and prediction script."
                            },
                            "knowledge_check": {
                                "question": "What is the primary advantage of bundling preprocessing steps and estimators together in a scikit-learn Pipeline?",
                                "options": [
                                    "It guarantees the exact same preprocessing transforms are applied at inference without data leakage",
                                    "It compiles Python code directly into CUDA GPU kernels",
                                    "It eliminates the need for test datasets",
                                    "It automatically achieves 100% test accuracy"
                                ],
                                "correct_answer": "It guarantees the exact same preprocessing transforms are applied at inference without data leakage",
                                "explanation": "Pipelines eliminate training-serving skew by encapsulating transformations and estimators in a single atomic artifact."
                            }
                        }
                    }
                ]
            },
            {
                "phase_id": "phase-3",
                "phase_number": 3,
                "name": "Advanced Phase",
                "difficulty": "Advanced",
                "description": "Deep learning architectures, neural network training dynamics, modern computer vision/NLP, model deployment via FastAPI, and end-to-end capstone AI systems.",
                "passing_score": 80,
                "assessment_question_count": 10,
                "modules": [
                    {
                        "id": "ai_adv_deep_learning",
                        "module_title": "Deep Learning",
                        "topic_title": "Deep Learning",
                        "estimated_duration": "4.0 hours",
                        "learning_objectives": [
                            "Understand computational graph construction and automatic differentiation (Autograd)",
                            "Analyze activation functions: ReLU, LeakyReLU, GELU, and Sigmoid dynamics",
                            "Implement backpropagation and weight updates with Adam / SGD with momentum",
                            "Mitigate vanishing and exploding gradients with Batch Normalization and residual connections"
                        ],
                        "learning_materials": {
                            "lesson": "Deep learning models learn hierarchical representations through stacked non-linear transformations. Frameworks like PyTorch construct dynamic computational graphs where forward passes compute predictions and backward passes (reverse-mode automatic differentiation) compute partial derivatives of loss with respect to every learnable parameter.",
                            "step_by_step_explanation": [
                                "1. Tensors & Gradients: PyTorch tensors track computation history when requires_grad=True.",
                                "2. Activation Functions: Non-linearities enable networks to approximate complex continuous functions (Universal Approximation Theorem).",
                                "3. Optimization: Adam (Adaptive Moment Estimation) computes adaptive learning rates for each parameter using first and second moment moving averages.",
                                "4. Regularization: Dropout randomly deactivates neurons during training to prevent co-adaptation; Weight Decay penalizes large parameter magnitudes."
                            ],
                            "code_examples": [
                                {
                                    "title": "PyTorch Neural Layer Forward and Backward Pass",
                                    "code": "import torch\nimport torch.nn as nn\n\n# Multi-layer perceptron\nclass SimpleMLP(nn.Module):\n    def __init__(self, in_features=10, hidden=32, out_features=1):\n        super().__init__()\n        self.network = nn.Sequential(\n            nn.Linear(in_features, hidden),\n            nn.ReLU(),\n            nn.BatchNorm1d(hidden),\n            nn.Dropout(0.2),\n            nn.Linear(hidden, out_features)\n        )\n    def forward(self, x):\n        return self.network(x)\n\nmodel = SimpleMLP()\nx_sample = torch.randn(8, 10)\nout = model(x_sample)\nprint('Output Tensor Shape:', out.shape)",
                                    "explanation": "Constructs a PyTorch modular neural network with Linear layers, ReLU activation, BatchNorm, and Dropout."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Custom PyTorch Training Loop",
                                    "instructions": "Write an explicit training loop in PyTorch with optimizer.zero_grad(), loss.backward(), and optimizer.step() over 10 epochs."
                                }
                            ],
                            "documentation": [
                                {"title": "PyTorch Official Documentation & Tutorials", "url": "https://pytorch.org/tutorials/"}
                            ],
                            "curated_videos": [
                                {"title": "Neural Networks: Zero to Hero by Andrej Karpathy", "url": "https://www.youtube.com/watch?v=VMj-3S1tku0"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: PyTorch Multi-Class Classifier",
                                "steps": [
                                    "Construct a 3-layer neural network in PyTorch",
                                    "Train using CrossEntropyLoss and Adam optimizer on synthetic feature clusters",
                                    "Track loss curve trajectory and validation accuracy per epoch"
                                ],
                                "expected_outcome": "A fully functional PyTorch training script with modular dataset loaders and loss tracking."
                            },
                            "knowledge_check": {
                                "question": "Why is optimizer.zero_grad() called before loss.backward() in standard PyTorch training loops?",
                                "options": [
                                    "Because PyTorch accumulates gradients in tensor buffers by default on backward passes",
                                    "To reset model weights to initial random values",
                                    "To clear GPU VRAM memory caches",
                                    "To prevent loss calculation from overflowing"
                                ],
                                "correct_answer": "Because PyTorch accumulates gradients in tensor buffers by default on backward passes",
                                "explanation": "PyTorch accumulates gradients by default; calling zero_grad() prevents summing gradients across multiple batches."
                            }
                        }
                    },
                    {
                        "id": "ai_adv_neural_networks",
                        "module_title": "Neural Networks",
                        "topic_title": "Neural Networks",
                        "estimated_duration": "4.0 hours",
                        "learning_objectives": [
                            "Master Convolutional Neural Networks (CNNs): convolutions, kernels, stride, and pooling",
                            "Understand Sequence Models: Recurrent Neural Networks (RNNs) and LSTMs",
                            "Grasp Self-Attention mechanism and Transformer architecture (Multi-Head Attention)",
                            "Fine-tune pre-trained models using Transfer Learning"
                        ],
                        "learning_materials": {
                            "lesson": "Specialized neural architectures capture spatial and temporal structures efficiently. CNNs use weight sharing and translation invariance for image and signal processing. Transformers replace recurrent recurrence with self-attention mechanisms, computing all-to-all token relationships in parallel and powering modern Large Language Models.",
                            "step_by_step_explanation": [
                                "1. Convolutions: Sliding kernel matrices computing feature maps for edge, texture, and object detection.",
                                "2. Pooling: Downsamples spatial dimensions while preserving dominant activations.",
                                "3. Attention Mechanism: Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) * V.",
                                "4. Transfer Learning: Freezing foundational layers and fine-tuning head layers on domain-specific datasets."
                            ],
                            "code_examples": [
                                {
                                    "title": "Scaled Dot-Product Attention in Pure PyTorch",
                                    "code": "import torch\nimport torch.nn.functional as F\n\ndef scaled_dot_product_attention(Q, K, V):\n    d_k = Q.size(-1)\n    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)\n    attention_weights = F.softmax(scores, dim=-1)\n    output = torch.matmul(attention_weights, V)\n    return output, attention_weights\n\n# Batch=1, 4 tokens, embed_dim=8\nq = torch.randn(1, 4, 8)\nk = torch.randn(1, 4, 8)\nv = torch.randn(1, 4, 8)\nout, weights = scaled_dot_product_attention(q, k, v)\nprint('Attended Representation Shape:', out.shape)",
                                    "explanation": "Calculates the exact attention formulation of the seminal 'Attention Is All You Need' paper."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: CNN Feature Map Visualizer",
                                    "instructions": "Pass a sample 28x28 grayscale image tensor through an nn.Conv2d(1, 16, kernel_size=3) layer and inspect output activation shapes."
                                }
                            ],
                            "documentation": [
                                {"title": "The Illustrated Transformer by Jay Alammar", "url": "https://jalammar.github.io/illustrated-transformer/"}
                            ],
                            "curated_videos": [
                                {"title": "Transformers Explained by 3Blue1Brown", "url": "https://www.youtube.com/watch?v=wjZofJX0v4U"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: Image / Sequence Embedding Extractor",
                                "steps": [
                                    "Instantiate a pre-trained feature extractor (e.g. ResNet or Transformer encoder)",
                                    "Pass domain samples to extract dense semantic embedding vectors",
                                    "Calculate cosine similarity between query and candidate representations"
                                ],
                                "expected_outcome": "A semantic embedding generator with cosine similarity search."
                            },
                            "knowledge_check": {
                                "question": "In the self-attention formula Attention(Q, K, V), why is the dot product Q K^T divided by sqrt(d_k)?",
                                "options": [
                                    "To scale variance and prevent the softmax function from having extremely small gradients",
                                    "To invert the matrix for dimensional reduction",
                                    "To convert negative values into positive probabilities",
                                    "To speed up GPU matrix multiplication operations"
                                ],
                                "correct_answer": "To scale variance and prevent the softmax function from having extremely small gradients",
                                "explanation": "Scaling by sqrt(d_k) keeps the dot product magnitudes stable, preventing softmax from saturating into near-zero gradient regions."
                            }
                        }
                    },
                    {
                        "id": "ai_adv_advanced_ml",
                        "module_title": "Advanced Machine Learning",
                        "topic_title": "Advanced Machine Learning",
                        "estimated_duration": "3.5 hours",
                        "learning_objectives": [
                            "Implement Gradient Boosting algorithms (XGBoost, LightGBM, CatBoost)",
                            "Apply Explainable AI (XAI) techniques: SHAP (Shapley Additive exPlanations) and LIME",
                            "Formulate dimensionality reduction: PCA (Principal Component Analysis) and t-SNE",
                            "Handle extreme class imbalance using SMOTE and cost-sensitive loss weighting"
                        ],
                        "learning_materials": {
                            "lesson": "Modern AI engineering balances raw predictive accuracy with explainability, compliance, and latency. Gradient Boosted Decision Trees (XGBoost / LightGBM) remain the gold standard for tabular data. Pairing them with SHAP values provides game-theoretic feature attribution required in healthcare, finance, and employment guidance.",
                            "step_by_step_explanation": [
                                "1. Gradient Boosting: Builds trees iteratively where each tree predicts the pseudo-residuals of the previous ensemble.",
                                "2. SHAP Values: Based on Shapley values from cooperative game theory; assigns each feature an exact marginal contribution to a prediction.",
                                "3. Dimensionality Reduction: PCA computes orthogonal eigenvectors of the covariance matrix maximizing variance along primary components.",
                                "4. Cost-Sensitive Training: Penalizing minority-class errors proportionately to rectify distribution skew."
                            ],
                            "code_examples": [
                                {
                                    "title": "PCA Dimensionality Reduction & Reconstruction",
                                    "code": "import numpy as np\nfrom sklearn.decomposition import PCA\n\nX_high_dim = np.random.randn(100, 20)\npca = PCA(n_components=5)\nX_reduced = pca.fit_transform(X_high_dim)\n\nprint('Original Shape:', X_high_dim.shape)\nprint('Reduced Shape:', X_reduced.shape)\nprint('Explained Variance Ratio Sum:', np.sum(pca.explained_variance_ratio_))",
                                    "explanation": "Projects high-dimensional space down to principal orthogonal axes while measuring retained variance."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Model Explanation Audit",
                                    "instructions": "Given a trained model, calculate top-5 most impactful features for an individual rejected candidate and explain why the score was low."
                                }
                            ],
                            "documentation": [
                                {"title": "SHAP (SHapley Additive exPlanations) Documentation", "url": "https://shap.readthedocs.io/en/latest/"}
                            ],
                            "curated_videos": [
                                {"title": "XGBoost Algorithm Explained (StatQuest)", "url": "https://www.youtube.com/watch?v=OtD8wVxBQgE"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: Explainable AI Career Fit Decision Engine",
                                "steps": [
                                    "Train a gradient boosted model predicting career fit probability",
                                    "Compute global and local SHAP feature attributions",
                                    "Render a structured explanation report for candidate feedback"
                                ],
                                "expected_outcome": "An explainable AI pipeline that justifies its predictions with quantitative feature importance."
                            },
                            "knowledge_check": {
                                "question": "What is the key theoretical guarantee provided by SHAP values in Explainable AI?",
                                "options": [
                                    "Fair and consistent distribution of marginal feature contributions based on cooperative game theory",
                                    "Zero runtime inference latency on mobile devices",
                                    "100% elimination of all dataset bias",
                                    "Direct conversion of decision trees into linear regression equations"
                                ],
                                "correct_answer": "Fair and consistent distribution of marginal feature contributions based on cooperative game theory",
                                "explanation": "SHAP values uniquely satisfy efficiency, symmetry, dummy, and additivity properties from Shapley game theory."
                            }
                        }
                    },
                    {
                        "id": "ai_adv_model_deployment",
                        "module_title": "Model Deployment",
                        "topic_title": "Model Deployment",
                        "estimated_duration": "3.5 hours",
                        "learning_objectives": [
                            "Build asynchronous high-throughput REST APIs for ML inference using FastAPI",
                            "Validate incoming payload structures using Pydantic schemas",
                            "Implement model versioning, health checks, and error logging",
                            "Containerize applications with Docker and configure production Uvicorn workers"
                        ],
                        "learning_materials": {
                            "lesson": "An AI model provides zero business value until deployed into production. Serving models requires low latency, strict input validation, graceful degradation during load spikes, and comprehensive monitoring. FastAPI with Uvicorn provides an asynchronous ASGI foundation capable of serving thousands of predictions per second.",
                            "step_by_step_explanation": [
                                "1. ASGI Architecture: FastAPI uses asynchronous non-blocking event loops, preventing blocking during I/O and DB queries.",
                                "2. Pydantic Schemas: Automatic deserialization, type coercion, and validation with HTTP 422 errors for malformed requests.",
                                "3. Model Life-Cycle: Load weights once during application startup (FastAPI lifespan context manager) rather than per request.",
                                "4. Containerization: Docker packages runtime binaries, Python libraries, and model weights into reproducible lightweight containers."
                            ],
                            "code_examples": [
                                {
                                    "title": "Production FastAPI ML Inference Endpoint",
                                    "code": "from fastapi import FastAPI, HTTPException\nfrom pydantic import BaseModel, Field\nfrom typing import List\n\napp = FastAPI(title='ML Inference Service')\n\nclass CandidateInput(BaseModel):\n    gpa: float = Field(..., ge=0.0, le=10.0)\n    technical_score: int = Field(..., ge=0, le=100)\n    skills: List[str] = []\n\nclass PredictionResponse(BaseModel):\n    employability_score: float\n    status: str\n\n@app.post('/predict', response_model=PredictionResponse)\nasync def predict_employability(candidate: CandidateInput):\n    # Simulate model forward pass\n    base_score = (candidate.gpa * 7.0) + (candidate.technical_score * 0.3)\n    score = round(min(98.0, base_score), 2)\n    status = 'HIGH_READINESS' if score >= 80.0 else 'IN_DEVELOPMENT'\n    return PredictionResponse(employability_score=score, status=status)",
                                    "explanation": "Illustrates schema-validated asynchronous inference with boundaries and typed output."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Dockerfile Construction",
                                    "instructions": "Draft a multi-stage Dockerfile that installs dependencies, copies model artifacts, and runs uvicorn on port 8000."
                                }
                            ],
                            "documentation": [
                                {"title": "FastAPI Official Documentation", "url": "https://fastapi.tiangolo.com/"},
                                {"title": "Uvicorn ASGI Server Reference", "url": "https://www.uvicorn.org/"}
                            ],
                            "curated_videos": [
                                {"title": "Deploying Machine Learning Models with FastAPI", "url": "https://www.youtube.com/watch?v=h5wLuVDr0oc"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: Self-Contained Microservice with Health Metrics",
                                "steps": [
                                    "Create a FastAPI application with /health, /metadata, and /predict endpoints",
                                    "Include pydantic schema validation and request timing metrics in headers",
                                    "Write automated integration tests verifying response status codes"
                                ],
                                "expected_outcome": "A production-ready microservice with health checks, schema validation, and test suite."
                            },
                            "knowledge_check": {
                                "question": "Why should ML model weights be loaded in FastAPI's startup lifespan rather than inside the POST route handler?",
                                "options": [
                                    "Loading on startup occurs once in memory; loading inside the route handler re-reads the disk on every incoming HTTP request, causing severe latency",
                                    "Because route handlers cannot access global variables",
                                    "Because Pydantic only validates models loaded during startup",
                                    "To prevent Python from executing garbage collection"
                                ],
                                "correct_answer": "Loading on startup occurs once in memory; loading inside the route handler re-reads the disk on every incoming HTTP request, causing severe latency",
                                "explanation": "Preloading weights once at startup keeps the model resident in RAM/VRAM, achieving millisecond inference."
                            }
                        }
                    },
                    {
                        "id": "ai_adv_capstone_project",
                        "module_title": "End-to-End AI Project",
                        "topic_title": "End-to-End AI Project",
                        "estimated_duration": "5.0 hours",
                        "learning_objectives": [
                            "Integrate data preprocessing, deep neural training, model evaluation, and deployment",
                            "Implement logging, monitoring, and automated test suites",
                            "Document architecture, API contracts, and user guide for presentation",
                            "Demonstrate final-year engineering competency with production-grade code"
                        ],
                        "learning_materials": {
                            "lesson": "The capstone project represents the culmination of your engineering journey. It proves your ability to build complete AI systems: from raw multi-modal student records, through algorithmic feature engineering and neural modeling, to secure FastAPI endpoints, reactive frontend dashboards, and automated verification.",
                            "step_by_step_explanation": [
                                "1. Architecture Design: Plan frontend React views, FastAPI backend endpoints, and MongoDB schemas.",
                                "2. Pipeline Integration: Connect live student data to model scoring and recommendation engines.",
                                "3. Quality Assurance: Write unit and integration tests verifying progression locking, scoring rules, and error paths.",
                                "4. Portfolio Presentation: Package clean README documentation, architectural diagrams, and verified test results."
                            ],
                            "code_examples": [
                                {
                                    "title": "End-to-End Capstone Verification Script",
                                    "code": "# Automated sanity check of complete AI career pipeline\nimport requests\n\ndef verify_platform_status(base_url: str = 'http://127.0.0.1:8000'):\n    health = requests.get(f'{base_url}/api/v1/health').json()\n    print('Backend Health:', health)\n    assert health.get('status') == 'healthy', 'System unhealthy'\n    print('All core engines operational!')\n\n# verify_platform_status()",
                                    "explanation": "Illustrates programmatic validation of system status across microservices."
                                }
                            ],
                            "practical_exercises": [
                                {
                                    "title": "Exercise: Capstone System Architecture Diagram",
                                    "instructions": "Draft a full sequence diagram illustrating how a student submission moves through the FastAPI backend, evaluates answers, updates MongoDB, and renders real-time dashboard progress."
                                }
                            ],
                            "documentation": [
                                {"title": "12-Factor App Modern Engineering Guide", "url": "https://12factor.net/"}
                            ],
                            "curated_videos": [
                                {"title": "Final Year Engineering Project Presentation Best Practices", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
                            ],
                            "mini_project": {
                                "title": "Mini-Project: Capstone System Integration",
                                "steps": [
                                    "Connect frontend roadmap components with backend level-locking APIs",
                                    "Verify 80% passing rule across Beginner, Intermediate, and Advanced assessments",
                                    "Document execution instructions and test case validation logs"
                                ],
                                "expected_outcome": "A complete, fully verified AI career intelligence and employability platform."
                            },
                            "knowledge_check": {
                                "question": "What is the primary indicator of a successful engineering capstone project?",
                                "options": [
                                    "A reliable, fully integrated full-stack application with real database persistence, verified test cases, and clear documentation",
                                    "Having the largest number of lines of uncommented code",
                                    "Using only frontend simulated animations without backend verification",
                                    "Copying code without understanding its operational architecture"
                                ],
                                "correct_answer": "A reliable, fully integrated full-stack application with real database persistence, verified test cases, and clear documentation",
                                "explanation": "Engineering excellence requires full-stack coherence, verifiable functionality, secure persistence, and maintainable architecture."
                            }
                        }
                    }
                ]
            }
        ]
    }
}

# Add alias fallbacks for Web Development and Data Science
def get_career_curriculum(career_id: str = "ai-engineer") -> Dict[str, Any]:
    norm_id = career_id.lower().replace(" ", "-").replace("_", "-")
    if norm_id in CAREER_CURRICULUMS:
        return CAREER_CURRICULUMS[norm_id]
    
    # Check if we have an AI or Data or Web match
    for k in CAREER_CURRICULUMS:
        if k in norm_id or norm_id in k:
            return CAREER_CURRICULUMS[k]
            
    # Default to AI Engineer if unknown
    return CAREER_CURRICULUMS["ai-engineer"]
