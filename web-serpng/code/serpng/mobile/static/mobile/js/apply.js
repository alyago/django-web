var ApplyAppView = AppViewBase.extend({
    events: {
        'submit #job-application': 'onSubmit'
    },

    initialize: function(options) {
        AppViewBase.prototype.initialize.apply(this, arguments);
    },

    onSubmit: function(e) {
        $('[type=submit]', e.target).attr('disabled', 'disabled')
                                    .html('Submitting...');
    }
});
