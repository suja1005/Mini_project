import json
import random
import re
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.database.connection import get_database
from app.services.evidence_service import get_or_create_user_evidence


def _question(
    question_id: str,
    skill: str,
    topic: str,
    difficulty: str,
    prompt: str,
    answer: str,
    options: Optional[List[str]] = None,
    accepted_answers: Optional[List[str]] = None,
    required_terms: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "question_id": question_id,
        "skill": skill,
        "topic": topic,
        "difficulty": difficulty,
        "type": "mcq" if options else "short_answer",
        "question": prompt,
        "options": options or [],
        "correct_answer": answer,
        "accepted_answers": accepted_answers or [answer],
        "required_terms": required_terms or [],
    }


QUESTION_BANK: Dict[str, List[Dict[str, Any]]] = {
    "Python": [
        _question("py-1", "Python", "Data types", "Beginner", "What is printed by `print(type(3.0).__name__)`?", "float", ["int", "float", "str", "decimal"]),
        _question("py-2", "Python", "Loops", "Beginner", "What is printed by `total = 0\nfor n in range(1, 4):\n    total += n\nprint(total)`?", "6", ["3", "6", "10", "123"]),
        _question("py-3", "Python", "Functions", "Intermediate", "Which value is returned by this function call?\n`def add_item(items, item):\n    items.append(item)\n    return len(items)`\n`add_item(['a'], 'b')`", "2", ["1", "2", "['a', 'b']", "None"]),
        _question("py-4", "Python", "Dictionaries", "Intermediate", "Which expression safely returns 0 when key `score` is missing from `data`?", "data.get('score', 0)", ["data['score']", "data.get('score', 0)", "data.score or 0", "data.find('score')"]),
        _question("py-5", "Python", "Debugging", "Intermediate", "Fix the off-by-one error so this sums all values in `values`: `for i in range(len(values) - 1): total += values[i]`.", "for i in range(len(values)): total += values[i]", accepted_answers=["for i in range(len(values)): total += values[i]", "for value in values: total += value"]),
        _question("py-6", "Python", "OOP", "Advanced", "In Python, which method is called to create a new instance before `__init__` initializes it?", "__new__", ["__init__", "__new__", "__call__", "__enter__"]),
        _question("py-7", "Python", "Problem solving", "Advanced", "Write a Python expression that returns the unique values of `items` while preserving their original order.", "list(dict.fromkeys(items))"),
    ],
    "Java": [
        _question("java-1", "Java", "Types", "Beginner", "Which Java type stores a whole number using 32 bits?", "int", ["int", "boolean", "char", "double"]),
        _question("java-2", "Java", "Loops", "Beginner", "How many times does `for (int i = 0; i < 3; i++)` execute its body?", "3", ["2", "3", "4", "It never executes"]),
        _question("java-3", "Java", "Collections", "Intermediate", "Which collection preserves insertion order and allows duplicate elements?", "ArrayList", ["HashSet", "ArrayList", "TreeSet", "Map"]),
        _question("java-4", "Java", "Debugging", "Intermediate", "Which keyword prevents a Java class from being subclassed?", "final", ["static", "final", "private", "abstract"]),
        _question("java-5", "Java", "OOP", "Advanced", "Which principle allows a subclass to provide its own implementation of an inherited method?", "Method overriding", ["Method overloading", "Method overriding", "Encapsulation", "Composition"]),
        _question("java-6", "Java", "Coding task", "Advanced", "Write a Java `for` loop header that visits indexes from 0 through `n - 1`.", "for (int i = 0; i < n; i++)", accepted_answers=["for (int i=0; i<n; i++)", "for(int i=0;i<n;i++)"]),
    ],
    "C": [
        _question("c-1", "C", "Types", "Beginner", "Which format specifier is used to print an `int` with `printf`?", "%d", ["%d", "%f", "%c", "%s"]),
        _question("c-2", "C", "Pointers", "Beginner", "What does the `&` operator return when applied to a variable?", "Its memory address", ["Its value", "Its memory address", "Its data type", "The address of the next variable"]),
        _question("c-3", "C", "Loops", "Intermediate", "What is printed by `int a[] = {2, 4, 6}; printf(\"%d\", a[1]);`?", "4", ["2", "4", "6", "1"]),
        _question("c-4", "C", "Debugging", "Intermediate", "Which function should be used to release memory allocated by `malloc`?", "free", ["delete", "remove", "free", "clear"]),
        _question("c-5", "C", "Arrays", "Advanced", "Write the C expression for the number of elements in array `values` while it is still in scope as an array.", "sizeof(values) / sizeof(values[0])", accepted_answers=["sizeof(values)/sizeof(values[0])", "sizeof(values) / sizeof(values[0])"]),
        _question("c-6", "C", "Coding task", "Advanced", "Write a C `for` loop header that visits indexes from 0 through `n - 1`.", "for (int i = 0; i < n; i++)", accepted_answers=["for (int i=0; i<n; i++)", "for(int i=0;i<n;i++)"]),
    ],
    "C++": [
        _question("cpp-1", "C++", "Types", "Beginner", "Which C++ keyword introduces a class definition?", "class", ["struct", "class", "object", "record"]),
        _question("cpp-2", "C++", "STL", "Beginner", "Which standard container stores elements in a resizable contiguous sequence?", "std::vector", ["std::set", "std::map", "std::vector", "std::queue"]),
        _question("cpp-3", "C++", "OOP", "Intermediate", "What does a virtual method enable when called through a base-class pointer?", "Runtime polymorphism", ["Compile-time constants", "Runtime polymorphism", "Automatic memory allocation", "Namespace lookup"]),
        _question("cpp-4", "C++", "Debugging", "Intermediate", "Which smart pointer is appropriate when one object has exclusive ownership of a resource?", "std::unique_ptr", ["std::shared_ptr", "std::unique_ptr", "std::weak_ptr", "A raw pointer"]),
        _question("cpp-5", "C++", "Algorithms", "Advanced", "Which standard algorithm sorts a vector `values` in ascending order?", "std::sort(values.begin(), values.end())", accepted_answers=["std::sort(values.begin(), values.end())", "sort(values.begin(), values.end())"]),
        _question("cpp-6", "C++", "Coding task", "Advanced", "Write a range-based C++ loop header that visits each `int value` in `values`.", "for (int value : values)", accepted_answers=["for(int value:values)", "for (int value : values)"]),
    ],
    "JavaScript": [
        _question("js-1", "JavaScript", "Variables", "Beginner", "Which declaration creates a block-scoped variable that can be reassigned?", "let", ["var", "let", "const", "static"]),
        _question("js-2", "JavaScript", "Output prediction", "Beginner", "What does `console.log(2 + '3')` print?", "23", ["5", "23", "NaN", "undefined"]),
        _question("js-3", "JavaScript", "Functions", "Intermediate", "What does an `async` function always return?", "A Promise", ["A callback", "A Promise", "An iterator", "A DOM node"]),
        _question("js-4", "JavaScript", "Debugging", "Intermediate", "Which array method returns a new array containing only items that pass a predicate?", "filter", ["map", "filter", "reduce", "forEach"]),
        _question("js-5", "JavaScript", "Problem solving", "Advanced", "Which operator safely reads `name` when `user` may be nullish?", "user?.name", ["user.name?", "user?.name", "user??.name", "user &&! name"]),
        _question("js-6", "JavaScript", "Coding task", "Advanced", "Write a JavaScript expression that creates a new array containing only positive numbers from `values`.", "values.filter(value => value > 0)", accepted_answers=["values.filter(value=>value>0)", "values.filter(value => value > 0)"]),
    ],
    "HTML": [
        _question("html-1", "HTML", "Semantic markup", "Beginner", "Which element represents the main content unique to a page?", "<main>", ["<div>", "<main>", "<section>", "<footer>"]),
        _question("html-2", "HTML", "Accessibility", "Beginner", "Which attribute provides alternative text for an informative image?", "alt", ["title", "name", "alt", "role"]),
        _question("html-3", "HTML", "Forms", "Intermediate", "Which form attribute associates a label with an input whose id is `email`?", "for=\"email\"", ["id=\"email\"", "for=\"email\"", "name=\"email\"", "aria-label=\"email\""]),
    ],
    "CSS": [
        _question("css-1", "CSS", "Selectors", "Beginner", "Which selector targets an element with `id=\"hero\"`?", "#hero", [".hero", "#hero", "hero", "*hero"]),
        _question("css-2", "CSS", "Layout", "Beginner", "Which Flexbox property aligns items along the main axis?", "justify-content", ["align-items", "justify-content", "align-content", "place-items"]),
        _question("css-3", "CSS", "Responsive design", "Intermediate", "Which CSS feature applies rules based on viewport width?", "@media", ["@supports", "@media", "@import", "@container-name"]),
    ],
    "React": [
        _question("react-1", "React", "Components", "Beginner", "Which syntax is used to pass data from a parent component to a child?", "Props", ["State", "Props", "Refs", "Effects"]),
        _question("react-2", "React", "Hooks", "Intermediate", "Which hook should synchronize a component with an external system after rendering?", "useEffect", ["useMemo", "useEffect", "useState", "useRef"]),
        _question("react-3", "React", "State", "Advanced", "Why should a React state array be replaced instead of mutated in place?", "A new reference lets React detect the update", ["Arrays cannot be mutated in JavaScript", "A new reference lets React detect the update", "It automatically sorts the array", "Mutation prevents event handlers"]),
    ],
    "SQL": [
        _question("sql-1", "SQL", "Queries", "Beginner", "Which clause filters rows before grouping?", "WHERE", ["HAVING", "WHERE", "ORDER BY", "LIMIT"]),
        _question("sql-2", "SQL", "Aggregation", "Intermediate", "Write a query fragment that returns the average salary for each department from table `employees`.", "SELECT department, AVG(salary) FROM employees GROUP BY department", accepted_answers=["select department, avg(salary) from employees group by department", "select department,avg(salary) from employees group by department"]),
        _question("sql-3", "SQL", "Joins", "Intermediate", "Which join keeps every row from the left table and matching rows from the right table?", "LEFT JOIN", ["INNER JOIN", "LEFT JOIN", "CROSS JOIN", "FULL JOIN"]),
        _question("sql-4", "SQL", "Debugging", "Advanced", "Which clause correctly filters grouped results to departments with more than 5 employees?", "HAVING COUNT(*) > 5", ["WHERE COUNT(*) > 5", "HAVING COUNT(*) > 5", "ORDER BY COUNT(*) > 5", "LIMIT COUNT(*) > 5"]),
    ],
    "MongoDB": [
        _question("mongo-1", "MongoDB", "Documents", "Beginner", "What is the default unique identifier field in a MongoDB document?", "_id", ["id", "_id", "key", "uuid"]),
        _question("mongo-2", "MongoDB", "Queries", "Intermediate", "Which operator matches documents where `score` is at least 70?", "$gte", ["$gt", "$gte", "$lte", "$eq"]),
        _question("mongo-3", "MongoDB", "Aggregation", "Advanced", "Which aggregation stage groups documents by a field and calculates totals?", "$group", ["$match", "$sort", "$group", "$project"]),
        _question("mongo-4", "MongoDB", "Query writing", "Advanced", "Write a MongoDB filter that selects documents whose `score` is at least 70.", '{"score": {"$gte": 70}}', accepted_answers=['{"score":{"$gte":70}}', "{'score': {'$gte': 70}}"]),
    ],
    "Machine Learning": [
        _question("ml-1", "Machine Learning", "Evaluation", "Beginner", "For a highly imbalanced classification problem, which metric is generally more informative than accuracy alone?", "F1 score", ["Accuracy", "F1 score", "Mean squared error", "R-squared"]),
        _question("ml-2", "Machine Learning", "Model validation", "Intermediate", "What problem does a separate test set help detect?", "Poor generalization to unseen data", ["Slow training", "Poor generalization to unseen data", "Missing feature names", "Unbalanced batches"]),
        _question("ml-3", "Machine Learning", "Overfitting", "Advanced", "A model scores very well on training data but poorly on validation data. What is the most likely issue?", "Overfitting", ["Underfitting", "Overfitting", "Data normalization", "High bias only"]),
    ],
    "Data Analysis": [
        _question("da-1", "Data Analysis", "Data quality", "Beginner", "A dataset contains missing values in a numeric feature. What should you do first?", "Inspect the missingness and its context before choosing a treatment", ["Replace every value with zero", "Delete the entire dataset", "Inspect the missingness and its context before choosing a treatment", "Convert the column to text"]),
        _question("da-2", "Data Analysis", "Statistics", "Intermediate", "Which measure is usually more robust to extreme outliers?", "Median", ["Mean", "Median", "Range", "Variance"]),
        _question("da-3", "Data Analysis", "Interpretation", "Advanced", "A chart shows correlation between ad spend and sales. What conclusion is justified without further analysis?", "The variables are associated, but causation is not established", ["Ad spend caused all sales growth", "The variables are associated, but causation is not established", "Sales caused ad spend", "There is no relationship"]),
    ],
    "Computer Networks": [
        _question("net-1", "Computer Networks", "Protocols", "Beginner", "Which protocol translates domain names into IP addresses?", "DNS", ["DHCP", "DNS", "HTTP", "ARP"]),
        _question("net-2", "Computer Networks", "Transport", "Intermediate", "Which transport protocol provides ordered, reliable delivery?", "TCP", ["UDP", "TCP", "IP", "ICMP"]),
        _question("net-3", "Computer Networks", "Troubleshooting", "Advanced", "A host can reach an IP address but not a hostname. Which service should be checked first?", "DNS resolution", ["DHCP lease time", "DNS resolution", "Ethernet duplex", "NAT table size"]),
    ],
    "Problem Solving": [
        _question("ps-1", "Problem Solving", "Logical reasoning", "Beginner", "A delivery route has 4 stops. You can visit each stop once and must end where you started. What should you clarify before comparing routes?", "The allowed travel connections and route constraints", ["The driver's favorite stop", "The allowed travel connections and route constraints", "The color of the vehicle", "The number of letters in each location"]),
        _question("ps-2", "Problem Solving", "Debugging", "Intermediate", "A report is wrong only for records added this week. What is the best first step?", "Compare recent records and recent processing changes", ["Rewrite the whole reporting system", "Compare recent records and recent processing changes", "Delete the new records", "Assume the database is unavailable"]),
        _question("ps-3", "Problem Solving", "Algorithms", "Advanced", "You need to find a value in a sorted list repeatedly. Which approach is generally most efficient?", "Binary search", ["Scan the full list every time", "Binary search", "Shuffle and retry", "Sort the list before every comparison"]),
    ],
    "Communication": [
        _question("com-1", "Communication", "Workplace communication", "Beginner", "A teammate requests a task update, but you are blocked. Which response is most useful?", "State the blocker, its impact, and the specific help or decision needed", ["Say only 'working on it'", "State the blocker, its impact, and the specific help or decision needed", "Wait until the deadline passes", "Blame another team"]),
        _question("com-2", "Communication", "Written communication", "Intermediate", "A client reports an issue without reproduction details. What should your written reply do first?", "Acknowledge the issue and ask concise, specific questions to reproduce it", ["Promise a fix date without investigation", "Acknowledge the issue and ask concise, specific questions to reproduce it", "Ask them to stop using the product", "Forward the message without context"]),
        _question("com-3", "Communication", "Presentation", "Advanced", "When presenting a technical decision to a non-technical audience, what should lead the explanation?", "The user or business impact, followed by the rationale", ["Implementation details only", "The user or business impact, followed by the rationale", "A list of acronyms", "The longest code sample"]),
        _question("com-4", "Communication", "Written status update", "Advanced", "Write a concise workplace status update that clearly states a blocker, its impact, and the next step.", "Blocker: the API response issue. Impact: integration testing is delayed. Next step: I am testing a fix and will share an update.", required_terms=["blocker", "impact", "next step"]),
    ],
    "Analytical Thinking": [
        _question("analytical-1", "Analytical Thinking", "Data interpretation", "Beginner", "A metric rose from 40 to 50. What is its percentage increase relative to the starting value?", "25%", ["10%", "20%", "25%", "50%"]),
        _question("analytical-2", "Analytical Thinking", "Decision making", "Intermediate", "Two experiments changed several variables at once. Why is it hard to identify the cause of the outcome?", "The effects of the changed variables are confounded", ["The sample has a median", "The effects of the changed variables are confounded", "The result is necessarily random", "The outcome cannot be measured"]),
        _question("analytical-3", "Analytical Thinking", "Prioritization", "Advanced", "Which issue should be investigated first when comparing options?", "The option with the highest expected impact relative to its cost and risk", ["The option with the newest name", "The option with the highest expected impact relative to its cost and risk", "The option with the most steps", "The option chosen most recently"]),
    ],
    "Aptitude": [
        _question("apt-1", "Aptitude", "Numerical reasoning", "Beginner", "A service handles 120 requests in 4 minutes at a constant rate. How many requests does it handle per minute?", "30", ["20", "30", "40", "480"]),
        _question("apt-2", "Aptitude", "Logical reasoning", "Intermediate", "What number comes next: 3, 6, 12, 24, ...?", "48", ["36", "42", "48", "51"]),
        _question("apt-3", "Aptitude", "Numerical reasoning", "Advanced", "A team completes 3/5 of a task in 6 hours at a constant rate. How many hours would the full task take?", "10", ["8", "9", "10", "12"]),
    ],
    "Mathematics": [
        _question("math-1", "Mathematics", "Statistics", "Beginner", "What is the mean of 2, 4, and 6?", "4", ["3", "4", "6", "12"]),
        _question("math-2", "Mathematics", "Probability", "Intermediate", "A fair coin is flipped twice. What is the probability of getting two heads?", "1/4", ["1/2", "1/3", "1/4", "3/4"]),
        _question("math-3", "Mathematics", "Algebra", "Advanced", "If 3x + 2 = 14, what is x?", "4", ["3", "4", "5", "6"]),
    ],
    "Git": [
        _question("git-1", "Git", "Version control", "Beginner", "Which command creates a new commit from staged changes?", "git commit", ["git add", "git commit", "git status", "git fetch"]),
        _question("git-2", "Git", "Branches", "Intermediate", "Which command incorporates commits from another branch into the current branch?", "git merge", ["git init", "git merge", "git clone", "git log"]),
        _question("git-3", "Git", "Debugging", "Advanced", "Which command helps identify the commit that introduced a regression by binary search?", "git bisect", ["git stash", "git bisect", "git tag", "git clean"]),
    ],
    "Teamwork": [
        _question("team-1", "Teamwork", "Collaboration", "Beginner", "A teammate disagrees with your approach. What is the most constructive next step?", "Compare the approaches against shared requirements and evidence", ["Escalate immediately", "Compare the approaches against shared requirements and evidence", "Stop communicating", "Implement both without discussion"]),
        _question("team-2", "Teamwork", "Conflict resolution", "Intermediate", "A handoff repeatedly misses details. What should the team do?", "Agree on a lightweight handoff checklist and review its effectiveness", ["Add more meetings without an agenda", "Agree on a lightweight handoff checklist and review its effectiveness", "Keep the process unchanged", "Assign blame publicly"]),
    ],
    "Adaptability": [
        _question("adapt-1", "Adaptability", "Change management", "Beginner", "A project requirement changes. What should you do before changing your implementation?", "Confirm the new outcome, constraints, and impact on existing work", ["Discard all existing work", "Confirm the new outcome, constraints, and impact on existing work", "Ignore the change", "Change unrelated components"]),
        _question("adapt-2", "Adaptability", "Learning", "Intermediate", "You are assigned an unfamiliar tool under a deadline. What is the best first action?", "Identify the task-critical features and validate a small working example", ["Read every page of documentation first", "Identify the task-critical features and validate a small working example", "Avoid the task", "Install unrelated tools"]),
    ],
}


