from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from DAL import create_table, insert_project_with_images, get_all_projects_with_images  

app = Flask(__name__)
create_table()  # ensures the table exists
app.secret_key = "supersecret" 

# --- Upload configuration ---
UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html", active="home")

@app.route("/about")
def about():
    return render_template("about.html", active="about")

@app.route('/projects')
def projects():
    projects = get_all_projects_with_images()
    return render_template('projects.html', projects=projects)


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        link = request.form.get('link') or None
        image_files = request.files.getlist('images')
        saved_filenames = []

        for file in image_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                saved_filenames.append(filename)

        insert_project_with_images(title, description, saved_filenames, link)
        return redirect(url_for('projects'))

    return render_template('form.html')


@app.route("/resume")
def resume():
    return render_template("resume.html", active="resume")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        first = request.form.get("firstName", "").strip()
        last = request.form.get("lastName", "").strip()
        email = request.form.get("email", "").strip()
        pw = request.form.get("password", "")
        cpw = request.form.get("confirmPassword", "")

        errors = []
        if not first:
            errors.append("First name is required.")
        if not last:
            errors.append("Last name is required.")
        if not email or "@" not in email:
            errors.append("A valid email is required.")
        if len(pw) < 8:
            errors.append("Password must be at least 8 characters.")
        if pw != cpw:
            errors.append("Passwords must match.")

        if errors:
            for e in errors:
                flash(e)
            return render_template("contact.html", active="contact"), 400

        return redirect(url_for("thankyou"))
    return render_template("contact.html", active="contact")

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html", active="thankyou")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

