from app import db 

def fetch_reviews(userId) -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query = 'Select * from Review WHERE UserId = "{}" LIMIT 15;'.format(userId)
    query_results = conn.execute(query).fetchall()
    print(query_results)
    conn.close()
    reviewList = []
    for result in query_results:
        conn = db.connect()
        query = 'Select LastName from Professor WHERE ProfessorId = "{}";'.format(result[1])
        prof_name = conn.execute(query).first()
        conn.close()
        item = {
            "course": result[0],
            "profId": prof_name[0],
            "gpa": result[3],
            "enjoyRate": result[4],
            "difficultRate": result[5],
            "timeRate": result[6],
            "feedback": result[7]
        }
        reviewList.append(item)
    return reviewList


def fetch_specific_reviews(userId, courseName) -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query = 'Select * from Review WHERE UserId = "{}" and CourseTitle = "{}" LIMIT 15;'.format(userId, courseName)
    query_results = conn.execute(query).fetchall()
    print(query_results)
    conn.close()
    reviewList = []
    for result in query_results:
        conn = db.connect()
        query = 'Select LastName from Professor WHERE ProfessorId = "{}";'.format(result[1])
        prof_name = conn.execute(query).first()
        conn.close()
        item = {
            "course": result[0],
            "profId": prof_name[0],
            "gpa": result[3],
            "enjoyRate": result[4],
            "difficultRate": result[5],
            "timeRate": result[6],
            "feedback": result[7]
        }
        reviewList.append(item)
    return reviewList


def update_review_feedback(coursename: str, user_id: int, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update Review set Feedback = "{}" where UserId = {} and CourseTitle = "{}";'.format(text, user_id, coursename)
    conn.execute(query)
    conn.close()



def insert_new_review(uId: int, courseName: str, prof: str,
    gpa: float, enjoyRate: int, diffRate: int, timeRate: int,
    feedback: str) ->  None:
    """Insert new review to table """
    conn = db.connect()
    query = 'SELECT ProfessorId FROM Professor WHERE LastName = "{}"'.format(prof)
    profID = conn.execute(query).first()[0]
    query = 'Insert Into Review (CourseTitle,ProfessorId, UserId, StudentGPA, EnjoyabilityRating,DifficultyRating,TimeConsumptionRating,Feedback) VALUES ("{}", {}, {}, {}, {},{},{},"{}");'.format(
        courseName, profID, uId, gpa, enjoyRate, diffRate, timeRate, feedback)
    query_results = conn.execute(query)
    conn.close()


def remove_review_by_id(review_id: int, course: str) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From Review where UserId={} and CourseTitle ="{}";'.format(review_id, course)
    conn.execute(query)
    conn.close()

def findCourseByAverage(method: str) -> dict:
    """ find courses by rating """
    conn = db.connect()
    if method == 'EnjoyabilityRating':
        query = 'SELECT c.CourseTitle, c.SubjectCode, c.CourseNumber, avg(r.{}) as avgRating FROM Review r join Course c on c.CourseTitle = r.CourseTitle GROUP BY CourseTitle ORDER BY avgRating desc LIMIT 15;'.format(method)
    else: 
        query = 'SELECT c.CourseTitle, c.SubjectCode, c.CourseNumber, avg(r.{}) as avgRating FROM Review r join Course c on c.CourseTitle = r.CourseTitle GROUP BY CourseTitle ORDER BY avgRating asc LIMIT 15;'.format(method)
    query_results = conn.execute(query).fetchall()
    conn.close()
    courseList = []
    for result in query_results:
        item = {
            "course": result[0],
            "subjCode": result[1],
            "courseNum": result[2],
            "rating": result[3]
        }
        courseList.append(item)
    return courseList


# PROFESSORS

def fetch_all_profs() -> dict:
    """Reads all professors listed in the professor table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT * from Professor;").fetchall()
    conn.close()
    all_profs = []
    for result in query_results:
        item = {
            "ProfessorId": result[0],
            "FirstName": result[1],
            "LastName": result[2]
        }
        all_profs.append(item)

    return all_profs

def insert_new_prof(ProfessorId: int, FirstName: str, LastName: str) ->  int:
    """Insert new prof to Professor table.

    Returns: The ProfessorId for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into Professor (ProfessorId, FirstName, LastName) VALUES ("{}", "{}", "{}");'.format(ProfessorId,
        FirstName, LastName)
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    professor_id = query_results[0][0]
    conn.close()

    return professor_id

def delete_prof(ProfessorId: int, FirstName: str, LastName: str) ->  None:
    """Insert new prof to Professor table.

    Returns: The ProfessorId for the inserted entry
    """

    conn = db.connect()
    query = 'Delete From Professor WHERE ProfessorId={} AND FirstName LIKE "{}" AND LastName LIKE "{}";'.format(ProfessorId, FirstName, LastName)
    conn.execute(query)
    conn.close()

