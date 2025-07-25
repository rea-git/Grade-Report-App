from flask import Flask, render_template, request
import matplotlib.pyplot as plt

app = Flask(__name__)

data = {
    'student_id': [],
    'course_id': [],
    'marks': []
}

# Load CSV
with open("data.csv") as f:
    next(f)
    for line in f:
        sid, cid, mark = line.strip().split(',')
        data['student_id'].append(int(sid))
        data['course_id'].append(int(cid))
        data['marks'].append(int(mark))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    id_type = request.form.get("ID")
    id_value = request.form.get("id_value")

    if not id_type or not id_value or not id_value.isdigit():
        return render_template("error.html")

    id_value = int(id_value)

    if id_type == "student_id":
        if id_value not in data['student_id']:
            return render_template("error.html")

        filtered = []
        total = 0
        for i in range(len(data['student_id'])):
            if data['student_id'][i] == id_value:
                filtered.append([
                    data['student_id'][i],
                    data['course_id'][i],
                    data['marks'][i]
                ])
                total += data['marks'][i]

        return render_template("student.html", data=filtered, total_marks=total)

    elif id_type == "course_id":
        if id_value not in data['course_id']:
            return render_template("error.html")

        marks_list = []
        for i in range(len(data['course_id'])):
            if data['course_id'][i] == id_value:
                marks_list.append(data['marks'][i])

        average = sum(marks_list) / len(marks_list)
        maximum = max(marks_list)

        # Save histogram image
        plt.figure()
        plt.hist(marks_list)
        plt.xlabel("Marks")
        plt.ylabel("Frequency")
        plt.title(f"Histogram for Course ID {id_value}")
        plt.savefig("static/histogram.png")
        plt.close()

        return render_template(
            "course.html",
            average_marks=round(average, 2),
            maximum_marks=maximum,
            image_path="/static/histogram.png"
        )
if __name__ == "__main__":
    app.run()