SignInFormModel = Backbone.Model.extend({
  defaults: {
    email: null,
    password: null,
    error: null
  }
});

SignInFormView = FormView.extend({
  errors: {
    'invalid-credentials': 'We were unable to log you in.</br></br>Please check that your email adddress and password are correct.',
    'unconfirmed account': 'Account activation required.</br></br>Before you can sign in, please click the link in the activation email we sent to '
  },

  events: {
    'blur #email' : 'onEmailChanged',
    'click .send-email-url': 'resendConfirmationEmail'
  },

  initialize: function() {
    this.baseInitialize();
    this.model.on('change:error', this.onErrorChanged, this);
    this.updateForgotPasswordLink();
  },

  validate: function() {
    try {
      ValidateEmail(this.model.get('email'));
    } catch(ex) {
      EventLog.accounts.sign_in_failed('invalid-email');
      this.model.set('error', ex.message);
      return false;
    }

    var password = this.$('#password').val();
    if (password == null || password == '') {
      EventLog.accounts.sign_in_failed('blank-password');
      this.model.set('error', 'Please enter your password.');
      return false;
    }

    this.model.set('password', password);

    return true;
  },

  submit: function() {

    // Hide all existing error messages.
    this.model.set('error', null);
    var forwardUrl = null;

    // Disable the form before submitting our login request.
    this.disable();

    // Submit request.
    var postParams = {
      'email' : this.model.get('email'),
      'password' : this.model.get('password')
    };

    if ('f' in this.options.appModel.queryParams) {
      forwardUrl = this.options.appModel.queryParams['f'];
      postParams['f'] = forwardUrl;
    }

    var self = this;
    var request = $.post('/a/member/msalogin', postParams)
    request.fail(function() {
      EventLog.accounts.sign_in_failed('ajax-failure');
      self.model.set('error', 'Sorry! Something went wrong! Please try again.');
      self.enable();
    })
    request.done(function(json_response, success) {
      var error_code = json_response['data']['error'];
      if (error_code == null) {

        // Success!
        if (!forwardUrl) {
          forwardUrl = json_response['data']['forward_url'];
        }

        EventLog.accounts.sign_in_succeeded(function() {
          window.location.replace(decodeURIComponent(forwardUrl));
        });
      } else {

        // Display some kind of user-friendly error.
        EventLog.accounts.sign_in_failed(error_code);
        if (!(error_code in self.errors)) {
          error_code = 'invalid-credentials';
        }
        var error_message = self.errors[error_code];
        if (error_code === 'unconfirmed account') {
          error_message += self.model.get('email');
          self.$('#send-email-link').show();
        }
        self.model.set('error', error_message);
        self.enable();
      }
    });

    return false;
  },

  updateForgotPasswordLink: function() {
    var paramDict = {
      'email' : this.model.get('email')
    };

    uri = MakeUri('/account/forgot-password', paramDict);
    this.$('#forgot-password-link').attr('href', uri);
  },

  resendConfirmationEmail: function(e) {
    if (e) {
      e.preventDefault();
    }

    // Hide all existing error messages.
    this.model.set('error', null);

    // Submit request.
    var email = this.model.get('email');
    var postParams = { 'email' : email };

    var self = this;
    var request = $.post('/a/member/forgot-password', postParams)
    request.fail(function() {
      EventLog.accounts.resend_confirmation_email_failed('ajax-failure');
      self.$('#error-message').text('Sorry! Something went wrong! Please try again.');
      self.$('#error-message').show();
      self.enable();
    })
    request.done(function(json_response, success) {
      if (json_response != null && json_response.data != null) {
        self.$('#success-message').text('Thanks! You should receive an email soon with instructions on how to confirm your account.');
        self.$('#success-message').show();
        self.$('*').css('cursor', 'auto');

        EventLog.accounts.resend_confirmation_email_succeeded();
      } else {

        // Display some kind of user-friendly error.
        var error_code = (json_response.data == null ? 'default-error' : json_response.data.error);
        EventLog.accounts.resend_confirmation_email_failed(error_code);
        self.$('#error-message').text(self._errors[error_code]);
        self.$('#error-message').show();
        self.enable();
      }
    });

    return false;
  },

  onEmailChanged: function() {
    this.model.set('email', this.$('#email').val());
    this.updateForgotPasswordLink();
  },

  onErrorChanged: function() {
    var error = this.model.get('error');
    if (error == null) {
      this.$('#error-message').hide();
      this.$('#send-email-link').hide();
    } else {
      this.$('#error-message').html(error);
      this.$('#success-message').hide();
      this.$('#error-message').show();
    }
  }
});

AppView = Backbone.View.extend({
  initialize: function() {
    this.signInFormModel = new SignInFormModel({
      'email' : this.$('#email').val()
    });

    this.signInFormView = new SignInFormView({
      el: this.$('#signin-form'),
      model: this.signInFormModel,
      appModel: this.model
    });

    this.signInFormModel.bind('change:email', this.updateSignUpLink, this);

    this.updateSignUpLink();
  },

  updateSignUpLink: function() {
    var paramDict = {
      'email' : this.signInFormModel.get('email')
    };

    if ('f' in this.model.queryParams) {
      paramDict['f'] = this.model.queryParams['f'];
    }

    uri = MakeUri('/account/signup', paramDict);
    this.$('#signup-link').attr('href', uri);
  }
});

$(function() {
  var appView = new AppView({
    el: $('body'),
    model: new AppModel()
  });
});
