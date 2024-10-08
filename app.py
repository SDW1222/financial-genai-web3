from flask import Flask,render_template,request
import google.generativeai as genai
import os
import numpy as np
from textblob import TextBlob


#api = os.getenv("MAKERSUITE_API_TOKEN")
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key="AIzaSyCluRjLkwn6IOe4f-dNTlusyuAkDUI7fQo")

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

@app.route("/sentiment_analysis", methods=["GET", "POST"])
def sentiment_analysis():
    sentiment_textblob = None
    sentiment_transformers = None

    if request.method == "POST":
        text = request.form.get("text")  # Get the input text from the form
        
        # Perform sentiment analysis using TextBlob
        sentiment_textblob = analyze_sentiment_textblob(text)
        
        # Perform sentiment analysis using transformers
        sentiment_transformers = analyze_sentiment_transformers(text)
    
    return render_template(
        "sentiment_analysis.html", 
        sentiment_textblob=sentiment_textblob,
        sentiment_transformers=sentiment_transformers
    )


@app.route("/makersuite", methods=["GET", "POST"])
def makersuite():
    return render_template("makersuite.html")

@app.route("/makersuite_1", methods=["GET", "POST"])
def makersuite_1():
    q = "Can you help me prepare my tax return?"
    r = model.generate_content(q) # Pass 'q' directly as the prompt
    return render_template("makersuite_1_reply.html", r=r.text)

@app.route("/makersuite_gen", methods=["GET", "POST"])
def makersuite_gen():
    q = request.form.get("q")
    r = model.generate_content(q)
    return render_template("makersuite_gen_reply.html", r=r.text)

@app.route("/sentiment", methods=["GET", "POST"])
def sentiment():
    if request.method == "POST":
        # Get the input text from the form
        input_text = request.form.get("text")
        
        # Check if the input text is not None or empty
        if input_text:
            # Perform sentiment analysis
            blob = TextBlob(input_text)
            sentiment = blob.sentiment
            
            # Extract polarity and subjectivity
            polarity = sentiment.polarity
            subjectivity = sentiment.subjectivity
            
            # Render the results in the template
            return render_template("sentiment_result.html", text=input_text, polarity=polarity, subjectivity=subjectivity)
        else:
            # Handle the case where no text was entered
            error_message = "Please enter some text to analyze."
            return render_template("sentiment.html", error=error_message)
    
    # Render the input form if the request method is GET
    return render_template("sentiment.html")

if __name__ == "__main__":
    app.run()