EventLog = (function() {
  /**
   * Maps to Event::log in platform modules/services/EventLogging/public-lib/Event.php
   *
   * @param name string
   *   event name
   * @param parameters object
   *   parameters passed to composers defined for the event
   * @param extra object
   *   extra data to merge into the final log entry array
   *
   */
  var do_log = function(name, parameters, extra, post_log_callback) {
    var jqxhr = $.post('//www.simplyhired.com/a/event/log', {
      'name': name,
      'parameters': parameters,
      'extra': extra
    })

    if (post_log_callback) {
      jqxhr.always(post_log_callback);
    }
  };

  return {
    'accounts': {
      'sign_in_succeeded': function(callback) {
        do_log('accounts.sign_in.succeeded', {}, {}, callback);
      },

      'sign_in_failed': function(error_code) {
        do_log('accounts.sign_in.failed', {}, { 'error_code' : error_code });
      },

      'sign_up_succeeded': function(callback) {
        do_log('accounts.sign_up.succeeded', {}, {}, callback);
      },

      'sign_up_failed': function(error_code) {
        do_log('accounts.sign_up.failed', {}, { 'error_code' : error_code });
      },

      'resend_confirmation_email_succeeded': function(callback) {
        do_log('accounts.resend_confirmation_email.succeeded', {}, {}, callback);
      },

      'resend_confirmation_email_failed': function(error_code) {
        do_log('accounts.resend_confirmation_email.failed', {}, { 'error_code' : error_code });
      },

      'forgot_password_succeeded': function(callback) {
        do_log('accounts.forgot_password.succeeded', {}, {}, callback);
      },

      'forgot_password_failed': function(error_code) {
        do_log('accounts.forgot_password.failed', {}, { 'error_code' : error_code });
      }
    }
  };
})();
