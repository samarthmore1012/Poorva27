from flask import Flask, request, redirect, url_for, session, render_template_string
import mysql.connector
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

app.secret_key = "insurance_secret_key"


# ============================================================
# DATABASE SETTINGS
# ============================================================

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root@123"
DB_NAME = "insurance_db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# ============================================================
# LOGIN CHECK
# ============================================================

def login_required():

    if "username" not in session:
        return False

    return True


# ============================================================
# COMMON CSS
# ============================================================

COMMON_CSS = """

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
}

body {
    background: #f4f7fb;
    color: #172033;
}

/* NAVBAR */

.navbar {
    width: 100%;
    min-height: 70px;

    background: #1e293b;

    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 30px;
}

.logo {
    color: white;
    font-size: 22px;
    font-weight: bold;
}

.nav-links {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.nav-links a {
    color: white;
    text-decoration: none;
    font-size: 15px;
    font-weight: 600;
}

.nav-links a:hover {
    color: #60a5fa;
}

/* MAIN */

.main {
    width: 100%;
    max-width: 1200px;

    margin: 40px auto;

    padding: 0 20px;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 25px;
}

.page-header h1 {
    font-size: 32px;
    color: #173b70;
}

/* BUTTON */

.btn {
    display: inline-block;

    background: #2563eb;
    color: white;

    text-decoration: none;

    border: none;
    border-radius: 8px;

    padding: 12px 20px;

    font-size: 15px;

    cursor: pointer;
}

.btn:hover {
    background: #1d4ed8;
}

.btn-danger {
    background: #dc3545;
}

.btn-danger:hover {
    background: #b02a37;
}

.btn-secondary {
    background: #64748b;
}

/* CARD */

.card {
    background: white;

    border-radius: 15px;

    padding: 25px;

    margin-bottom: 25px;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.08);
}

/* TABLE */

.table-container {
    overflow-x: auto;
}

table {
    width: 100%;

    border-collapse: collapse;

    background: white;
}

th {
    background: #1e293b;
    color: white;

    padding: 13px;

    text-align: left;
}

td {
    padding: 12px;

    border-bottom: 1px solid #e2e8f0;
}

tr:hover {
    background: #f8fafc;
}

/* FORM */

.form-card {
    max-width: 650px;
    margin: auto;
}

.form-group {
    margin-bottom: 18px;
}

.form-group label {
    display: block;

    margin-bottom: 7px;

    font-weight: bold;

    color: #27364d;
}

.form-group input,
.form-group select {
    width: 100%;

    padding: 13px;

    border: 1px solid #cbd5e1;

    border-radius: 8px;

    font-size: 15px;

    outline: none;
}

.form-group input:focus,
.form-group select:focus {
    border-color: #2563eb;
}

/* ERROR */

.error {
    background: #fee2e2;

    color: #b91c1c;

    padding: 13px;

    border-radius: 8px;

    margin-bottom: 20px;
}

/* SUCCESS */

.success {
    background: #dcfce7;

    color: #166534;

    padding: 13px;

    border-radius: 8px;

    margin-bottom: 20px;
}

/* DASHBOARD */

.dashboard-grid {
    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 20px;
}

.dashboard-card {
    background: white;

    padding: 25px;

    border-radius: 15px;

    text-align: center;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.08);
}

.dashboard-card .icon {
    font-size: 40px;

    margin-bottom: 12px;
}

.dashboard-card h3 {
    margin-bottom: 10px;
}

.dashboard-card a {
    display: inline-block;

    margin-top: 12px;

    color: #2563eb;

    text-decoration: none;

    font-weight: bold;
}

/* HOME */

.hero {
    min-height: 80vh;

    display: flex;

    justify-content: center;

    align-items: center;

    text-align: center;

    padding: 40px;
}

.hero h1 {
    font-size: 48px;

    color: #173b70;

    margin-bottom: 20px;
}

.hero h1 span {
    color: #2563eb;
}

.hero p {
    max-width: 700px;

    margin: auto;

    color: #64748b;

    font-size: 18px;

    line-height: 1.7;
}

.features {
    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 20px;

    margin-top: 40px;
}

.feature {
    background: white;

    padding: 25px;

    border-radius: 15px;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.08);
}

.feature h3 {
    margin: 10px 0;
}

/* LOGIN */

.login-page {
    min-height: 100vh;

    display: flex;

    justify-content: center;

    align-items: center;

    background: linear-gradient(
        135deg,
        #eef4ff,
        #dce8ff
    );
}

.login-container {
    width: 900px;

    max-width: 95%;

    min-height: 520px;

    display: flex;

    background: white;

    border-radius: 22px;

    overflow: hidden;

    box-shadow:
        0 15px 40px rgba(0,0,0,0.15);
}

.login-left {
    width: 50%;

    background: linear-gradient(
        135deg,
        #2563eb,
        #1e40af
    );

    color: white;

    padding: 55px 45px;

    display: flex;

    flex-direction: column;

    justify-content: center;
}

.login-left .icon {
    font-size: 60px;

    margin-bottom: 20px;
}

.login-left h1 {
    font-size: 38px;

    margin-bottom: 20px;
}

.login-left p {
    font-size: 16px;

    line-height: 1.7;
}

.login-right {
    width: 50%;

    padding: 55px 50px;

    display: flex;

    flex-direction: column;

    justify-content: center;
}

.login-right h2 {
    font-size: 32px;

    margin-bottom: 8px;
}

.subtitle {
    color: #64748b;

    font-size: 17px;

    margin-bottom: 28px;
}

.login-button {
    width: 100%;

    padding: 15px;

    border: none;

    border-radius: 9px;

    background: #2563eb;

    color: white;

    font-size: 17px;

    font-weight: bold;

    cursor: pointer;
}

.login-button:hover {
    background: #1d4ed8;
}

.home-link {
    text-align: center;

    margin-top: 20px;
}

.home-link a {
    color: #2563eb;

    text-decoration: none;

    font-weight: bold;
}

/* REPORT */

.report-grid {
    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 20px;
}

.report-card {
    background: white;

    padding: 25px;

    border-radius: 15px;

    text-align: center;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.08);
}

.report-card h2 {
    color: #2563eb;

    font-size: 32px;

    margin-top: 10px;
}

/* MOBILE */

@media(max-width: 800px) {

    .dashboard-grid,
    .report-grid,
    .features {
        grid-template-columns: 1fr 1fr;
    }

    .login-container {
        flex-direction: column;
    }

    .login-left,
    .login-right {
        width: 100%;
    }

}

@media(max-width: 500px) {

    .dashboard-grid,
    .report-grid,
    .features {
        grid-template-columns: 1fr;
    }

}

</style>

"""


