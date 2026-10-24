"""
Master Curriculum Definition for the 7 Core Skills across 3 Progressive Levels.
Supports Python, Machine Learning, Mathematics, Problem Solving, Git and GitHub, SQL, and Communication.
"""
from typing import Dict, List, Any

CURRICULUM: Dict[str, Dict[str, Any]] = {
    "python": {
        "skill": "Python",
        "skill_slug": "python",
        "category": "Technical",
        "icon": "Code2",
        "description": "High-level programming language essential for Artificial Intelligence, Data Science, and Backend Automation.",
        "levels": [
            {
                "level": 1,
                "title": "Level 1 \u2013 Beginner",
                "difficulty": "Beginner",
                "estimated_hours": "18 hours",
                "description": "Foundational programming concepts, syntax, core collections, functions, and fundamental problem-solving in Python.",
                "learning_objectives": [
                    "Master core Python syntax, variables, and primitive data types",
                    "Construct decision logic using conditionals and loops",
                    "Organize data using Lists, Tuples, Sets, and Dictionaries",
                    "Write reusable, modular functions with parameters and return values",
                    "Handle runtime exceptions safely using try/except blocks"
                ],
                "topics": [
                    [
                        "Introduction to Python and installation",
                        "1 hour",
                        "Overview of Python's interpreted architecture, PEP8 conventions, and setting up the environment.",
                        "import sys\nprint('Python Version:', sys.version)",
                        "Write a Python script that prints 'Hello, AI Career Platform!' and your Python runtime version.",
                        "Use print() and sys.version"
                    ],
                    [
                        "Variables and naming rules",
                        "1 hour",
                        "Python variable assignments, dynamic typing, and snake_case naming conventions.",
                        "student_name = 'Alex'\nage = 21\ngpa = 3.85\nprint(f'{student_name} (Age: {age}, GPA: {gpa})')",
                        "Declare variables for candidate name, career target, and graduation year with valid PEP8 names.",
                        "Variables cannot start with numbers or hyphens"
                    ],
                    [
                        "Data types",
                        "1.5 hours",
                        "Primitive types: int, float, str, bool, and type checking mechanisms.",
                        "x, y, z = 42, 3.14, 'AI'\nprint(type(x), type(y), type(z))",
                        "Create variables of all 4 primitive types and verify their types using type().",
                        "Use type() to verify each type"
                    ],
                    [
                        "Type conversion",
                        "1 hour",
                        "Explicit vs implicit casting between numbers, strings, and booleans.",
                        "raw_score = '88'\nnumeric_score = int(raw_score)\nprint('Normalized:', numeric_score / 100)",
                        "Convert a string '99.5' into float, then cast it to integer.",
                        "float() first, then int()"
                    ],
                    [
                        "Input and output",
                        "1 hour",
                        "Standard user input parsing and formatted output using f-strings.",
                        "career = input('Target Career: ')\nprint(f'Path locked for: {career.strip().title()}')",
                        "Prompt user for daily study hours and calculate their weekly study total.",
                        "input() returns string; cast to float/int"
                    ],
                    [
                        "Operators",
                        "1.5 hours",
                        "Arithmetic, comparison, logical, assignment, and membership operators.",
                        "score = 85\npassed = (score >= 70) and not (score > 100)\nprint('Qualified:', passed)",
                        "Evaluate an expression checking if GPA >= 3.5 and attendance >= 80%.",
                        "Combine comparison with logical and"
                    ],
                    [
                        "Conditional statements",
                        "1.5 hours",
                        "Branching logic with if, elif, and else statements.",
                        "score = 82\nif score >= 90: grade = 'A'\nelif score >= 75: grade = 'B'\nelse: grade = 'C'\nprint('Grade:', grade)",
                        "Write a grade classifier returning 'Distinction', 'Pass', or 'Needs Improvement'.",
                        "Check highest score boundaries first"
                    ],
                    [
                        "For and while loops",
                        "2 hours",
                        "Iterating over sequences, range generators, break, continue, and loop else.",
                        "for i in range(1, 6):\n    if i == 3: continue\n    print('Step:', i)",
                        "Write a while loop calculating the factorial of a positive integer N.",
                        "Multiply and decrement N"
                    ],
                    [
                        "Strings and string methods",
                        "1.5 hours",
                        "Slicing, formatting, casing, splitting, joining, and search methods.",
                        "msg = '  python machine learning  '\nclean = msg.strip().title()\nprint(clean) # Python Machine Learning",
                        "Count occurrences of vowels in a given input sentence.",
                        "Use lower() and check membership in 'aeiou'"
                    ],
                    [
                        "Lists, tuples, sets, and dictionaries",
                        "2 hours",
                        "Sequence containers, mutability vs immutability, unique sets, and key-value maps.",
                        "skills = ['Python', 'SQL', 'Git']\nskills.append('ML')\nprofile = {'name': 'Sam', 'skills': tuple(skills)}\nprint(profile)",
                        "Create a student dictionary mapping subjects to scores and calculate the average score.",
                        "Use sum(scores) / len(scores)"
                    ],
                    [
                        "Functions and parameters",
                        "1.5 hours",
                        "Positional, keyword, default parameters, and variable argument unpacking.",
                        "def calculate_fit(score, weight=1.0):\n    return round(score * weight, 2)\nprint(calculate_fit(85, 0.85))",
                        "Define a function that takes *skills and returns a sorted list of unique skills.",
                        "Use set() and sorted()"
                    ],
                    [
                        "Basic exception handling",
                        "1 hour",
                        "Defensive programming with try, except, else, and finally.",
                        "try:\n    val = int('invalid')\nexcept ValueError as err:\n    print('Safely caught error:', err)",
                        "Wrap division of two numbers in try/except ZeroDivisionError and ValueError.",
                        "Catch specific exceptions"
                    ],
                    [
                        "Basic coding problems",
                        "1.5 hours",
                        "Palindromes, fizzbuzz, fibonacci, and list reversal algorithms.",
                        "def is_palindrome(s: str) -> bool:\n    clean = ''.join(c.lower() for c in s if c.isalnum())\n    return clean == clean[::-1]\nprint(is_palindrome('Radar'))",
                        "Solve FizzBuzz for numbers 1 to 50 returning a list of results.",
                        "Check % 15 == 0 before % 3 and % 5"
                    ]
                ]
            },
            {
                "level": 2,
                "title": "Level 2 \u2013 Intermediate",
                "difficulty": "Intermediate",
                "estimated_hours": "26 hours",
                "description": "Functional patterns, object-oriented architecture, modular development, API consumption, and unit testing.",
                "learning_objectives": [
                    "Implement functional programming paradigms using lambdas and comprehensions",
                    "Design robust object-oriented classes with encapsulation and inheritance",
                    "Manage files, JSON serialization, and external REST API integrations",
                    "Work with virtual environments and package dependency management",
                    "Write automated test assertions and debug runtime state"
                ],
                "topics": [
                    [
                        "Functions in depth",
                        "2 hours",
                        "First-class functions, closures, higher-order functions, and recursion.",
                        "def make_multiplier(n):\n    return lambda x: x * n\ntriple = make_multiplier(3)\nprint(triple(10)) # 30",
                        "Create a memoized recursive Fibonacci function using a dictionary closure.",
                        "Store computed results before recursive call"
                    ],
                    [
                        "Scope and namespaces",
                        "1.5 hours",
                        "LEGB rule (Local, Enclosing, Global, Built-in) and global/nonlocal keywords.",
                        "counter = 0\ndef increment():\n    global counter\n    counter += 1\nincrement()\nprint(counter)",
                        "Demonstrate nonlocal variable modification inside a nested helper function.",
                        "Declare nonlocal inside inner function"
                    ],
                    [
                        "Lambda, map, filter, and comprehensions",
                        "2 hours",
                        "Declarative data processing across iterables with list/dict/set comprehensions.",
                        "scores = [65, 82, 90, 45, 78]\npassed = [s for s in scores if s >= 70]\nprint(passed)",
                        "Transform a list of temperatures from Celsius to Fahrenheit using a comprehension.",
                        "Formula: (c * 9/5) + 32"
                    ],
                    [
                        "Modules and packages",
                        "1.5 hours",
                        "Module imports, __name__ == '__main__', sys.path, and package layout.",
                        "# file: math_utils.py\ndef add(a, b): return a + b\nif __name__ == '__main__':\n    print(add(2, 3))",
                        "Create a multi-file package structure with an __init__.py exposing top-level functions.",
                        "Use relative or package imports"
                    ],
                    [
                        "File handling",
                        "2 hours",
                        "Context-managed file I/O for text, CSV, and binary data.",
                        "with open('skills.txt', 'w') as f:\n    f.write('Python\\nSQL\\nGit\\n')\nwith open('skills.txt') as f:\n    print(f.readlines())",
                        "Read a CSV file of student records and return average scores per department.",
                        "Use csv.DictReader or split(',')"
                    ],
                    [
                        "Exception handling in depth",
                        "2 hours",
                        "Custom exception hierarchies, exception chaining (raise from), and traceback analysis.",
                        "class CareerException(Exception): pass\nclass InvalidScoreError(CareerException): pass\n# raise InvalidScoreError('Score > 100')",
                        "Create a custom DomainValidationError class with field and error code attributes.",
                        "Inherit from Exception"
                    ],
                    [
                        "Object-oriented programming",
                        "2.5 hours",
                        "Classes, __init__, instance attributes vs class attributes, and methods.",
                        "class Student:\n    school = 'Tech Academy'\n    def __init__(self, name, gpa):\n        self.name = name\n        self.gpa = gpa\ns = Student('Maya', 3.8)\nprint(s.school, s.name)",
                        "Build a Course class tracking enrolled students with capacity enforcement.",
                        "Check len(self.students) < self.capacity"
                    ],
                    [
                        "Classes, objects, inheritance, and polymorphism",
                        "2.5 hours",
                        "Subclassing, super() calls, method overriding, and polymorphic interfaces.",
                        "class Role:\n    def get_salary(self): return 0\nclass Engineer(Role):\n    def get_salary(self): return 95000\nprint(Engineer().get_salary())",
                        "Create a base Assessment class and specialized CodingAssessment and QuizAssessment subclasses.",
                        "Override evaluate() in each subclass"
                    ],
                    [
                        "Iterators and generators",
                        "2 hours",
                        "Iterator protocol (__iter__, __next__), yield statements, and infinite streams.",
                        "def countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\nprint(list(countdown(3))) # [3, 2, 1]",
                        "Implement a generator that streams batches of records from a large list.",
                        "Slice in step intervals and yield slices"
                    ],
                    [
                        "Virtual environments and pip",
                        "1.5 hours",
                        "Dependency isolation, venv creation, requirements.txt, and pip management.",
                        "# python -m venv .venv\n# source .venv/bin/activate (or .venv\\Scripts\\activate)\n# pip install -r requirements.txt",
                        "Generate a requirements.txt with pinned dependencies using pip freeze.",
                        "Pin versions with =="
                    ],
                    [
                        "Working with JSON and APIs",
                        "2.5 hours",
                        "json module serialization/deserialization and HTTP requests via urllib/requests.",
                        "import json\ndata = {'skill': 'Python', 'level': 2}\ns = json.dumps(data)\nloaded = json.loads(s)\nprint(loaded['skill'])",
                        "Fetch data from a public REST API or mock JSON string and extract nested attributes.",
                        "Use json.loads() and dictionary traversal"
                    ],
                    [
                        "Debugging and testing basics",
                        "2 hours",
                        "pdb breakpoint inspection, unittest/pytest frameworks, and test fixtures.",
                        "# def test_addition():\n#     assert 2 + 2 == 4",
                        "Write a test suite of 3 pytest functions verifying edge cases for a calculate_grade() helper.",
                        "Use assert and pytest.raises"
                    ],
                    [
                        "Intermediate coding problems",
                        "2.5 hours",
                        "Two-sum, anagram detection, string run-length compression, and stack evaluation.",
                        "def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen: return [seen[target - n], i]\n        seen[n] = i\nprint(two_sum([2, 7, 11, 15], 9))",
                        "Write a function that validates balanced parentheses, braces, and brackets in a string.",
                        "Use a stack container"
                    ]
                ]
            },
            {
                "level": 3,
                "title": "Level 3 \u2013 Advanced",
                "difficulty": "Advanced",
                "estimated_hours": "34 hours",
                "description": "High-performance architecture, metaprogramming, asynchronous concurrency, profiling, design patterns, and production deployment.",
                "learning_objectives": [
                    "Implement metaprogramming patterns using decorators, closures, and descriptors",
                    "Architect high-throughput concurrent systems with asyncio, threading, and multiprocessing",
                    "Optimize execution latency using cProfile, memory_profiler, and algorithmic tuning",
                    "Apply classical Gang of Four architectural design patterns in Python",
                    "Package, test, and release production-ready Python modules with CI pipelines"
                ],
                "topics": [
                    [
                        "Advanced object-oriented design",
                        "2.5 hours",
                        "Abstract Base Classes (abc), dunder methods (__call__, __enter__, __repr__), and descriptors.",
                        "from abc import ABC, abstractmethod\nclass Pipeline(ABC):\n    @abstractmethod\n    def run(self): pass",
                        "Implement a validation descriptor ensuring an attribute is always a positive integer.",
                        "Define __get__ and __set__ methods"
                    ],
                    [
                        "Decorators and closures",
                        "2.5 hours",
                        "Function and class decorators, parameterized decorators, functools.wraps, and stateful decorators.",
                        "import functools, time\ndef timer(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kw):\n        t0 = time.time()\n        res = func(*args, **kw)\n        print(f'{func.__name__} took {time.time()-t0:.4f}s')\n        return res\n    return wrapper",
                        "Build a @rate_limit decorator allowing at most N calls per second.",
                        "Track timestamps of past calls in a deque"
                    ],
                    [
                        "Context managers",
                        "2 hours",
                        "contextlib.contextmanager, __enter__ and __exit__ protocols, and resource management.",
                        "from contextlib import contextmanager\n@contextmanager\ndef temp_log():\n    print('Start')\n    try: yield\n    finally: print('End')",
                        "Create a class-based TimerContextManager measuring elapsed execution time.",
                        "Record time in __enter__ and difference in __exit__"
                    ],
                    [
                        "Advanced generators and iterators",
                        "2.5 hours",
                        "generator.send(), throw(), close(), and itertools combinations/permutations/groupby.",
                        "import itertools\nitems = [('A', 1), ('A', 2), ('B', 3)]\nfor k, g in itertools.groupby(items, key=lambda x: x[0]):\n    print(k, list(g))",
                        "Construct a streaming coroutine pipeline using generator send() to filter and aggregate records.",
                        "Prime the generator with next() before send()"
                    ],
                    [
                        "Type hints and advanced typing",
                        "2 hours",
                        "TypeVar, Generic, Protocol, Union, Optional, Literal, and static analysis with mypy.",
                        "from typing import Generic, TypeVar, List\nT = TypeVar('T')\nclass Stack(Generic[T]):\n    def __init__(self): self.items: List[T] = []\n    def push(self, item: T) -> None: self.items.append(item)",
                        "Define a runtime Protocol requiring a predict(x: list) -> float method.",
                        "Inherit from typing.Protocol"
                    ],
                    [
                        "Concurrency and parallelism",
                        "3 hours",
                        "Global Interpreter Lock (GIL) mechanics, CPU-bound vs I/O-bound bottlenecks.",
                        "# GIL allows only one native thread to execute Python bytecode at a time for CPU-bound tasks.\n# Multiprocessing bypasses GIL by spawning distinct OS processes.",
                        "Benchmark single-threaded vs multi-threaded execution for I/O operations.",
                        "Use concurrent.futures.ThreadPoolExecutor"
                    ],
                    [
                        "Threading, multiprocessing, and asynchronous programming",
                        "3.5 hours",
                        "asyncio event loop, async/await, Tasks, Gather, ThreadPoolExecutor, and ProcessPoolExecutor.",
                        "import asyncio\nasync def fetch(id):\n    await asyncio.sleep(0.1)\n    return f'Result {id}'\nasync def main():\n    res = await asyncio.gather(fetch(1), fetch(2))\n    print(res)",
                        "Write an async pipeline downloading 5 mock endpoints concurrently with asyncio.gather().",
                        "Use asyncio.gather(*[fetch(i) for i in range(5)])"
                    ],
                    [
                        "Advanced exception handling and logging",
                        "2.5 hours",
                        "Structured logging with logging module, rotating file handlers, formatters, and correlation IDs.",
                        "import logging\nlogging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')\nlogging.info('Pipeline initialized')",
                        "Configure a multi-handler logger writing DEBUG to file and WARNING to console.",
                        "Use StreamHandler and RotatingFileHandler"
                    ],
                    [
                        "Profiling and performance optimization",
                        "3 hours",
                        "cProfile, line_profiler, memory_profiler, timeit, and cython/numba JIT acceleration.",
                        "import cProfile\ndef expensive(): return sum(i**2 for i in range(100000))\ncProfile.run('expensive()')",
                        "Profile a search algorithm and optimize from O(n^2) to O(n) using a hash map.",
                        "Compare cProfile function call counts"
                    ],
                    [
                        "Design patterns in Python",
                        "3 hours",
                        "Creational (Singleton, Factory), Structural (Adapter, Decorator), and Behavioral (Observer, Strategy).",
                        "class StrategyA:\n    def execute(self): return 'Fast'\nclass Context:\n    def __init__(self, strat): self.strat = strat\n    def run(self): return self.strat.execute()",
                        "Implement the Observer pattern allowing listeners to subscribe to model training events.",
                        "Maintain a subscribers list and notify in loop"
                    ],
                    [
                        "Unit testing and test automation",
                        "2.5 hours",
                        "pytest fixtures, monkeypatching, mock objects (unittest.mock.patch), and test coverage.",
                        "from unittest.mock import Mock\nmock_api = Mock()\nmock_api.get_score.return_value = 95\nassert mock_api.get_score() == 95",
                        "Mock an external HTTP service in a unit test to verify failure recovery behavior.",
                        "Use unittest.mock.patch"
                    ],
                    [
                        "Building a reusable Python package",
                        "2.5 hours",
                        "pyproject.toml, setuptools, wheels, semantic versioning, and publishing to PyPI/private index.",
                        "# [build-system]\n# requires = ['setuptools>=61.0']\n# build-backend = 'setuptools.build_meta'",
                        "Write a complete pyproject.toml specification for a custom utility library.",
                        "Specify name, version, authors, and dependencies"
                    ],
                    [
                        "Production-oriented Python project",
                        "3.5 hours",
                        "Docker containerization, environment configuration (pydantic-settings), health checks, and graceful shutdown.",
                        "from pydantic_settings import BaseSettings\nclass Settings(BaseSettings):\n    ENV: str = 'production'\n    PORT: int = 8000",
                        "Create a production-ready application entrypoint with structured health check and graceful SIGTERM handling.",
                        "Catch signal.SIGTERM and clean up resources"
                    ]
                ]
            }
        ]
    },
    "machine-learning": {
        "skill": "Machine Learning",
        "skill_slug": "machine-learning",
        "category": "Technical",
        "icon": "Cpu",
        "description": "Mathematical models and statistical algorithms that learn patterns from empirical data to predict outcomes.",
        "levels": [
            {
                "level": 1,
                "title": "Level 1 \u2013 Beginner",
                "difficulty": "Beginner",
                "estimated_hours": "20 hours",
                "description": "Core paradigms of machine learning, dataset mechanics, tabular data wrangling with NumPy and Pandas, and foundational linear models.",
                "learning_objectives": [
                    "Distinguish supervised vs unsupervised machine learning paradigms",
                    "Clean, inspect, and manipulate tabular datasets with Pandas and NumPy",
                    "Split data into train, validation, and test partitions to prevent data leakage",
                    "Fit and evaluate simple Linear and Logistic regression models using scikit-learn",
                    "Compute foundational classification and regression performance metrics"
                ],
                "topics": [
                    [
                        "Introduction to Artificial Intelligence and Machine Learning",
                        "1 hour",
                        "Historical evolution, symbolic AI vs data-driven machine learning, and business impact.",
                        "# Machine learning learns a mapping f(X) -> y directly from historical examples.",
                        "Identify 3 enterprise machine learning applications and categorize their input features and targets.",
                        "Differentiate classification from regression"
                    ],
                    [
                        "AI vs ML vs Deep Learning",
                        "1 hour",
                        "Taxonomy of artificial intelligence, statistical machine learning, and multi-layer neural networks.",
                        "# AI (broadest) -> ML (data-driven models) -> DL (deep neural architectures)",
                        "Create a comparative table contrasting traditional ML (tabular) and Deep Learning (unstructured).",
                        "Focus on feature engineering vs feature representation"
                    ],
                    [
                        "Supervised and unsupervised learning",
                        "1.5 hours",
                        "Labeled training targets vs pattern discovery in unlabeled clusters.",
                        "# Supervised: labels present (y). Unsupervised: only feature matrix (X).",
                        "Classify 5 real-world scenarios into Supervised, Unsupervised, or Semi-supervised.",
                        "Look for target label presence"
                    ],
                    [
                        "Dataset, features, labels, and target variables",
                        "1 hour",
                        "Feature vectors, matrices, label vectors, and continuous vs categorical targets.",
                        "import numpy as np\nX = np.array([[21, 3.8], [22, 3.2]]) # Features: Age, GPA\ny = np.array([1, 0]) # Target: Hired",
                        "Design a feature matrix schema for predicting student career readiness.",
                        "Identify independent vs dependent variables"
                    ],
                    [
                        "Training, validation, and test datasets",
                        "1.5 hours",
                        "Data partitioning rationale, train_test_split, stratification, and test holdouts.",
                        "from sklearn.model_selection import train_test_split\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)",
                        "Write a train/validation/test split function using a 70/15/15 ratio.",
                        "Split twice: first 70/30, then 30 into 50/50"
                    ],
                    [
                        "Introduction to NumPy and Pandas",
                        "2 hours",
                        "Vectorized ndarrays, broadcasting, Series, DataFrames, indexing, and Boolean masking.",
                        "import pandas as pd\ndf = pd.DataFrame({'skill': ['Python', 'SQL'], 'score': [85, 92]})\nprint(df[df['score'] > 80])",
                        "Load a dataset and compute per-column summary statistics using df.describe().",
                        "Use pandas DataFrame methods"
                    ],
                    [
                        "Basic data cleaning",
                        "1.5 hours",
                        "Data type coercion, whitespace trimming, invalid records, and column renaming.",
                        "df['score'] = pd.to_numeric(df['score'], errors='coerce')\ndf.columns = [c.lower().strip() for c in df.columns]",
                        "Clean a dirty DataFrame containing irregular casing, currency symbols, and extra spaces.",
                        "Use str.replace() and to_numeric()"
                    ],
                    [
                        "Missing values and duplicate records",
                        "1.5 hours",
                        "Imputation strategies (mean, median, mode), dropna(), and drop_duplicates().",
                        "df.drop_duplicates(inplace=True)\ndf['score'] = df['score'].fillna(df['score'].median())",
                        "Identify missing values per column and impute numerical columns with median.",
                        "Check df.isnull().sum()"
                    ],
                    [
                        "Descriptive statistics",
                        "1.5 hours",
                        "Measures of central tendency (mean, median), dispersion (variance, std, IQR), and skewness.",
                        "print('Mean:', df['score'].mean(), 'Std:', df['score'].std())",
                        "Calculate mean, median, IQR, and 95th percentile for student test scores.",
                        "Use df.quantile([0.25, 0.75, 0.95])"
                    ],
                    [
                        "Introduction to scikit-learn",
                        "1.5 hours",
                        "Estimator API conventions: fit(), transform(), predict(), and score().",
                        "from sklearn.base import BaseEstimator\n# All scikit-learn models follow fit(X, y) and predict(X)",
                        "Instantiate a scikit-learn estimator, inspect its default hyperparameters, and check fit signature.",
                        "Review get_params()"
                    ],
                    [
                        "Linear regression",
                        "2 hours",
                        "Ordinary least squares, slope coefficients, intercept, and residual sum of squares.",
                        "from sklearn.linear_model import LinearRegression\nreg = LinearRegression().fit([[1], [2], [3]], [2, 4, 6])\nprint('Slope:', reg.coef_[0])",
                        "Train a LinearRegression model predicting salary from years of experience and print equation.",
                        "Equation: y = coef * X + intercept"
                    ],
                    [
                        "Logistic regression",
                        "2 hours",
                        "Sigmoid activation function, log-odds, decision boundaries, and binary classification.",
                        "from sklearn.linear_model import LogisticRegression\nclf = LogisticRegression().fit([[60], [80], [90]], [0, 1, 1])\nprint(clf.predict_proba([[75]]))",
                        "Fit LogisticRegression on student assessment scores to classify Pass (>=70) vs Fail.",
                        "Inspect predict_proba()"
                    ],
                    [
                        "Basic classification and regression metrics",
                        "1.5 hours",
                        "Accuracy, precision, recall, MAE, MSE, RMSE, and R-squared.",
                        "from sklearn.metrics import accuracy_score, mean_squared_error\n# accuracy = accuracy_score(y_true, y_pred)\n# rmse = mean_squared_error(y_true, y_pred, squared=False)",
                        "Compute MAE, RMSE, and R2 on test set predictions and interpret results.",
                        "RMSE penalizes large errors more than MAE"
                    ],
                    [
                        "Simple ML workflow",
                        "1.5 hours",
                        "End-to-end pipeline: problem definition, data loading, train/test split, model fitting, and evaluation.",
                        "# Load -> Clean -> Split -> Fit -> Predict -> Evaluate",
                        "Build an end-to-end script from raw CSV to evaluated baseline model with documented metrics.",
                        "Keep training and test data strictly separate"
                    ]
                ]
            },
            {
                "level": 2,
                "title": "Level 2 \u2013 Intermediate",
                "difficulty": "Intermediate",
                "estimated_hours": "30 hours",
                "description": "Feature engineering, classical non-linear classifiers, clustering, cross-validation, and diagnostic evaluation.",
                "learning_objectives": [
                    "Perform rigorous Exploratory Data Analysis and data preprocessing pipelines",
                    "Engineer features through encoding, scaling, and transformation",
                    "Train, tune, and evaluate Decision Trees, Random Forests, SVMs, and KNN",
                    "Diagnose overfitting, underfitting, and high bias vs high variance",
                    "Handle imbalanced classes and prevent data leakage during model selection"
                ],
                "topics": [
                    [
                        "Exploratory Data Analysis",
                        "2 hours",
                        "Bivariate distributions, correlation heatmaps, box plots, and outlier detection.",
                        "import seaborn as sns\n# sns.heatmap(df.corr(), annot=True, cmap='coolwarm')",
                        "Perform full EDA on a multi-feature dataset and identify top 3 predictive features.",
                        "Calculate Pearson correlation coefficients"
                    ],
                    [
                        "Data preprocessing pipelines",
                        "2 hours",
                        "sklearn.pipeline.Pipeline, ColumnTransformer, and combining imputers with scalers.",
                        "from sklearn.pipeline import Pipeline\nfrom sklearn.preprocessing import StandardScaler\npipe = Pipeline([('scaler', StandardScaler()), ('clf', LogisticRegression())])",
                        "Build a Pipeline with median imputation and standard scaling chained into a classifier.",
                        "Ensure transformations fit only on training data"
                    ],
                    [
                        "Feature encoding and scaling",
                        "1.5 hours",
                        "OneHotEncoder, OrdinalEncoder, StandardScaler, MinMaxScaler, and RobustScaler.",
                        "from sklearn.preprocessing import OneHotEncoder\nohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')",
                        "Encode nominal categorical variables and scale continuous features without data leakage.",
                        "Use handle_unknown='ignore' for robust inference"
                    ],
                    [
                        "Feature selection and feature engineering",
                        "2 hours",
                        "Interaction terms, polynomial features, SelectKBest, mutual info, and variance threshold.",
                        "from sklearn.feature_selection import SelectKBest, f_classif\nselector = SelectKBest(score_func=f_classif, k=5)",
                        "Create 2 interaction features and select top 5 features using mutual information.",
                        "Combine domain logic with statistical scoring"
                    ],
                    [
                        "Decision trees and random forests",
                        "2.5 hours",
                        "Information gain, Gini impurity, tree pruning, bagging ensemble, and out-of-bag error.",
                        "from sklearn.ensemble import RandomForestClassifier\nrf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)",
                        "Train a Random Forest, tune max_depth to prevent overfitting, and plot feature importances.",
                        "Inspect rf.feature_importances_"
                    ],
                    [
                        "K-Nearest Neighbors",
                        "1.5 hours",
                        "Distance metrics (Euclidean, Manhattan), curse of dimensionality, and finding optimal K.",
                        "from sklearn.neighbors import KNeighborsClassifier\nknn = KNeighborsClassifier(n_neighbors=5, metric='minkowski')",
                        "Tune KNN neighbor count K from 1 to 25 and plot validation accuracy curve.",
                        "Always scale features before KNN"
                    ],
                    [
                        "Support Vector Machines",
                        "2 hours",
                        "Hyperplanes, maximal margin classifiers, soft margin slack, and kernel trick (RBF, poly).",
                        "from sklearn.svm import SVC\nsvm = SVC(kernel='rbf', C=1.0, gamma='scale')",
                        "Compare linear SVM vs RBF kernel SVM on non-linearly separable data.",
                        "Tune C (regularization) and gamma (kernel width)"
                    ],
                    [
                        "Naive Bayes",
                        "1.5 hours",
                        "Bayes theorem, conditional independence assumption, Gaussian, Multinomial, and Bernoulli NB.",
                        "from sklearn.naive_bayes import GaussianNB\nnb = GaussianNB().fit(X_train, y_train)",
                        "Train a GaussianNB classifier for rapid baseline classification and evaluate inference speed.",
                        "Assumes independent feature distributions"
                    ],
                    [
                        "K-Means clustering",
                        "2 hours",
                        "Unsupervised centroid optimization, inertia, Elbow method, and silhouette score.",
                        "from sklearn.cluster import KMeans\nkmeans = KMeans(n_clusters=3, random_state=42).fit(X)",
                        "Determine optimal cluster count K on unlabeled data using the silhouette score.",
                        "Plot silhouette coefficient across K=2 to 8"
                    ],
                    [
                        "Cross-validation",
                        "2 hours",
                        "K-Fold, Stratified K-Fold, TimeSeriesSplit, and cross_val_score.",
                        "from sklearn.model_selection import cross_val_score, StratifiedKFold\nscores = cross_val_score(rf, X, y, cv=StratifiedKFold(n_splits=5))",
                        "Run 5-fold Stratified Cross-Validation and report mean score and standard error.",
                        "Stratification preserves class balance in folds"
                    ],
                    [
                        "Hyperparameter tuning",
                        "2 hours",
                        "GridSearchCV, RandomizedSearchCV, parameter distributions, and scoring metrics.",
                        "from sklearn.model_selection import GridSearchCV\ngrid = GridSearchCV(rf, {'max_depth': [3, 5, 8], 'n_estimators': [50, 100]}, cv=3)",
                        "Optimize Random Forest hyperparameters using GridSearchCV with F1-macro scoring.",
                        "GridSearchCV fits cv * combinations models"
                    ],
                    [
                        "Confusion matrix, precision, recall, and F1-score",
                        "1.5 hours",
                        "True positives, false positives, false negatives, precision-recall trade-off, and F1.",
                        "from sklearn.metrics import classification_report, confusion_matrix\nprint(classification_report(y_true, y_pred))",
                        "Generate a confusion matrix and calculate precision and recall manually from the matrix.",
                        "Precision = TP / (TP + FP); Recall = TP / (TP + FN)"
                    ],
                    [
                        "ROC-AUC and regression evaluation metrics",
                        "2 hours",
                        "Receiver Operating Characteristic curve, Area Under Curve, MAE, MSE, and MAPE.",
                        "from sklearn.metrics import roc_auc_score, roc_curve\nauc = roc_auc_score(y_true, y_prob)",
                        "Plot ROC curve for 2 competing models and compare their ROC-AUC scores.",
                        "Higher AUC indicates superior discrimination"
                    ],
                    [
                        "Overfitting and underfitting",
                        "1.5 hours",
                        "Model complexity vs generalization gap, training curves, and early stopping.",
                        "# Overfitting: low train error, high test error. Underfitting: high train error, high test error.",
                        "Plot learning curves across training set sizes to detect overfitting in a complex tree.",
                        "Use sklearn.model_selection.learning_curve"
                    ],
                    [
                        "Bias-variance trade-off",
                        "1.5 hours",
                        "Mathematical decomposition of expected prediction error: bias^2 + variance + noise.",
                        "# High bias = overly simple model. High variance = overly sensitive to training noise.",
                        "Diagram the bias-variance curve showing training vs validation error across model capacity.",
                        "Sweet spot minimizes validation error"
                    ],
                    [
                        "Data leakage and class imbalance",
                        "2 hours",
                        "Target leakage, temporal leakage, SMOTE, class weighting, and stratified sampling.",
                        "from sklearn.utils.class_weight import compute_class_weight\n# or LogisticRegression(class_weight='balanced')",
                        "Train a model on an imbalanced dataset (90/10) using class_weight='balanced' vs default.",
                        "Compare F1-scores rather than raw accuracy"
                    ],
                    [
                        "Model comparison and selection",
                        "2 hours",
                        "Systematic benchmarking of multiple algorithms using standardized evaluation metrics.",
                        "models = {'LR': LogisticRegression(), 'RF': RandomForestClassifier(), 'SVM': SVC()}\n# evaluate each on identical CV folds",
                        "Benchmark 4 algorithms on identical train/test splits and construct a summary comparison matrix.",
                        "Rank by CV mean score and standard deviation"
                    ]
                ]
            },
            {
                "level": 3,
                "title": "Level 3 \u2013 Advanced",
                "difficulty": "Advanced",
                "estimated_hours": "36 hours",
                "description": "Gradient boosting, Explainable AI, production ML pipelines, model monitoring, serialization, and deep learning fundamentals.",
                "learning_objectives": [
                    "Master gradient boosted decision trees (XGBoost, LightGBM, CatBoost)",
                    "Explain black-box model decisions using SHAP values and permutation importance",
                    "Build reproducible deployment pipelines with model serialization and FastAPI",
                    "Monitor production models for data drift, concept drift, and performance decay",
                    "Understand foundational artificial neural networks and deep representation learning"
                ],
                "topics": [
                    [
                        "Gradient boosting and ensemble learning",
                        "3 hours",
                        "Sequential boosting theory, residual fitting, learning rate shrinkage, and AdaBoost vs GBM.",
                        "from sklearn.ensemble import GradientBoostingClassifier\ngbm = GradientBoostingClassifier(learning_rate=0.05, n_estimators=150)",
                        "Train GradientBoostingClassifier with early stopping on validation deviance.",
                        "Tune learning_rate alongside n_estimators"
                    ],
                    [
                        "XGBoost or other boosting frameworks",
                        "3 hours",
                        "Second-order Taylor expansion loss, regularization (gamma, lambda), and histogram binning.",
                        "# import xgboost as xgb\n# model = xgb.XGBClassifier(n_estimators=200, learning_rate=0.05, max_depth=4)",
                        "Configure an XGBoost model with tree pruning parameters and evaluate against Random Forest.",
                        "Tune subsample and colsample_bytree"
                    ],
                    [
                        "Advanced feature engineering",
                        "2.5 hours",
                        "Target encoding with smoothing, cyclic date encodings (sin/cos), and text TF-IDF features.",
                        "import numpy as np\n# hour_sin = np.sin(2 * np.pi * df['hour'] / 24)\n# hour_cos = np.cos(2 * np.pi * df['hour'] / 24)",
                        "Encode cyclical timestamp features using sine and cosine transformations.",
                        "Preserves cyclical continuity across midnight"
                    ],
                    [
                        "Imbalanced learning techniques",
                        "2.5 hours",
                        "Synthetic Minority Over-sampling (SMOTE), Tomek Links, and focal loss mechanics.",
                        "# from imblearn.over_sampling import SMOTE\n# X_res, y_res = SMOTE(random_state=42).fit_resample(X_train, y_train)",
                        "Apply SMOTE only to training folds inside a cross-validation pipeline.",
                        "Never apply SMOTE to test or validation splits"
                    ],
                    [
                        "Explainable AI and feature importance",
                        "3 hours",
                        "SHAP (Shapley Additive exPlanations), TreeSHAP, summary plots, and LIME local surrogates.",
                        "# import shap\n# explainer = shap.TreeExplainer(model)\n# shap_values = explainer.shap_values(X_test)",
                        "Generate a SHAP summary plot and explain individual predictions for 2 contrastive test cases.",
                        "Shapley values sum to prediction minus base value"
                    ],
                    [
                        "Model calibration and threshold optimization",
                        "2.5 hours",
                        "Platt scaling, isotonic regression, reliability diagrams, and cost-sensitive threshold tuning.",
                        "from sklearn.calibration import CalibratedClassifierCV\ncalibrated = CalibratedClassifierCV(clf, method='sigmoid', cv=3)",
                        "Optimize the decision threshold of a classifier to maximize profit given false positive costs.",
                        "Sweep threshold from 0.0 to 1.0"
                    ],
                    [
                        "ML pipelines and reproducibility",
                        "2.5 hours",
                        "Deterministic random seeding, modular feature pipelines, and DVC data versioning.",
                        "# Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])",
                        "Construct an end-to-end reproducible scikit-learn Pipeline saved as a single self-contained artifact.",
                        "Bundle all transformers and estimator"
                    ],
                    [
                        "Model serialization and deployment",
                        "3 hours",
                        "joblib, pickle, ONNX runtime format, and wrapping models in FastAPI endpoints.",
                        "import joblib\njoblib.dump(pipe, 'model.joblib')\nloaded_pipe = joblib.load('model.joblib')",
                        "Build a FastAPI REST endpoint that loads a serialized pipeline and serves inference predictions.",
                        "Validate input payloads with Pydantic"
                    ],
                    [
                        "Model monitoring and data drift",
                        "2.5 hours",
                        "Covariate shift, prior probability shift, Kolmogorov-Smirnov test, and PSI (Population Stability Index).",
                        "# PSI = sum((actual% - expected%) * ln(actual% / expected%))",
                        "Calculate Population Stability Index (PSI) between training and production feature distributions.",
                        "PSI > 0.2 indicates significant drift"
                    ],
                    [
                        "Experiment tracking",
                        "2 hours",
                        "MLflow, Weights & Biases, logging parameters, metrics, artifacts, and model registries.",
                        "# mlflow.log_params(params)\n# mlflow.log_metric('val_f1', score)\n# mlflow.sklearn.log_model(model, 'model')",
                        "Set up experiment tracking logging parameters and test metrics for 3 hyperparameter runs.",
                        "Track git commit hash with each run"
                    ],
                    [
                        "Responsible AI, fairness, and privacy",
                        "2 hours",
                        "Disparate impact ratio, demographic parity, differential privacy, and model cards.",
                        "# Disparate Impact = P(Y=1 | Group A) / P(Y=1 | Group B)\n# Disparate impact < 0.8 violates the 80% rule.",
                        "Compute demographic parity difference between demographic subgroups on model predictions.",
                        "Evaluate false positive rate parity"
                    ],
                    [
                        "Introduction to neural networks and deep learning",
                        "3 hours",
                        "Perceptrons, multi-layer perceptrons, forward propagation, backpropagation, and loss functions.",
                        "# Output = activation(W * X + b)\n# Gradient descent updates: W = W - lr * dL/dW",
                        "Implement a 2-layer forward propagation pass using NumPy matrix operations.",
                        "Apply ReLU activation to hidden layer"
                    ],
                    [
                        "Model optimization and scalability",
                        "2.5 hours",
                        "Quantization, model pruning, batch inference optimization, and distributed training basics.",
                        "# Batching requests increases GPU/CPU vectorized utilization over single-item inference.",
                        "Benchmark single-item vs vectorized batch inference latency on 10,000 predictions.",
                        "Use time.perf_counter() to measure latency"
                    ],
                    [
                        "End-to-end ML project deployment",
                        "3.5 hours",
                        "Production architecture: CI/CD test automation, containerized inference image, and health checks.",
                        "# Dockerfile + FastAPI + Prometheus metrics + Pydantic validation",
                        "Package a complete ML scoring microservice with Dockerfile, health check, and test suite.",
                        "Include automated test verifying schema compliance"
                    ]
                ]
            }
        ]
    },
    "mathematics": {
        "skill": "Mathematics",
        "skill_slug": "mathematics",
        "category": "Foundational",
        "icon": "Calculator",
        "description": "Linear algebra, multivariable calculus, probability theory, and optimization foundations underpinning machine learning.",
        "levels": [
            {
                "level": 1,
                "title": "Level 1 \u2013 Beginner",
                "difficulty": "Beginner",
                "estimated_hours": "16 hours",
                "description": "Core algebraic concepts, functional relationships, coordinate geometry, introductory probability, and statistical summaries.",
                "learning_objectives": [
                    "Manipulate powers, roots, logarithms, and algebraic equations fluently",
                    "Graph and analyze linear functions, slopes, and coordinate geometry",
                    "Compute statistical measures: mean, median, mode, range, and variance",
                    "Apply fundamental set theory operations and summation notation",
                    "Calculate basic discrete event probabilities and compound chances"
                ],
                "topics": [
                    [
                        "Basic arithmetic",
                        "1 hour",
                        "Order of operations (PEMDAS), signed numbers, absolute values, and estimation.",
                        "# -3 * (4 - 7) + 2 = -3 * (-3) + 2 = 9 + 2 = 11",
                        "Evaluate arithmetic operations with parentheses and powers following strict order of operations.",
                        "Perform operations inside parentheses first"
                    ],
                    [
                        "Fractions, percentages, and ratios",
                        "1 hour",
                        "Simplifying fractions, decimal equivalents, percentage change, and proportions.",
                        "# Growth = (New - Old) / Old * 100",
                        "Compute the percentage increase in accuracy from 72% to 90%.",
                        "Percentage increase = (18 / 72) * 100 = 25%"
                    ],
                    [
                        "Powers, roots, and logarithms",
                        "1.5 hours",
                        "Exponent laws, radical expressions, logarithmic identities, and base e (natural log).",
                        "# log_b(x * y) = log_b(x) + log_b(y)\n# ln(e^x) = x",
                        "Solve for x: e^(2x) = 100 using natural logarithms.",
                        "Take natural log of both sides: 2x = ln(100)"
                    ],
                    [
                        "Algebraic expressions",
                        "1 hour",
                        "Polynomial expansion, factoring quadratics, and simplifying rational expressions.",
                        "# (a + b)^2 = a^2 + 2ab + b^2",
                        "Factor the quadratic expression: x^2 - 5x + 6 = 0.",
                        "Factors: (x - 2)(x - 3)"
                    ],
                    [
                        "Linear equations",
                        "1.5 hours",
                        "Single and multivariable linear equations, substitution, and elimination.",
                        "# y = mx + c; Slope m = (y2 - y1) / (x2 - x1)",
                        "Find the slope and y-intercept of the line passing through (2, 3) and (6, 11).",
                        "Slope = (11 - 3)/(6 - 2) = 8/4 = 2"
                    ],
                    [
                        "Functions and graphs",
                        "1.5 hours",
                        "Domain, range, function mapping, monotonicity, and asymptotic behavior.",
                        "# f: X -> Y; Sigmoid f(x) = 1 / (1 + e^-x)",
                        "Plot and evaluate the sigmoid activation function for x in [-5, 0, 5].",
                        "At x=0, sigmoid(0) = 0.5"
                    ],
                    [
                        "Basic coordinate geometry",
                        "1 hour",
                        "Euclidean distance, midpoint formula, and geometric representations in R2.",
                        "# d = sqrt((x2 - x1)^2 + (y2 - y1)^2)",
                        "Compute the Euclidean distance between points (1, 2) and (4, 6).",
                        "sqrt(3^2 + 4^2) = sqrt(25) = 5"
                    ],
                    [
                        "Mean, median, and mode",
                        "1 hour",
                        "Central tendency calculation and identifying resistance to extreme values.",
                        "# Median is robust to extreme outliers; Mean is sensitive.",
                        "Calculate mean, median, and mode for: [4, 7, 7, 8, 12, 100].",
                        "Notice how 100 inflates the mean but not median"
                    ],
                    [
                        "Range and variance introduction",
                        "1.5 hours",
                        "Spread of data, sample vs population variance, and standard deviation.",
                        "# Var(X) = sum((x_i - mean)^2) / (N - 1)",
                        "Compute the sample variance of [2, 4, 4, 4, 5, 5, 7, 9].",
                        "Compute mean first, then average squared deviations"
                    ],
                    [
                        "Basic probability",
                        "1.5 hours",
                        "Sample spaces, event probability P(A), complement rule, and independent events.",
                        "# P(A U B) = P(A) + P(B) - P(A n B)",
                        "Find the probability of rolling a sum >= 10 using two fair six-sided dice.",
                        "Favorable pairs: (4,6),(5,5),(5,6),(6,4),(6,5),(6,6) -> 6/36 = 1/6"
                    ],
                    [
                        "Basic set theory",
                        "1 hour",
                        "Union, intersection, set difference, Cartesian products, and Venn diagrams.",
                        "# A n B = elements in both A and B\n# A U B = elements in either A or B",
                        "Given set A={1,2,3,4} and B={3,4,5,6}, compute A union B and A intersect B.",
                        "Union has 6 elements; Intersect has {3, 4}"
                    ],
                    [
                        "Summation notation",
                        "1.5 hours",
                        "Sigma notation rules, indexing, expanding series, and double summations.",
                        "# Sum(i, i=1..N) = N*(N+1)/2",
                        "Evaluate the sum of (2i - 1) for i = 1 to 5.",
                        "Sum = 1 + 3 + 5 + 7 + 9 = 25 (which is 5^2)"
                    ]
                ]
            },
            {
                "level": 2,
                "title": "Level 2 \u2013 Intermediate",
                "difficulty": "Intermediate",
                "estimated_hours": "25 hours",
                "description": "Linear algebra, matrix operations, differential calculus, probability distributions, and gradient descent mechanics.",
                "learning_objectives": [
                    "Perform matrix and vector operations, dot products, and transformations",
                    "Solve systems of linear equations using Gaussian elimination and inverses",
                    "Calculate analytical derivatives and partial derivatives of loss functions",
                    "Analyze probability distributions (Gaussian, Binomial) and Bayes' theorem",
                    "Understand gradient descent step updates and rate of convergence"
                ],
                "topics": [
                    [
                        "Matrices and matrix operations",
                        "2 hours",
                        "Matrix addition, scalar multiplication, transposition, and matrix dimensions.",
                        "import numpy as np\nA = np.array([[1, 2], [3, 4]])\nprint(A.T) # Transpose",
                        "Given matrix A (3x2) and B (3x2), compute 2A - B.",
                        "Element-wise operations require identical shapes"
                    ],
                    [
                        "Vectors and vector operations",
                        "1.5 hours",
                        "Vector addition, norm (L1, L2 norm), unit vectors, and orthogonal projections.",
                        "v = np.array([3, 4])\nl2_norm = np.linalg.norm(v) # 5.0",
                        "Compute L1 norm and L2 norm of vector [-3, 4, 0].",
                        "L1 norm = |-3| + 4 + 0 = 7; L2 norm = sqrt(9 + 16) = 5"
                    ],
                    [
                        "Systems of linear equations",
                        "2 hours",
                        "Ax = b representations, augmented matrices, row reduction, and unique vs infinite solutions.",
                        "# Ax = b -> x = inv(A) * b",
                        "Solve the 2x2 system: 2x + y = 8 and x - y = 1 using substitution or elimination.",
                        "Add equations: 3x = 9 -> x = 3, y = 2"
                    ],
                    [
                        "Linear algebra fundamentals",
                        "2 hours",
                        "Linear combinations, span, linear independence, and basis vectors.",
                        "# Vectors are linearly independent if c1*v1 + c2*v2 = 0 implies c1=c2=0.",
                        "Determine whether [1, 2] and [2, 4] are linearly independent.",
                        "[2, 4] = 2 * [1, 2], hence linearly dependent"
                    ],
                    [
                        "Dot products and matrix multiplication",
                        "2 hours",
                        "Inner product, geometric angle cos(theta), and matrix product row-column dotting.",
                        "A = np.array([[1, 2], [3, 4]])\nB = np.array([[5, 6], [7, 8]])\nC = np.dot(A, B)",
                        "Multiply a 2x3 matrix by a 3x2 matrix and confirm resulting shape (2x2).",
                        "(m x k) * (k x n) = (m x n)"
                    ],
                    [
                        "Functions and transformations",
                        "1.5 hours",
                        "Linear maps, rotation matrices, scaling matrices, and affine transformations.",
                        "# T(x) = A * x + b",
                        "Apply a 2D scaling matrix diag(2, 3) to vector [4, 5].",
                        "Result: [2*4, 3*5] = [8, 15]"
                    ],
                    [
                        "Derivatives and differentiation",
                        "2 hours",
                        "Limit definition, power rule, product rule, quotient rule, and chain rule.",
                        "# d/dx (x^3 - 4x + 7) = 3x^2 - 4",
                        "Find the derivative of f(x) = (3x^2 + 1)^4 using the chain rule.",
                        "f'(x) = 4*(3x^2 + 1)^3 * (6x) = 24x*(3x^2 + 1)^3"
                    ],
                    [
                        "Partial derivatives introduction",
                        "2 hours",
                        "Multivariable functions, treating other variables as constants, and gradient vector del f.",
                        "# f(x, y) = x^2 * y + 3y\n# df/dx = 2xy; df/dy = x^2 + 3",
                        "Compute partial derivatives with respect to w and b for Loss = (y - (w*x + b))^2.",
                        "dLoss/dw = -2x*(y - (wx + b)); dLoss/db = -2*(y - (wx + b))"
                    ],
                    [
                        "Descriptive statistics in depth",
                        "1.5 hours",
                        "Moments of distributions, skewness, kurtosis, and Chebyshev's inequality.",
                        "# Skewness measures asymmetry; Kurtosis measures tail heaviness.",
                        "Explain how a positive skew affects the relationship between mean, median, and mode.",
                        "In right-skewed data: Mean > Median > Mode"
                    ],
                    [
                        "Probability distributions",
                        "2 hours",
                        "Probability Density Functions, Cumulative Distribution Functions, Normal and Bernoulli distributions.",
                        "# Standard Normal Z ~ N(0, 1); 68-95-99.7 empirical rule",
                        "Calculate the Z-score for a score of 85 given mean 70 and standard deviation 10.",
                        "Z = (85 - 70) / 10 = 1.5"
                    ],
                    [
                        "Conditional probability and Bayes' theorem",
                        "2 hours",
                        "P(A|B) = P(B|A) * P(A) / P(B), prior, likelihood, and posterior calculation.",
                        "# P(Spam | Word) = P(Word | Spam) * P(Spam) / P(Word)",
                        "Compute posterior probability of disease given positive test result.",
                        "Apply Bayes rule with false positive rates"
                    ],
                    [
                        "Sampling and statistical inference basics",
                        "1.5 hours",
                        "Central Limit Theorem, standard error of the mean, and confidence intervals introduction.",
                        "# SE = sigma / sqrt(n)",
                        "Compute standard error for sample size 100 with population standard deviation 15.",
                        "SE = 15 / sqrt(100) = 1.5"
                    ],
                    [
                        "Correlation and covariance",
                        "1.5 hours",
                        "Cov(X, Y) = E[(X - mu_x)(Y - mu_y)], Pearson r, and Spearman rank correlation.",
                        "# r = Cov(X, Y) / (sigma_x * sigma_y); Bounds: [-1, 1]",
                        "Interpret a correlation coefficient of r = -0.82 between study hours and error rate.",
                        "Strong negative linear association"
                    ],
                    [
                        "Gradient descent fundamentals",
                        "2 hours",
                        "Objective function minimization, gradient vector direction, learning rate alpha, and step updates.",
                        "# theta_new = theta_old - alpha * grad_L(theta)",
                        "Perform 2 manual iterations of gradient descent for f(x) = x^2 with alpha=0.1 starting at x=5.",
                        "Step 1: x = 5 - 0.1*(10) = 4. Step 2: x = 4 - 0.1*(8) = 3.2"
                    ]
                ]
            },
            {
                "level": 3,
                "title": "Level 3 \u2013 Advanced",
                "difficulty": "Advanced",
                "estimated_hours": "32 hours",
                "description": "Spectral theory, matrix factorizations, multivariable optimization, statistical hypothesis testing, and loss landscape geometry.",
                "learning_objectives": [
                    "Compute eigenvalues, eigenvectors, SVD, and PCA projection mathematics",
                    "Optimize multivariable loss surfaces using Hessian matrices and Taylor approximations",
                    "Estimate statistical parameters using Maximum Likelihood Estimation (MLE)",
                    "Conduct rigorous hypothesis tests (t-tests, ANOVA, Chi-Square) and confidence intervals",
                    "Derive mathematical foundations of regularized regression (L1 Lasso, L2 Ridge)"
                ],
                "topics": [
                    [
                        "Eigenvalues and eigenvectors",
                        "2.5 hours",
                        "Characteristic polynomial det(A - lambda*I) = 0, eigenspaces, and geometric stretching.",
                        "# A * v = lambda * v",
                        "Find eigenvalues for 2x2 matrix [[2, 1], [1, 2]].",
                        "det([[2-l, 1], [1, 2-l]]) = (2-l)^2 - 1 = 0 -> l = 3, l = 1"
                    ],
                    [
                        "Matrix decompositions",
                        "3 hours",
                        "Eigendecomposition (PDP^-1), Singular Value Decomposition (U Sigma V^T), and Cholesky.",
                        "# SVD: Any real matrix A (m x n) = U (m x m) * Sigma (m x n) * V^T (n x n)",
                        "Deconstruct Principal Component Analysis into SVD on mean-centered data.",
                        "Principal directions are right singular vectors V"
                    ],
                    [
                        "Vector spaces and linear transformations",
                        "2 hours",
                        "Subspaces, null space (kernel), column space (range), and rank-nullity theorem.",
                        "# Dim(Col(A)) + Dim(Null(A)) = n (number of columns)",
                        "Find the basis and dimension of the null space of a rank-1 3x3 matrix.",
                        "Rank 1 means nullity = 3 - 1 = 2"
                    ],
                    [
                        "Multivariable calculus",
                        "2.5 hours",
                        "Directional derivatives, gradient vectors, tangent hyperplanes, and Jacobian matrix.",
                        "# Jacobian J_ij = df_i / dx_j",
                        "Compute the Jacobian matrix for vector function F(x, y) = [x^2 + y, 3x - y^2].",
                        "J = [[2x, 1], [3, -2y]]"
                    ],
                    [
                        "Gradients and optimization",
                        "2.5 hours",
                        "Hessian matrix of second partials, convexity, saddle points, and Taylor expansions.",
                        "# Hessian H_ij = d^2 f / (dx_i dx_j); Convex if H is positive semi-definite.",
                        "Determine if critical point (0, 0) of f(x, y) = x^2 - y^2 is a local min, max, or saddle point.",
                        "Hessian has eigenvalues +2 and -2 (indefinite) -> saddle point"
                    ],
                    [
                        "Chain rule and its ML applications",
                        "2.5 hours",
                        "Multivariable chain rule, computational graphs, and backpropagation gradient flow.",
                        "# dL/dx = (dL/dy) * (dy/dx)",
                        "Trace backpropagation gradient flow through a computational graph node z = f(x, y).",
                        "Accumulate gradients along all incoming pathways"
                    ],
                    [
                        "Advanced probability distributions",
                        "2.5 hours",
                        "Multivariate Gaussian distribution, covariance matrix Sigma, Poisson, and exponential distributions.",
                        "# f(x) = (2*pi)^(-k/2) * |Sigma|^(-1/2) * exp(-0.5 * (x-mu)^T * Sigma^-1 * (x-mu))",
                        "Calculate the Mahalanobis distance between a sample vector and population mean.",
                        "d = sqrt((x - mu)^T * inv(Sigma) * (x - mu))"
                    ],
                    [
                        "Maximum likelihood estimation",
                        "3 hours",
                        "Likelihood function L(theta), log-likelihood log L(theta), and score equations.",
                        "# argmax_theta sum(log P(x_i | theta))",
                        "Derive the MLE estimator for the mean mu of a normal distribution with known variance.",
                        "d/d_mu sum((x_i - mu)^2) = 0 -> mu_mle = mean(x)"
                    ],
                    [
                        "Hypothesis testing",
                        "2.5 hours",
                        "Null vs alternative hypothesis, Type I & Type II errors, p-values, t-test, and z-test.",
                        "# p-value: probability of observing result at least as extreme under H0.",
                        "Perform a two-sample t-test to determine if a new model significantly outperforms baseline.",
                        "Reject H0 if p-value < alpha (e.g. 0.05)"
                    ],
                    [
                        "Confidence intervals",
                        "2 hours",
                        "Margin of error, critical values (z*, t*), and coverage probability interpretation.",
                        "# CI = x_bar +- z* * (sigma / sqrt(n))",
                        "Construct a 95% confidence interval for model accuracy across 500 test samples.",
                        "Use z* = 1.96 for 95% confidence"
                    ],
                    [
                        "Regularization mathematics",
                        "2.5 hours",
                        "L1 norm (Lasso, sparsity geometry) vs L2 norm (Ridge, spherical shrinkage).",
                        "# L2 Ridge: min ||y - Xw||^2 + lambda * ||w||_2^2\n# L1 Lasso: min ||y - Xw||^2 + lambda * ||w||_1",
                        "Explain geometrically why L1 regularization produces sparse feature weights with exact zeros.",
                        "Contour lines of loss meet diamond corners on axes"
                    ],
                    [
                        "Optimization methods",
                        "3 hours",
                        "Newton-Raphson, stochastic gradient descent (SGD), momentum, AdaGrad, RMSprop, and Adam.",
                        "# Adam combines first moment (momentum) and second moment (RMSprop).",
                        "Write updating equations for Gradient Descent with Momentum and compare to standard SGD.",
                        "v_t = beta * v_{t-1} + (1 - beta) * grad; w_t = w_{t-1} - lr * v_t"
                    ],
                    [
                        "Mathematical foundations of ML algorithms",
                        "2.5 hours",
                        "Convex duality, Lagrange multipliers, Support Vector Machine maximal margin derivation.",
                        "# L(w, b, alpha) = 0.5 * ||w||^2 - sum(alpha_i * [y_i(w^T x_i + b) - 1])",
                        "Formulate the primal and dual optimization problems for soft-margin SVM.",
                        "KKT conditions ensure complementary slackness"
                    ]
                ]
            }
        ]
    },
    "problem-solving": {
        "skill": "Problem Solving",
        "skill_slug": "problem-solving",
        "category": "Foundational",
        "icon": "Brain",
        "description": "Algorithmic thinking, data structure selection, computational complexity analysis, and systematic problem decomposition.",
        "levels": [
            {
                "level": 1,
                "title": "Level 1 \u2013 Beginner",
                "difficulty": "Beginner",
                "estimated_hours": "18 hours",
                "description": "Problem decomposition, input/output boundary analysis, algorithm step formulation, flowcharts, and dry runs.",
                "learning_objectives": [
                    "Dissect complex problem statements into explicit inputs, outputs, and constraints",
                    "Design stepwise algorithms and flowcharts before writing source code",
                    "Conduct manual execution trace dry runs on test cases and edge boundaries",
                    "Solve foundational number, array, and string algorithmic tasks",
                    "Analyze basic time complexity and operational step growth"
                ],
                "topics": [
                    [
                        "Understanding problem statements",
                        "1 hour",
                        "Deconstructing requirements, identifying constraints, edge cases, and expected outputs.",
                        "# Identify: Inputs (types, ranges), Outputs, Edge Cases (empty, negatives, extremes).",
                        "Extract input constraints and corner cases from an ambiguous problem prompt.",
                        "Ask: What if input is empty, null, or huge?"
                    ],
                    [
                        "Identifying inputs and outputs",
                        "1 hour",
                        "Specifying input contracts, return types, error conditions, and idempotent properties.",
                        "# Contract: find_max(arr: List[int]) -> Optional[int]",
                        "Define full type signatures and boundary constraints for 3 problem statements.",
                        "Clarify behavior for empty collections"
                    ],
                    [
                        "Breaking problems into smaller steps",
                        "1.5 hours",
                        "Divide and conquer, subproblem isolation, and compositional function decomposition.",
                        "# Problem: Calculate student rank -> Step 1: Filter, Step 2: Sum, Step 3: Sort, Step 4: Assign.",
                        "Break down a string anagram grouping problem into 4 discrete subproblems.",
                        "Decompose into: normalize, sort key, hash map collect, return values"
                    ],
                    [
                        "Algorithms and pseudocode",
                        "1.5 hours",
                        "Writing structured, language-independent pseudocode with clear control flow.",
                        "// Algorithm: Binary Search\n// WHILE low <= high:\n//    mid = (low + high) / 2",
                        "Write formal pseudocode for finding the second largest unique number in an array.",
                        "Maintain first_max and second_max variables"
                    ],
                    [
                        "Flowcharts",
                        "1 hour",
                        "Standard flowchart notation: terminals, decision diamonds, processes, and I/O rhombuses.",
                        "# Oval (Start/End) -> Diamond (Decision: x > 0?) -> Rectangle (Process) -> Parallelogram (I/O)",
                        "Draw/design a flowchart for user login credential verification with 3 attempt limits.",
                        "Track retry counter and decision branch"
                    ],
                    [
                        "Variables and operators in problem-solving",
                        "1.5 hours",
                        "State tracking, accumulators, sentinel values, and Boolean flags.",
                        "# has_found = False; accumulator = 0",
                        "Trace an accumulator loop tracking running minimum, maximum, and average.",
                        "Initialize min to +infinity and max to -infinity"
                    ],
                    [
                        "Conditional logic",
                        "1.5 hours",
                        "Compound Boolean predicates, truth tables, short-circuit evaluation, and guard clauses.",
                        "# if not valid(x): return None # Early exit guard clause",
                        "Refactor 4 levels of nested if-else statements into clean early-return guard clauses.",
                        "Handle edge cases and invalid states first"
                    ],
                    [
                        "Loops and patterns",
                        "2 hours",
                        "Nested loops, triangle and pyramid patterns, matrix traversal, and invariant properties.",
                        "for i in range(1, 5):\n    print('*' * i)",
                        "Write nested loops generating a symmetric diamond pattern of asterisks.",
                        "First loop increments rows, second decrements"
                    ],
                    [
                        "Basic number problems",
                        "1.5 hours",
                        "Prime checking, GCD (Euclidean algorithm), LCM, digit extraction, and Armstrong numbers.",
                        "def is_prime(n):\n    if n < 2: return False\n    return all(n % i != 0 for i in range(2, int(n**0.5) + 1))",
                        "Implement the Euclidean algorithm to compute Greatest Common Divisor GCD(a, b).",
                        "While b != 0: a, b = b, a % b"
                    ],
                    [
                        "Basic string problems",
                        "1.5 hours",
                        "String reversal, palindrome verification, anagram checking, and character counting.",
                        "def are_anagrams(s1, s2):\n    return sorted(s1.lower()) == sorted(s2.lower())",
                        "Count the frequency of each word in a paragraph ignoring punctuation and case.",
                        "Use regex or strip punctuation before counting"
                    ],
                    [
                        "Basic array problems",
                        "1.5 hours",
                        "Linear scan, running sum, finding missing number in 1..N, and rotating arrays.",
                        "def missing_number(nums):\n    n = len(nums)\n    return (n * (n + 1)) // 2 - sum(nums)",
                        "Find the only element that appears once in an array where all other elements appear twice.",
                        "XOR all elements together: a ^ a = 0"
                    ],
                    [
                        "Manual dry runs",
                        "1.5 hours",
                        "Tracing state variable changes row by row across iteration cycles.",
                        "# Trace Table: Step | i | sum | arr[i] | Condition",
                        "Construct a complete trace table for a selection sort pass on [5, 2, 8, 1].",
                        "Log variable values at each loop iteration"
                    ],
                    [
                        "Introduction to time complexity",
                        "1 hour",
                        "Big-O notation, constant O(1), linear O(n), quadratic O(n^2), and counting operations.",
                        "# O(1) < O(log n) < O(n) < O(n log n) < O(n^2)",
                        "Determine Big-O time and space complexity for 3 contrasting search functions.",
                        "Count dominant loop iterations relative to input size N"
                    ]
                ]
            },
            {
                "level": 2,
                "title": "Level 2 \u2013 Intermediate",
                "difficulty": "Intermediate",
                "estimated_hours": "28 hours",
                "description": "Two pointers, sliding window, recursion, binary search, stacks, queues, linked lists, and tree traversals.",
                "learning_objectives": [
                    "Apply two-pointer and sliding-window techniques to linear data structures",
                    "Implement divide-and-conquer binary search algorithms with boundary conditions",
                    "Master recursive formulations and stack-based problem solving",
                    "Navigate non-linear tree structures using BFS and DFS traversals",
                    "Evaluate rigorous asymptotic time and space complexity trade-offs"
                ],
                "topics": [
                    [
                        "Arrays and strings in depth",
                        "2 hours",
                        "Dynamic arrays, amortized resizing, memory locality, and in-place transformations.",
                        "# Amortized O(1) append: doubling array capacity when full.",
                        "Rotate an array of size N to the right by K steps in O(n) time and O(1) space.",
                        "Reverse full array, then reverse first k, then reverse remaining"
                    ],
                    [
                        "Searching and sorting algorithms",
                        "2.5 hours",
                        "Merge sort, Quick sort, insertion sort, stability, and comparison sort lower bounds.",
                        "# Merge sort: O(n log n) guaranteed, stable, O(n) auxiliary space.",
                        "Implement Merge Sort recursively and trace its split and merge recursion tree.",
                        "Base case: len(arr) <= 1"
                    ],
                    [
                        "Two-pointer technique",
                        "2 hours",
                        "Opposite-end pointers, same-direction slow-fast pointers, and partition passes.",
                        "def reverse_vowels(s):\n    l, r = 0, len(s) - 1 # Pointers move toward center",
                        "Solve 3Sum problem (find all unique triplets summing to 0) using sorting and two pointers.",
                        "Sort array first, fix one element, use two pointers for remaining two"
                    ],
                    [
                        "Sliding-window technique",
                        "2 hours",
                        "Fixed-size windows, dynamic-size variable windows, and substring frequency tracking.",
                        "# Dynamic window expands right pointer, shrinks left pointer when condition violated.",
                        "Find the length of the longest substring without repeating characters.",
                        "Track last seen indices in a hash map"
                    ],
                    [
                        "Hash maps and hash sets",
                        "2 hours",
                        "Hash functions, collision resolution (chaining, open addressing), load factor, and O(1) lookups.",
                        "# Lookups, insertions, and deletions are O(1) average time.",
                        "Implement an LRU Cache skeleton using a Hash Map combined with a Doubly Linked List.",
                        "Map keys to Doubly Linked List nodes"
                    ],
                    [
                        "Recursion",
                        "2 hours",
                        "Call stack execution frames, base cases, recurrence relations, and recursion tree visualization.",
                        "def factorial(n):\n    if n <= 1: return 1 # Base case\n    return n * factorial(n - 1)",
                        "Write a recursive function generating all subsets (the power set) of a set of unique numbers.",
                        "At each index, choose to either include or exclude the element"
                    ],
                    [
                        "Stack and queue",
                        "2 hours",
                        "LIFO stack mechanics, FIFO queue mechanics, monotonic stacks, and circular buffers.",
                        "# Monotonic stack maintains elements in strictly increasing or decreasing order.",
                        "Solve the Daily Temperatures problem (find days until warmer temperature) using a monotonic stack.",
                        "Store indices on the stack"
                    ],
                    [
                        "Linked lists",
                        "2 hours",
                        "Singly linked, doubly linked, sentinel dummy heads, and fast/slow pointer cycle detection.",
                        "class Node:\n    def __init__(self, val, next=None):\n        self.val = val; self.next = next",
                        "Reverse a singly linked list iteratively in O(n) time and O(1) space.",
                        "Track prev, curr, and next_node"
                    ],
                    [
                        "Binary search",
                        "2 hours",
                        "Sorted array lookups, lower bound, upper bound, and binary search on answer space.",
                        "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2",
                        "Implement search in a rotated sorted array in O(log n) time.",
                        "Identify which half (left or right) is sorted at each mid"
                    ],
                    [
                        "Prefix sums",
                        "1.5 hours",
                        "Cumulative sum arrays, O(1) range sum queries, and 2D prefix sum matrices.",
                        "prefix = [0] + list(itertools.accumulate(nums))\n# Range sum [L, R] = prefix[R+1] - prefix[L]",
                        "Find the total count of contiguous subarrays whose elements sum up to target K.",
                        "Use a hash map storing prefix sum frequencies"
                    ],
                    [
                        "Greedy algorithms",
                        "2 hours",
                        "Greedy choice property, optimal substructure, interval scheduling, and fractional knapsack.",
                        "# Activity Selection: sort intervals by finish time and greedily select compatible intervals.",
                        "Solve the Gas Station circular tour problem using a single-pass greedy algorithm.",
                        "If total gas >= total cost, a valid starting index is guaranteed"
                    ],
                    [
                        "Trees and binary trees",
                        "2 hours",
                        "Binary search trees, tree height, maximum depth, and diameter.",
                        "# BST invariant: left < node < right",
                        "Verify whether a given binary tree satisfies the Binary Search Tree property.",
                        "Pass down (min_val, max_val) valid ranges"
                    ],
                    [
                        "Breadth-first search and depth-first search",
                        "2.5 hours",
                        "Queue-based level-order BFS, stack/recursive DFS (preorder, inorder, postorder).",
                        "from collections import deque\n# queue.append(root); while queue: node = queue.popleft()",
                        "Implement Level Order Traversal of a Binary Tree returning nodes grouped by depth level.",
                        "Process queue level-by-level using len(queue)"
                    ],
                    [
                        "Time and space complexity analysis",
                        "1.5 hours",
                        "Master theorem, recursion tree analysis, amortized analysis, and auxiliary vs total space.",
                        "# T(n) = 2T(n/2) + O(n) -> O(n log n) by Master Theorem case 2.",
                        "Derive the exact Big-O time and space complexity for QuickSelect algorithm.",
                        "Average O(n), Worst case O(n^2)"
                    ]
                ]
            },
            {
                "level": 3,
                "title": "Level 3 \u2013 Advanced",
                "difficulty": "Advanced",
                "estimated_hours": "36 hours",
                "description": "Dynamic programming, graph theory, advanced data structures, backtracking, bit manipulation, and competitive optimization.",
                "learning_objectives": [
                    "Design optimal memoized and bottom-up Dynamic Programming state transitions",
                    "Execute complex graph traversals (Dijkstra, Bellman-Ford, Kruskal, Topological Sort)",
                    "Implement advanced data structures including Tries, Heaps, and Segment Trees",
                    "Apply bit manipulation techniques to optimize computational space and speed",
                    "Solve competitive programming and engineering interview challenges under time constraints"
                ],
                "topics": [
                    [
                        "Graph algorithms",
                        "3 hours",
                        "Adjacency list representations, directed vs undirected, cycle detection, and bipartite verification.",
                        "graph = {0: [1, 2], 1: [2], 2: [0, 3], 3: [3]} # Adjacency list",
                        "Detect a cycle in a directed graph using 3-color DFS (White, Gray, Black).",
                        "Gray node encounter indicates back-edge cycle"
                    ],
                    [
                        "Dynamic programming",
                        "3.5 hours",
                        "Optimal substructure, overlapping subproblems, memoization vs tabulation, and state transitions.",
                        "# dp[i] = min(dp[i - c] + 1 for c in coins)",
                        "Solve the 0/1 Knapsack problem with weights and values using a 1D space-optimized DP array.",
                        "Iterate weights backwards to prevent duplicate use"
                    ],
                    [
                        "Backtracking",
                        "2.5 hours",
                        "Constraint satisfaction, search tree pruning, N-Queens, Sudoku solver, and permutations.",
                        "# explore(path) -> if goal: save -> for choice: make, explore, undo",
                        "Solve the N-Queens problem on an N x N chessboard returning all valid queen placements.",
                        "Track occupied columns and diagonal sets"
                    ],
                    [
                        "Advanced tree problems",
                        "2.5 hours",
                        "Lowest Common Ancestor (LCA), binary tree maximum path sum, and tree serialization.",
                        "# LCA in BST vs general Binary Tree",
                        "Find the maximum path sum between any two nodes in a binary tree.",
                        "At each node calculate max single-arm path to pass up"
                    ],
                    [
                        "Shortest-path algorithms",
                        "3 hours",
                        "Dijkstra's algorithm (priority queue), Bellman-Ford (negative weights), and Floyd-Warshall.",
                        "import heapq\n# heapq.heappush(pq, (0, start_node))",
                        "Implement Dijkstra's shortest path algorithm using a min-heap priority queue.",
                        "Relax distance edges: dist[v] = min(dist[v], dist[u] + weight)"
                    ],
                    [
                        "Minimum spanning trees",
                        "2.5 hours",
                        "Kruskal's algorithm (Disjoint Set Union / Union-Find) and Prim's algorithm.",
                        "# DSU with path compression and union by rank achieves near O(1) operations.",
                        "Build Kruskal's algorithm to find the Minimum Spanning Tree of a weighted graph.",
                        "Sort edges by weight and skip if already in same component"
                    ],
                    [
                        "Topological sorting",
                        "2.5 hours",
                        "Kahn's algorithm (in-degree queue) and DFS post-order stack on Directed Acyclic Graphs.",
                        "# In-degree 0 nodes pushed to queue -> decrement neighbors -> detect cycles.",
                        "Solve the Course Schedule II problem determining the valid order of course prerequisites.",
                        "Return empty list if topological sort length < total courses"
                    ],
                    [
                        "Advanced greedy algorithms",
                        "2.5 hours",
                        "Huffman coding, gas station routing, jump game minimum hops, and candy distribution.",
                        "# Greedy choice must be mathematically proven optimal via exchange argument.",
                        "Solve the Jump Game II problem finding minimum jumps to reach the final index.",
                        "Track current interval boundary and farthest reachable index"
                    ],
                    [
                        "Bit manipulation",
                        "2 hours",
                        "Bitwise AND, OR, XOR, NOT, left/right shifts, bitmasks, and Brian Kernighan's bit count.",
                        "# count = 0; while n: n &= n - 1; count += 1 # Clears lowest set bit",
                        "Find two non-repeating elements in an array where every other element appears twice.",
                        "XOR all numbers, isolate rightmost set bit, divide array into two groups"
                    ],
                    [
                        "Tries and advanced data structures",
                        "3 hours",
                        "Prefix trees (Trie), Fenwick Trees (Binary Indexed Tree), and Disjoint Set Union.",
                        "class TrieNode:\n    def __init__(self): self.children = {}; self.is_end = False",
                        "Implement a Trie supporting insert(), search(), and startsWith() prefix lookups in O(L) time.",
                        "Traverse characters as child dictionary keys"
                    ],
                    [
                        "Advanced algorithm optimization",
                        "2.5 hours",
                        "State compression DP with bitmasks, meet-in-the-middle, and sliding window maximum with deque.",
                        "# collections.deque maintains decreasing indices for O(1) window maximum.",
                        "Solve Sliding Window Maximum in O(n) time using a monotonic doubly ended queue deque.",
                        "Pop elements from back smaller than current item"
                    ],
                    [
                        "Competitive programming-style problems",
                        "3 hours",
                        "Complex constraint reasoning, boundary edge handling, memory limits, and fast I/O.",
                        "# Fast I/O: sys.stdin.readline() for processing 10^6 input lines.",
                        "Solve a competitive programming challenge under 1-second execution constraint.",
                        "Avoid O(n^2) when N >= 10^5"
                    ],
                    [
                        "Complex interview problem-solving practice",
                        "3.5 hours",
                        "Systematic communication: clarify constraints, brainstorm solutions, write clean code, dry run, analyze complexity.",
                        "# Step 1: Clarify -> Step 2: Examples -> Step 3: High Level -> Step 4: Code -> Step 5: Test",
                        "Conduct a structured mock technical interview solving a hard LeetCode problem out loud.",
                        "State time and space complexity explicitly"
                    ]
                ]
            }
        ]
    },
    "git-and-github": {
        "skill": "Git and GitHub",
        "skill_slug": "git-and-github",
        "category": "Technical",
        "icon": "GitBranch",
        "description": "Distributed version control system and collaborative development workflows for modern software engineering.",
        "levels": [
            {
                "level": 1,
                "title": "Level 1 \u2013 Beginner",
                "difficulty": "Beginner",
                "estimated_hours": "14 hours",
                "description": "Version control fundamentals, local Git states, core repository management, staging, committing, and basic GitHub workflows.",
                "learning_objectives": [
                    "Understand snapshots vs delta-based version control models",
                    "Navigate the Working Directory, Staging Area, and Git Repository",
                    "Execute core local commands: init, status, add, commit, log, and diff",
                    "Connect local repositories to remote GitHub repositories",
                    "Push, pull, and document projects with markdown README files"
                ],
                "topics": [
                    [
                        "What is Git and version control?",
                        "1 hour",
                        "Centralized vs distributed version control, immutable commit graphs, and audit history.",
                        "# Git tracks complete project snapshots via cryptographic SHA-1/SHA-256 hashes.",
                        "Explain the advantages of distributed version control (Git) over centralized systems (SVN).",
                        "Every developer possesses a full copy of the repository"
                    ],
                    [
                        "Git vs GitHub",
                        "1 hour",
                        "Git CLI tool vs GitHub cloud hosting platform, collaboration features, and repository hosting.",
                        "# Git is local CLI software; GitHub is a cloud service hosting remote Git repositories.",
                        "Summarize differences between Git local CLI and GitHub cloud platform features.",
                        "GitHub adds PRs, Issues, Actions, and team permissions"
                    ],
                    [
                        "Installing and configuring Git",
                        "1 hour",
                        "git config user.name, user.email, default branch main, and autocrlf settings.",
                        "git config --global user.name 'Your Name'\ngit config --global user.email 'name@example.com'\ngit config --global init.defaultBranch main",
                        "Configure your global Git username, email address, and default editor.",
                        "Verify settings with git config --list"
                    ],
                    [
                        "Repositories",
                        "1 hour",
                        "Repository anatomy, the hidden .git directory, objects database, and references.",
                        "# .git contains HEAD, config, index (staging area), and objects database.",
                        "Inspect the contents of a local .git directory and locate the HEAD pointer.",
                        "cat .git/HEAD displays current branch reference"
                    ],
                    [
                        "Working directory, staging area, and repository",
                        "1.5 hours",
                        "The three trees of Git: Working Tree (unstaged), Index/Stage (prepared), and Commit Tree (permanent).",
                        "# Working Dir -> (git add) -> Staging Area -> (git commit) -> Git Repo",
                        "Diagram the lifecycle of a file across untracked, modified, staged, and committed states.",
                        "git status shows state across all three areas"
                    ],
                    [
                        "git init",
                        "1 hour",
                        "Initializing new Git repositories and converting existing folders into Git projects.",
                        "mkdir my_project && cd my_project\ngit init",
                        "Initialize a new Git repository in a blank directory and inspect the generated .git folder.",
                        "git init creates the local Git metadata skeleton"
                    ],
                    [
                        "git status",
                        "1 hour",
                        "Checking working tree status, tracking states, staged changes, and branch position.",
                        "git status\ngit status -s # Short format",
                        "Interpret the status output for untracked, modified, and staged files.",
                        "Red indicates unstaged; Green indicates staged"
                    ],
                    [
                        "git add",
                        "1 hour",
                        "Staging modifications, selective staging with git add -p (patch), and tracking new files.",
                        "git add main.py\ngit add . # Stage all changes",
                        "Stage specific individual files while keeping other modified files in working directory.",
                        "Avoid blindly adding temporary files"
                    ],
                    [
                        "git commit",
                        "1.5 hours",
                        "Atomic commits, commit message conventions (Conventional Commits), and SHA hashes.",
                        "git commit -m 'feat: implement student assessment scoring module'",
                        "Write 3 conventional commit messages following feat:, fix:, and docs: prefixes.",
                        "Keep subject lines under 50 characters in imperative mood"
                    ],
                    [
                        "git log",
                        "1 hour",
                        "History inspection, --oneline, --graph, --decorate, author filtering, and pagination.",
                        "git log --oneline --graph --decorate --all",
                        "Format commit history as a compact graphical oneline tree using git log flags.",
                        "Use git log -n 5 to view recent commits"
                    ],
                    [
                        "git diff",
                        "1 hour",
                        "Inspecting modifications: working tree vs staged (git diff) and staged vs HEAD (git diff --staged).",
                        "git diff # Unstaged modifications\ngit diff --staged # Staged changes ready for commit",
                        "Compare unstaged changes with last commit using git diff.",
                        "+ indicates added lines; - indicates removed lines"
                    ],
                    [
                        "Creating a GitHub repository",
                        "1 hour",
                        "Creating remote repositories, private vs public visibility, and SSH vs HTTPS authentication.",
                        "git remote add origin https://github.com/username/project.git\ngit branch -M main",
                        "Create a remote repository on GitHub and link your local repository via remote add origin.",
                        "Verify remote URL with git remote -v"
                    ],
                    [
                        "git push and git pull",
                        "1.5 hours",
                        "Synchronizing local and remote branches, upstream tracking (-u), and fetching commits.",
                        "git push -u origin main\ngit pull origin main",
                        "Push your local commits to GitHub and configure upstream branch tracking.",
                        "-u sets default remote branch for future push/pull"
                    ],
                    [
                        "Basic README files",
                        "1 hour",
                        "Project documentation in Markdown: headers, installation steps, badges, and code blocks.",
                        "# Project Title\n## Description\n```bash\npip install -r requirements.txt\n```",
                        "Author a comprehensive README.md with badges, setup commands, and feature overview.",
                        "Use standard GitHub Flavored Markdown syntax"
                    ]
                ]
            },
            {
                "level": 2,
                "title": "Level 2 \u2013 Intermediate",
                "difficulty": "Intermediate",
                "estimated_hours": "22 hours",
                "description": "Branching workflows, merge strategies, conflict resolution, Pull Requests, code review, and history correction.",
                "learning_objectives": [
                    "Create, switch, and manage independent feature branches",
                    "Execute fast-forward and 3-way recursive branch merges",
                    "Diagnose and resolve merge conflicts cleanly",
                    "Open, review, and collaborate on GitHub Pull Requests",
                    "Safely stash, revert, reset, and cherry-pick individual commits"
                ],
                "topics": [
                    [
                        "Branches and branch switching",
                        "1.5 hours",
                        "Branch pointers, creating branches, git switch, git checkout -b, and deleting branches.",
                        "git switch -c feature/assessment-engine\ngit branch -d feature/old-branch",
                        "Create a new feature branch, commit changes, and switch back to main.",
                        "git switch is modern replacement for git checkout"
                    ],
                    [
                        "Merging branches",
                        "2 hours",
                        "Fast-forward merges vs 3-way merge commits (--no-ff), and merge base calculation.",
                        "git switch main\ngit merge feature/assessment-engine",
                        "Perform a fast-forward merge and a 3-way merge commit between two branches.",
                        "Fast-forward simply moves branch pointer forward"
                    ],
                    [
                        "Merge conflicts",
                        "2 hours",
                        "Conflict markers (<<<<<<< HEAD, =======, >>>>>>>), causes, and manual resolution.",
                        "# Edit file to remove markers and keep correct lines\ngit add resolved_file.py\ngit commit -m 'chore: resolve merge conflict'",
                        "Simulate and resolve a merge conflict created by editing the same line on two branches.",
                        "Always run tests after resolving conflicts"
                    ],
                    [
                        "Remote repositories",
                        "1.5 hours",
                        "Remote tracking branches (origin/main), remote management, and multiple remotes (upstream).",
                        "git remote -v\ngit remote add upstream https://github.com/original/repo.git",
                        "Add an upstream remote to a forked repository and verify remote endpoints.",
                        "origin points to fork; upstream points to source repo"
                    ],
                    [
                        "git fetch and git pull",
                        "1.5 hours",
                        "Differences between fetch (downloads objects only) and pull (fetch + merge).",
                        "git fetch origin\ngit merge origin/main # Equivalent to git pull origin main",
                        "Inspect incoming remote commits with git fetch and git log origin/main before merging.",
                        "Fetching is safe and never modifies working files"
                    ],
                    [
                        "Pull requests",
                        "2 hours",
                        "PR lifecycle, branch comparison, PR descriptions, draft PRs, and linking GitHub issues.",
                        "# Compare: feature/branch -> base: main\n# Closes #42 in PR description auto-closes issue on merge",
                        "Open a Pull Request on GitHub with a structured summary, testing checklist, and screenshots.",
                        "Use PR templates for consistent submission standards"
                    ],
                    [
                        "Code reviews",
                        "1.5 hours",
                        "Reviewing diffs, line comments, requesting changes, approving PRs, and review etiquette.",
                        "# Constructive reviews: comment on architecture, test coverage, and edge cases.",
                        "Conduct a thorough code review on a peer's PR, suggesting code improvements.",
                        "Be empathetic and offer concrete code suggestions"
                    ],
                    [
                        ".gitignore",
                        "1 hour",
                        "Excluding build artifacts, secrets, .env files, virtual environments, and node_modules.",
                        "# .gitignore\n__pycache__/\n*.pyc\n.venv/\n.env\nnode_modules/",
                        "Create a robust .gitignore file for a Python/Node.js full-stack application.",
                        "Never commit secrets or sensitive credentials to git"
                    ],
                    [
                        "Undoing changes safely",
                        "1.5 hours",
                        "Discarding unstaged edits (git restore), un-staging files (git restore --staged).",
                        "git restore file.py # Discards unstaged edits\ngit restore --staged file.py # Unstages file",
                        "Discard uncommitted changes in a specific file without affecting other modified files.",
                        "Use git restore to recover working copy"
                    ],
                    [
                        "Revert and reset differences",
                        "2 hours",
                        "Public vs private undo: git revert (creates compensating commit) vs git reset (--soft, --mixed, --hard).",
                        "git revert <commit-hash> # Safe for shared branches\ngit reset --soft HEAD~1 # Keeps changes staged",
                        "Revert a committed bug on a shared branch using git revert.",
                        "Never git reset --hard on public shared branches"
                    ],
                    [
                        "Cherry-picking",
                        "1.5 hours",
                        "Applying a specific commit from another branch using git cherry-pick.",
                        "git cherry-pick <commit-hash>",
                        "Cherry-pick a critical hotfix commit from a feature branch directly onto production main.",
                        "Applies only the selected commit diff"
                    ],
                    [
                        "Stashing changes",
                        "1.5 hours",
                        "Temporarily shelving uncommitted work: git stash, stash pop, stash apply, and stash list.",
                        "git stash push -m 'wip: assessment logic'\ngit switch main\n# fix bug\ngit switch feature\ngit stash pop",
                        "Stash uncommitted changes, switch branches to apply a quick fix, and pop stashed work.",
                        "git stash pop re-applies changes and drops stash item"
                    ],
                    [
                        "Forking and collaboration workflows",
                        "1.5 hours",
                        "Fork & Pull Request model, syncing forks, and open source collaboration etiquette.",
                        "git fetch upstream\ngit merge upstream/main\ngit push origin main",
                        "Fork an open-source repository, clone locally, create a feature branch, and sync with upstream.",
                        "Keep local main in sync with upstream/main"
                    ],
                    [
                        "GitHub Issues and project boards",
                        "1 hour",
                        "Issue tracking, labels, milestones, assignees, and Kanban boards with GitHub Projects.",
                        "# Closes #123 auto-links PR to GitHub Issue",
                        "Create 3 linked GitHub issues on a project board categorized into Todo, In Progress, Done.",
                        "Assign labels: bug, enhancement, documentation"
                    ]
                ]
            },
            {
                "level": 3,
                "title": "Level 3 \u2013 Advanced",
                "difficulty": "Advanced",
                "estimated_hours": "30 hours",
                "description": "Interactive rebase, Git hooks, CI/CD with GitHub Actions, branch protection, release tagging, and monorepo management.",
                "learning_objectives": [
                    "Master interactive rebase to squash, reword, and reorder commit histories",
                    "Resolve complex multi-branch merge and rebase conflicts confidently",
                    "Automate pre-commit quality checks using custom Git hooks",
                    "Author CI/CD automation pipelines using GitHub Actions workflows",
                    "Implement repository security, branch protection, and semantic release versioning"
                ],
                "topics": [
                    [
                        "Interactive rebase",
                        "2.5 hours",
                        "git rebase -i HEAD~N, pick, squash, fixup, reword, drop, and linear history hygiene.",
                        "git rebase -i HEAD~3\n# Change 'pick' to 'squash' (or 's') to combine commits",
                        "Squash 4 messy WIP commits into a single clean atomic commit using git rebase -i.",
                        "Linear commit histories are easier to bisect and audit"
                    ],
                    [
                        "Advanced commit history management",
                        "2.5 hours",
                        "git reflog (recovering lost commits), git bisect (binary search bug finder), and git filter-repo.",
                        "git reflog # Shows all HEAD movements\ngit reset --hard HEAD@{2} # Recover deleted commit\ngit bisect start # Binary search for bug",
                        "Use git reflog to recover a branch deleted by mistake.",
                        "Reflog tracks local HEAD movements for 30-90 days"
                    ],
                    [
                        "Rebase vs merge",
                        "2 hours",
                        "Linear history (rebase) vs preservation of true timeline (merge), golden rule of rebasing.",
                        "# Rebase rewrites commit SHAs. Never rebase public branches shared with collaborators.",
                        "Construct a side-by-side comparison diagram showing rebased vs merged branch topologies.",
                        "Rebase creates a flat linear history"
                    ],
                    [
                        "Resolving complex merge conflicts",
                        "2.5 hours",
                        "3-way merge tools, git rerere (reuse recorded resolution), and aborting rebase safely.",
                        "git config --global rerere.enabled true\ngit rebase --abort # Aborts rebase and restores state",
                        "Enable git rerere and resolve a recurring conflict across multiple rebased branches.",
                        "Rerere automatically replays previous conflict resolutions"
                    ],
                    [
                        "Git tags and releases",
                        "2 hours",
                        "Lightweight vs annotated tags, semantic versioning (SemVer: v1.2.3), and GitHub Releases.",
                        "git tag -a v1.0.0 -m 'Release version 1.0.0'\ngit push origin v1.0.0",
                        "Create an annotated semantic release tag and publish a GitHub Release with changelog notes.",
                        "Annotated tags store author, date, and cryptographic signature"
                    ],
                    [
                        "Git hooks",
                        "2.5 hours",
                        "Client-side hooks (pre-commit, commit-msg, pre-push) and server-side hooks; tools like Husky and pre-commit.",
                        "#!/bin/sh\n# .git/hooks/pre-commit\npytest tests || exit 1",
                        "Write a pre-commit shell hook that runs a linter and prevents commit if linting errors exist.",
                        "Hook script must return non-zero exit code to abort commit"
                    ],
                    [
                        "GitHub Actions fundamentals",
                        "2.5 hours",
                        "Workflows, events (on: push, pull_request), jobs, runners (ubuntu-latest), and actions/checkout.",
                        "# .github/workflows/ci.yml\nname: CI\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n    - uses: actions/checkout@v4",
                        "Create a GitHub Actions workflow that executes automated unit tests on every pull request.",
                        "Workflows live in .github/workflows/*.yml"
                    ],
                    [
                        "CI/CD workflow basics",
                        "3 hours",
                        "Continuous Integration (automated test/lint) and Continuous Delivery (automated Docker build/deploy).",
                        "# Steps: Checkout -> Setup Python -> Install dependencies -> Run Pytest -> Build image",
                        "Build a complete multi-step CI pipeline caching pip packages and publishing test coverage.",
                        "Use actions/cache@v3 to accelerate dependency installation"
                    ],
                    [
                        "Branch protection and repository security",
                        "2 hours",
                        "Required PR reviews, status checks passing, dismissing stale reviews, signed commits, and Secret Scanning.",
                        "# Settings -> Branches -> Add branch protection rule: main\n# Require pull request reviews, Require status checks to pass",
                        "Configure branch protection rules preventing direct pushes to main and requiring 1 approved review.",
                        "Enforce linear commit history if desired"
                    ],
                    [
                        "Release management",
                        "2 hours",
                        "Release branches, changelog automation, GitHub milestone tracking, and rollback strategies.",
                        "# GitHub CLI: gh release create v2.0.0 --generate-notes",
                        "Generate automated release notes from merged pull request titles.",
                        "Tag pull requests with labels to group release notes"
                    ],
                    [
                        "Monorepo fundamentals",
                        "2 hours",
                        "Single repository multi-project architecture, path filters in CI, and package tooling.",
                        "# CI on: paths: ['backend/**'] vs paths: ['frontend/**']",
                        "Configure independent CI workflows in a monorepo triggered only when specific subdirectories change.",
                        "Use paths filters in GitHub Actions"
                    ],
                    [
                        "Team collaboration strategies",
                        "2.5 hours",
                        "Trunk-based development vs GitFlow vs GitHub Flow, CODEOWNERS file, and branch naming standards.",
                        "# CODEOWNERS\n/backend/ @backend-team\n/frontend/ @frontend-team",
                        "Create a CODEOWNERS file defining required review ownership across codebase domains.",
                        "GitHub auto-requests reviews from listed code owners"
                    ],
                    [
                        "Managing a professional project repository",
                        "3 hours",
                        "Issue templates, PR templates, CONTRIBUTING.md, LICENSE, security policies (SECURITY.md).",
                        "# .github/pull_request_template.md\n## Description\n## Checklist\n- [ ] Tests pass",
                        "Assemble a complete professional repository governance suite (templates, contributing guide, license).",
                        "Place templates in .github/ folder"
                    ]
                ]
            }
        ]
    },
    "sql": {
        "skill": "SQL",
        "skill_slug": "sql",
        "category": "Technical",
        "icon": "Database",
        "description": "Structured Query Language for relational database management, complex analytical aggregations, and performance tuning.",
        "levels": [
            {
                "level": 1,
                "title": "Level 1 \u2013 Beginner",
                "difficulty": "Beginner",
                "estimated_hours": "18 hours",
                "description": "Relational database concepts, schema definitions (DDL), data manipulation (DML), basic SELECT filtering, and group aggregations.",
                "learning_objectives": [
                    "Understand relational tables, data types, primary keys, and foreign keys",
                    "Execute DDL statements (CREATE, ALTER, DROP, TRUNCATE) to manage schemas",
                    "Perform DML operations (INSERT, UPDATE, DELETE) with data integrity",
                    "Query datasets using SELECT, WHERE, ORDER BY, DISTINCT, and LIMIT",
                    "Aggregate tabular data using COUNT, SUM, AVG, GROUP BY, and HAVING"
                ],
                "topics": [
                    [
                        "Introduction to databases and relational databases",
                        "1 hour",
                        "RDBMS architecture (PostgreSQL, SQLite, MySQL), ACID properties, and relational models.",
                        "-- RDBMS stores data in structured tables linked by relational key constraints.",
                        "Explain how relational tables differ from unstructured NoSQL document stores.",
                        "RDBMS emphasizes ACID consistency and strict schemas"
                    ],
                    [
                        "Tables, rows, columns, and data types",
                        "1 hour",
                        "Relational entities, columns, data types (INT, VARCHAR, TEXT, BOOLEAN, TIMESTAMP).",
                        "-- Column: Attribute (e.g. name VARCHAR(100))\n-- Row: Tuple instance (e.g. 1, 'Maya', 3.8)",
                        "Design a table schema for student enrollments choosing appropriate data types for each attribute.",
                        "Use TIMESTAMP for temporal tracking"
                    ],
                    [
                        "Primary keys and foreign keys",
                        "1.5 hours",
                        "Entity identity (PRIMARY KEY), referential integrity (FOREIGN KEY REFERENCES), and cascade rules.",
                        "CREATE TABLE students (\n    id SERIAL PRIMARY KEY,\n    email VARCHAR(255) UNIQUE NOT NULL\n);",
                        "Define a 1-to-many relationship between Students and AssessmentSubmissions with foreign keys.",
                        "Add ON DELETE CASCADE where child records depend on parent"
                    ],
                    [
                        "CREATE, ALTER, DROP, and TRUNCATE",
                        "1.5 hours",
                        "Data Definition Language (DDL): creating tables, modifying columns, dropping objects, and truncating rows.",
                        "ALTER TABLE students ADD COLUMN gpa NUMERIC(3, 2);\nTRUNCATE TABLE logs; -- Fast wipe without deleting schema",
                        "Write DDL to create a courses table, alter it to add a credits column, and drop a test table.",
                        "TRUNCATE is faster than DELETE without WHERE"
                    ],
                    [
                        "INSERT, UPDATE, and DELETE",
                        "1.5 hours",
                        "Data Manipulation Language (DML): inserting tuples, modifying values, and conditional deletion.",
                        "INSERT INTO students (name, email) VALUES ('Alex', 'alex@edu.com');\nUPDATE students SET gpa = 3.9 WHERE id = 1;",
                        "Insert 3 student records, update the GPA of one student, and safely delete test records with WHERE.",
                        "Never execute UPDATE or DELETE without a WHERE clause in production!"
                    ],
                    [
                        "SELECT statements",
                        "1 hour",
                        "Projection of columns, aliasing (AS), literal expressions, and arithmetic in projections.",
                        "SELECT name, gpa * 25 AS normalized_score FROM students;",
                        "Write a query selecting student names and calculating their percentage score out of 100.",
                        "Use column aliases with AS for readable output"
                    ],
                    [
                        "WHERE conditions",
                        "1 hour",
                        "Filtering rows using equality, inequality, and relational predicates.",
                        "SELECT * FROM students WHERE gpa >= 3.5 AND department = 'Computer Science';",
                        "Filter candidates whose assessment score is >= 70 and who enrolled after '2024-01-01'.",
                        "Wrap string literals in single quotes"
                    ],
                    [
                        "Comparison and logical operators",
                        "1 hour",
                        "=, !=, <>, <, >, <=, >=, AND, OR, NOT, and operator precedence.",
                        "SELECT * FROM tasks WHERE (priority = 'HIGH' OR priority = 'MEDIUM') AND status != 'LOCKED';",
                        "Write a query combining AND and OR logic with parentheses to prioritize operator evaluation.",
                        "Parentheses override default AND precedence over OR"
                    ],
                    [
                        "ORDER BY",
                        "1 hour",
                        "Sorting results, ASC (default), DESC, multi-column sorting, and NULLS FIRST/LAST.",
                        "SELECT name, gpa FROM students ORDER BY gpa DESC, name ASC;",
                        "Query top 10 students ordered by highest GPA, resolving ties alphabetically by name.",
                        "DESC sorts descending; ASC sorts ascending"
                    ],
                    [
                        "DISTINCT",
                        "1 hour",
                        "Eliminating duplicate rows across selected columns.",
                        "SELECT DISTINCT department FROM students;",
                        "Find all distinct career tracks chosen by registered students.",
                        "DISTINCT operates on the entire tuple of selected columns"
                    ],
                    [
                        "LIMIT",
                        "1 hour",
                        "Restricting result row counts, pagination using LIMIT and OFFSET.",
                        "SELECT * FROM assessments ORDER BY score DESC LIMIT 5 OFFSET 10;",
                        "Write a paginated query retrieving page 2 of student records (10 records per page).",
                        "Page 2 with 10 per page uses LIMIT 10 OFFSET 10"
                    ],
                    [
                        "LIKE, IN, BETWEEN, and IS NULL",
                        "1.5 hours",
                        "Pattern matching (% and _), set membership (IN), range checks (BETWEEN), and NULL handling.",
                        "SELECT * FROM students WHERE email LIKE '%@bitsathy.ac.in'\n  AND score BETWEEN 70 AND 100\n  AND phone IS NOT NULL;",
                        "Find students whose name starts with 'A', scored between 80 and 95, and department is in ('CS', 'AI').",
                        "NULL checks must use IS NULL or IS NOT NULL, never = NULL"
                    ],
                    [
                        "Aggregate functions",
                        "1.5 hours",
                        "Summary statistics: COUNT(*), COUNT(col), SUM(), AVG(), MIN(), MAX().",
                        "SELECT COUNT(*) AS total_students, AVG(gpa) AS mean_gpa, MAX(gpa) AS top_gpa FROM students;",
                        "Compute total count of students, average assessment score, and highest score across all records.",
                        "COUNT(*) counts all rows; COUNT(col) ignores NULLs"
                    ],
                    [
                        "GROUP BY and HAVING",
                        "1.5 hours",
                        "Grouping rows by dimensions, aggregating within groups, and filtering groups via HAVING.",
                        "SELECT department, AVG(gpa) AS avg_gpa\nFROM students\nGROUP BY department\nHAVING AVG(gpa) >= 3.5;",
                        "Find departments with more than 5 enrolled students and an average GPA above 3.2.",
                        "WHERE filters individual rows; HAVING filters aggregated groups"
                    ],
                    [
                        "Basic constraints",
                        "1 hour",
                        "Integrity constraints: NOT NULL, UNIQUE, CHECK (score >= 0), DEFAULT.",
                        "CREATE TABLE submissions (\n    id SERIAL PRIMARY KEY,\n    score INT CHECK (score BETWEEN 0 AND 100),\n    status VARCHAR(20) DEFAULT 'PENDING'\n);",
                        "Create a table with CHECK constraints validating that score is between 0 and 100.",
                        "CHECK constraints enforce domain rules at database level"
                    ]
                ]
            },
            {
                "level": 2,
                "title": "Level 2 \u2013 Intermediate",
                "difficulty": "Intermediate",
                "estimated_hours": "26 hours",
                "description": "Relational joins, subqueries, Common Table Expressions, window functions, and database normalization.",
                "learning_objectives": [
                    "Formulate complex multi-table queries using INNER, LEFT, RIGHT, and FULL joins",
                    "Write scalar, column, and correlated subqueries with EXISTS and IN predicates",
                    "Structure complex analytics using Common Table Expressions (WITH clauses)",
                    "Apply analytical window functions (ROW_NUMBER, RANK, DENSE_RANK, OVER)",
                    "Understand relational normalization forms (1NF, 2NF, 3NF) and database transactions"
                ],
                "topics": [
                    [
                        "INNER JOIN",
                        "1.5 hours",
                        "Matching records across tables based on join predicate (ON), Cartesian products prevention.",
                        "SELECT s.name, a.title, sub.score\nFROM students s\nINNER JOIN submissions sub ON s.id = sub.student_id\nINNER JOIN assessments a ON sub.assessment_id = a.id;",
                        "Write an INNER JOIN query combining students, their enrolled courses, and their final grades.",
                        "Only returns rows with matching keys in both tables"
                    ],
                    [
                        "LEFT JOIN, RIGHT JOIN, and FULL JOIN concepts",
                        "2 hours",
                        "Outer joins, preserving unmatched left or right rows, NULL propagation in non-matches.",
                        "SELECT s.name, sub.score\nFROM students s\nLEFT JOIN submissions sub ON s.id = sub.student_id\nWHERE sub.id IS NULL; -- Students with NO submissions",
                        "Find all students who have never submitted an assessment using a LEFT JOIN with IS NULL filter.",
                        "LEFT JOIN returns all left rows regardless of right match"
                    ],
                    [
                        "Self joins",
                        "1.5 hours",
                        "Joining a table to itself using distinct aliases, hierarchical manager/employee relationships.",
                        "SELECT e.name AS employee, m.name AS mentor\nFROM students e\nLEFT JOIN students m ON e.mentor_id = m.id;",
                        "Query student peer pairings where student A has a higher score than student B in the same department.",
                        "Table must be aliased with two distinct names (e.g. s1, s2)"
                    ],
                    [
                        "Multiple-table queries",
                        "2 hours",
                        "Combining 3 or more tables across normalized relationships with composite join conditions.",
                        "SELECT u.email, c.title, r.current_employability\nFROM users u\nJOIN roadmaps r ON u.id = r.user_id\nJOIN careers c ON r.career_id = c.id;",
                        "Construct a 4-table join query connecting users, roadmaps, levels, and assessment attempt records.",
                        "Check each join condition to avoid unintended cross joins"
                    ],
                    [
                        "Subqueries",
                        "2 hours",
                        "Subqueries in WHERE, FROM (derived tables), and SELECT clauses; scalar vs multi-row subqueries.",
                        "SELECT name, gpa\nFROM students\nWHERE gpa > (SELECT AVG(gpa) FROM students);",
                        "Find students whose assessment score exceeds the average score of all candidates.",
                        "Subquery in WHERE clause evaluates once if uncorrelated"
                    ],
                    [
                        "Correlated subqueries",
                        "2 hours",
                        "Subqueries referencing columns from outer query, per-row evaluation, EXISTS, and NOT EXISTS.",
                        "SELECT s.name, s.department, s.gpa\nFROM students s\nWHERE s.gpa > (\n    SELECT AVG(s2.gpa) FROM students s2 WHERE s2.department = s.department\n);",
                        "Find students whose GPA is higher than the average GPA of their own specific department.",
                        "Correlated subquery executes for every outer row"
                    ],
                    [
                        "CASE expressions",
                        "1.5 hours",
                        "Conditional projection logic in SELECT and ORDER BY: CASE WHEN ... THEN ... ELSE ... END.",
                        "SELECT name, score,\n       CASE WHEN score >= 90 THEN 'Expert'\n            WHEN score >= 70 THEN 'Proficient'\n            ELSE 'Developing' END AS proficiency_band\nFROM assessment_results;",
                        "Categorize student scores into 'Distinction' (>=85), 'Pass' (>=70), and 'Retake' using CASE.",
                        "Evaluate most specific WHEN conditions first"
                    ],
                    [
                        "String and date functions",
                        "1.5 hours",
                        "CONCAT, SUBSTRING, UPPER, LOWER, LENGTH, NOW(), DATE_TRUNC, EXTRACT(YEAR FROM date), INTERVAL.",
                        "SELECT CONCAT(first_name, ' ', last_name) AS full_name,\n       DATE_PART('year', AGE(NOW(), enrolled_date)) AS years_enrolled\nFROM students;",
                        "Calculate the duration between enrollment date and completion date in days using date subtraction.",
                        "Use AGE() or EXTRACT(epoch from interval) for temporal math"
                    ],
                    [
                        "Views",
                        "1.5 hours",
                        "Creating virtual tables (CREATE VIEW), security abstraction, materialized views concept.",
                        "CREATE VIEW active_student_progress AS\nSELECT s.id, s.name, COUNT(sub.id) AS total_completed\nFROM students s\nLEFT JOIN submissions sub ON s.id = sub.student_id\nGROUP BY s.id, s.name;",
                        "Create a view encapsulating a complex 3-table join of verified student skill credentials.",
                        "Views simplify complex queries for frontend consumers"
                    ],
                    [
                        "Index fundamentals",
                        "2 hours",
                        "B-Tree index structure, speeding up lookups, covering indexes, and write overhead.",
                        "CREATE INDEX idx_students_dept_gpa ON students(department, gpa);",
                        "Create a composite index on (user_id, status) and explain when it accelerates queries.",
                        "Indexes speed up reads but add overhead to INSERT/UPDATE/DELETE"
                    ],
                    [
                        "UNION and UNION ALL",
                        "1.5 hours",
                        "Combining result sets vertically: UNION (deduplicating) vs UNION ALL (faster, preserving duplicates).",
                        "SELECT email, 'Student' AS role FROM students\nUNION ALL\nSELECT email, 'Instructor' AS role FROM instructors;",
                        "Combine active student emails and alumni emails into a unified non-duplicating mailing list.",
                        "Use UNION ALL when results are known to be disjoint to avoid sorting cost"
                    ],
                    [
                        "Common Table Expressions",
                        "2 hours",
                        "WITH cte_name AS (...), readability, modular SQL development, and referencing multiple CTEs.",
                        "WITH dept_averages AS (\n    SELECT department, AVG(gpa) AS avg_gpa FROM students GROUP BY department\n)\nSELECT s.name, s.department, s.gpa, d.avg_gpa\nFROM students s\nJOIN dept_averages d ON s.department = d.department;",
                        "Refactor a nested subquery into two clean, readable Common Table Expressions.",
                        "CTEs can be chained sequentially: WITH a AS (...), b AS (...)"
                    ],
                    [
                        "Window functions introduction",
                        "2.5 hours",
                        "OVER (PARTITION BY ... ORDER BY ...), ROW_NUMBER(), RANK(), DENSE_RANK().",
                        "SELECT name, department, gpa,\n       DENSE_RANK() OVER (PARTITION BY department ORDER BY gpa DESC) AS dept_rank\nFROM students;",
                        "Rank students within each department by GPA using DENSE_RANK(), resolving ties gracefully.",
                        "Window functions do not collapse rows like GROUP BY does"
                    ],
                    [
                        "Transactions and ACID properties",
                        "1.5 hours",
                        "BEGIN TRANSACTION, COMMIT, ROLLBACK, Atomicity, Consistency, Isolation, and Durability.",
                        "BEGIN;\nUPDATE accounts SET balance = balance - 100 WHERE id = 1;\nUPDATE accounts SET balance = balance + 100 WHERE id = 2;\nCOMMIT;",
                        "Write a transactional block transferring credits between two accounts with a conditional ROLLBACK.",
                        "ROLLBACK reverts all changes within the current transaction"
                    ],
                    [
                        "Normalization fundamentals",
                        "2 hours",
                        "Anomalies (Insertion, Update, Deletion), First Normal Form (1NF), Second (2NF), and Third (3NF).",
                        "-- 1NF: Atomic values, no repeating groups.\n-- 2NF: 1NF + no partial dependency on composite key.\n-- 3NF: 2NF + no transitive dependencies.",
                        "Decompose an un-normalized spreadsheet table with repeating skills columns into 3NF relational tables.",
                        "Eliminate transitive dependencies where non-key determines non-key"
                    ]
                ]
            },
            {
                "level": 3,
                "title": "Level 3 \u2013 Advanced",
                "difficulty": "Advanced",
                "estimated_hours": "32 hours",
                "description": "Analytical windowing, recursive CTEs, query execution plan inspection, index optimization, concurrency, and performance tuning.",
                "learning_objectives": [
                    "Formulate complex analytics using advanced window functions and frames",
                    "Traverse hierarchical trees and graphs with Recursive CTEs",
                    "Inspect and interpret query execution plans using EXPLAIN ANALYZE",
                    "Design composite and covering indexes to eliminate table scans",
                    "Manage transaction isolation levels, concurrency conflicts, and deadlock prevention"
                ],
                "topics": [
                    [
                        "Advanced window functions",
                        "3 hours",
                        "LEAD(), LAG(), FIRST_VALUE(), NTILE(), moving averages with ROWS BETWEEN N PRECEDING AND CURRENT ROW.",
                        "SELECT student_id, attempt_date, score,\n       score - LAG(score, 1) OVER (PARTITION BY student_id ORDER BY attempt_date) AS score_improvement\nFROM test_attempts;",
                        "Calculate the 7-day moving average of daily platform signups using a window frame.",
                        "Use ROWS BETWEEN 6 PRECEDING AND CURRENT ROW"
                    ],
                    [
                        "Recursive CTEs",
                        "2.5 hours",
                        "WITH RECURSIVE anchor_query UNION ALL recursive_query, terminating conditions, tree traversals.",
                        "WITH RECURSIVE category_tree AS (\n    SELECT id, name, parent_id, 1 AS depth FROM categories WHERE parent_id IS NULL\n    UNION ALL\n    SELECT c.id, c.name, c.parent_id, ct.depth + 1 FROM categories c JOIN category_tree ct ON c.parent_id = ct.id\n)\nSELECT * FROM category_tree;",
                        "Query an organizational hierarchy to list all subordinates of a manager with depth levels.",
                        "Ensure recursive query has join condition to prevent infinite loops"
                    ],
                    [
                        "Query execution plans",
                        "2.5 hours",
                        "EXPLAIN (ANALYZE, BUFFERS), sequential scans vs index scans, bitmap heap scans, and node costs.",
                        "EXPLAIN ANALYZE SELECT * FROM students WHERE email = 'alex@edu.com';",
                        "Run EXPLAIN ANALYZE on an un-indexed query and compare execution time after adding an index.",
                        "Sequential scan reads entire table from disk"
                    ],
                    [
                        "Query optimization",
                        "2.5 hours",
                        "SARGable queries, avoiding functions on indexed columns in WHERE, join order optimization, and subquery flattening.",
                        "-- Non-SARGable: WHERE EXTRACT(YEAR FROM date) = 2024\n-- SARGable: WHERE date >= '2024-01-01' AND date < '2025-01-01'",
                        "Rewrite a non-SARGable query using date ranges so that PostgreSQL can use an index.",
                        "Applying functions to columns disables standard index lookups"
                    ],
                    [
                        "Composite and covering indexes",
                        "2.5 hours",
                        "Index column ordering (leftmost prefix rule), covering indexes with INCLUDE, index size trade-offs.",
                        "CREATE INDEX idx_student_cover ON students(department, gpa) INCLUDE (name);",
                        "Design a covering index allowing an Index-Only Scan without hitting the table heap.",
                        "Put high-cardinality equality columns first in composite index"
                    ],
                    [
                        "Index trade-offs",
                        "2 hours",
                        "B-Tree vs Hash vs GIN vs GiST indexes, index bloat, maintenance cost on high-write tables.",
                        "# GIN indexes are ideal for JSONB and array fields; B-Tree is general purpose.",
                        "Select appropriate index types for full-text search, JSONB columns, and primary keys.",
                        "GIN indexes excel for array and JSON containment queries (@>)"
                    ],
                    [
                        "Advanced normalization and denormalization",
                        "2.5 hours",
                        "Boyce-Codd Normal Form (BCNF), 4NF, intentional denormalization for read-heavy OLAP architectures.",
                        "-- Denormalization trades storage and update complexity for sub-millisecond read latency.",
                        "Evaluate whether to denormalize a dashboard summary table given 1,000,000 reads per second.",
                        "Maintain cache invalidation or materialized views"
                    ],
                    [
                        "Database design",
                        "2.5 hours",
                        "ER diagrams, surrogate vs natural keys, UUIDv7 vs auto-increment, soft deletes, and temporal tables.",
                        "-- Soft delete pattern: deleted_at TIMESTAMP NULL",
                        "Design a complete normalized schema for an online learning management system with versioning.",
                        "Use UUID or BIGSERIAL for primary keys"
                    ],
                    [
                        "Stored procedures and triggers",
                        "2.5 hours",
                        "PL/pgSQL functions, triggers (BEFORE/AFTER INSERT/UPDATE), audit logging, and business rules.",
                        "CREATE OR REPLACE FUNCTION update_timestamp()\nRETURNS TRIGGER AS $$\nBEGIN NEW.updated_at = NOW(); RETURN NEW; END;\n$$ LANGUAGE plpgsql;",
                        "Create a trigger that automatically updates updated_at timestamp on row modification.",
                        "Execute trigger BEFORE UPDATE FOR EACH ROW"
                    ],
                    [
                        "Isolation levels and concurrency",
                        "2.5 hours",
                        "Read Uncommitted, Read Committed, Repeatable Read, Serializable; dirty reads, phantom reads.",
                        "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;",
                        "Explain how Repeatable Read prevents non-repeatable read anomalies in multi-step reporting.",
                        "Serializable isolation guarantees equivalent serial execution"
                    ],
                    [
                        "Deadlocks",
                        "2 hours",
                        "Deadlock conditions, lock ordering, row-level locks (SELECT ... FOR UPDATE), and deadlock detection.",
                        "-- SELECT * FROM inventory WHERE id = 5 FOR UPDATE;",
                        "Demonstrate how acquiring locks in identical order across transactions prevents deadlocks.",
                        "Always sort resource IDs before locking multiple rows"
                    ],
                    [
                        "Advanced transaction management",
                        "2 hours",
                        "Savepoints (SAVEPOINT s1; ROLLBACK TO s1), two-phase commits, and optimistic concurrency (version column).",
                        "-- UPDATE items SET val = 'new', version = version + 1 WHERE id = 1 AND version = 5;",
                        "Implement an optimistic locking pattern using a version number column to prevent lost updates.",
                        "Check affected rows == 1 to detect concurrency collisions"
                    ],
                    [
                        "Database security and access control",
                        "2 hours",
                        "Roles, GRANT/REVOKE, Row-Level Security (RLS), SQL injection prevention via parameterized queries.",
                        "ALTER TABLE student_records ENABLE ROW LEVEL SECURITY;\nCREATE POLICY student_view ON student_records FOR SELECT USING (user_id = current_user_id());",
                        "Configure Row-Level Security ensuring students can only view their own personal submission records.",
                        "Never concatenate user input directly into SQL strings"
                    ],
                    [
                        "Performance tuning",
                        "2.5 hours",
                        "Connection pooling (PgBouncer), work_mem, shared_buffers, VACUUM ANALYZE, and autovacuum tuning.",
                        "# VACUUM ANALYZE reclaims dead tuples and updates table planner statistics.",
                        "Identify and resolve bloated tables using pg_stat_user_tables and VACUUM FULL.",
                        "Autovacuum prevents transaction ID wraparound and table bloat"
                    ],
                    [
                        "Complex analytical SQL queries",
                        "3 hours",
                        "Cohort analysis, user retention curves, funnel conversion drop-offs, and multi-dimensional aggregations.",
                        "SELECT cohort_month, month_number, COUNT(DISTINCT user_id) AS active_users\nFROM user_monthly_activity\nGROUP BY cohort_month, month_number;",
                        "Write a complete cohort retention analysis query tracking monthly student activity after signup.",
                        "Group by signup cohort and calculate active count per relative month"
                    ]
                ]
            }
        ]
    },
    "communication": {
        "skill": "Communication",
        "skill_slug": "communication",
        "category": "Soft Skills",
        "icon": "MessageSquare",
        "description": "Clarity, technical articulation, structured explanations, professional writing, and interview communication.",
        "levels": [
            {
                "level": 1,
                "title": "Level 1 \u2013 Beginner",
                "difficulty": "Beginner",
                "estimated_hours": "14 hours",
                "description": "Fundamental grammar, sentence construction, parts of speech, everyday vocabulary, and simple technical conversation.",
                "learning_objectives": [
                    "Formulate grammatically correct English sentences with appropriate word order",
                    "Apply correct subject-verb agreement and foundational verb tenses",
                    "Deliver concise, professional self-introductions in technical contexts",
                    "Ask clear questions and extract information during conversations",
                    "Identify and correct common grammatical and syntactical mistakes"
                ],
                "topics": [
                    [
                        "Basic English sentence structure",
                        "1 hour",
                        "Subject-Verb-Object (SVO) word order, declarative, interrogative, and imperative sentences.",
                        "# Subject (The developer) + Verb (writes) + Object (clean Python code).",
                        "Reorder jumbled sentence fragments into grammatically sound technical statements.",
                        "Identify subject and primary action verb first"
                    ],
                    [
                        "Parts of speech",
                        "1 hour",
                        "Nouns, pronouns, verbs, adjectives, adverbs, prepositions, conjunctions, and interjections.",
                        "# 'The skilled engineer (adj + noun) quickly deployed (adv + verb) the secure API (adj + noun).'",
                        "Classify all parts of speech in a short paragraph describing a software bug.",
                        "Adverbs modify verbs; adjectives modify nouns"
                    ],
                    [
                        "Nouns, pronouns, verbs, and adjectives",
                        "1 hour",
                        "Countable vs uncountable nouns, personal pronouns, action vs linking verbs, and comparative adjectives.",
                        "# 'She wrote better code than anyone else on her team.'",
                        "Replace ambiguous pronouns with clear noun antecedents in a project summary.",
                        "Avoid ambiguous pronouns like 'it' without clear context"
                    ],
                    [
                        "Basic tenses",
                        "1.5 hours",
                        "Simple Present (habits, facts), Simple Past (completed actions), and Simple Future (plans).",
                        "# Present: 'I study machine learning daily.'\n# Past: 'I completed the Python module yesterday.'",
                        "Convert 5 present tense sentences into past tense and future tense forms.",
                        "Regular past tense adds -ed; beware irregular verbs"
                    ],
                    [
                        "Subject-verb agreement",
                        "1.5 hours",
                        "Singular subjects with singular verbs, plural subjects, collective nouns, and intervening prepositional phrases.",
                        "# Correct: 'The list of candidates is long.' (Subject is 'list', not 'candidates')",
                        "Identify and fix 5 subject-verb agreement errors in a technical report snippet.",
                        "Ignore words between subject and verb when matching number"
                    ],
                    [
                        "Articles and prepositions",
                        "1 hour",
                        "Definite (the) vs indefinite (a, an) articles, prepositions of time (in, on, at), place, and direction.",
                        "# 'I completed the assessment on Monday at 3 PM in the laboratory.'",
                        "Insert correct articles and prepositions into a technical onboarding email.",
                        "Use 'an' before vowel sounds: 'an AI model'"
                    ],
                    [
                        "Everyday vocabulary",
                        "1 hour",
                        "Collocations, technical workplace terminology, context clues, and avoiding buzzword inflation.",
                        "# 'Collaborate on a sprint', 'Debug an issue', 'Meet a deadline', 'Deploy a feature'.",
                        "Compile a list of 10 professional workplace collocations and use each in a sentence.",
                        "Collocations are words that naturally go together"
                    ],
                    [
                        "Asking and answering questions",
                        "1 hour",
                        "Open-ended (WH-questions: what, why, how) vs closed (yes/no), clarifying questions.",
                        "# Open: 'How did you resolve the database deadlock?'\n# Closed: 'Did the build pass?'",
                        "Formulate 3 clarifying questions to ask when receiving an ambiguous task ticket.",
                        "Open questions invite detailed explanations"
                    ],
                    [
                        "Self-introduction",
                        "1.5 hours",
                        "Structuring an elevator pitch: Present role + Key skills + Relevant project + Future aspiration.",
                        "# 'Hi, I am Alex, a Computer Science graduate specializing in Python and Machine Learning...'",
                        "Write a polished 60-second professional self-introduction tailored for technical recruiters.",
                        "Focus on tangible skills and problem-solving passion"
                    ],
                    [
                        "Simple conversation practice",
                        "1 hour",
                        "Active listening cues, turn-taking, acknowledgment phrases, and polite disagreement.",
                        "# 'That makes sense; however, have we considered the latency impact?'",
                        "Script a constructive conversation discussing conflicting project deadlines with a team lead.",
                        "Acknowledge the other person's point before sharing your perspective"
                    ],
                    [
                        "Reading short passages",
                        "1 hour",
                        "Skimming for main idea, scanning for specific keywords, and drawing inferences.",
                        "# Technique: Read first and last sentence of paragraphs for high-level comprehension.",
                        "Read a short technical release note and extract 3 key bug fixes and 1 breaking change.",
                        "Focus on change logs and bullet points"
                    ],
                    [
                        "Basic listening comprehension",
                        "1 hour",
                        "Identifying speaker intent, tone, key requirements, and taking structured meeting notes.",
                        "# Meeting note format: Context | Decisions Made | Action Items (Who/What/When).",
                        "Summarize verbal instructions into 3 clear, actionable bullet points with deadlines.",
                        "Identify who owns what deliverable"
                    ],
                    [
                        "Common grammar mistakes",
                        "1.5 hours",
                        "Run-on sentences, comma splices, sentence fragments, dangling modifiers, its vs it's, their/there/they're.",
                        "# Its = possessive ('Its performance is high.')\n# It's = it is ('It's running fast.')",
                        "Proofread and correct 8 common grammar and punctuation errors in a draft pull request note.",
                        "Dangling modifier error: 'Running fast, the error occurred.'"
                    ]
                ]
            },
            {
                "level": 2,
                "title": "Level 2 \u2013 Intermediate",
                "difficulty": "Intermediate",
                "estimated_hours": "20 hours",
                "description": "Continuous and perfect tenses, technical explanation articulation, email communication, group discussions, and interview practice.",
                "learning_objectives": [
                    "Express precise timelines using Perfect and Continuous English tenses",
                    "Explain complex technical concepts clearly to non-technical stakeholders",
                    "Compose professional, well-structured emails, status reports, and technical updates",
                    "Participate actively and constructively in technical group discussions",
                    "Structure compelling answers to behavioral interview questions using the STAR framework"
                ],
                "topics": [
                    [
                        "All major English tenses in practical usage",
                        "2 hours",
                        "Present Perfect ('have implemented'), Past Continuous, Future Perfect, and temporal nuances.",
                        "# 'I have worked with SQL for two years.' (Experience continuing to present)",
                        "Write a paragraph utilizing Present Perfect, Past Simple, and Past Continuous correctly.",
                        "Present Perfect connects past actions to present impact"
                    ],
                    [
                        "Sentence formation and correction",
                        "1.5 hours",
                        "Compound and complex sentences, relative clauses (who, which, that), and transitional adverbs.",
                        "# 'Although the model trained for 10 hours, the validation loss did not decrease.'",
                        "Combine simple choppy sentences into sophisticated complex sentences using subordinating conjunctions.",
                        "Use 'although', 'because', 'whereas'"
                    ],
                    [
                        "Paragraph writing",
                        "1.5 hours",
                        "PEEL framework: Point, Evidence, Explanation, Link to overarching objective.",
                        "# Point: Scalability is critical. Evidence: Traffic doubled. Explanation: Bottlenecks arise. Link: Hence Redis.",
                        "Write a structured 150-word PEEL paragraph explaining why database indexing is crucial.",
                        "Every paragraph should have one central thesis statement"
                    ],
                    [
                        "Vocabulary building",
                        "1.5 hours",
                        "Domain-specific terminology, active verbs for resumes (spearheaded, architected, optimized).",
                        "# Replace 'did a project' with 'architected an end-to-end classification pipeline'.",
                        "Upgrade 5 passive bullet points into high-impact action-oriented achievement statements.",
                        "Start with past tense strong action verbs"
                    ],
                    [
                        "Listening and speaking exercises",
                        "1.5 hours",
                        "Paraphrasing for confirmation, managing interruptions politely, and vocal pacing.",
                        "# 'If I understand correctly, our primary objective for this sprint is minimizing latency?'",
                        "Practice paraphrasing a complex client requirement to verify mutual alignment.",
                        "Paraphrasing prevents costly miscommunications"
                    ],
                    [
                        "Explaining technical concepts in English",
                        "2 hours",
                        "Feynman technique, analogies, avoiding unnecessary jargon, and tailoring to audience.",
                        "# Analogy: 'An API is like a restaurant menu; you order, the kitchen prepares, the waiter delivers.'",
                        "Explain how a Neural Network or Decision Tree works to an 8th grader without using math symbols.",
                        "Use relatable real-world physical analogies"
                    ],
                    [
                        "Group discussion fundamentals",
                        "1.5 hours",
                        "Initiating discussions, inviting quieter peers to speak, summarizing consensus, and disagreeing diplomatically.",
                        "# 'Sarah, we would love to hear your thoughts on the database migration plan.'",
                        "Script an exchange where you guide a derailed group discussion back to the core agenda.",
                        "Focus on common ground before addressing points of friction"
                    ],
                    [
                        "Presentation skills",
                        "2 hours",
                        "Slide deck structuring (Signposting: Agenda -> Problem -> Solution -> Demo -> Q&A), vocal variety.",
                        "# 'First, we will examine the problem; next, our architectural approach; and finally, the live demo.'",
                        "Create a 5-slide outline with speaking notes for an architectural proposal presentation.",
                        "Signpost transitions between presentation sections"
                    ],
                    [
                        "Email writing",
                        "1.5 hours",
                        "Subject line clarity, greeting etiquette, BLUF (Bottom Line Up Front), call to action (CTA), and sign-offs.",
                        "# Subject: Action Required: Database Migration Scheduled for Oct 15\n# BLUF: Maintenance window is 2-4 AM UTC.",
                        "Draft a professional email requesting approval from a technical lead for an architecture change.",
                        "State the primary request or deadline in the first two sentences"
                    ],
                    [
                        "Interview question practice",
                        "2 hours",
                        "STAR Method: Situation, Task, Action, Result; quantifying results with metrics.",
                        "# S: Outage at peak hours. T: Restore service. A: Identified memory leak. R: 99.9% uptime restored.",
                        "Structure a complete STAR answer to 'Describe a time you solved a difficult technical bug under pressure.'",
                        "Dedicate 70% of response time to Action and Result"
                    ],
                    [
                        "Describing projects and experiences",
                        "1.5 hours",
                        "Elevator project summaries: Tech stack, personal contribution, challenge overcome, measurable impact.",
                        "# 'I engineered a recommendation service using FastAPI and scikit-learn, cutting response latency by 35%.'",
                        "Write a 90-second technical project walkthrough highlighting your specific individual code contributions.",
                        "Always quantify results where possible"
                    ],
                    [
                        "Expressing opinions clearly",
                        "1 hour",
                        "Hedging appropriately ('The data suggests that...'), asserting recommendations with evidence.",
                        "# 'Based on our load test benchmarks, migrating to PostgreSQL appears to be the most viable path.'",
                        "Write a balanced technical recommendation comparing two competing programming languages.",
                        "Support subjective recommendations with objective performance data"
                    ],
                    [
                        "Pronunciation and fluency practice",
                        "1 hour",
                        "Word stress (PRO-ject vs pro-JECT), syllable timing, thought groups, and pausing for emphasis.",
                        "# Pause at punctuation boundaries; stress key content nouns and verbs rather than prepositions.",
                        "Read aloud a 100-word technical passage with intentional pauses and clear consonant articulation.",
                        "Pause for emphasis before delivering key statistics"
                    ]
                ]
            },
            {
                "level": 3,
                "title": "Level 3 \u2013 Advanced",
                "difficulty": "Advanced",
                "estimated_hours": "24 hours",
                "description": "Executive presence, persuasive communication, mock interviews, technical whitepaper writing, and crisis communication.",
                "learning_objectives": [
                    "Deliver high-impact technical presentations to cross-functional executive stakeholders",
                    "Navigate tough technical and behavioral mock interview interrogations with confidence",
                    "Author persuasive technical proposals, architecture decision records (ADRs), and post-mortems",
                    "De-escalate high-pressure workplace conflicts and lead structured feedback conversations",
                    "Communicate complex trade-offs with brevity, precision, and persuasive executive presence"
                ],
                "topics": [
                    [
                        "Professional communication",
                        "2 hours",
                        "Executive presence, communication brevity, high-stakes stakeholder alignment, and managing upwards.",
                        "# Rule of 3: Structure arguments into at most 3 concise, high-impact pillars.",
                        "Summarize a 10-page architecture document into a 1-page executive brief for a CTO.",
                        "Lead with business impact, cost, and risk factors"
                    ],
                    [
                        "Advanced grammar and sentence variety",
                        "1.5 hours",
                        "Parallel structure, inversion for emphasis, subjunctive mood, and eliminating wordiness.",
                        "# Parallel: 'He was responsible for designing the database, coding the API, and testing the UI.'",
                        "Refactor 5 bloated sentences into tight, crisp professional prose with parallel structure.",
                        "Maintain grammatical parallelism in lists and series"
                    ],
                    [
                        "Technical presentation delivery",
                        "2 hours",
                        "Engaging live technical demos, handling slide malfunctions, pacing, and executive storytelling.",
                        "# Hook the audience in the first 30 seconds with a striking problem statement or metric.",
                        "Record or deliver a 5-minute technical demo addressing architecture, scale, and future roadmap.",
                        "Always have a backup video or screenshot plan for live demos"
                    ],
                    [
                        "Mock HR and technical interviews",
                        "2.5 hours",
                        "Handling tough questions ('What is your greatest technical failure?'), salary negotiations, and culture fit.",
                        "# Acknowledge mistakes openly, highlight root cause analysis, and detail permanent safeguards installed.",
                        "Conduct a mock interview answer addressing a catastrophic production deployment failure.",
                        "Focus on lessons learned and proactive preventative safeguards"
                    ],
                    [
                        "Advanced group discussion practice",
                        "2 hours",
                        "Navigating heated architectural debates, synthesizing divergent opinions, and steering to consensus.",
                        "# 'We have two strong proposals here; let us compare their trade-offs against our Q3 throughput goal.'",
                        "Simulate resolving an architectural dispute between microservices vs monolithic deployment.",
                        "Use objective evaluation criteria to depersonalize decisions"
                    ],
                    [
                        "Persuasive communication",
                        "2 hours",
                        "Aristotle's rhetorical triangle (Ethos, Pathos, Logos), Cialdini's influence principles, and objection handling.",
                        "# Logos: Benchmarks prove 4x speedup. Ethos: Standard in industry. Pathos: Relieves on-call burnout.",
                        "Write a persuasive proposal convincing management to allocate two sprints for technical debt refactoring.",
                        "Pair logical data (Logos) with team health impact (Pathos)"
                    ],
                    [
                        "Professional email and report writing",
                        "2 hours",
                        "Incident Post-Mortems (Blameless Root Cause Analysis), Architecture Decision Records (ADRs).",
                        "# ADR Structure: Title | Status | Context | Decision | Consequences (Pros & Cons).",
                        "Draft a blameless post-mortem for a 45-minute database downtime incident.",
                        "Focus on systemic process improvements, not personal blame"
                    ],
                    [
                        "Storytelling and structured explanations",
                        "2 hours",
                        "Narrative arcs in business: Context -> Conflict -> Climax -> Resolution -> Vision.",
                        "# Take the audience on a journey: from initial struggling architecture to triumph of new system.",
                        "Craft a compelling narrative describing the evolution of your AI career journey and projects.",
                        "Conflict makes technical triumphs memorable"
                    ],
                    [
                        "Handling follow-up questions",
                        "1.5 hours",
                        "Active listening before responding, bridging techniques ('That is an important point, and what we found was...').",
                        "# If you do not know: 'I do not have the exact number on hand; I will verify and follow up by 3 PM.'",
                        "Practice answering 3 aggressive cross-examination questions regarding your model's accuracy claims.",
                        "Never invent data; admit unknowns and promise timely follow-up"
                    ],
                    [
                        "Communicating under pressure",
                        "2 hours",
                        "Maintaining emotional composure, clear crisis broadcast during P0 outages, and de-escalation.",
                        "# P0 Broadcast: Current Status | User Impact | Immediate Mitigation in Progress | Next Update in 15 mins.",
                        "Draft a real-time incident notification message to enterprise customers during an active outage.",
                        "Keep tone calm, transparent, and authoritative"
                    ],
                    [
                        "Workplace communication",
                        "1.5 hours",
                        "Cross-functional collaboration with product managers, UX designers, and non-technical stakeholders.",
                        "# Translate technical constraints into product impact: 'This indexing work will cut checkout load times in half.'",
                        "Write an explanation to a Product Manager explaining why a requested feature requires 3 extra days.",
                        "Explain trade-offs in terms of user experience and stability"
                    ],
                    [
                        "Giving and receiving feedback",
                        "1.5 hours",
                        "SBI Model (Situation, Behavior, Impact), receiving critical reviews with growth mindset.",
                        "# Situation: During yesterday's sprint demo. Behavior: Interrupted the client twice. Impact: Client felt unheard.",
                        "Construct actionable, constructive peer feedback for a teammate whose PRs lack unit tests.",
                        "Address specific observable behaviors, not personal character"
                    ],
                    [
                        "Confidence, clarity, and fluency evaluation",
                        "2 hours",
                        "Eliminating filler words (um, uh, like, basically), steady vocal projection, and purposeful pausing.",
                        "# Replace filler sounds with silent 1-second pauses; silent pauses convey thoughtfulness and authority.",
                        "Record a 2-minute impromptu response on a technical topic with zero filler words.",
                        "Embrace silence instead of filling pauses with 'um' or 'like'"
                    ]
                ]
            }
        ]
    }
}

