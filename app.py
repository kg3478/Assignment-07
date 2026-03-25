from flask import Flask, request

import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        singer = request.form["singer"]
        videos = request.form["videos"]
        duration = request.form["duration"]
        email = request.form["email"]

        try:
            subprocess.run([
                "python3",
                "102303478.py",
                singer,
                videos,
                duration,
                "output.mp3"
            ])

            return f"""
            <h3>Mashup created successfully!</h3>
            <p>Requested by: {email}</p>
            <p>File generated: output.mp3</p>
            """

        except:
            return "Error occurred"

    return """
    <h2>Mashup Generator</h2>
    <form method="post">
        Singer Name: <input name="singer"><br><br>
        Number of Videos: <input name="videos"><br><br>
        Duration: <input name="duration"><br><br>
        Email: <input name="email"><br><br>
        <button type="submit">Generate</button>
    </form>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