# ============================================================
# NAVBAR
# ============================================================

def navbar():

    return """

    <div class="navbar">

        <div class="logo">
            🛡️ Insurance Management
        </div>

        <div class="nav-links">

            <a href="/dashboard">
                Dashboard
            </a>

            <a href="/customers">
                Customers
            </a>

            <a href="/policies">
                Policies
            </a>

            <a href="/claims">
                Claims
            </a>

            <a href="/prediction">
                Prediction
            </a>

            <a href="/reports">
                Reports
            </a>

            <a href="/admin">
                Admin
            </a>

            <a href="/logout">
                Logout
            </a>

        </div>

    </div>

    """


# ============================================================
# HOME HTML
# ============================================================

HOME_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Insurance Management System
</title>

""" + COMMON_CSS + """

</head>

<body>

<section class="hero">

<div>

<div style="font-size:60px;">
🛡️
</div>

<h1>
Insurance <span>Management</span>
</h1>

<p>

Welcome to the Insurance Management System.

Manage customers, policies, claims and
claim predictions easily from one place.

</p>

<br><br>

<a href="/login" class="btn">
Login
</a>

<div class="features">

<div class="feature">

<h3>
👥 Customers
</h3>

<p>
Manage customer information.
</p>

</div>


<div class="feature">

<h3>
📄 Policies
</h3>

<p>
Manage insurance policies.
</p>

