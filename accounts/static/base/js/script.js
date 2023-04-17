function saveCourse() {
  const userId = user_id
  const courseId = course_id

  fetch('/course/save_course/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      course_id: courseId
    })
  })
  .then(response => {
    if (response.ok) {
      alert('Course add');
      location.reload();

    } else {
      alert('Course error');
    }
  })
  .catch(error => {
    console.error('error:', error);
  });
}


function rmCourse() {
  const userId = user_id
  const courseId = course_id

  fetch('/course/delete_course/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      course_id: courseId
    })
  })
  .then(response => {
    if (response.ok) {
      alert('Course rm');
      location.reload();

    } else {
      alert('Course error');
    }
  })
  .catch(error => {
    console.error('error:', error);
  });
}




const courseButtonAdd = document.getElementById('course-add');
if (courseButtonAdd) {
  courseButtonAdd.addEventListener('click', saveCourse);
}

const courseButtonRm = document.getElementById('course-rm');
if (courseButtonRm) {
  courseButtonRm.addEventListener('click', rmCourse);
}

