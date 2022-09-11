$(function () {
    $("#data-processing").on("click", function () {
        console.log("here sir");
        $.ajax({
            type: "POST",
            url: window.location.href,
            data: $('.form-horizontal').serialize(),
            success: function (response) {
                var fd = new FormData();
                var input = document.getElementById("file_video")
                fd.append('x-amz-credential', response['clientPayload']['x-amz-credential'])
                fd.append('x-amz-algorithm', response['clientPayload']['x-amz-algorithm'])
                fd.append('x-amz-date', response['clientPayload']['x-amz-date'])
                fd.append("x-amz-signature", response['clientPayload']['x-amz-signature'])
                fd.append("key", response['clientPayload']['key']);
                fd.append("policy", response['clientPayload']['policy']);
                fd.append("success_action_status", 201);
                fd.append("success_action_redirect", "");
                fd.append('file', input.files[0]);
                $.ajax({
                    xhr: function () {
                        var xhr = new window.XMLHttpRequest();
                        xhr.upload.addEventListener("progress", function (evt) {
                            if (evt.lengthComputable) {
                                var percentComplete = ((evt.loaded / evt.total) * 100);
                                $(".progress-bar").width(percentComplete + '%');
                                // $(".progress-bar").html(percentComplete.toFixed(1) + '%');
                                $("#valuenow").html(percentComplete.toFixed(3));
                            }
                        }, false);
                        return xhr;
                    },
                    datatype: 'xml',
                    contentType: false,
                    type: 'POST',
                    url: response['clientPayload']['uploadLink'],
                    data: fd,
                    processData: false,
                    crossDomain: true,
                    success: function (resp) {
                        
                        window.location.replace("https://www.alfayed-edu.com/dashboard/courses_admin");
                    },
                    error: function (resp) {
                        console.log(resp.responseText);
                    }
                });

            }
        });
    });
    window.addEventListener('offline', () => {
        if (confirm("انقطعة خدمة الانترنت من فضلك اعد المحولة عندما يكون الانترنت سابت")) {
            window.location.replace("https://www.alfayed-edu.com/dashboard/courses_admin");
        }
    });
});

