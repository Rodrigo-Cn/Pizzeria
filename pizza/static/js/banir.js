$(document).ready(function() {
    var deleteBtn = $('.delete');

    $(deleteBtn).on('click', function(e) {
        e.preventDefault();

        var link = $(this).attr('href');
        var result = confirm('Tem certeza que vai banir o usuário?');

        if (result) {
            window.location.href = link;
        }
    });
});