</div>


<div class="feature">

<h3>
📝 Claims
</h3>

<p>
Manage insurance claims.
</p>

</div>


<div class="feature">

<h3>
🤖 Prediction
</h3>

<p>
Predict claim approval using ML.
</p>

</div>

</div>

</div>

</section>

</body>

</html>

"""


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/")
def home():

    return render_template_string(
        HOME_HTML
    )


# ============================================================
# LOGIN HTML
# ============================================================

LOGIN_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Login - Insurance Management
</title>

""" + COMMON_CSS + """

</head>

<body>

<div class="login-page">

<div class="login-container">


<!-- LEFT -->

<div class="login-left">

<div class="icon">
🛡️
</div>

<h1>
Insurance Management
</h1>

<p>

Manage customers, policies and claims
easily using the Insurance Management System.

</p>

</div>


<!-- RIGHT -->

<div class="login-right">

<h2>
Welcome Back
</h2>

<p class="subtitle">
Login to your account
</p>


{% if error %}

<div class="error">

{{ error }}

</div>

{% endif %}


<form method="POST"
      action="{{ url_for('login') }}">


<div class="form-group">

<label>
Username
</label>

<input
    type="text"
    name="username"
    placeholder="Enter username"
    required
>

</div>


<div class="form-group">

<label>
Password
</label>

<input
    type="password"
    name="password"
    placeholder="Enter password"
    required
>

</div>


<button
    type="submit"
    class="login-button"
>

Login

</button>


</form>


<div class="home-link">

<a href="/">
← Back to Home
</a>

</div>


</div>

</div>

</div>

</body>

</html>

"""


# ============================================================
# LOGIN ROUTE
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "GET":

        return render_template_string(
            LOGIN_HTML,
            error=None
        )


    username = request.form.get(
        "username",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    ).strip()


    if not username or not password:

        return render_template_string(
            LOGIN_HTML,
            error="Please enter username and password."
        )


    conn = None
    cursor = None

    try:

        conn = get_db_connection()

        cursor = conn.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT
                UserID,
                Name,
                Email,
                Username,
                Password
            FROM users
            WHERE Username = %s
            AND Password = %s
            LIMIT 1
            """,

            (
                username,
                password
            )
        )


        user = cursor.fetchone()


        if user is None:

            return render_template_string(
                LOGIN_HTML,
                error="Invalid username or password."
            )


        session["user_id"] = user["UserID"]

        session["username"] = user["Username"]

        session["name"] = user["Name"]

        session["email"] = user["Email"]


        return redirect(
            url_for("dashboard")
        )


    except mysql.connector.Error as e:

        return render_template_string(
            LOGIN_HTML,
            error="Database Error: " + str(e)
        )


    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


# ============================================================
# DASHBOARD HTML
# ============================================================

DASHBOARD_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Dashboard
</title>

""" + COMMON_CSS + """

</head>

<body>

""" + navbar() + """

<div class="main">

<div class="page-header">

<h1>
📊 Dashboard
</h1>

</div>


<div class="card">

<h2>
Welcome, {{ name }}
</h2>

<p style="margin-top:10px;color:#64748b;">

Insurance Management System Dashboard

</p>

</div>


<div class="dashboard-grid">


<div class="dashboard-card">

<div class="icon">
👥
</div>

<h3>
Customers
</h3>

<p>
Manage customers
</p>

<a href="/customers">
Open
</a>

</div>


<div class="dashboard-card">

<div class="icon">
📄
</div>

<h3>
Policies
</h3>

<p>
Manage policies
</p>

<a href="/policies">
Open
</a>

</div>


<div class="dashboard-card">

<div class="icon">
📝
</div>

<h3>
Claims
</h3>

<p>
Manage claims
</p>

<a href="/claims">
Open
</a>

</div>


<div class="dashboard-card">

<div class="icon">
🤖
</div>

<h3>
Prediction
</h3>

<p>
Predict claim status
</p>

<a href="/prediction">
Open
</a>

</div>


<div class="dashboard-card">

<div class="icon">
📈
</div>

<h3>
Reports
</h3>

<p>
View claim reports
</p>

<a href="/reports">
Open
</a>

</div>


<div class="dashboard-card">

<div class="icon">
👤
</div>

<h3>
Admin
</h3>

<p>
Manage users
</p>

<a href="/admin">
Open
</a>

</div>


</div>

</div>

</body>

</html>

"""