ALIASES = {
    "ml": "Machine Learning",
    "js": "JavaScript",
    "htmlcss": "HTML",
    "htmlandcss": "HTML",
    "problem solving": "Problem Solving",
    "problemsolving": "Problem Solving",
    "analyticalthinking": "Analytical Thinking",
    "machinelearning": "Machine Learning",
    "dataanalysis": "Data Analysis",
    "computernetworks": "Computer Networks",
    "mongodb": "MongoDB",
    "aptitude": "Aptitude",
    "criticalthinking": "Analytical Thinking",
    "communicationskills": "Communication",
}

ROADMAP_CONTENT = {
    "Python": (["Variables, types, and control flow", "Functions and collections"], ["Modules, exceptions, and file handling", "Classes, testing, and common algorithms"], ["Concurrency, profiling, and architecture", "Packaging and production-quality Python"]),
    "Java": (["Types, control flow, and methods", "Arrays, strings, and collections"], ["Object-oriented design and exceptions", "Generics, streams, and unit testing"], ["Concurrency and JVM performance", "Design patterns and service architecture"]),
    "C": (["Types, operators, and control flow", "Functions, arrays, and strings"], ["Pointers, structs, and dynamic memory", "Debugging and modular programs"], ["Memory safety and performance", "Systems programming and build tooling"]),
    "C++": (["Types, control flow, and functions", "Strings, vectors, and algorithms"], ["Classes, RAII, and templates", "STL algorithms and testing"], ["Concurrency and performance", "Modern C++ design and architecture"]),
    "JavaScript": (["Values, variables, and control flow", "Functions, arrays, and objects"], ["Promises, modules, and browser APIs", "Testing and error handling"], ["Performance and event-loop behavior", "Accessible, maintainable application architecture"]),
    "HTML": (["Semantic elements and document structure", "Forms and accessible labels"], ["Accessible interactions and validation", "Responsive content structures"], ["Web performance and SEO", "Design systems and maintainable templates"]),
    "CSS": (["Selectors, cascade, and box model", "Flexbox and responsive layouts"], ["Grid, custom properties, and components", "Accessibility and browser debugging"], ["Architecture, animations, and performance", "Design systems and cross-browser quality"]),
    "React": (["Components, props, and JSX", "State and event handling"], ["Effects, forms, and data fetching", "Routing and component testing"], ["Rendering performance and accessibility", "Application architecture and resilient state"]),
    "SQL": (["SELECT, filtering, and sorting", "Aggregates and grouping"], ["Joins, subqueries, and transactions", "Indexes and query plans"], ["Window functions and optimization", "Data modeling and reliable migrations"]),
    "MongoDB": (["Documents, collections, and CRUD", "Filters and projections"], ["Indexes and aggregation pipelines", "Schema design and atomic updates"], ["Replication and sharding concepts", "Performance and production operations"]),
    "Machine Learning": (["Supervised learning and train/test splits", "Metrics and data preprocessing"], ["Feature engineering and model selection", "Cross-validation and error analysis"], ["Deployment, drift, and monitoring", "Reproducible ML pipelines"]),
    "Data Analysis": (["Data cleaning and descriptive statistics", "Tables and visual summaries"], ["Exploratory analysis and SQL", "Uncertainty and stakeholder questions"], ["Experiment design and reproducible reports", "Insight communication and decision impact"]),
    "Computer Networks": (["OSI/TCP-IP layers and addressing", "DNS, DHCP, and common protocols"], ["TCP/UDP behavior and routing", "Network diagnostics and security basics"], ["Network design and performance", "Resilience, monitoring, and incident analysis"]),
    "Problem Solving": (["Clarifying a problem and constraints", "Breaking work into testable steps"], ["Compare solutions and debug systematically", "Use data to prioritize root causes"], ["Analyze tradeoffs and edge cases", "Design measurable, sustainable solutions"]),
    "Communication": (["Clear status updates and active listening", "Concise workplace writing"], ["Explain technical decisions to stakeholders", "Give and receive actionable feedback"], ["Facilitate alignment and negotiation", "Present evidence-based recommendations"]),
    "Analytical Thinking": (["Read tables, charts, and percentages", "Separate observations from assumptions"], ["Compare evidence and competing explanations", "Make decisions under constraints"], ["Evaluate uncertainty and tradeoffs", "Communicate analysis with caveats"]),
    "Aptitude": (["Number patterns and arithmetic", "Ratios, percentages, and estimation"], ["Logical deduction and word problems", "Multi-step numerical reasoning"], ["Timed mixed reasoning sets", "Check assumptions and solution efficiency"]),
    "Mathematics": (["Algebra and arithmetic fluency", "Descriptive statistics"], ["Probability and distributions", "Linear algebra and functions"], ["Optimization and statistical inference", "Apply mathematical models to career problems"]),
    "Git": (["Working tree, staging, and commits", "Branches and merge basics"], ["Resolve conflicts and use remotes", "Review history and collaboration workflows"], ["Bisect regressions and recover safely", "Release strategy and repository hygiene"]),
    "Teamwork": (["Agree on shared goals and roles", "Reliable task handoffs"], ["Resolve disagreement with evidence", "Coordinate dependencies and feedback"], ["Facilitate cross-functional decisions", "Improve team processes using outcomes"]),
    "Adaptability": (["Clarify changing requirements", "Learn unfamiliar tools in small steps"], ["Re-plan around new constraints", "Validate assumptions with stakeholders"], ["Manage uncertainty and tradeoffs", "Turn feedback into measurable iteration"]),
}


