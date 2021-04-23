$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/


    // SHOW AND SUBMIT UPDATE
    $('#update-modal').on('show.bs.modal', function (event) {
        console.log("hey");
        const button = $(event.relatedTarget) // Button that triggered the modal
        // coursename id
        const reviewID = button.data('source') // Extract info from data-* attributes 
        // feedback
        const content = button.data('content') // Extract info from data-* attributes
        const userID = document.getElementById('userID').value;

        const modal = $(this)
        
        modal.find('.modal-title').text('Edit Review')
        $('#task-form-display').attr('reviewID', reviewID)

        modal.find('.form-control').val(content);
    });

    $('#submit-review-update').click(function () {
        const rID = $('#task-form-display').attr('reviewID');
        const uID = $('#update-modal').find('#userID').val()
        console.log($('#update-modal').find('.form-control').val())
        console.log(rID)
        console.log(uID)
        $.ajax({
            type: 'POST',
            url: '/editReview/' + uID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'description': $('#update-modal').find('.form-control').val(),
                'courseName': rID
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    // VIEW ALL REVIEWS
    $('#see-reviews').click(function () {
        $('#view-modal').modal('hide');
        console.log("hi");
        userId = $('#view-modal').find('.viewUserId').val()
        $.ajax({
            type: 'GET',
            url: '/viewAllReviews/' + userId,
            success: function (res) {
                console.log("HEYOoooooo")
                console.log(res.response)
                window.location.href = '/viewAllReviews/' + userId;
                // window.location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    // SUBMIT NEW REVIEW
    $('#submit-new-review').click(function () {
        console.log("hiee");
        userId = $('#review-modal').find('#newUserId').val()
        course = $('#review-modal').find('#newCourse').val()
        prof = $('#review-modal').find('#newProfessor').val()
        gpa = $('#review-modal').find('#newGPA').val()
        enjoy = $('#review-modal').find('#newEnjoy').val()
        diff = $('#review-modal').find('#newDiff').val()
        time = $('#review-modal').find('#newTime').val()

        $('#review-modal').modal('hide');
        $.ajax({
            type: 'POST',
            url: '/createReview/',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'uID': userId,
                'courseName' : course,
                'professor' : prof,
                'gpa' : gpa,
                'enjoyRating': enjoy,
                'difficultyRating': diff,
                'timeConsumpRating': time,
                'feedback': $('#review-modal').find('#newFeedback').val()
            }),
            success: function (res) {
                console.log("HEYOoooooo")
                console.log(res.response)
                window.location.href = '/viewAllReviews/' + userId;
                // window.location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    // SHOW DELETE MODAL
    $('#delete-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        // coursename id
        const reviewID = button.data('source') // Extract info from data-* attributes 

        const modal = $(this)
        
        $('#task-form-display').attr('reviewID', reviewID)
    });

    $('#confirm-delete').click(function () {
        const rID = $('#task-form-display').attr('reviewID');
        const uID = $('#delete-modal').find('#userID').val()
        $.ajax({
            type: 'POST',
            url: '/deleteReview/' + uID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'courseName': rID
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    // VIEW SPECIFIC REVIEWS
    $('#see-specific-reviews').click(function () {
        $('#view-specific-modal').modal('hide');
        userId = $('#view-specific-modal').find('#userID').val()
        console.log(userId)
        courseName = $('#view-specific-modal').find('#courseName').val()
        console.log(courseName)
        $.ajax({
            type: 'GET',
            url: '/viewSpecific/' + userId + '/course/' + courseName,
            success: function (res) {
                console.log(res.response)
                window.location.href = '/viewSpecific/' + userId + '/course/' + courseName
                // window.location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    // FIND COURSES BY RATING
    $('#find-courses-from-avg').click(function () {
        sortMethod = document.getElementById("ratings").value;
        $.ajax({
            type: 'GET',
            url: '/findCoursesByAverage/' + sortMethod,
            success: function (res) {
                console.log("HEYOoooooo")
                console.log(res.response)
                window.location.href = '/findCoursesByAverage/' + sortMethod
                // window.location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});