# ============================================================
# DASHBOARD ROUTE
# ============================================================

@app.route("/dashboard")
def dashboard():

    if not login_required():

        return redirect(
            url_for("login")
        )


    return render_template_string(
        DASHBOARD_HTML,
        name=session.get(
            "name",
            "User"
        )
    )


# ============================================================
# CUSTOMERS PAGE
# ============================================================

CUSTOMERS_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Customers
</title>

""" + COMMON_CSS + """

</head>

<body>

""" + navbar() + """

<div class="main">

<div class="page-header">

<h1>
👥 Customers
</h1>

<a href="/add_customer"
   class="btn">

+ Add Customer

</a>

</div>


<div class="card table-container">

<table>

<tr>

<th>
ID
</th>

<th>
Name
</th>

<th>
Age
</th>

<th>
Gender
</th>

<th>
Income
</th>

<th>
Policy Type
</th>

</tr>


{% for c in customers %}

<tr>

<td>
{{ c.CustomerID }}
</td>

<td>
{{ c.Name }}
</td>

<td>
{{ c.Age }}
</td>

<td>
{{ c.Gender }}
</td>

<td>
{{ c.Income }}
</td>

<td>
{{ c.PolicyType }}
</td>

</tr>

{% endfor %}

</table>

</div>

</div>

</body>

</html>

"""


# ============================================================
# CUSTOMERS ROUTE
# ============================================================

@app.route("/customers")
def customers():

    if not login_required():

        return redirect(
            url_for("login")
        )


    conn = None
    cursor = None

    try:

        conn = get_db_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM Customer
            ORDER BY CustomerID DESC
            """
        )

        data = cursor.fetchall()


        return render_template_string(
            CUSTOMERS_HTML,
            customers=data
        )


    except mysql.connector.Error as e:

        return "Database Error: " + str(e)


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ============================================================
# ADD CUSTOMER
# ============================================================

ADD_CUSTOMER_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Add Customer
</title>

""" + COMMON_CSS + """

</head>

<body>

""" + navbar() + """

<div class="main">

<div class="card form-card">

<h1>
Add Customer
</h1>

<br>


<form method="POST">


<div class="form-group">

<label>
Name
</label>

<input
    type="text"
    name="name"
    required
>

</div>


<div class="form-group">

<label>
Age
</label>

<input
    type="number"
    name="age"
    min="1"
    required
>

</div>


<div class="form-group">

<label>
Gender
</label>

<select name="gender"
        required>

<option value="">
Select Gender
</option>

<option value="Male">
Male
</option>

<option value="Female">
Female
</option>

<option value="Other">
Other
</option>

</select>

</div>


<div class="form-group">

<label>
Income
</label>

<input
    type="number"
    name="income"
    step="0.01"
    required
>

</div>


<div class="form-group">

<label>
Policy Type
</label>

<select name="policy_type"
        required>

<option value="">
Select Policy Type
</option>

<option value="Health">
Health
</option>

<option value="Life">
Life
</option>

<option value="Vehicle">
Vehicle
</option>

<option value="Travel">
Travel
</option>

</select>

</div>


<button
    type="submit"
    class="btn">

Save Customer

</button>


<a href="/customers"
   class="btn btn-secondary">

Cancel

</a>


</form>

</div>

</div>

</body>

</html>

"""


@app.route(
    "/add_customer",
    methods=["GET", "POST"]
)
def add_customer():

    if not login_required():

        return redirect(
            url_for("login")
        )


    if request.method == "POST":

        name = request.form["name"]

        age = request.form["age"]

        gender = request.form["gender"]

        income = request.form["income"]

        policy_type = request.form["policy_type"]


        conn = get_db_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            INSERT INTO Customer
            (Name, Age, Gender, Income, PolicyType)
            VALUES (%s, %s, %s, %s, %s)
            """,

            (
                name,
                age,
                gender,
                income,
                policy_type
            )
        )


        conn.commit()

        cursor.close()

        conn.close()


        return redirect(
            url_for("customers")
        )


    return render_template_string(
        ADD_CUSTOMER_HTML
    )


