$(document).ready(function(){
    $(document).on('click', '.cjkcms-collapsible button', function(){
        var $target = $(this).parent().find('.cjkcms-collapsible-target');

        if (!$(this).parent().hasClass('collapsed')) {
            $(this).parent().addClass('collapsed');
            $target.hide('fast');
        } else {
            $(this).parent().removeClass('collapsed');
            $target.show('fast');
        }
    });
});