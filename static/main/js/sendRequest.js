let send_data = function (data, url, successFun = function () {}) {
    var fd = new FormData();
    $.each(data, function (key, value) {
        fd.append(key, value);
    });


    $.ajax({
        type: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
        },
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        beforeSend: function () {
            alertBox.innerHTML = ""
        },
        xhr: function () {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e => {
                // console.log(e)
                if (e.lengthComputable) {
                    const percent = e.loaded / e.total * 100
                    console.log(percent)
                    progressBox.innerHTML = `<div class="progress">
                                                <div class="progress-bar" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100"></div>
                                            </div>
                                            <p>${percent.toFixed(1)}%</p>`
                }

            })
            cancelBtn.addEventListener('click', () => {
                xhr.abort()
                setTimeout(() => {
                    uploadForm.reset()
                    progressBox.innerHTML = ""
                    alertBox.innerHTML = ""
                    cancelBox.classList.add('not-visible')
                }, 2000)
            })
            return xhr
        },
        success: function (response) {
            alertBox.innerHTML = `<div class="alert alert-success text-center d-flex flex-column justify-content-center align-items-center" role="alert">
                                    تم التحميل و جاري المعالجه انتظر قليل فقط
                                    <div class="spinner-border mt-3 text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                    </div>
                                </div>`
            cancelBox.classList.add('not-visible')
        },
        error: function (error) {
            console.log(error)
            alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                    Ups... something went wrong
                                </div>`
        },
        cache: false,
        contentType: false,
        processData: false,
    });




};





// $.ajax({
//         type: "POST",
//         headers: {
//             "X-CSRFToken": csrftoken,
//         },
//         url: url,
//         data: fd,
//         processData: false,
//         contentType: false,
//         success: function (response) {
//             successFun(response);
//         },
//     });