# ============================================================
# POLICIES PAGE
# ============================================================

POLICIES_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Policies
</title>

""" + COMMON_CSS + """

</head>

<body>

""" + navbar() + """

<div class="main">

<div class="page-header">

<h1>
📄 Policies
</h1>

<a href="/add_policy"
   class="btn">

+ Add Policy

</a>

</div>


<div class="card table-container">

<table>

<tr>

<th>
Policy ID
</th>

<th>
Customer ID
</th>

<th>
Customer Name
</th>

<th>
Duration
</th>

<th>
Premium
</th>

</tr>


{% for p in policies %}

<tr>

<td>
{{ p.PolicyID }}
</td>

<td>
{{ p.CustomerID }}
</td>

<td>
{{ p.Name }}
</td>

<td>
{{ p.PolicyDuration }}
years
</td>

<td>
₹ {{ p.PremiumAmount }}
</td>

</tr>

{% endfor %}

</table>

</div>

</div>

</body>

</html>

"""


@app.route("/policies")
def policies():

    if not login_required():

        return redirect(
            url_for("login")
        )


    conn = get_db_connection()

    cursor = conn.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            p.PolicyID,
            p.CustomerID,
            c.Name,
            p.PolicyDuration,
            p.PremiumAmount
        FROM Policy p
        JOIN Customer c
        ON p.CustomerID = c.CustomerID
        ORDER BY p.PolicyID DESC
        """
    )


    data = cursor.fetchall()


    cursor.close()

    conn.close()


    return render_template_string(
        POLICIES_HTML,
        policies=data
    )


# ============================================================
# ADD POLICY
# ============================================================

ADD_POLICY_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Add Policy
</title>

""" + COMMON_CSS + """

</head>

<body>

""" + navbar() + """

<div class="main">

<div class="card form-card">

<h1>
Add Policy
</h1>

<br>


<form method="POST">


<div class="form-group">

<label>
Customer
</label>

<select name="customer_id"
        required>

<option value="">
Select Customer
</option>

{% for c in customers %}

<option value="{{ c.CustomerID }}">

{{ c.CustomerID }} - {{ c.Name }}

</option>

{% endfor %}

</select>

</div>


<div class="form-group">

<label>
Policy Duration
</label>

<input
    type="number"
    name="duration"
    min="1"
    required
>

</div>


<div class="form-group">

<label>
Premium Amount
</label>

<input
    type="number"
    name="premium"
    step="0.01"
    required
>

</div>


<button
    type="submit"
    class="btn">

Save Policy

</button>


<a href="/policies"
   class="btn btn-secondary">

Cancel

</a>


</form>

</div>

</div>

</body>

</html>

