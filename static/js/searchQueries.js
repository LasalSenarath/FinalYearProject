$(document).ready(function () {
    $('#btnPost').click(function () {
        $.ajax({
            url: '/byMaterialSearch',
            data: {
                message: $('#message').val()
            },
            type: 'POST',
            success: function (response) {
                var table = $('#tblResults tbody');
                $('#tblResults tbody').empty();
                    table.append("<tr></tr><td>Preprocessed Post</td><td>" + response[0] + "</td></tr></tr>");
                    table.append("<tr></tr><td>Movie Name</td><td>" + response[1] + "</td></tr></tr>");
                    table.append("<tr></tr><td>Label</td><td>" + response[2] + "</td></tr></tr>");
                    $('#message').val('');
        },
            error: function (error) {
                $('#tblResults tbody').empty();
                alert(error);
            }
        });
    });
});