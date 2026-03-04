from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app import db, bcrypt
from app.models import User, Quiz, Question, Attempt
from app.models import User, Quiz, Question, Attempt

main = Blueprint('main', __name__)


@main.route("/")
def home():
    return redirect(url_for("main.login"))


# ---------------- REGISTER ----------------
@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(username=username, email=email, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@main.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    quizzes = Quiz.query.filter_by(user_id=session["user_id"]).all()
    attempts = Attempt.query.filter_by(user_id=session["user_id"]).all()

    # Chart data
    chart_labels = []
    chart_scores = []

    total_percentage = 0

    for i, attempt in enumerate(attempts):

        chart_labels.append(f"Attempt {i+1}")

        if attempt.total > 0:
            percentage = int((attempt.score / attempt.total) * 100)
        else:
            percentage = 0

        chart_scores.append(percentage)
        total_percentage += percentage

    # Analytics metrics
    total_attempts = len(attempts)

    avg_score = int(total_percentage / total_attempts) if total_attempts > 0 else 0

    best_score = max(chart_scores) if chart_scores else 0

    return render_template(
        "dashboard.html",
        quizzes=quizzes,
        attempts=attempts,
        chart_labels=chart_labels,
        chart_scores=chart_scores,
        avg_score=avg_score,
        best_score=best_score
    )


# ---------------- CREATE QUIZ ----------------
@main.route("/create_quiz", methods=["GET", "POST"])
def create_quiz():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":

        title = request.form["title"]

        quiz = Quiz(
            title=title,
            user_id=session["user_id"]
        )

        db.session.add(quiz)
        db.session.commit()

        flash("Quiz created successfully!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("create_quiz.html")


# ---------------- QUIZ DETAIL ----------------
@main.route("/quiz/<int:quiz_id>")
def quiz_detail(quiz_id):

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    quiz = Quiz.query.get_or_404(quiz_id)

    return render_template(
        "quiz_detail.html",
        quiz=quiz
    )


# ---------------- ADD QUESTION ----------------
@main.route("/add_question/<int:quiz_id>", methods=["GET", "POST"])
def add_question(quiz_id):

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == "POST":

        question = Question(

            question_text=request.form["question_text"],

            option_a=request.form["option_a"],
            option_b=request.form["option_b"],
            option_c=request.form["option_c"],
            option_d=request.form["option_d"],

            correct_answer=request.form["correct_answer"],

            quiz_id=quiz.id
        )

        db.session.add(question)
        db.session.commit()

        flash("Question added successfully!", "success")
        return redirect(url_for("main.quiz_detail", quiz_id=quiz.id))

    return render_template(
        "add_question.html",
        quiz=quiz
    )


# ---------------- TAKE QUIZ ----------------
@main.route("/take_quiz/<int:quiz_id>", methods=["GET", "POST"])
def take_quiz(quiz_id):

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == "POST":

        score = 0

        for question in quiz.questions:

            selected = request.form.get(str(question.id))

            if selected == question.correct_answer:
                score += 1

        attempt = Attempt(
            score=score,
            total=len(quiz.questions),
            user_id=session["user_id"],
            quiz_id=quiz.id
        )

        db.session.add(attempt)
        db.session.commit()

        return render_template(
            "result.html",
            score=score,
            total=len(quiz.questions)
        )

    return render_template(
        "take_quiz.html",
        quiz=quiz
    )
    
    # ---------------- DELETE ----------------
@main.route("/delete_quiz/<int:quiz_id>", methods=["POST"])
def delete_quiz(quiz_id):

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    quiz = Quiz.query.get_or_404(quiz_id)

    # delete related questions
    Question.query.filter_by(quiz_id=quiz.id).delete()

    # delete related attempts
    Attempt.query.filter_by(quiz_id=quiz.id).delete()

    # delete the quiz
    db.session.delete(quiz)
    db.session.commit()

    flash("Quiz deleted successfully!", "warning")

    return redirect(url_for("main.dashboard"))


# ---------------- LOGOUT ----------------
@main.route("/logout")
def logout():

    session.pop("user_id", None)

    return redirect(url_for("main.login"))