"""


@app.route(
    "/add_policy",
    methods=["GET", "POST"]
)
def add_policy():

    if not login_required():

        return redirect(
            url_for("login")
        )


    conn = get_db_connection()

    cursor = conn.cursor(
        dictionary=True
    )


    if request.method == "POST":

        customer_id = request.form[
            "customer_id"
        ]

        duration = request.form[
            "duration"
        ]

        premium = request.form[
            "premium"
        ]


        cursor.execute(
            """
            INSERT INTO Policy
            (
                CustomerID,
                PolicyDuration,
                PremiumAmount
            )
            VALUES (%s, %s, %s)
            """,

            (
                customer_id,
                duration,
                premium
            )
        )


        conn.commit()

        cursor.close()

        conn.close()


        return redirect(
            url_for("policies")
        )


    cursor.execute(
        """
        SELECT
            CustomerID,
            Name
        FROM Customer
        ORDER BY Name
        """
    )


    customers_data = cursor.fetchall()


    cursor.close()

    conn.close()


    return render_template_string(
        ADD_POLICY_HTML,
        customers=customers_data
    )


# ============================================================
# CLAIMS PAGE
# ============================================================

CLAIMS_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Claims
</title>

""" + COMMON_CSS + """

</head>

<body>

""" + navbar() + """

<div class="main">

<div class="page-header">

<h1>
📝 Claims
</h1>

<a href="/add_claim"
   class="btn">

+ Add Claim

</a>

</div>


<div class="card table-container">

<table>

<tr>

<th>
Claim ID
</th>

<th>
Policy ID
</th>

<th>
Customer
</th>

<th>
Claim Amount
</th>

<th>
Status
</th>

</tr>


{% for c in claims %}

<tr>

<td>
{{ c.ClaimID }}
</td>

<td>
{{ c.PolicyID }}
</td>

<td>
{{ c.Name }}
</td>

<td>
₹ {{ c.ClaimAmount }}
</td>

<td>
{{ c.ClaimStatus }}
</td>

</tr>

{% endfor %}

</table>

</div>

</div>

</body>

</html>

"""


@app.route("/claims")
def claims():

    if not login_required():

        return redirect(
            url_for("login")
        )


    conn = get_db_connection()

    cursor = conn.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            cl.ClaimID,
            cl.PolicyID,
            c.Name,
            cl.ClaimAmount,
            cl.ClaimStatus
        FROM Claim cl
        JOIN Policy p
        ON cl.PolicyID = p.PolicyID
        JOIN Customer c
        ON p.CustomerID = c.CustomerID
        ORDER BY cl.ClaimID DESC
        """
    )


    data = cursor.fetchall()


    cursor.close()

    conn.close()


    return render_template_string(
        CLAIMS_HTML,
        claims=data
    )


# ============================================================
# ADD CLAIM
# ============================================================

ADD_CLAIM_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Add Claim
</title>

""" + COMMON_CSS + """

</head>

<body>

""" + navbar() + """

<div class="main">

<div class="card form-card">

<h1>
Add Claim
</h1>

<br>


<form method="POST">


<div class="form-group">

<label>
Policy
</label>

<select name="policy_id"
        required>

<option value="">
Select Policy
</option>

{% for p in policies %}

<option value="{{ p.PolicyID }}">

Policy {{ p.PolicyID }}
-
{{ p.Name }}

</option>

{% endfor %}

</select>

</div>


<div class="form-group">

<label>
Claim Amount
</label>

<input
    type="number"
    name="claim_amount"
    step="0.01"
    required
>

</div>


<div class="form-group">

<label>
Claim Status
</label>

<select name="claim_status"
        required>

<option value="Approved">
Approved
</option>

<option value="Rejected">
Rejected
</option>

</select>

</div>


<button
    type="submit"
    class="btn">

Save Claim

</button>


<a href="/claims"
   class="btn btn-secondary">

Cancel

</a>


</form>

</div>

</div>

</body>

</html>

"""


@app.route(
    "/add_claim",
    methods=["GET", "POST"]
)
def add_claim():

    if not login_required():

        return redirect(
            url_for("login")
        )


    conn = get_db_connection()

    cursor = conn.cursor(
        dictionary=True
    )


    if request.method == "POST":

        policy_id = request.form[
            "policy_id"
        ]

        claim_amount = request.form[
            "claim_amount"
        ]

        claim_status = request.form[
            "claim_status"
        ]


        cursor.execute(
            """
            INSERT INTO Claim
            (
                PolicyID,
                ClaimAmount,
                ClaimStatus
            )
            VALUES (%s, %s, %s)
            """,

            (
                policy_id,
                claim_amount,
                claim_status
            )
        )


        conn.commit()

        cursor.close()

        conn.close()


        return redirect(
            url_for("claims")
        )


    cursor.execute(
        """
        SELECT
            p.PolicyID,
            c.Name
        FROM Policy p
        JOIN Customer c
        ON p.CustomerID = c.CustomerID
        ORDER BY p.PolicyID
        """
    )


    policies_data = cursor.fetchall()


    cursor.close()

    conn.close()


    return render_template_string(
        ADD_CLAIM_HTML,
        policies=policies_data
    )


