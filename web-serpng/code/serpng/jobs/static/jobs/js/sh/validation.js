// Make sure SH namespace is defined.
var SH = SH || {};

/**
 * @class Validation functions.
 */
SH.validation = function() {

  var email_max   = 256;
  var email_regex = /^[a-z0-9\-\_\+]+(\.[a-z0-9\-\_\+]+)*\@(([a-z0-9\-\_\+]+(\.[a-z0-9\-\_\+]+)*){1,}\.[a-z]{2,}|([0-9]+\.){3}[0-9]+)$/i;

  return {

    // Basic email validation.
    // Returns false if no error.
    validate_email: function(email) {

      if (typeof(email) != 'string') {
        return 'not-a-string';
      }

      // Remove leading/trailing whitespace.
      email = email.replace(/(^\s+|\s+$)/g,'');

      if (email == '') {
        return 'blank-email';
      } else if (email.length > email_max) {
        return 'long-email';
      } else if (email.search(email_regex) == -1) {
        return 'invalid-email';
      }

      return false;
    }
  };
 
}(); // SH.validation() 
