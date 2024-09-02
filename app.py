from flask import Flask,render_template,request
import google.generativeai as palm
import os
import numpy as np

api = os.getenv("MAKERSUITE_API_TOKEN")
model = {"model": "models/text-bison-001"}
palm.configure(api_key="AIzaSyCluRjLkwn6IOe4f-dNTlusyuAkDUI7fQo")

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


@app.route("/joke", methods=["GET", "POST"])
def joke():
    joke = """Why did the Singaporean bring a tissue packet to the job interview?

Answer:
To "chope" the best seat in the waiting area!"""
    return render_template("joke.html", j=joke)


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
def creditability_prediction():
    q = float(request.form.get("q"))
    r=1.22937616 + (-0.00011189*q)
    r = np.where(r >= 0.5, "yes","no")
    r = str(r)
    return(render_template("creditability_prediction.html",r=r))

@app.route("/makersuite", methods=["GET", "POST"])
def makersuite():
    return render_template("makersuite.html")

@app.route("/makersuite_1", methods=["GET", "POST"])
def makersuite_1():
    q = "Can you help me prepare my tax return?"
    try:
        r = palm.generate_text(**model, prompt=q)  # Pass 'q' directly as the prompt
        response_text = r.result  # Assuming 'result' is a method or property that gives the generated text
    except Exception as e:
        print(f"An error occurred: {e}")
        response_text = "An error occurred while processing your request."
    return render_template("makersuite_1_reply.html", r=response_text)

@app.route("/makersuite_gen", methods=["GET", "POST"])
def makersuite_gen():
    q = request.form.get("q")
    try:
        r = palm.generate_text(**model, prompt=q)  # Pass 'q' directly as the prompt
        response_text = r.result  # Assuming 'result' is a method or property that gives the generated text
    except Exception as e:
        print(f"An error occurred: {e}")
        response_text = "An error occurred while processing your request."
    return render_template("makersuite_gen_reply.html", r=response_text)




if __name__ == "__main__":
    app.run()