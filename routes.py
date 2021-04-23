from flask import render_template, request, jsonify, redirect
from app import app
from app import database as db_helper

@app.route("/deleteReview/<int:uID>", methods=['POST'])
def delete(uID):
    """ recieved post requests for entry delete """
    data = request.get_json()
    try:
        db_helper.remove_review_by_id(uID, data['courseName'])
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/editReview/<int:uID>", methods=['POST'])
def update(uID):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        db_helper.update_review_feedback(data['courseName'], uID, data["description"])
        result = {'success': True, 'response': 'Task Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/createReview/", methods=['POST'])
def createR():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_review(data['uID'], data['courseName'], data['professor'],
    data['gpa'], data['enjoyRating'], data['difficultyRating'], data['timeConsumpRating'],
    data['feedback'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/")
def homepageR():
    """ returns rendered homepage """
    return render_template("index.html")

@app.route("/reviews.html")
def homepageR2():
    """ returns rendered homepage """
    return render_template("reviews.html")


@app.route("/viewAllReviews/<int:userId>", methods=['GET'])
def viewAll(userId):
    """ returns rendered homepage """
    items = db_helper.fetch_reviews(userId)
    return render_template("reviews.html", items=items)


@app.route("/viewSpecific/<int:userId>/course/<courseName>", methods=['GET'])
def viewSpecific(userId, courseName):
    """ returns rendered homepage """
    items = db_helper.fetch_specific_reviews(userId, courseName)
    return render_template("reviews.html", items=items)


@app.route("/findCoursesByAverage/<method>", methods=['GET'])
def findCoursesByAverage(method):
    """ returns rendered homepage """
    items = db_helper.findCourseByAverage(method)
    return render_template("reviews.html", courseItems=items)




# professor 

@app.route("/createProf", methods=['POST'])
def createP():
    """ recieves post requests to add new professor """
    form = request.form
    # data = request.get_json()
    # print(data)
    if 'add' in form:
        db_helper.insert_new_prof(form['ProfessorId'], form['FirstName'], form['LastName'])
    elif 'delete' in form:
        db_helper.delete_prof(form['ProfessorId'], form['FirstName'], form['LastName'])
    elif 'edit' in form:
        db_helper.update_last_name(form['ProfessorId'], form['FirstName'], form['LastName'])

    #result = {'success': True, 'response': 'Done'}
    items = db_helper.fetch_all_profs()
    return render_template('professors.html', items=items)

@app.route("/professors.html")
def homepageP():
    """ returns rendered homepage """
    items = db_helper.fetch_all_profs()
    return render_template("professors.html", items=items)

@app.route("/findProfs", methods=['GET'])
def advancedP():
    items = db_helper.fetch_best_profs()
    return render_template("professors.html", items=items)

@app.route("/searchProfs", methods=['POST','GET'])
def searchP():
    form = request.form
    print(form)
    items = db_helper.fetch_wanted_profs(form['LastName'])
    return render_template("professors.html", items=items)



# department

@app.route("/createDepartment", methods=['POST'])
def createD():
    """ recieves post requests to add new department """
    form = request.form
    # data = request.get_json()
    # print(data)
    if 'add' in form:
        db_helper.insert_new_dept(form['SubjectCode'], form['DepartmentTitle'])
    elif 'delete' in form:
        db_helper.delete_dept(form['SubjectCode'], form['DepartmentTitle'])
    elif 'edit' in form:
        db_helper.update_dept_title(form['SubjectCode'], form['DepartmentTitle'])

    #result = {'success': True, 'response': 'Done'}
    items = db_helper.fetch_all_depts()
    return render_template('departments.html', items=items)

@app.route("/departments.html")
def homepageD():
    """ returns rendered homepage """
    items = db_helper.fetch_all_depts()
    return render_template("departments.html", items=items)

@app.route("/findDepartments", methods=['GET'])
def advancedD():
    items = db_helper.fetch_hardest_depts()
    return render_template("departments.html", items=items)

@app.route("/searchDepartments", methods=['POST','GET'])
def searchD():
    form = request.form
    print(form)
    items = db_helper.fetch_search_title(form['DepartmentTitle'])
    return render_template("departments.html", items=items)


# courses

@app.route('/cud', methods = ['POST'])
def cud():

    cud_type = request.form['cud-type']
    subj_code = request.form['subject-code']
    crn = request.form['crn']
    course_title = request.form['course-title']

    if (cud_type == "add"): 
        createCourse(subj_code, crn, course_title)
    elif (cud_type == "update"): 
        updateCourse(subj_code, crn, course_title)
    elif (cud_type == "delete"):
        deleteCourse(course_title)
    
    return redirect('/courses.html')


def createCourse(subj_code, crn, course_title):
    """ recieves post requests for course creation """
    try:
        db_helper.create_new_course(subj_code, crn, course_title)
        result = {'success': True, 'response': 'Course created'}
    except:
        result = {'success': False, 'response': 'Failed to create course'}
    pass


def updateCourse(subj_code, crn, course_title):
    """ recieved post requests for course title update """
    try:
        db_helper.update_course_title(subj_code, crn, course_title)
        result = {'success': True, 'response': 'Course updated'}
    except:
        result = {'success': False, 'response': 'Failed to update course'}
    pass

    
def deleteCourse(course_title):
    """ recieved post requests for course deletion """
    try:
        db_helper.delete_course(course_title)
        result = {'success': True, 'response': 'Course deleted'}
    except:
        result = {'success': False, 'response': 'Failed to delete course'}
    pass







@app.route('/customGetTitle', methods = ['POST'])
def customGetTitle():

    subj_code = request.form['subject-code']
    crn = request.form['crn']
    data = db_helper.getCourseTitle(subj_code, crn)
    return render_template('courses.html', data = data)


@app.route('/customGetScAndCrn', methods = ['POST'])
def customGetScAndCrn():

    course_title = request.form['course-title']
    data = db_helper.getSCandCRN(course_title)
    return render_template('courses.html', data = data)






@app.route('/queryCourses', methods = ['POST'])
def queryCourses():

    query_search_type = request.form['search']

    if (query_search_type == "1"): 
        data = db_helper.top15_easiest_courses()
        return render_template('courses.html', data = data)
    if (query_search_type == "2"): 
        data = db_helper.top15_hardest_courses()
        return render_template('courses.html', data = data)
    if (query_search_type == "3"):
        data = db_helper.top15_enjoyable_courses()
        return render_template('courses.html', data = data)
    if (query_search_type == "4"):
        data = db_helper.advanced_query()
        return render_template('courses.html', data = data)
    if (query_search_type == "5"):
        data = db_helper.number_of_courses()
        return render_template('courses.html', data = data)

    return redirect('/courses.html')



@app.route('/backToHome', methods = ['POST'])
def backToHome():
    return redirect('/courses.html')

@app.route("/courses.html")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_queries()
    return render_template("courses.html", items = items)
