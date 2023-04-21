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

function saveLeaf() {
  const userId = user_id
  const leafId = leaf_id

  fetch('/course/save_leaf/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      leaf_id: leafId
    })
  })
  .then(response => {
    if (response.ok) {
      alert('Leaf add');
      location.reload();

    } else {
      alert('Leaf error');
    }
  })
  .catch(error => {
    console.error('error:', error);
  });
}


function rmLeaf() {
  const userId = user_id
  const leafId = leaf_id

  fetch('/course/delete_leaf/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      leaf_id: leafId
    })
  })
  .then(response => {
    if (response.ok) {
      alert('Leaf rm');
      location.reload();

    } else {
      alert('Leaf error');
    }
  })
  .catch(error => {
    console.error('error:', error);
  });
}


const leafButtonAdd = document.getElementById('leaf-add');
if (leafButtonAdd) {
  leafButtonAdd.addEventListener('click', saveLeaf);
}

const leafButtonRm = document.getElementById('leaf-rm');
if (leafButtonRm) {
  leafButtonRm.addEventListener('click', rmLeaf);
}

const courseButtonAdd = document.getElementById('course-add');
if (courseButtonAdd) {
  courseButtonAdd.addEventListener('click', saveCourse);
}

const courseButtonRm = document.getElementById('course-rm');
if (courseButtonRm) {
  courseButtonRm.addEventListener('click', rmCourse);
}


function sendJSONRequest(url, checkpointValue, status) {
    var data = {
        'value': checkpointValue,
        'status': status
    };
    $.ajax({
        url: url,
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data) {
            console.log('Success!');
        },
        error: function(xhr, status, error) {
            console.log('Error!');
        }
    });
}

$(document).ready(function() {
    $('.checkpoint input[type="checkbox"]').on('change', function() {
        var checkpointValue = $(this).val();
        var status = $(this).is(':checked') ? 'done' : 'not_done';
        sendJSONRequest('/accounts/change-leafs/', checkpointValue, status);
    });
});



$(document).ready(function() {
    $("button[name='complitle'], button[name='refusal']").click(function() {
        var data = {
            'button_name': $(this).attr('name'),
            'button_value': $(this).val(),
            'url':window.location.href
        };
        $.ajax({
            url: '/accounts/change-status-course/',
            type: 'POST',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function(response) {
                location.reload();
            },
            error: function(response) {
            }
        });
    });
});

