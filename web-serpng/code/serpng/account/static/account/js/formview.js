FormView = Backbone.View.extend({

    baseEvents: {
        'click button[type="submit"]': 'onSubmit'
    },

    baseInitialize: function() {
        this.events = _.extend(this.baseEvents, this.events);
    },

    disable: function() {
        this.$('button,input').attr('disabled', 'disabled');
        this.$('*').css('cursor', 'wait');
    },

    email_providers: [
      { suffix: '@gmail.com',   name: 'Gmail',       url: 'https://mail.google.com' },
      { suffix: '@yahoo.com',   name: 'Yahoo! Mail', url: 'https://mail.yahoo.com' },
      { suffix: '@hotmail.com', name: 'Hotmail',     url: 'https://www.hotmail.com' },
      { suffix: '@live.com',    name: 'Live Mail',   url: 'https://www.outlook.com' },
      { suffix: '@outlook.com', name: 'Outlook',     url: 'https://www.outlook.com' }
    ],

    enable: function() {
        this.$('[disabled="disabled"]').removeAttr('disabled');
        this.$('*').css('cursor', 'auto');
    },

    validate: function() {
        return true;
    },

    submit: function() {
    },

    onSubmit: function() {
        var isValid = this.validate();
        if (isValid) {
            this.submit();
        }

        return false;
    }
});
