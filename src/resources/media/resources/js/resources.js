jQuery(function($) {
    $('form.autosubmit button').hide();
    $('form.autosubmit select').change(function(ev) {
        $(this).parents('form.autosubmit').submit();
    });
});