RESOURCE_LINKS = {
    "Python": [("Python Tutorial", "https://docs.python.org/3/tutorial/"), ("Python Course", "https://www.youtube.com/watch?v=rfscVS0vtbw")],
    "Java": [("Dev.java Learn", "https://dev.java/learn/"), ("Java Course", "https://www.youtube.com/watch?v=grEKMHGYyns")],
    "C": [("GNU C manual", "https://www.gnu.org/software/gnu-c-manual/"), ("C Programming Course", "https://www.youtube.com/watch?v=KJgsSFOSQv0")],
    "C++": [("C++ reference", "https://en.cppreference.com/w/"), ("C++ Course", "https://www.youtube.com/watch?v=vLnPwxZdW4Y")],
    "JavaScript": [("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"), ("JavaScript Course", "https://www.youtube.com/watch?v=PkZNo7MFNFg")],
    "HTML": [("MDN HTML", "https://developer.mozilla.org/en-US/docs/Learn/HTML"), ("HTML Course", "https://www.youtube.com/watch?v=kUMe1FH4CHE")],
    "CSS": [("MDN CSS", "https://developer.mozilla.org/en-US/docs/Learn/CSS"), ("CSS Course", "https://www.youtube.com/watch?v=OXGznpKZ_sA")],
    "React": [("React Learn", "https://react.dev/learn"), ("React Course", "https://www.youtube.com/watch?v=bMknfKXIFA8")],
    "SQL": [("PostgreSQL Tutorial", "https://www.postgresql.org/docs/current/tutorial.html"), ("SQL Course", "https://www.youtube.com/watch?v=HXV3zeQKqGY")],
    "MongoDB": [("MongoDB University", "https://learn.mongodb.com/"), ("MongoDB Course", "https://www.youtube.com/watch?v=c2M-rlkkT5o")],
    "Machine Learning": [("scikit-learn User Guide", "https://scikit-learn.org/stable/user_guide.html"), ("ML Course", "https://www.youtube.com/watch?v=NWONeJKn6kc")],
    "Data Analysis": [("pandas Getting Started", "https://pandas.pydata.org/docs/getting_started/"), ("Data Analysis Course", "https://www.youtube.com/watch?v=r-uOLxNrNk8")],
    "Computer Networks": [("Cloudflare Learning Center", "https://www.cloudflare.com/learning/"), ("Networking Course", "https://www.youtube.com/watch?v=qiQR5rTSshw")],
    "Problem Solving": [("HackerRank Problem Solving", "https://www.hackerrank.com/domains/algorithms"), ("Problem Solving Course", "https://www.youtube.com/watch?v=8hly31xKli0")],
    "Communication": [("Purdue OWL Workplace Writing", "https://owl.purdue.edu/owl/subject_specific_writing/professional_technical_writing/index.html"), ("Workplace Communication", "https://www.youtube.com/watch?v=HAnw168huqA")],
    "Analytical Thinking": [("Our World in Data", "https://ourworldindata.org/"), ("Data Literacy", "https://www.youtube.com/watch?v=5Zg-C8AAIGg")],
    "Aptitude": [("Khan Academy Arithmetic", "https://www.khanacademy.org/math/arithmetic"), ("Logical Reasoning", "https://www.youtube.com/watch?v=3VbWkGz7k4U")],
    "Mathematics": [("Khan Academy Statistics", "https://www.khanacademy.org/math/statistics-probability"), ("Statistics Course", "https://www.youtube.com/watch?v=xxpc-HPKN28")],
    "Git": [("Pro Git Book", "https://git-scm.com/book/en/v2"), ("Git Course", "https://www.youtube.com/watch?v=RGOj5yH7evk")],
    "Teamwork": [("Atlassian Team Playbook", "https://www.atlassian.com/team-playbook"), ("Teamwork Skills", "https://www.youtube.com/watch?v=VZg5r9iJb8Y")],
    "Adaptability": [("MindTools Adaptability", "https://www.mindtools.com/a4wo118/adaptability/"), ("Adaptability at Work", "https://www.youtube.com/watch?v=9cKmXvG1p0g")],
}


