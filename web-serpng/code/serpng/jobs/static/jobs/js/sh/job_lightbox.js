// Make sure SH namespace is defined.
var SH = SH || {};

/**
 * @class job view lightbox
 *
 * New user job view lightbox (jquery ui dialog).
 * Shown on first job click only, create email alert form.
 */
SH.JobLightbox = function() {

  // Private variables

  // Lightbox seen flag
  var hasSeenEmailAlert = !!SH.cookies.getSubcookie('shua', 'uaalertbox');

  // Template class names
  var editClass = 'edit_alert';
  var closeBoxClass = 'box_close';

  // URLs
  var lightboxUrl = '/a/job-alerts/lightbox';
  var createAlertUrl = '/a/job-alerts/create-json';

  // jQuery objects
  var $dialog = null;
  var $form = null;
  var $formInputs = null;
  var $message = null;
  var $closeBox = null;
  var $continueLink = null;
  var $keywords = null;
  var $location = null;

  // Job data
  var jobUrl = null;

  // Private Functions

  /**
   * Initialize email alerts lightbox dialog and display dialog.
   * Organic job must be clicked to display dialog.
   * @param {Object} jobLink The object for the job link clicked.
   */
  var init = function(jobLink) {

    // Element selectors
    var alertDialog = '#c_alerts_offer';

    $dialog = $(alertDialog);

    // Check if the lightbox is available.
    if (!$dialog.length) {
      return false;
    }

    // Track event.
    SH.EventLog.serpng.email_alert_interstitial_display();

    // Set job url and append tracking parameter.
    if (!!jobLink) {

      // For unbinding event.
      jobUrl = jobLink.href;

      // For metrics.
      if (!!jobUrl) {
        jobUrl += jobUrl.indexOf('?') == -1 ? '?uea=y' : '&uea=y';
      }
    }

    // Load jquery fancybox and create dialog.
    SH.fancybox(function() {

      /**
       * Create fancybox.
       * Setting locked to false ensures the fancybox is centered and stays centered.
       * Setting autoSize to false prevents the fancybox from showing then moving to the center.
       * Setting height and width ensures the fancybox is sized correctly.
       * Setting the padding to 0 makes it so the highlighed edge is flush with the box border.
       */
      $.fancybox.open([{
        beforeShow: beforeShow,
        helpers: {
          overlay: {
            closeClick: false,
            locked: false
          }
        },
        href: alertDialog
      }],{
        autoSize: false,
        height: 500,
        padding: 0,
        width: 565
      });

      // Handle dialog click.
      $dialog.on('click', click);

      // Set form handler.
      $form = $('form', $dialog).on('submit', submit);

      // Initialize the jQuery objects.
      $message = $("div.message", $form);
      $continueLink = $("a.continue", $dialog);
      $keywords = $("p.keywords", $dialog);
      $location = $("p.location", $dialog);
      $formInputs = $("input[type=text]", $form);

      initPlaceholders();

      // Set/hide continue link and close link.
      if (!!jobUrl) {
        $continueLink.attr('href', jobUrl);
        $dialog.append('<a class="' + closeBoxClass + '" href="' + jobUrl + '" target="_blank"></a>');
      } else {
        $continueLink.hide();
        $dialog.append('<a class="' + closeBoxClass + '"></a>');
      }

      // Set lightbox as seen in the cookies.
      var d = new Date().getTime();
      if (!hasSeenEmailAlert) {
        SH.cookies.setSubcookie('shua', 'uaalertbox', d);
        hasSeenEmailAlert = true;
      }
    });

    return true;
  };

  /**
   * Adds the placeholder text to the input fields
   */
  var initPlaceholders = function() {
    //TODO (delaney) Fix placeholderFallback to work with multiple elements.
    $formInputs.each(function() {
      $(this).placeholderFallback();
    });
  };

  /**
   * Removes the placeholder text from input fields.
   * Should be called before getting the value of inputs.
   */
  var removePlaceholders = function() {
    $formInputs.placeholderFallback('remove');
  };

  /**
   * Gets the values from the inputs on the form.
   * @return {Object} The text inputs from the form with their name as the key.
   */
  var getFormInputs = function() {
    var inputs = {};

    // Remove the placeholders before getting form values to ensure no placeholder text in inputs.
    removePlaceholders();

    $formInputs.each(function() {
      inputs[this.name] = $(this).val();
    });

    initPlaceholders();
    return inputs;
  };

  /**
   * Pre-fills the users email from the cookies
   * Callback for Fancybox beforeShow event
   */
  var beforeShow = function() {
    // Prefill email from shua cookie.
    var shuaEmail = SH.cookies.getSubcookie('shua', 'uaemail');
    if (!!shuaEmail) {
      $('form', $dialog).find("input[name=email]").val(shuaEmail);
    }
  };

  /**
   * Closes the Fancybox.
   * @return {boolean} false for some reason probably relating to event handling.
   */
  var close = function() {

    // Make sure the fancybox javascript is loaded.
    if (!!$.fancybox) {
      $.fancybox.close();
    }
    return false;
  };

  /**
   * Opens the jobUrl (if present) in a new window.
   */
  var loadJob = function() {
    if (!!jobUrl) {
      window.open(jobUrl, '_blank');
      jobUrl = null;
    }
  };

  /**
   * Handles the click events in the Fancybox window.
   * @param {Event} e The click event.
   */
  var click = function(e) {
    var $target = $(e.target);

    if ($target.hasClass(closeBoxClass) ||
        $target.hasClass('continue') ||
        $target.parent().hasClass('continue')) {
      close();
    } else if ($target.hasClass('edit')) {

      // Toggle edit mode.
      edit();

      // Highlight input.
      select();
    } else if ($target.hasClass('save')) {
      if (!validate(true)) {
        return false;
      }

      // Update display.
      update();

      // Toggle view mode.
      view();
    }
  };

  /**
   * Handles the submit event on the Fancybox form.
   * @param {Event} e The click event.
   * @return {boolean} false if form validation fails.
   */
  var submit = function(e) {
    e.preventDefault();

    if (!validate()) {
      return false;
    }

    var form = getFormInputs();

    // Get email alert url.
    var url = createAlertUrl;
    if (form.q !== "") {
      url += '/q-' + form.q;
    }
    if (form.l !== "") {
      url += '/l-' + form.l;
    }
    url += '?uea=y';

    lockForm();

    // Track event.
    SH.EventLog.serpng.email_alert_interstitial_form_submit();

    // Open the job link
    loadJob();

    // Remove the link from the close button.
    // Need to refresh the jQuery object for this to work.
    $closeBox = $("a." + closeBoxClass).removeAttr("href");

    // Submit form.
    $.post(url, {email:form.email}, function(r) {
      if (r && r.ret_id) {
        setSuccess(r.data.email);
      } else if (r && r.data && 'errors' in r.data) {
        setError(r.data.errors);
        if (r.data.errors.search) {
          edit();
        }
      } else {
        setFailure();
      }
    }, 'json');

  };

  /**
   * Validates the data in the Fancybox form.
   * @param {boolean} search_only If true it disables email validation.
   * @return {boolean} False on error, otherwise true.
   */
  var validate = function(search_only) {

    // Get query, location, and email address
    var form = getFormInputs();

    // Validate search and email (same format as return value).
    // Just make sure the search and location fields aren't empty.
    var errors = {
      search: (form.q == '' && form.l == '') ? 'empty-inputs' : false,
      location: (form.q == '' && form.l == '') ? 'empty-inputs' : false,
      email: search_only ? false : SH.validation.validate_email(form.email)
    };

    if (!!errors.search || !!errors.location || !!errors.email) {
      setError(errors);
      return false;
    }

    return true;
  };

  /**
   * Updates the information in the Fancybox form.
   */
  var update = function() {

    // Get query, location, and email address.
    var form = getFormInputs();
    var keywords = form.q;
    var location = form.l;

    // Update display.
    if (SH.messages.alert_search_format) {
      $keywords.html(SH.messages.alert_search_format.replace('{{search}}', keywords?keywords:location));
      $location.html(keywords?location:'');
    } else {
      $keywords.html(keywords?keywords:location);
      $location.html(keywords?location:'');
    }

    clearError();
  };

  /**
   * Triggers the select event for the fields in the Fancybox form.
   */
  var select = function() {
    var form = getFormInputs();
    if (form.q !== "") {
      $form.find("[name=q]").select();
    } else if (form.l !== "") {
      $form.find("[name=l]").select();
    } else {
      $form.find("[name=q]").focus();
    }
  };

  /**
   * Switches the form to 'edit' mode.
   */
  var edit = function() {
    $form.addClass(editClass);
  };

  /**
   * Switches the form to 'view' mode.
   */
  var view = function() {
    $form.removeClass(editClass);
  };

  /**
   * Tells if the lightbox should be shown.
   * @return {boolean} True if the lightbox should be shown, false otherwise.
   */
  var eligible = function() {
    var alertCreated = !!SH.cookies.getSubcookie('shua', 'uaemail');

    // Don't show the interstitial if cookies are disabled.
    if (!SH.cookies.enabled) {
      return false;
    }

    // Don't show interstitial if the user has already created an alert or has seen the it.
    if (alertCreated || hasSeenEmailAlert) {
      return false;
    }

    return true;
  };

  /**
   * Changes the form contents when the email alert creation is successful.
   * @param {boolean} unconfirmed Tells which alert creation message to use.
   */
  var setSuccess = function(unconfirmed) {
    $form.html('<div class="success"><div class="message">' + (unconfirmed?SH.messages.alert_created_unconfirmed:SH.messages.alert_created_confirmed) + '</div></div>');
  };

  /**
   * Changes the form contents when there is an error in alert creation.
   * @param {Object} errors The errors encountered.
   */
  var setError = function(errors) {
    var html = SH.messages.alert_errors;
    unlockForm();

    if (!!errors.search) {
      $form.find('[name=q]').parent().addClass('error');
      html += '<br/>' + SH.messages.alert_search_error + ' ';
    }

    if (!!errors.location) {
      var inputs = getFormInputs();
      $form.find('[name=l]').parent().addClass('error');

      // Don't show a message if the location is blank, the search error message covers this.
      if (!!inputs.l) {
        html += '<br/>' + SH.messages.alert_location_error.replace('{{location}}', inputs.l) + ' ';
      }
    }

    if (!!errors.email) {
      $form.find('[name=email]').parent().addClass('error');
      html += '<br/>' + SH.messages.alert_email_error + ' ';
    }

    $message.html('<p class="error">' + html + '</p>');
  };

  /**
   * Clears the error message from the form.
   */
  var clearError = function() {
    $message.html('');
  };

  /**
   * Shows the failure message
   */
  var setFailure = function() {
    unlockForm();

    //TODO (bryan) - should we really have an alert here? 
    // Maybe just display the message in the form?
    alert(SH.messages.alert_failure);
  };

  /**
   * Disables the inputs and buttons on the form
   */
  var lockForm = function() {
    $('input,button', $form).attr('disabled', true);
  };

  /**
   * Enables the inputs and buttons on the form
   */
  var unlockForm = function() {
    $('input,button', $form).removeAttr('disabled');
  };

  // Public functions

  /**
   * Public interface to open/activate the lightbox.
   * @param {Object} job The job link element that was clicked.
   */
  var openPublic = function(jobLink, forceOpen) {

    // Don't show lightbox if not eligible unless forceOpen is true.
    if (!forceOpen && !eligible()) {
      return false;
    }

    return init(jobLink);
  };

  /**
   * Resets the hasSeenEmailAlert flag, used for unit testing.
   */
  var resetEmailAlertPublic = function() {
    hasSeenEmailAlert = false;
  };

  return {
    // Reveal public pointers to functions.
    resetEmailAlert: resetEmailAlertPublic,
    open: openPublic
  };

}(); //SH.JobLightbox()
