from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# =====================================================
# DATABASE CONFIG (PUT YOUR LEAPCELL DETAILS HERE)
# =====================================================
DB_CONFIG = {
    "host": "9qasp5v56q8ckkf5dc.leapcellpool.com",
    "database": "hsffoptfuzrlioyiiawh",
    "user": "myptxdhligxjqhlphkfb",
    "password": "hitoxmaevgwpldxcibyoqtgtqzcpos",
    "port": 6438,
    "sslmode": "require"
}

# =====================================================
# DB CONNECTION (PER REQUEST)
# =====================================================
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None


# =====================================================
# REGISTER
# =====================================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password)
            )
        except psycopg2.errors.UniqueViolation:
            cur.close()
            conn.close()
            return "<h3>Username already exists ❌</h3>"

        cur.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

# =====================================================
# LOGIN
# =====================================================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT password_hash FROM users WHERE username = %s",
            (username,)
        )
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user and user[0] == password:
            return "<h2>Login Successful ✅</h2>"
        else:
            return "<h2>Invalid Credentials ❌</h2>"

    return render_template("login.html")

# =====================================================
if __name__ == "__main__":
    app.run(debug=True)

