import json
import os

new_questions = [
    # ==================== HTML ====================
    {
        "id": "web_html_b01", "skill": "Web Development", "skill_slug": "web-development", "level": 1, "topic": "HTML",
        "type": "mcq", "difficulty": "Beginner",
        "question": "Which HTML5 element represents self-contained content, such as a blog post or news story?",
        "options": ["<article>", "<section>", "<aside>", "<div>"],
        "correct_answer": "<article>",
        "explanation": "The <article> tag specifies independent, self-contained content that could stand alone.",
        "acceptable_answers": ["<article>"]
    },
    {
        "id": "web_html_b02", "skill": "Web Development", "skill_slug": "web-development", "level": 1, "topic": "HTML",
        "type": "mcq", "difficulty": "Beginner",
        "question": "Which attribute is required on an <img> tag for web accessibility (WCAG compliance)?",
        "options": ["alt", "title", "src-alt", "aria-image"],
        "correct_answer": "alt",
        "explanation": "The alt attribute provides alternative text for screen readers and when images fail to load.",
        "acceptable_answers": ["alt"]
    },
    {
        "id": "web_html_b03", "skill": "Web Development", "skill_slug": "web-development", "level": 1, "topic": "HTML",
        "type": "mcq", "difficulty": "Beginner",
        "question": "Which HTML5 input type provides built-in email format validation in browser forms?",
        "options": ["type='email'", "type='text'", "type='mail'", "type='address'"],
        "correct_answer": "type='email'",
        "explanation": "input type='email' activates browser validation requiring a valid email format before submission.",
        "acceptable_answers": ["type='email'"]
    },
    {
        "id": "web_html_i01", "skill": "Web Development", "skill_slug": "web-development", "level": 2, "topic": "HTML",
        "type": "mcq", "difficulty": "Intermediate",
        "question": "What is the primary purpose of the meta viewport tag with width=device-width?",
        "options": ["Configures responsive rendering and scaling on mobile devices", "Locks screen resolution to desktop standard", "Preloads mobile assets asynchronously", "Enables CSS Grid hardware acceleration"],
        "correct_answer": "Configures responsive rendering and scaling on mobile devices",
        "explanation": "The viewport meta tag matches screen width in device-independent pixels to ensure proper responsive scaling.",
        "acceptable_answers": ["Configures responsive rendering and scaling on mobile devices"]
    },
    {
        "id": "web_html_a01", "skill": "Web Development", "skill_slug": "web-development", "level": 3, "topic": "HTML",
        "type": "mcq", "difficulty": "Advanced",
        "question": "In HTML Web Components, what is the role of Shadow DOM?",
        "options": ["Encapsulates CSS styles and DOM tree so they do not leak into or out of the component", "Provides GPU-accelerated 3D WebGL rendering", "Caches component HTML templates in IndexedDB", "Minifies HTML attributes during compilation"],
        "correct_answer": "Encapsulates CSS styles and DOM tree so they do not leak into or out of the component",
        "explanation": "Shadow DOM provides hidden, scoped DOM trees and style scoping for web components.",
        "acceptable_answers": ["Encapsulates CSS styles and DOM tree so they do not leak into or out of the component"]
    },

    # ==================== CSS ====================
    {
        "id": "web_css_b01", "skill": "Web Development", "skill_slug": "web-development", "level": 1, "topic": "CSS",
        "type": "mcq", "difficulty": "Beginner",
        "question": "In the CSS Box Model, what is the correct order from outermost to innermost component?",
        "options": ["Margin -> Border -> Padding -> Content", "Border -> Margin -> Padding -> Content", "Padding -> Margin -> Border -> Content", "Margin -> Padding -> Border -> Content"],
        "correct_answer": "Margin -> Border -> Padding -> Content",
        "explanation": "The standard CSS box model starts with Margin (outermost), then Border, Padding, and Content.",
        "acceptable_answers": ["Margin -> Border -> Padding -> Content"]
    },
    {
        "id": "web_css_b02", "skill": "Web Development", "skill_slug": "web-development", "level": 1, "topic": "CSS",
        "type": "mcq", "difficulty": "Beginner",
        "question": "Which CSS Flexbox property aligns flex items along the primary main axis?",
        "options": ["justify-content", "align-items", "align-content", "flex-direction"],
        "correct_answer": "justify-content",
        "explanation": "justify-content distributes space along the main axis; align-items controls cross-axis alignment.",
        "acceptable_answers": ["justify-content"]
    },
    {
        "id": "web_css_i01", "skill": "Web Development", "skill_slug": "web-development", "level": 2, "topic": "CSS",
        "type": "mcq", "difficulty": "Intermediate",
        "question": "What does setting 'box-sizing: border-box' achieve in CSS layouts?",
        "options": ["Includes padding and border within the declared width and height of an element", "Removes margins between consecutive block elements", "Forces elements to render with flexbox layout", "Disables element clipping when overflow occurs"],
        "correct_answer": "Includes padding and border within the declared width and height of an element",
        "explanation": "border-box causes width/height to encompass content, padding, and border, preventing layout breakage.",
        "acceptable_answers": ["Includes padding and border within the declared width and height of an element"]
    },
    {
        "id": "web_css_a01", "skill": "Web Development", "skill_slug": "web-development", "level": 3, "topic": "CSS",
        "type": "mcq", "difficulty": "Advanced",
        "question": "Which CSS selector has the highest calculated specificity according to W3C rules?",
        "options": ["#header .nav (1 ID, 1 Class)", ".nav.active:hover (3 Classes/Pseudo-classes)", "nav ul li a (4 Element tags)", "header > div (2 Element tags)"],
        "correct_answer": "#header .nav (1 ID, 1 Class)",
        "explanation": "ID selectors have specificity value 1-0-0, which always outweighs any number of classes (0-1-0).",
        "acceptable_answers": ["#header .nav (1 ID, 1 Class)"]
    },

    # ==================== JAVASCRIPT ====================
    {
        "id": "web_js_b01", "skill": "Web Development", "skill_slug": "web-development", "level": 1, "topic": "JavaScript",
        "type": "mcq", "difficulty": "Beginner",
        "question": "What is the key difference between 'let' and 'const' in modern JavaScript (ES6+)?",
        "options": ["Variables declared with const cannot be reassigned, while let variables can be reassigned", "let is function-scoped while const is block-scoped", "const variables are hoisted while let is not", "const allocates memory on the stack whereas let uses the heap"],
        "correct_answer": "Variables declared with const cannot be reassigned, while let variables can be reassigned",
        "explanation": "Both let and const are block-scoped; const prevents identifier reassignment, let permits reassignment.",
        "acceptable_answers": ["Variables declared with const cannot be reassigned, while let variables can be reassigned"]
    },
    {
        "id": "web_js_b02", "skill": "Web Development", "skill_slug": "web-development", "level": 1, "topic": "JavaScript",
        "type": "mcq", "difficulty": "Beginner",
        "question": "What does the strict equality operator '===' check in JavaScript?",
        "options": ["Both value and data type without implicit type coercion", "Only the value, coercing types automatically", "Whether both objects share the same prototype chain", "Memory address identity only"],
        "correct_answer": "Both value and data type without implicit type coercion",
        "explanation": "Strict equality (===) validates that operands have the identical type and equal value.",
        "acceptable_answers": ["Both value and data type without implicit type coercion"]
    },
    {
        "id": "web_js_i01", "skill": "Web Development", "skill_slug": "web-development", "level": 2, "topic": "JavaScript",
        "type": "mcq", "difficulty": "Intermediate",
        "question": "What is a JavaScript Closure?",
        "options": ["A function bundled together with references to its surrounding lexical environment", "A method that executes immediately upon script loading", "A syntax error when curly braces are unbalanced", "A thread worker running in the background"],
        "correct_answer": "A function bundled together with references to its surrounding lexical environment",
        "explanation": "A closure gives an inner function access to an outer function scope even after the outer function finishes.",
        "acceptable_answers": ["A function bundled together with references to its surrounding lexical environment"]
    },
    {
        "id": "web_js_i02", "skill": "Web Development", "skill_slug": "web-development", "level": 2, "topic": "JavaScript",
        "type": "mcq", "difficulty": "Intermediate",
        "question": "In the JavaScript Event Loop, which queue is processed first after the current call stack empties?",
        "options": ["Microtask Queue (Promises, queueMicrotask)", "Macrotask Queue (setTimeout, setInterval)", "I/O Polling Queue", "RequestAnimationFrame Queue"],
        "correct_answer": "Microtask Queue (Promises, queueMicrotask)",
        "explanation": "Microtasks (Promise callbacks) have priority over macrotasks (such as setTimeout) in the event loop.",
        "acceptable_answers": ["Microtask Queue (Promises, queueMicrotask)"]
    },
    {
        "id": "web_js_a01", "skill": "Web Development", "skill_slug": "web-development", "level": 3, "topic": "JavaScript",
        "type": "mcq", "difficulty": "Advanced",
        "question": "What is the output of Promise.all() when one of the passed promises rejects?",
        "options": ["Immediately rejects with the reason of the first rejected promise", "Waits for remaining promises then returns partial results", "Ignores the error and resolves with undefined", "Retries the failed promise three times"],
        "correct_answer": "Immediately rejects with the reason of the first rejected promise",
        "explanation": "Promise.all fails fast: if any promise in the iterable rejects, the whole Promise.all immediately rejects.",
        "acceptable_answers": ["Immediately rejects with the reason of the first rejected promise"]
    },

    # ==================== REACT ====================
    {
        "id": "web_react_b01", "skill": "Web Development", "skill_slug": "web-development", "level": 1, "topic": "React",
        "type": "mcq", "difficulty": "Beginner",
        "question": "Which React Hook is used to add reactive local state to a functional component?",
        "options": ["useState", "useEffect", "useContext", "useReducer"],
        "correct_answer": "useState",
        "explanation": "useState declares state variables that trigger component re-render when their setter function is called.",
        "acceptable_answers": ["useState"]
    },
    {
        "id": "web_react_b02", "skill": "Web Development", "skill_slug": "web-development", "level": 1, "topic": "React",
        "type": "mcq", "difficulty": "Beginner",
        "question": "Why should list elements in React be given a unique 'key' prop?",
        "options": ["Helps React identify which items have changed, added, or removed for efficient DOM reconciliation", "Applies unique CSS styles to individual list nodes", "Allows direct DOM manipulation via document.getElementById", "Encrypts list data before rendering"],
        "correct_answer": "Helps React identify which items have changed, added, or removed for efficient DOM reconciliation",
        "explanation": "Keys give elements a stable identity so React diffs and reconciles lists efficiently without full re-mounts.",
        "acceptable_answers": ["Helps React identify which items have changed, added, or removed for efficient DOM reconciliation"]
    },
    {
        "id": "web_react_i01", "skill": "Web Development", "skill_slug": "web-development", "level": 2, "topic": "React",
        "type": "mcq", "difficulty": "Intermediate",
        "question": "When does the cleanup function returned by useEffect() execute?",
        "options": ["Before re-running the effect on dependency change and when component unmounts", "Only once when the browser window closes", "Immediately before the initial render", "Whenever useState throws an uncaught error"],
        "correct_answer": "Before re-running the effect on dependency change and when component unmounts",
        "explanation": "useEffect cleanup cleans up subscriptions/listeners before the next effect cycle and on unmount.",
        "acceptable_answers": ["Before re-running the effect on dependency change and when component unmounts"]
    },
    {
        "id": "web_react_a01", "skill": "Web Development", "skill_slug": "web-development", "level": 3, "topic": "React",
        "type": "mcq", "difficulty": "Advanced",
        "question": "What does React.memo() do to optimize rendering performance?",
        "options": ["Skips re-rendering a component if its incoming props have not changed", "Caches component HTML directly in service worker storage", "Converts functional components to WebAssembly binary", "Runs component lifecycle methods asynchronously on a Web Worker"],
        "correct_answer": "Skips re-rendering a component if its incoming props have not changed",
        "explanation": "React.memo is a higher order component that performs a shallow comparison of props to prevent unnecessary renders.",
        "acceptable_answers": ["Skips re-rendering a component if its incoming props have not changed"]
    },

    # ==================== BACKEND DEVELOPMENT ====================
    {
        "id": "web_be_b01", "skill": "Web Development", "skill_slug": "web-development", "level": 1, "topic": "Backend development",
        "type": "mcq", "difficulty": "Beginner",
        "question": "Which HTTP status code signifies that a resource was successfully created on the server?",
        "options": ["201 Created", "200 OK", "204 No Content", "301 Moved Permanently"],
        "correct_answer": "201 Created",
        "explanation": "HTTP 201 indicates that the request succeeded and resulted in the creation of a new resource.",
        "acceptable_answers": ["201 Created"]
    },
    {
        "id": "web_be_i01", "skill": "Web Development", "skill_slug": "web-development", "level": 2, "topic": "Backend development",
        "type": "mcq", "difficulty": "Intermediate",
        "question": "What is Middleware in backend frameworks like Express or FastAPI?",
        "options": ["Functions with access to request and response objects that execute during the HTTP request-response cycle", "A physical router connecting databases to web servers", "A database compression plugin", "Frontend code that renders UI templates"],
        "correct_answer": "Functions with access to request and response objects that execute during the HTTP request-response cycle",
        "explanation": "Middleware intercepts HTTP requests to perform authentication, logging, header validation, or data parsing.",
        "acceptable_answers": ["Functions with access to request and response objects that execute during the HTTP request-response cycle"]
    },
    {
        "id": "web_be_a01", "skill": "Web Development", "skill_slug": "web-development", "level": 3, "topic": "Backend development",
        "type": "mcq", "difficulty": "Advanced",
        "question": "What is the purpose of JWT (JSON Web Token) 'exp' claim in stateless authentication?",
        "options": ["Defines the expiration Unix timestamp after which the token is invalid", "Contains the encrypted password hash of the student", "Designates the server IP address permitted to issue responses", "Stores database query execution timeout limits"],
        "correct_answer": "Defines the expiration Unix timestamp after which the token is invalid",
        "explanation": "The exp registered claim specifies token expiration to limit the window of vulnerability if a token is intercepted.",
        "acceptable_answers": ["Defines the expiration Unix timestamp after which the token is invalid"]
    },

    # ==================== WEB APPLICATION CONCEPTS ====================
    {
        "id": "web_app_b01", "skill": "Web Development", "skill_slug": "web-development", "level": 1, "topic": "Web application concepts",
        "type": "mcq", "difficulty": "Beginner",
        "question": "What does CORS (Cross-Origin Resource Sharing) protect against in web browsers?",
        "options": ["Restricts web pages from requesting sensitive API resources located on a different domain without explicit permission", "Prevents CSS styles from colliding across components", "Stops memory leaks in single-page applications", "Encrypts local database queries on localhost"],
        "correct_answer": "Restricts web pages from requesting sensitive API resources located on a different domain without explicit permission",
        "explanation": "CORS is a browser security mechanism that restricts cross-origin HTTP requests made by scripts.",
        "acceptable_answers": ["Restricts web pages from requesting sensitive API resources located on a different domain without explicit permission"]
    },
    {
        "id": "web_app_i01", "skill": "Web Development", "skill_slug": "web-development", "level": 2, "topic": "Web application concepts",
        "type": "mcq", "difficulty": "Intermediate",
        "question": "What is the primary difference between localStorage and sessionStorage in browsers?",
        "options": ["localStorage persists until explicitly cleared; sessionStorage expires when the browser tab/session closes", "localStorage is encrypted; sessionStorage is plain text", "sessionStorage holds 50MB while localStorage holds 5KB", "localStorage is shared with all other installed apps on Windows"],
        "correct_answer": "localStorage persists until explicitly cleared; sessionStorage expires when the browser tab/session closes",
        "explanation": "localStorage data has no expiration date; sessionStorage is cleared whenever the page session ends.",
        "acceptable_answers": ["localStorage persists until explicitly cleared; sessionStorage expires when the browser tab/session closes"]
    },

    # ==================== DATA SCIENCE: STATISTICS & DATA ANALYSIS ====================
    {
        "id": "ds_stat_b01", "skill": "Data Science", "skill_slug": "data-science", "level": 1, "topic": "Statistics",
        "type": "mcq", "difficulty": "Beginner",
        "question": "Which measure of central tendency is least affected by extreme outlier values?",
        "options": ["Median", "Mean", "Mid-range", "Standard Deviation"],
        "correct_answer": "Median",
        "explanation": "The median represents the 50th percentile rank and is robust against skewed extreme values.",
        "acceptable_answers": ["Median"]
    },
    {
        "id": "ds_stat_i01", "skill": "Data Science", "skill_slug": "data-science", "level": 2, "topic": "Statistics",
        "type": "mcq", "difficulty": "Intermediate",
        "question": "In hypothesis testing, what does a p-value less than alpha (0.05) indicate?",
        "options": ["Statistically significant evidence to reject the Null Hypothesis", "Fail to reject the Null Hypothesis", "The sample size is insufficient", "The experiment produced a Type II error"],
        "correct_answer": "Statistically significant evidence to reject the Null Hypothesis",
        "explanation": "A p-value < 0.05 implies observed results are unlikely under the null hypothesis, justifying rejection.",
        "acceptable_answers": ["Statistically significant evidence to reject the Null Hypothesis"]
    },
    {
        "id": "ds_analysis_b01", "skill": "Data Science", "skill_slug": "data-science", "level": 1, "topic": "Data analysis",
        "type": "mcq", "difficulty": "Beginner",
        "question": "In Python Pandas, which method returns summary statistics (count, mean, std, quartiles) of numeric columns?",
        "options": ["df.describe()", "df.summary()", "df.info()", "df.stats()"],
        "correct_answer": "df.describe()",
        "explanation": "describe() computes descriptive statistics summarizing the central tendency, dispersion and shape of dataset.",
        "acceptable_answers": ["df.describe()"]
    },
    {
        "id": "ds_analysis_i01", "skill": "Data Science", "skill_slug": "data-science", "level": 2, "topic": "Data analysis",
        "type": "mcq", "difficulty": "Intermediate",
        "question": "What is the purpose of One-Hot Encoding in feature preprocessing?",
        "options": ["Converts categorical variables into binary vectors without imposing false ordinal relationships", "Normalizes continuous variables between 0 and 1", "Imputes missing values using K-Nearest Neighbors", "Removes collinear features with high variance inflation"],
        "correct_answer": "Converts categorical variables into binary vectors without imposing false ordinal relationships",
        "explanation": "One-hot encoding creates binary dummy columns for each category so linear models do not infer numerical ordering.",
        "acceptable_answers": ["Converts categorical variables into binary vectors without imposing false ordinal relationships"]
    },

    # ==================== ARTIFICIAL INTELLIGENCE FUNDAMENTALS ====================
    {
        "id": "ai_fund_b01", "skill": "Artificial Intelligence", "skill_slug": "artificial-intelligence", "level": 1, "topic": "AI fundamentals",
        "type": "mcq", "difficulty": "Beginner",
        "question": "In Artificial Intelligence search problems, what distinguishes A* Search from standard Dijkstra algorithm?",
        "options": ["A* uses a heuristic function h(n) estimating remaining cost to goal alongside path cost g(n)", "A* searches strictly in a depth-first direction", "A* ignores edge weights entirely", "Dijkstra requires negative edge weights while A* forbids them"],
        "correct_answer": "A* uses a heuristic function h(n) estimating remaining cost to goal alongside path cost g(n)",
        "explanation": "A* calculates f(n) = g(n) + h(n), combining actual distance with heuristic estimates to guide search efficiently.",
        "acceptable_answers": ["A* uses a heuristic function h(n) estimating remaining cost to goal alongside path cost g(n)"]
    },
    {
        "id": "ai_fund_i01", "skill": "Artificial Intelligence", "skill_slug": "artificial-intelligence", "level": 2, "topic": "AI fundamentals",
        "type": "mcq", "difficulty": "Intermediate",
        "question": "What is the vanishing gradient problem in deep neural networks?",
        "options": ["Gradients become exponentially small as backpropagation travels to early layers, slowing training", "Model weights become infinite, producing NaN loss values", "The loss function reaches zero after a single epoch", "Dropout removes all neuron connections simultaneously"],
        "correct_answer": "Gradients become exponentially small as backpropagation travels to early layers, slowing training",
        "explanation": "Repeated multiplications of fractional derivatives in deep networks cause gradients to shrink toward zero.",
        "acceptable_answers": ["Gradients become exponentially small as backpropagation travels to early layers, slowing training"]
    },
    {
        "id": "ai_math_b01", "skill": "Artificial Intelligence", "skill_slug": "artificial-intelligence", "level": 1, "topic": "Mathematics for AI",
        "type": "mcq", "difficulty": "Beginner",
        "question": "What mathematical condition is required to compute matrix product A (size m x k) and B (size p x n)?",
        "options": ["k must equal p (columns of A must equal rows of B)", "m must equal n", "Both matrices must be square (m = k = p = n)", "k must equal n"],
        "correct_answer": "k must equal p (columns of A must equal rows of B)",
        "explanation": "Matrix multiplication requires inner dimensions to match: (m x k) * (k x n) = (m x n).",
        "acceptable_answers": ["k must equal p (columns of A must equal rows of B)"]
    },
    {
        "id": "ai_math_i01", "skill": "Artificial Intelligence", "skill_slug": "artificial-intelligence", "level": 2, "topic": "Mathematics for AI",
        "type": "mcq", "difficulty": "Intermediate",
        "question": "In gradient descent optimization, what does the gradient vector represent?",
        "options": ["The direction of steepest ascent of the loss function", "The minimum eigenvalues of the Hessian matrix", "The global minimum location in feature space", "The variance of input parameters"],
        "correct_answer": "The direction of steepest ascent of the loss function",
        "explanation": "The gradient vector points in the direction of steepest increase; gradient descent steps in the negative direction.",
        "acceptable_answers": ["The direction of steepest ascent of the loss function"]
    }
]

file_path = os.path.join(os.path.dirname(__file__), "level_assessment_questions.json")
with open(file_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_ids = {q["id"] for q in existing}
added = 0
for q in new_questions:
    if q["id"] not in existing_ids:
        existing.append(q)
        added += 1

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=2)

print(f"Added {added} new questions. Total questions now: {len(existing)}")
