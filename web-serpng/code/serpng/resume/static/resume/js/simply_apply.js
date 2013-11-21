function validate_input(element) {
    if (!element.length) {
        element = $(this);
    }

    if ("/^\s+$/".match(element.val())) {
        element.nextAll('span.error').text('This field is required');
        return false;
    }
    else {
        element.nextAll('span.error').text('');
    }

    return true;
}

function form_has_errors() {
    has_errors = false;
    for(var i = 0; i < required_fields.length; i++) {
        $(required_fields[i] + ':visible:enabled').each(function() {
            if (!validate_input($(this))) {
                has_errors = true;
            }
        });
    }

    return has_errors;
}

function bind_required_fields() {
    for (var i = 0; i < required_fields.length; i++) {
        $(required_fields[i]).each(function () {
            $(this).bind({'keyup': validate_input, 'blur': validate_input});
            $(this).change(validate_input);
        });
    }
}

function dropdown() {
    $('select#resume_select').bind('change', function() {
        var option = $(this).find('option:selected');
        if (option.val() != "") {
            $('a#download').removeAttr('style');
            $('input#upload_new_resume').attr('disabled', 'disabled');
        }
        else {
            $('a#download').attr('style', 'display: none');
            $('input#upload_new_resume').removeAttr('disabled');
        }
    });
}

function form_toggle() {
    $('a.form_toggle').click(function() {
        $('div.container').each(function() { $(this).toggle(); });
    });
}

function change_resume_toggle() {
    $('a.resume_toggle').click(function() {
        $('div[name="change_resume"]').each(function() { $(this).toggle(); });
    });
}

function edit_name() {
    $('a.edit_name').click(function() {
        $('div[name="change_name"]').each(function() { $(this).toggle(); });
    });
}

function mobile_update_display(element, fields) {
    var id = element.attr('name');
    var string_array = [];

    for (var i = 0; i < fields.length; i++) {
        var value = $('input#id_' + id + '-' + fields[i]).attr('value')
        value ? string_array.push(value) : null;
    }

    if (string_array.length) {
        $('a[href=#' + id + ']').text(string_array.join(' at '));
    }
}

function submit() {
    $('form').submit(function() {
        $(this).find('input[type=submit]').attr('disabled', 'disabled');
        $(this).find('input[type=submit]').attr('value', 'Submitting...');
    });
}

$(document).ready(function() {
    required_fields = ['input[type=text]', 'input[type=password]', 'input[type=file]'];

    submit();
    dropdown();
    form_toggle();
    change_resume_toggle();
    edit_name();
    bind_required_fields();
});
