/*
 * add a resume page upload resume progress bar lightbox (jquery ui dialog)
 */

function validate_input(element) {
    if (!element.length) {
        element = $(this);
    }

    if ("/^\s+$/".match(element.val())) {
        element.next('span.error').text('This field is required');
        return false;
    } else {
        element.next('span.error').text('');
    }

    return true;
}

function validate_review_form() {
    var scroll_to = -1;
    for(var i = 0; i < required_fields.length; i++) {
        // Skip form is set to delete.
        var delete_form = $(required_fields[i].split('-', 2).join('-') + '-DELETE');
        if (delete_form.length > 0 && delete_form.val() == "1") {
            continue;
        }
        $('form[name=edit_review] ' + required_fields[i]).each(function () {
            if (!validate_input($(this))) {
                // Unhide the edit form first, since you can't get the position of a 'display: none' element.
                var parent = $(this).parents('div.description');
                if (!parent.find('div#form_edit').is(":visible")) {
                    toggle_element(parent.find('div#form_edit'));
                    toggle_element(parent.find('div.display'));
                }
                if (scroll_to < 0) {
                    scroll_to = $(this).offset().top - 90;
                }
            }

            if (required_fields[i] == 'input#id_email') {
                var re = /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i;
                if (!re.test($(this).attr('value'))) {
                    var parent = $(this).parents('div.description');
                    if (!parent.find('div#form_edit').is(":visible")) {
                        toggle_element(parent.find('div#form_edit'));
                        toggle_element(parent.find('div.display'));
                    }

                    $(this).next('span.error').text('Please enter a valid email address');
                    if (scroll_to < 0) {
                        scroll_to = $(this).offset().top - 90;
                    }
                } else {
                    $(this).next('span.error').text('');
                }
            }
        });
    }

    if (scroll_to > 0) {
        $(window).scrollTop(scroll_to);
        return false;
    }

    return true;
}

function toggle_element(element) {
    if ($(element).hasClass('hidden')) {
        $(element).removeClass('hidden');
    } else {
        $(element).addClass('hidden');
    }
}

function upload_resume() {
    $('form#upload_res').change(
        function() {
            $(this).submit();
        }
    );
}

function toggle_edit() {
    var parent = $(this).parent('div.description');
    var display = parent.find('div.display');
    toggle_element(display);

    var edit_div = parent.find('div#form_edit');

    edit_div.find('input[id^=id_],textarea[id^=id_],option:selected').each(function() {
        if ($(this).prop('tagName') === 'OPTION') {
            prev_values[$(this).parent().attr('id')] = $(this).val();
        } else {
            prev_values[$(this).attr('id')] = $(this).val();
        }
    });

    toggle_element(edit_div);
}

function edit_continue() {
    // Change the display to reflect the new changes.
    // Also set the cancel variable to off.
    var edit_parent = $(this).parents('div#form_edit');
    var display_parent = edit_parent.prev('div.display');
    var form_valid = true;

    for (var i = 0; i < required_fields.length; i++) {
        var input_thing = edit_parent.find(required_fields[i]);
        if (input_thing.length) {
            if (!validate_input(input_thing)) {
                return;
            }
            break; // Only 1 required field per edit form...
        }
    }

    edit_parent.find("input#cancel").removeAttr('value');
    toggle_element(display_parent);
    toggle_element(edit_parent);
    edit_parent.find('input[id^=id_], textarea[id^=id_]').each(function() {
        var cur_val = $(this).val();
        var cur_id = $(this).attr('id');
        var display_element = display_parent.find('#' + cur_id);
        if (display_element.length && display_element.text() != cur_val) {
            display_element.text(cur_val);
            display_element.effect('highlight', {color: '#d9edf7'}, 2000);
        }
        delete prev_values[cur_id];
    });

    // Handle dates.
    if (edit_parent.find('select[id*=_date]').length) {
        var date_id = edit_parent.find('select[id*=_date]').attr('id').split('-');
        date_id = date_id[0] + '-' + date_id[1];
        var start_month = edit_parent.find('select[id*=start_date_month] option:selected').text();
        var start_year = edit_parent.find('select[id*=start_date_year] option:selected').text();
        var end_month = edit_parent.find('select[id*=end_date_month] option:selected').text();
        var end_year = edit_parent.find('select[id*=end_date_year] option:selected').text();
        var current = edit_parent.find('input[id$=-current]').is(':checked');

        if (start_month || start_year) {
            display_parent.find('#' + date_id + '-start_date').text(start_month + ' ' + start_year + ' - ');
        } else {
            display_parent.find('#' + date_id + '-start_date').text(start_month + ' ' + start_year);
        }

        if (current) {
            display_parent.find('#' + date_id + '-end_date').text('Present');
        } else {
            display_parent.find('#' + date_id + '-end_date').text(end_month + ' ' + end_year);
        }
    }
}

function edit_cancel() {
    var parent = $(this).parents('div.description');
    var edit_form = parent.find('div#form_edit');
    toggle_element(edit_form);
    toggle_element(parent.find('div.display'));
    edit_form.find("input#cancel").attr('value', 1);
    edit_form.find('input[id^=id_],textarea[id^=id_],option:selected').each(function() {
        var this_id = $(this).attr('id');
        if ($(this).prop('tagName') === 'OPTION') {
            this_id = $(this).parent('select').attr('id')
            var option_prev_value = prev_values[this_id];
            $(this).parent('#' + this_id).find("option[value=" + option_prev_value + "]").attr('selected', 'selected');
        } else {
            $(this).attr('value', prev_values[$(this).attr('id')]);
        }
        delete prev_values[this_id]
    });
}