def update_last_name(ProfessorId: int, FirstName: str, LastName: str) -> None:

    conn = db.connect()
    query = 'Update Professor set LastName = "{}" where ProfessorId = {} AND FirstName LIKE "{}";'.format(LastName, ProfessorId, FirstName)
    conn.execute(query)
    conn.close()

def fetch_best_profs() -> dict:
    conn = db.connect()
    query_results = conn.execute("SELECT P.ProfessorId, P.FirstName, P.LastName, AVG(R.EnjoyabilityRating) FROM Professor P JOIN Review R on P.ProfessorId = R.ProfessorId GROUP BY P.ProfessorId ORDER BY AVG(R.EnjoyabilityRating) DESC LIMIT 15;").fetchall()
    conn.close()
    best_profs = []
    for result in query_results:
        item = {
            "ProfessorId": result[0],
            "FirstName": result[1],
            "LastName": result[2],
        }
        best_profs.append(item)

    return best_profs

def fetch_wanted_profs(LastName: str) -> dict:
    """Reads all professors listed in the professor table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    q = ('SELECT * from Professor P WHERE P.LastName LIKE "{}";').format(LastName)
    query_results = conn.execute(q)
    conn.close()
    all_profs = []
    for result in query_results:
        item = {
            "ProfessorId": result[0],
            "FirstName": result[1],
            "LastName": result[2]
        }
        all_profs.append(item)

    return all_profs





# department

def fetch_all_depts() -> dict:
    """Reads all departments listed in the Department table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT * from Department;").fetchall()
    conn.close()
    all_depts = []
    for result in query_results:
        item = {
            "SubjectCode": result[0],
            "DepartmentTitle": result[1]
        }
        all_depts.append(item)

    return all_depts

