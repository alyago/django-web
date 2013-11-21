// Test email alert function on the SERP.


casper.test.begin('SERP Page email alert create form should work.', 6, function suite(test) {

  // Load an initial SERP page, check that its title is good, and
  // create an email alert.
  casper.start('http://www.simplyhired.com/jobs/q-cook', function() {
    test.assertTitle('Cook Jobs | Job Search with Simply Hired',
      'Expected title with Simply Hired and keywords');
    test.assertExists('.email_alert_form', 'Found email alert form.');

    // Stub jQuery.ajax so that email alert create Ajax calls return successfully.
    this.evaluate(function() {
      jQuery.ajax = function(settings) {
        if (settings.success) {
          settings.success({'ret_id': true });
        }
      };
    });

    this.fill('.email_alert_form', {email: 'abc@xyz.com'}, true);
    this.waitUntilVisible('.email_alert_dialog', function then() {
      test.assertTruthy(true, 'Email alert confirmation dialog is visible after form submission.');
    }, function timeout() {
      test.assertFalsy(true, 'Email alert confirmation dialog is visible after form submission.');
    });

    // Reload the page and re-submit email form with an invalid email address, and
    // check that the error message div is visible while the confirmation dialog is not.
    this.reload(function() {
      test.assertExists('.email_alert_form', 'Found email alert form.');
      this.fill('.email_alert_form', {email: 'abc@xyz'}, true);
        this.waitUntilVisible('.invalid_email_error', function then() {
        test.assertTruthy(true, 'Email alert error message is visible after form submission with invalid email.');
        test.assertNotVisible('.email_alert_dialog',
          'Email alert confirmation dialog is not visible after form submission with invalid email.');
      }, function timeout() {
        test.assertFalsy(true, 'Email alert error message is visible after form submission with invalid email.');
      });
    });
  });

  casper.run(function() {
    test.done();
  });
});