function edit_remove() {
    if (confirm('Are you sure?') == true) {
        var type = $(this).attr('name');
        var parent = $(this).parents('div.description');

        parent.addClass('hidden');
        // Set form to delete.
        if (parent.find('input[name$=-DELETE]').length) {
            parent.find('input[name$=-DELETE]').attr('value', '1');
        } else {
        // no 'DELETE' for this newly added form, so just delete it
            parent.remove();
        }

        if (type == 'job' && $('div[name=job] div.row.description:visible').length == 0) {
            $('#no_job_error').show();
        }
    }
}

function edit_hover_mouseenter() {
    $(this).find('div.edit').removeClass('hidden');
}
function edit_hover_mouseleave() {
    $(this).find('div.edit').addClass('hidden');
}

function edit_click() {
    $('div.edit').click(toggle_edit);
}

function edit_hover() {
    $('div.description').mouseenter(edit_hover_mouseenter).mouseleave(edit_hover_mouseleave);
}

// Continue/Cancel buttons.
function form_edit() {
    $('span.edit_continue').click(edit_continue);
    $('span.edit_cancel').click(edit_cancel);
}

function landing_upload_button() {
    $('.input_wrapper').mousedown(function() {
        var button = $(this);
        button.addClass('clicked');
        setTimeout(function(){
            button.removeClass('clicked');
        },50);
    });
}

function serp() {
    $('#review_submit').click(function() {
        $('form[name=edit_review]').submit();
    });
}

function save_button() {
    $('.btn-submit').click(function() {
        if ($('div#register').length > 0) {
	  $("html, body").animate({ scrollTop: 0 }, "fast");
          $('div#error').addClass("alert alert-error");
          $('div#error').html('<span class="error" style="margin-bottom: 0px;"><i class="icon-remove"></i> Please Register or Sign In.</span>');
	  $('div#error').fadeToggle('slow', 'linear');
          return false;
        }

        if (get_source() == 'manage') {
            if (validate_review_form()) {
                $('form[name=edit_review]').submit();
            }
        } else {
            if (validate_review_form()) {
                $('div#modal').modal({show: true, backdrop: true, keyboard: true});
            }
        }
    });
}

function add_remove_entry() {
    $('a.add_form').click(function() {
        var type = $(this).attr('name');
        var total = parseInt($(this).parent().find('#id_' + type + '-TOTAL_FORMS').val());
        if (total === NaN) {
            total = 0;
        }
        // Handle cases where there are no forms in formsets.
        var clone_element = $('div#clone_' + type);
        $(this).before(clone_element.html().replace(/__prefix__/g, total));
        total++;
        $('#id_' + type + '-TOTAL_FORMS').val(total);
        var new_form = $(this).prev();
        // Bind events.
        //new_form.bind({mouseenter: edit_hover_mouseenter, mouseleave: edit_hover_mouseleave});
        new_form.find('span.edit_continue').bind({click: edit_continue});
        new_form.find('span.edit_cancel').bind({click: edit_cancel});
        new_form.find('span.edit_remove').bind({click: edit_remove});
        new_form.find('div.edit').bind({click: toggle_edit});
        if (type == 'job') {
            new_form.find('input[id$=-title]').bind({'keyup': validate_input, 'blur': validate_input});
        }
    });

    $('span.edit_remove').click(edit_remove);
}

function nav_scroll() {
    var isFixed = 0;
    var navTop = $('.summarybar').length && $('.summarybar').offset().top - 40;

    $(window).scroll(function() {
        var i, scrollTop = $(window).scrollTop();
        if (!isFixed && scrollTop >= navTop) {
            $('.summarybar').addClass('nav-fixed');
            isFixed = 1;
        } else if (isFixed && scrollTop <= navTop) {
            $('.summarybar').removeClass('nav-fixed');
            isFixed = 0;
        }
    });
}

function bind_required_fields() {
    for (var i = 0; i < required_fields.length; i++) {
        $('form[name=edit_review] ' + required_fields[i]).each(function () {
            $(this).bind({'keyup': validate_input, 'blur': validate_input});
        });
    }
}

function get_source() {
    var qsParm = new Array();
    var query = window.location.search.substring(1);
    var parms = query.split('&');

    for (var i=0; i<parms.length; i++) {
        var pos = parms[i].indexOf('=');
        if (pos > 0) {
            var key = parms[i].substring(0,pos);
            var val = parms[i].substring(pos+1);
            qsParm[key] = val;
        }
    }

    return qsParm['source'];
}

function nav_bar_click() {
    $('.summarybar a.btn').click(function() {
        var anchor_name = $(this).attr('name');
        if ($('div[name=' + anchor_name + ']').offset()) {
            var scroll_to = $('div[name=' + anchor_name + ']').offset().top - 35;
            $(window).scrollTop(scroll_to);
        }
    });
}

function jobs() {
    $('a.add_form[name=job]').bind('click', function() {
        $('#no_job_error').hide();
    });

    $('span.edit_remove[name=job]').bind('click', function() {
        if ($('div[name=job] div.row.description:visible').length == 0) {
            $('#no_job_error').show();
        }
    });
}

$(document).ready(function() {
    prev_values = new Array();
    required_fields = ['input#id_email', 'input#id_first_name', 'input#id_last_name', 'input#id_job-0-title'];

    upload_resume();
    landing_upload_button();
    edit_click();
    form_edit();
    save_button();
    serp();
    add_remove_entry();
    nav_scroll();
    nav_bar_click();
    bind_required_fields();
    jobs();
});