# ============================================================
# PREDICTION PAGE
# ============================================================

PREDICTION_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Claim Prediction
</title>

""" + COMMON_CSS + """

</head>

<body>

""" + navbar() + """

<div class="main">

<div class="card form-card">

<h1>
🤖 Insurance Claim Prediction
</h1>

<br>

{% if error %}

<div class="error">
{{ error }}
</div>

{% endif %}


{% if result %}

<div class="success">

<h2>
Prediction Result
</h2>

<br>

<p>
{{ result }}
</p>

<br>

<p>
Accuracy: {{ accuracy }}%
</p>

</div>

{% endif %}


<form method="POST">


<div class="form-group">

<label>
Age
</label>

<input
    type="number"
    name="age"
    required
>

</div>


<div class="form-group">

<label>
Income
</label>

<input
    type="number"
    name="income"
    step="0.01"
    required
>

</div>


<div class="form-group">

<label>
Policy Duration
</label>

<input
    type="number"
    name="duration"
    required
>

</div>


<div class="form-group">

<label>
Premium Amount
</label>

<input
    type="number"
    name="premium"
    step="0.01"
    required
>

</div>


<div class="form-group">

<label>
Claim Amount
</label>

<input
    type="number"
    name="claim_amount"
    step="0.01"
    required
>

</div>


<button
    type="submit"
    class="btn">

Predict Claim

</button>


</form>

</div>

</div>

</body>

</html>

"""


# ============================================================
# PREDICTION ROUTE
# ============================================================

@app.route(
    "/prediction",
    methods=["GET", "POST"]
)
def prediction():

    if not login_required():

        return redirect(
            url_for("login")
        )


    if request.method == "GET":

        return render_template_string(
            PREDICTION_HTML,
            result=None,
            accuracy=0,
            error=None
        )


    try:

        age = float(
            request.form["age"]
        )

        income = float(
            request.form["income"]
        )

        duration = float(
            request.form["duration"]
        )

        premium = float(
            request.form["premium"]
        )

        claim_amount = float(
            request.form["claim_amount"]
        )


        conn = get_db_connection()

        cursor = conn.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT
                c.Age,
                c.Income,
                p.PolicyDuration,
                p.PremiumAmount,
                cl.ClaimAmount,
                cl.ClaimStatus
            FROM Customer c
            JOIN Policy p
            ON c.CustomerID = p.CustomerID
            JOIN Claim cl
            ON p.PolicyID = cl.PolicyID
            """
        )


        data = cursor.fetchall()


        cursor.close()

        conn.close()


        if len(data) < 2:

            return render_template_string(
                PREDICTION_HTML,
                result=None,
                accuracy=0,
                error=(
                    "At least 2 claim records "
                    "are required for prediction."
                )
            )


        df = pd.DataFrame(data)


        df["ClaimStatus"] = (
            df["ClaimStatus"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "rejected": 0,
                "approved": 1
            })
        )


        df = df.dropna()


        if df["ClaimStatus"].nunique() < 2:

            return render_template_string(
                PREDICTION_HTML,
                result=None,
                accuracy=0,
                error=(
                    "Training data must contain "
                    "both Approved and Rejected claims."
                )
            )


        features = [
            "Age",
            "Income",
            "PolicyDuration",
            "PremiumAmount",
            "ClaimAmount"
        ]


        X = df[features]

        y = df["ClaimStatus"]


        if len(df) >= 4:

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.25,
                random_state=42,
                stratify=y
            )

        else:

            X_train = X

            X_test = X

            y_train = y

            y_test = y


        scaler = StandardScaler()


        X_train_scaled = scaler.fit_transform(
            X_train
        )

        X_test_scaled = scaler.transform(
            X_test
        )


        model = LogisticRegression()

        model.fit(
            X_train_scaled,
            y_train
        )


        prediction_data = [[
            age,
            income,
            duration,
            premium,
            claim_amount
        ]]


        prediction_scaled = scaler.transform(
            prediction_data
        )


        prediction_value = model.predict(
            prediction_scaled
        )[0]


        test_prediction = model.predict(
            X_test_scaled
        )


        accuracy = accuracy_score(
            y_test,
            test_prediction
        ) * 100


        if prediction_value == 1:

            result = "Claim is likely to be APPROVED."

        else:

            result = "Claim is likely to be REJECTED."


        return render_template_string(
            PREDICTION_HTML,
            result=result,
            accuracy=round(
                accuracy,
                2
            ),
            error=None
        )


    except Exception as e:

        return render_template_string(
            PREDICTION_HTML,
            result=None,
            accuracy=0,
            error=str(e)
        )


