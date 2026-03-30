from flask import Flask, render_template_string, request
from essay_scoring.model import vectorizer, model
from code_scoring.test_cases import evaluate_code
from code_scoring.code_features import code_quality_score
from essay_scoring.plagiarism import plagiarism_score
from essay_scoring.feature_extraction import explain_essay
from code_scoring.code_feedback import get_code_feedback
import multiprocessing

multiprocessing.freeze_support()

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AutoGrade System</title>
<style>
body{
font-family:Arial;
background:linear-gradient(135deg,#667eea,#764ba2);
margin:0;
padding:0;
color:white;
}

.container{
width:80%;
margin:auto;
padding:30px;
}

h1{
text-align:center;
margin-bottom:40px;
}

.card{
background:white;
color:#333;
padding:25px;
border-radius:12px;
margin-bottom:30px;
box-shadow:0px 10px 25px rgba(0,0,0,0.2);
}

textarea{
width:100%;
padding:12px;
border-radius:8px;
border:1px solid #ccc;
font-size:15px;
}

button{
margin-top:15px;
padding:12px 25px;
background:linear-gradient(135deg,#667eea,#764ba2);
border:none;
border-radius:25px;
color:white;
font-size:16px;
cursor:pointer;
}

.result{
background:#00c9a7;
padding:15px;
border-radius:10px;
font-size:18px;
text-align:center;
margin-top:20px;
color:white;
}

footer{
text-align:center;
margin-top:40px;
font-size:14px;
opacity:0.8;
}

.progress{
width:100%;
background:#ddd;
border-radius:10px;
overflow:hidden;
margin:10px 0 20px 0;
height:22px;
}

.progress-bar{
height:100%;
text-align:center;
font-weight:bold;
color:white;
line-height:22px;
border-radius:10px;
}

.green{background:#28a745;}
.yellow{background:#ffc107;color:black;}
.red{background:#dc3545;}
</style>
</head>

<body>

<div class="container">

<h1> AutoGrade Evaluation System</h1>

<div class="card">
<h2>📝 Essay Scoring</h2>
<form method="post">
<textarea name="essay" rows="6" placeholder="Paste your essay here..."></textarea>
<br>
<button type="submit">Evaluate Essay</button>
</form>
</div>

<div class="card">
<h2>💻 Code Scoring (Python)</h2>
<form method="post">
<textarea name="code" rows="6" placeholder="Paste your Python code here..."></textarea>
<br>
<button type="submit">Evaluate Code</button>
</form>
</div>

{% if result %}
<div class="result">
{{ result | safe }}
</div>
{% endif %}

<footer>
AutoGrade | ML-Based Automatic Code & Essay Scoring
</footer>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():

    result = None

    if request.method == "POST":

        essay = request.form.get("essay","").strip()
        code = request.form.get("code","").strip()

        if essay:

            vec = vectorizer.transform([essay])
            score = model.predict(vec)[0]

            reference_essay = "Artificial intelligence is transforming education and automation."
            similarity = plagiarism_score(essay, reference_essay)

            if similarity > 70:
                plagiarism_status = "⚠️ High Similarity Found"
                plag_color = "red"
            else:
                plagiarism_status = " Similarity Within Expected Range"
                plag_color = "green"

            score_percent = int((score/10)*100)

            if score >= 7:
                score_color = "green"
            elif score >= 5:
                score_color = "yellow"
            else:
                score_color = "red"

            feedback = explain_essay(essay)

            result = f"""
<b>Predicted Essay Score:</b> {round(score,2)} / 10

<div class="progress">
<div class="progress-bar {score_color}" style="width:{score_percent}%">
{score_percent}%
</div>
</div>

<b>Expected Similarity:</b> {round(similarity,2)}%

<div class="progress">
<div class="progress-bar {plag_color}" style="width:{similarity}%">
{round(similarity,2)}%
</div>
</div>

<b>Status:</b> {plagiarism_status}<br><br>

<b>Essay Analysis:</b><br>
Word Count: {feedback['word_count']}<br>
Vocabulary Richness: {feedback['vocab_richness']}<br>
{feedback['length_feedback']}<br>
{feedback['vocab_feedback']}
"""

        elif code:

            feedback = get_code_feedback(code)

            if feedback["status"] != "ok":

                result = f"<b>Code Feedback:</b><br>{feedback['message']}"

            else:

                test_cases = [
                    {"input":(2,3),"output":5},
                    {"input":(5,5),"output":10}
                ]

                test_score, test_results = evaluate_code(code, test_cases, func_name="add")
                quality_score = code_quality_score(code)

                final_score = (0.7*test_score) + (0.3*quality_score)

                result = f"""
                    <b>Final Code Score:</b> {round(final_score,2)} / 10<br><br>
                    <b>Test Case Score:</b> {round(test_score,2)} / 10<br>
                    <b>Code Quality Score:</b> {round(quality_score,2)} / 10<br><br>
                    <b>Code Feedback:</b><br>
                    {feedback['message']}
                    """

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