def get_all_skills() -> List[Dict[str, Any]]:
    """Returns metadata list for all 7 available skills."""
    skills = []
    for slug, s in CURRICULUM.items():
        skills.append({
            "skill": s["skill"],
            "skill_slug": s["skill_slug"],
            "category": s["category"],
            "icon": s["icon"],
            "description": s["description"],
            "total_levels": 3
        })
    return skills

def get_skill_curriculum(skill_slug: str) -> Dict[str, Any]:
    """Returns full 3-level curriculum for a specified skill."""
    return CURRICULUM.get(skill_slug.lower())

def get_level_curriculum(skill_slug: str, level_num: int) -> Dict[str, Any]:
    """Returns specific level curriculum with all topics and practice challenges."""
    skill_data = CURRICULUM.get(skill_slug.lower())
    if not skill_data:
        # Try matching by skill name
        for s in CURRICULUM.values():
            if s["skill"].lower() == skill_slug.lower():
                skill_data = s
                break
    if not skill_data:
        return None
    for lvl in skill_data["levels"]:
        if lvl["level"] == level_num:
            return lvl
    return None

def get_all_curriculum_levels() -> List[Dict[str, Any]]:
    """Returns flat list of all 21 levels (7 skills * 3 levels)."""
    all_levels = []
    for s_slug, s_data in CURRICULUM.items():
        for lvl in s_data["levels"]:
            level_id = f"{s_slug}_lvl_{lvl['level']}"
            all_levels.append({
                "id": level_id,
                "skill": s_data["skill"],
                "skill_slug": s_slug,
                "category": s_data["category"],
                "icon": s_data["icon"],
                **lvl
            })
    return all_levels