def score_category(score: int) -> str:
    if score < 50:
        return "Weak"
    if score < 70:
        return "Needs Improvement"
    if score < 85:
        return "Good"
    return "Strong"


def _canonical_skill(name: str) -> Optional[str]:
    compact = re.sub(r"[^a-z0-9]", "", name.lower())
    alias = ALIASES.get(compact)
    if alias:
        return alias
    return next((skill for skill in QUESTION_BANK if skill.lower() == name.lower()), None)


def _load_careers() -> List[Dict[str, Any]]:
    data_path = Path(__file__).resolve().parents[2] / "data" / "careers.json"
    try:
        with data_path.open(encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def get_career_and_skills(profile: Dict[str, Any]) -> Tuple[str, List[str], List[str]]:
    career_title = str(profile.get("target_role") or "").strip()
    careers = _load_careers()
    career = next(
        (item for item in careers if item.get("title", "").lower() == career_title.lower()),
        None,
    )
    if career:
        career_title = career.get("title", career_title)
    elif not career_title:
        raise ValueError("Select a career in your student profile before starting the practical assessment.")

    claimed: List[str] = []
    for skill in (profile.get("technical_skills") or {}).keys():
        canonical = _canonical_skill(str(skill))
        if canonical and canonical not in claimed:
            claimed.append(canonical)
    for skill in profile.get("soft_skills") or []:
        canonical = _canonical_skill(str(skill))
        if canonical and canonical not in claimed:
            claimed.append(canonical)
    aptitude_scores = profile.get("aptitude_scores") or {}
    if aptitude_scores:
        claimed.extend(
            skill for skill in ("Aptitude", "Analytical Thinking")
            if skill not in claimed
        )

    career_skills: List[str] = []
    if career:
        required = career.get("required_skills", {})
        for skill in list(required.keys()) + career.get("required_soft_skills", []):
            canonical = _canonical_skill(str(skill))
            if canonical and canonical not in career_skills:
                career_skills.append(canonical)
        if career.get("required_aptitude"):
            for skill in ("Aptitude", "Analytical Thinking"):
                if skill not in career_skills:
                    career_skills.append(skill)
    return career_title, claimed, career_skills


def build_adaptive_roadmap(
    skill_results: List[Dict[str, Any]], career_title: str
) -> List[Dict[str, Any]]:
    weak_results = sorted(
        (item for item in skill_results if item["score"] < 70),
        key=lambda item: (item["score"], item["skill"].lower()),
    )
    personalized = []
    for item in weak_results:
        skill = item["skill"]
        phases = ROADMAP_CONTENT.get(skill)
        if not phases:
            continue
        phase_data = []
        for level, topics in zip(("Beginner", "Intermediate", "Advanced"), phases):
            topic_data = []
            for title in topics:
                topic_data.append({
                    "title": title,
                    "explanation": f"Build practical {skill} capability for {career_title} by learning {title.lower()} and applying it to realistic work.",
                    "examples": [
                        f"Explain the key decisions involved in {title.lower()}.",
                        f"Apply {title.lower()} to a small {career_title} task and document the result.",
                    ],
                    "practice_exercises": [
                        f"Complete three focused {skill} exercises about {title.lower()}.",
                        f"Review one incorrect attempt and write down the root cause.",
                    ],
                    "coding_challenges": [
                        f"Create a small challenge that demonstrates {title.lower()}."
                    ] if skill in {"Python", "Java", "C", "C++", "JavaScript", "React", "SQL", "MongoDB"} else [],
                    "mini_project": f"Build a {level.lower()}-level {skill} mini project for a {career_title} portfolio, incorporating {title.lower()}.",
                    "resources": [
                        {"title": name, "url": url}
                        for name, url in RESOURCE_LINKS.get(skill, [])
                    ],
                    "completion_requirements": [
                        f"Finish at least 3 exercises on {title.lower()} with 80% accuracy.",
                        "Submit the mini project with a short explanation of the approach and test results.",
                    ],
                })
            phase_data.append({"level": level, "topics": topic_data})
        personalized.append({
            "skill": skill,
            "score": item["score"],
            "category": item["category"],
            "priority": "HIGH" if item["score"] < 50 else "MEDIUM",
            "phases": phase_data,
        })
    return personalized


async def _load_student_context(user_id: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    db = get_database()
    if db is None:
        raise RuntimeError("The practical assessment requires an active MongoDB connection.")
    profile = await db.student_profiles.find_one({"user_id": user_id})
    if not profile:
        raise ValueError("Complete your student profile and select a career before starting the practical assessment.")
    projects = await db.project_evidence.find({"user_id": user_id}).to_list(length=100)
    certificates = await db.certificate_evidence.find({"user_id": user_id}).to_list(length=100)
    return profile, projects, certificates


def create_question_set(
    skills: List[str], previous_ids: List[str], per_skill: int = 2
) -> List[Dict[str, Any]]:
    rng = random.SystemRandom()
    selected = []
    for skill in skills:
        bank = QUESTION_BANK.get(skill, [])
        if not bank:
            continue
        unseen = [question for question in bank if question["question_id"] not in previous_ids]
        pool = deepcopy(unseen or bank)
        rng.shuffle(pool)
        selected.extend(pool[:min(per_skill, len(pool))])
    rng.shuffle(selected)
    for question in selected:
        if question["options"]:
            question["options"] = list(question["options"])
            rng.shuffle(question["options"])
    return selected


def evaluate_answers(
    questions: List[Dict[str, Any]], answers: Dict[str, Any]
) -> Tuple[int, List[Dict[str, Any]], List[Dict[str, Any]]]:
    expected_ids = {question["question_id"] for question in questions}
    if set(answers) != expected_ids:
        raise ValueError("Submit exactly one answer for every question in this assessment.")

    review = []
    skill_counts: Dict[str, Dict[str, int]] = {}
    for question in questions:
        skill = question["skill"]
        counts = skill_counts.setdefault(skill, {"correct_count": 0, "total_questions": 0})
        counts["total_questions"] += 1
        submitted = answers[question["question_id"]]
        if isinstance(submitted, int) and question["options"] and 0 <= submitted < len(question["options"]):
            submitted = question["options"][submitted]
        answer = str(submitted).strip()
        normalized = re.sub(r"\s+", "", answer).lower()
        accepted = {
            re.sub(r"\s+", "", str(candidate)).lower()
            for candidate in question.get("accepted_answers", [question["correct_answer"]])
        }
        required_terms = [term.lower() for term in question.get("required_terms", [])]
        is_correct = (
            all(term in answer.lower() for term in required_terms)
            if required_terms
            else normalized in accepted
        )
        if is_correct:
            counts["correct_count"] += 1
        review.append({
            "question_id": question["question_id"],
            "skill": skill,
            "question": question["question"],
            "user_answer": answer,
            "correct_answer": question["correct_answer"],
            "is_correct": is_correct,
            "topic": question["topic"],
            "difficulty": question["difficulty"],
        })

    correct_count = sum(counts["correct_count"] for counts in skill_counts.values())
    total = len(questions)
    results = []
    for skill, counts in skill_counts.items():
        score = round(counts["correct_count"] / counts["total_questions"] * 100)
        results.append({
            "skill": skill,
            "score": score,
            "category": score_category(score),
            "correct_count": counts["correct_count"],
            "total_questions": counts["total_questions"],
        })
    return round(correct_count / total * 100) if total else 0, results, review


async def start_assessment(user_id: str) -> Dict[str, Any]:
    db = get_database()
    if db is None:
        raise RuntimeError("The practical assessment requires an active MongoDB connection.")
    profile, projects, certificates = await _load_student_context(user_id)
    profile_certificates = profile.get("certificates") or []
    if isinstance(profile_certificates, list):
        certificates.extend(
            item for item in profile_certificates if isinstance(item, dict)
        )
    career_title, claimed_skills, career_skills = get_career_and_skills(profile)
    evidence_skills = []
    for record in projects + certificates:
        skills = record.get("skills_used") or record.get("skills") or []
        if isinstance(skills, str):
            skills = [skills]
        evidence_skills.extend(str(skill) for skill in skills)
    test_skills = list(claimed_skills)
    for skill in career_skills + [_canonical_skill(skill) for skill in evidence_skills]:
        if skill and skill not in test_skills:
            test_skills.append(skill)
    if not test_skills:
        raise ValueError("Add claimed skills to your profile or select a career with assessable requirements.")

    past_attempts = await db.practical_assessment_attempts.find(
        {"user_id": user_id}, {"question_ids": 1}
    ).to_list(length=200)
    previous_ids = [
        question_id for attempt in past_attempts
        for question_id in attempt.get("question_ids", [])
    ]
    questions = create_question_set(test_skills, previous_ids)
    if not questions:
        raise ValueError("No practical questions are available for the skills in your profile.")
    for skill in test_skills:
        project = next(
            (
                item for item in projects
                if any(_canonical_skill(str(name)) == skill for name in (item.get("skills_used") or []))
            ),
            None,
        )
        if project:
            question = next((item for item in questions if item["skill"] == skill), None)
            if question:
                description = str(project.get("description") or "").strip()
                context = f"Your submitted project '{project.get('title', 'project')}' used {skill}. "
                if description:
                    context += f"Project detail: {description[:160]}. "
                question["question"] = context + question["question"]

    now = datetime.now(timezone.utc)
    assessment_id = f"practical_{uuid.uuid4().hex}"
    active = {
        "assessment_id": assessment_id,
        "user_id": user_id,
        "career_title": career_title,
        "claimed_skills": claimed_skills,
        "evidence_submitted": {"projects": len(projects), "certificates": len(certificates)},
        "project_skill_names": list(dict.fromkeys(
            canonical
            for project in projects
            for raw_skill in (project.get("skills_used") or [])
            if (canonical := _canonical_skill(str(raw_skill)))
        )),
        "full_questions": questions,
        "created_at": now.isoformat(),
    }
    await db.active_practical_assessments.replace_one(
        {"user_id": user_id}, active, upsert=True
    )
    return {
        "assessment_id": assessment_id,
        "career_title": career_title,
        "time_limit_minutes": 30,
        "total_questions": len(questions),
        "skills": list(dict.fromkeys(question["skill"] for question in questions)),
        "questions": [
            {key: question[key] for key in ("question_id", "skill", "topic", "difficulty", "type", "question", "options")}
            for question in questions
        ],
    }


async def submit_assessment(user_id: str, assessment_id: str, answers: Dict[str, Any]) -> Dict[str, Any]:
    db = get_database()
    if db is None:
        raise RuntimeError("The practical assessment requires an active MongoDB connection.")
    active = await db.active_practical_assessments.find_one({
        "user_id": user_id,
        "assessment_id": assessment_id,
    })
    if not active:
        raise ValueError("This assessment is not active for your account. Start a new attempt.")
    created_at = datetime.fromisoformat(active["created_at"])
    if (datetime.now(timezone.utc) - created_at).total_seconds() > 30 * 60:
        await db.active_practical_assessments.delete_one({"user_id": user_id, "assessment_id": assessment_id})
        raise TimeoutError("The assessment time limit has expired. Start a new attempt.")

    questions = active["full_questions"]
    overall_score, skill_results, review = evaluate_answers(questions, answers)
    submitted_at = datetime.now(timezone.utc).isoformat()
    attempt_id = f"practical_attempt_{uuid.uuid4().hex}"
    for skill_result in skill_results:
        skill_result["verified"] = (
            skill_result["score"] >= 70
            and skill_result["skill"] in active.get("project_skill_names", [])
        )
    skill_map = {result["skill"]: result["score"] for result in skill_results}
    adaptive_roadmap = build_adaptive_roadmap(skill_results, active["career_title"])
    attempt = {
        "attempt_id": attempt_id,
        "user_id": user_id,
        "assessment_id": assessment_id,
        "career_title": active["career_title"],
        "overall_score": overall_score,
        "correct_count": sum(result["correct_count"] for result in skill_results),
        "total_questions": len(questions),
        "skill_results": skill_results,
        "claimed_skills": active["claimed_skills"],
        "evidence_submitted": active["evidence_submitted"],
        "verified_skills": [result["skill"] for result in skill_results if result["verified"]],
        "skills_needing_improvement": [result["skill"] for result in skill_results if result["score"] < 70],
        "adaptive_roadmap": adaptive_roadmap,
        "question_ids": [question["question_id"] for question in questions],
        "answers": answers,
        "review": review,
        "submitted_at": submitted_at,
    }
    await db.practical_assessment_attempts.insert_one(attempt)
    await db.student_profiles.update_one(
        {"user_id": user_id},
        {"$set": {
            "practical_skill_results": skill_map,
            "practical_assessment_completed_at": submitted_at,
        }},
    )
    await get_or_create_user_evidence(user_id)
    await db.active_practical_assessments.delete_one({"user_id": user_id, "assessment_id": assessment_id})
    return {key: value for key, value in attempt.items() if key not in {"user_id", "assessment_id", "question_ids", "answers", "review"}}


async def get_status(user_id: str) -> Dict[str, Any]:
    db = get_database()
    if db is None:
        raise RuntimeError("The practical assessment requires an active MongoDB connection.")
    latest = await db.practical_assessment_attempts.find_one(
        {"user_id": user_id}, sort=[("submitted_at", -1)]
    )
    if not latest:
        profile = await db.student_profiles.find_one({"user_id": user_id}) or {}
        career_title = str(profile.get("target_role") or "")
        projects = await db.project_evidence.count_documents({"user_id": user_id})
        certificates = await db.certificate_evidence.count_documents({"user_id": user_id})
        certificates += len(profile.get("certificates") or [])
        return {
            "has_completed": False,
            "career_title": career_title,
            "skill_results": [],
            "claimed_skills": list((profile.get("technical_skills") or {}).keys()) + list(profile.get("soft_skills") or []),
            "evidence_submitted": {"projects": projects, "certificates": certificates},
            "verified_skills": [],
            "skills_needing_improvement": [],
            "adaptive_roadmap": [],
        }
    return {
        "has_completed": True,
        **{
            key: latest.get(key, default)
            for key, default in (
                ("career_title", ""),
                ("skill_results", []),
                ("claimed_skills", []),
                ("evidence_submitted", {"projects": 0, "certificates": 0}),
                ("verified_skills", []),
                ("skills_needing_improvement", []),
                ("adaptive_roadmap", []),
            )
        },
    }


async def get_history(user_id: str) -> List[Dict[str, Any]]:
    db = get_database()
    if db is None:
        raise RuntimeError("The practical assessment requires an active MongoDB connection.")
    cursor = db.practical_assessment_attempts.find(
        {"user_id": user_id},
        {"_id": 0, "attempt_id": 1, "career_title": 1, "overall_score": 1, "total_questions": 1, "correct_count": 1, "skill_results": 1, "submitted_at": 1},
    ).sort("submitted_at", -1)
    return await cursor.to_list(length=50)


async def get_attempt_review(user_id: str, attempt_id: str) -> Optional[Dict[str, Any]]:
    db = get_database()
    if db is None:
        raise RuntimeError("The practical assessment requires an active MongoDB connection.")
    attempt = await db.practical_assessment_attempts.find_one(
        {"user_id": user_id, "attempt_id": attempt_id},
        {"_id": 0, "attempt_id": 1, "review": 1, "overall_score": 1, "skill_results": 1},
    )
    return attempt
