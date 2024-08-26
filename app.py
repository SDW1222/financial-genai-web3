from flask import Flask, render_template, request
import google.generativeai as palm

model = {"model": "models/chat-bison-001"}
palm.configure(api_key="AIzaSyCaQcgKn95ZO6AR1t2PXzk9UydTkt4sWZQ")

app = Flask(__name__)
user_name = ""
flag = 1

@app.route("/", methods=["GET", "POST"])
def index():
    global flag
    flag = 1
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    global flag, user_name
    if flag == 1:
        user_name = request.form.get("q")
        flag = 0
    return render_template("main.html", r=user_name)

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    q = request.form.get("q")
    return render_template("prediction.html", r=q)

@app.route("/DBS", methods=["GET", "POST"])
def DBS():
    return render_template("DBS.html")

@app.route("/DBS_prediction", methods=["GET", "POST"])
def DBS_prediction():
    q = request.form.get("q")
    q = float(q)  # Convert q to a float before using it in a calculation
    return render_template("DBS_prediction.html", r=90.2 + (-50.6 * q))

@app.route("/creditability",methods=["GET","POST"])
def creditability():
    return(render_template("creditability.html"))

@app.route("/creditability_prediction",methods=["GET","POST"])
def creditabiity_prediction():
    q = float(request.form.get("q"))
    return(render_template("credictability_prediction.html",r=1.22937616 + (-0.00011189*q)))

@app.route("/makersuite", methods=["GET", "POST"])
def makersuite():
    return render_template("makersuite.html")

@app.route("/makersuite_1", methods=["GET", "POST"])
def makersuite_1():
    q = "Can you help me prepare my tax return?"
    r = palm.chat(**model, messages=[{"content": q}])
    response_text = r.last['content']  # Ensure you're extracting the 'content' key
    return render_template("makersuite_1_reply.html", r=response_text)

@app.route("/makersuite_gen", methods=["GET", "POST"])
def makersuite_gen():
    q = request.form.get("q")
    r = palm.chat(**model, messages=[{"content": q}])
    response_text = r.last['content']  # Extracting the 'content' key from the response
    return render_template("makersuite_gen_reply.html", r=response_text)

if __name__ == "__main__":
    app.run()

#W4