def insert_new_dept(SubjectCode: str, DepartmentTitle: str) ->  str:
    """Insert new dept to Department table.

    Returns: The SubjectCode for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into Department (SubjectCode, DepartmentTitle) VALUES ("{}", "{}");'.format(SubjectCode,
        DepartmentTitle)
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    sub_code = query_results[0][0]
    conn.close()

    return sub_code

def delete_dept(SubjectCode: str, DepartmentTitle: str) ->  None:
    """Insert new dept to Department table.

    Returns: The SubjectCode for the inserted entry
    """

    conn = db.connect()
    query = 'Delete From Department WHERE SubjectCode LIKE "{}" AND DepartmentTitle LIKE "{}";'.format(SubjectCode, DepartmentTitle)
    conn.execute(query)
    conn.close()

def update_dept_title(SubjectCode: str, DepartmentTitle: str) -> None:
    conn = db.connect()
    query = 'Update Department SET DepartmentTitle = "{}" WHERE SubjectCode LIKE "{}";'.format(DepartmentTitle, SubjectCode)
    conn.execute(query)
    conn.close()

def fetch_hardest_depts() -> dict:
    conn = db.connect()
    query_results = conn.execute("SELECT D.DepartmentTitle, D.SubjectCode, (SELECT COUNT(*) FROM Course c1 WHERE D.SubjectCode = c1.SubjectCode GROUP BY D.SubjectCode) as NumCourses, avg(R.StudentGPA) as AvgGPA, avg(R.DifficultyRating) as AvgDifficulty, COUNT(*) as NumReviews FROM Department D JOIN Course C ON C.SubjectCode = D.SubjectCode JOIN Review R ON C.CourseTitle = R.CourseTitle GROUP BY D.SubjectCode, D.DepartmentTitle HAVING NumReviews > 4 ORDER BY AvgDifficulty DESC, AvgGPA DESC LIMIT 15;").fetchall()
    conn.close()
    hardest_depts = []
    for result in query_results:
        item = {
            "DepartmentTitle": result[0],
            "SubjectCode": result[1],
            "NumCourses": result[2],
            "AvgGPA": result[3],
            "AvgDifficulty": result[4]
        }
        hardest_depts.append(item)

    return hardest_depts

def fetch_search_title(DepartmentTitle: str) -> dict:
    conn = db.connect()
    q = ('SELECT * from Department D WHERE D.DepartmentTitle LIKE "{}";').format(DepartmentTitle)
    query_results = conn.execute(q)
    conn.close()
    search_dept = []
    for result in query_results:
        item = {
            "DepartmentTitle": result[0],
            "SubjectCode": result[1]
        }
        search_dept.append(item)

    return search_dept




# courses

def fetch_queries() -> dict:
    """Reads all queries listed in the query table

    Returns:
        A list of dictionaries
    """

    query_list = [
        {
            "id": 1, 
            "query": "Top 15 easiest courses", 
            "status": "Search"
        }, 
        {
            "id": 2, 
            "query": "Top 15 hardest courses", 
            "status": "Search"
        }, 
        {
            "id": 3, 
            "query": "Top 15 most enjoyable courses", 
            "status": "Search"
        }, 
        {
            "id": 4, 
            "query": "Top 15 easiest or most enjoyable courses", 
            "status": "Search"
        }, 
        {
            "id": 5, 
            "query": "Number of courses", 
            "status": "Search"
        }
    ]
    return query_list



def create_new_course(subj_code: int, course_num: int, course_title: str) ->  None:
    """Inserts new course to course table.

    Args:
        subj_code (int): Course subject code
        course_num (str): Course number
        course_title (str): Course title

    Returns:
        None
    """
    conn = db.connect()
    query = 'INSERT INTO Course (SubjectCode, CourseNumber, CourseTitle) VALUES ("{}", "{}", "{}");'.format(
        subj_code, course_num, course_title)
    print(query)
    conn.execute(query)
    conn.close()
    pass


def update_course_title(subj_code: int, course_num: int, course_title: str) -> None:
    """Updates course title based on given subject code and course number.

    Args:
        subj_code (int): Course subject code
        course_num (str): Course number
        course_title (str): Course title

    Returns:
        None
    """
    conn = db.connect()
    query = 'UPDATE Course SET CourseTitle = "{}" WHERE SubjectCode = "{}" AND CourseNumber = {};'.format(course_title, subj_code, course_num)
    print("query")
    conn.execute(query)
    conn.close()
    pass


def delete_course(course_title: str) -> None:
    """ Removes courses based on course title
    
    Args:
        course_title (str): Course title

    Returns:
        None
    """

    conn = db.connect()
    query = 'DELETE FROM Course WHERE CourseTitle = "{}";'.format(course_title)
    conn.execute(query)
    conn.close()
    pass





def getCourseTitle(subj_code, crn):
    conn = db.connect()
    query = 'SELECT 1, SubjectCode, CourseNumber, CourseTitle, "" FROM Course WHERE SubjectCode = "{}" AND CourseNumber = {};'.format(subj_code, crn)
    data = conn.execute(query).fetchall()
    conn.close()
    return data

def getSCandCRN(course_title):
    conn = db.connect()
    query = 'SELECT 1, SubjectCode, CourseNumber, CourseTitle, "" FROM Course WHERE CourseTitle = "{}";'.format(course_title)
    data = conn.execute(query).fetchall()
    conn.close()
    return data






def top15_easiest_courses():
    conn = db.connect()
    query = 'SELECT 1, c.SubjectCode, c.CourseNumber, c.CourseTitle, 5 - AVG(r.DifficultyRating) FROM Course c JOIN Review r ON c.CourseTitle = r.CourseTitle GROUP BY r.CourseTitle ORDER BY AVG(r.DifficultyRating) ASC LIMIT 15;'
    data = conn.execute(query).fetchall()
    conn.close()
    return data

def top15_hardest_courses():
    conn = db.connect()
    query = 'SELECT 1, c.SubjectCode, c.CourseNumber, c.CourseTitle, AVG(r.DifficultyRating) FROM Course c JOIN Review r ON c.CourseTitle = r.CourseTitle GROUP BY r.CourseTitle ORDER BY AVG(r.DifficultyRating) DESC LIMIT 15;'
    data = conn.execute(query).fetchall()
    conn.close()
    return data

def top15_enjoyable_courses():
    conn = db.connect()
    query = 'SELECT 1, c.SubjectCode, c.CourseNumber, c.CourseTitle, AVG(r.EnjoyabilityRating) FROM Course c JOIN Review r ON c.CourseTitle = r.CourseTitle GROUP BY r.CourseTitle ORDER BY AVG(r.EnjoyabilityRating) DESC LIMIT 15;'
    data = conn.execute(query).fetchall()
    conn.close()
    return data

def advanced_query():
    conn = db.connect()
    query = '(SELECT 1, c.SubjectCode, c.CourseNumber, c.CourseTitle, AVG(r.EnjoyabilityRating) AS Rating, COUNT(r.CourseTitle) AS NumReviews FROM Course c JOIN Review r ON c.CourseTitle = r.CourseTitle GROUP BY r.CourseTitle HAVING AVG(r.EnjoyabilityRating) > 3 AND COUNT(r.CourseTitle) > 5) UNION (SELECT 1, c.SubjectCode, c.CourseNumber, c.CourseTitle, (5-AVG(r.DifficultyRating)) AS Rating, COUNT(r.CourseTitle) AS NumReviews FROM Course c JOIN Review r ON c.CourseTitle = r.CourseTitle GROUP BY r.CourseTitle HAVING AVG(r.DifficultyRating) < 3 AND COUNT(r.CourseTitle) > 5) ORDER BY Rating DESC LIMIT 15;'
    data = conn.execute(query).fetchall()
    conn.close()
    return data

def number_of_courses():
    conn = db.connect()
    query = 'SELECT COUNT(*), "", "", "", "" FROM Course;'
    data = conn.execute(query).fetchall()
    conn.close()
    return data

