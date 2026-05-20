from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def init_db():

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            role TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET", "POST"])
def home():

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]

        cursor.execute(
            "INSERT INTO jobs (company, role, status) VALUES (?, ?, ?)",
            (company, role, status)
        )

        conn.commit()

        return redirect("/")

    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    conn.close()

    return render_template("index.html", jobs=jobs)


@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)