# ============================================================
# REPORTS
# ============================================================

REPORTS_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Reports
</title>

""" + COMMON_CSS + """

</head>

<body>

""" + navbar() + """

<div class="main">

<div class="page-header">

<h1>
📈 Claim Reports
</h1>

</div>


<div class="report-grid">


<div class="report-card">

<h3>
Total Claims
</h3>

<h2>
{{ total_claims }}
</h2>

</div>


<div class="report-card">

<h3>
Approved Claims
</h3>

<h2>
{{ approved_claims }}
</h2>

</div>


<div class="report-card">

<h3>
Rejected Claims
</h3>

<h2>
{{ rejected_claims }}
</h2>

</div>


<div class="report-card">

<h3>
Total Claim Amount
</h3>

<h2>
₹ {{ total_amount }}
</h2>

</div>


</div>

</div>

</body>

</html>

"""


@app.route("/reports")
def reports():

    if not login_required():

        return redirect(
            url_for("login")
        )


    conn = get_db_connection()

    cursor = conn.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM Claim
        """
    )

    total_claims = cursor.fetchone()[
        "total"
    ]


    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM Claim
        WHERE LOWER(TRIM(ClaimStatus))
        = 'approved'
        """
    )

    approved_claims = cursor.fetchone()[
        "total"
    ]


    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM Claim
        WHERE LOWER(TRIM(ClaimStatus))
        = 'rejected'
        """
    )

    rejected_claims = cursor.fetchone()[
        "total"
    ]


    cursor.execute(
        """
        SELECT
            COALESCE(
                SUM(ClaimAmount),
                0
            ) AS total
        FROM Claim
        """
    )

    total_amount = cursor.fetchone()[
        "total"
    ]


    cursor.close()

    conn.close()


    return render_template_string(
        REPORTS_HTML,

        total_claims=total_claims,

        approved_claims=approved_claims,

        rejected_claims=rejected_claims,

        total_amount=total_amount
    )


# ============================================================
# ADMIN PAGE
# ============================================================

ADMIN_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>
Admin
</title>

""" + COMMON_CSS + """

</head>

<body>

""" + navbar() + """

<div class="main">

<div class="page-header">

<h1>
👤 Admin
</h1>

</div>


<div class="card table-container">

<table>

<tr>

<th>
User ID
</th>

<th>
Name
</th>

<th>
Email
</th>

<th>
Username
</th>

</tr>


{% for u in users %}

<tr>

<td>
{{ u.UserID }}
</td>

<td>
{{ u.Name }}
</td>

<td>
{{ u.Email }}
</td>

<td>
{{ u.Username }}
</td>

</tr>

{% endfor %}

</table>

</div>

</div>

</body>

</html>

"""


@app.route("/admin")
def admin():

    if not login_required():

        return redirect(
            url_for("login")
        )


    conn = get_db_connection()

    cursor = conn.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            UserID,
            Name,
            Email,
            Username
        FROM users
        ORDER BY UserID
        """
    )


    users_data = cursor.fetchall()


    cursor.close()

    conn.close()


    return render_template_string(
        ADMIN_HTML,
        users=users_data
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print(
        "Starting Insurance Management System..."
    )

    try:

        test_conn = get_db_connection()

        test_conn.close()

        print(
            "Database connected successfully!"
        )

    except Exception as e:

        print(
            "Database connection failed:"
        )

        print(e)


    app.run(
        debug=True
    )
