var EmailAlertView = Backbone.View.extend({

    el: '#email-box',

    events: {
        'click .confirm-dialog .close-btn': 'onEmailCloseButtonClicked',
        'submit .input-dialog': 'onEmailSubmitted'
    },

    initialize: function() {
        this.collection.on('add', this.onEmailAlertCreated, this);
    },

    render: function() {
        if (!this.collection.where({ query:this.options.pageQuery }).length) {
            this.$el.html(JST.email_alert({
                mode:'input',
                emailAddress:this.model.getEmail()
             }));
        } else {
            this.$el.html(JST.email_alert({ mode:'already-exists' }));
        }

        this.updatePlaceholderText(this.options.pageKeywords, this.options.pageLocation);
    },

    //
    // EVENT HANDLERS
    //

    onEmailCloseButtonClicked: function(e) {
        this.trigger('close');
    },

    onEmailSubmitted: function(e) {
        e.preventDefault();

        // TODO: For now, we'll construct the title on the client side. To be more
        //       consistent, we should simply pass the title over from the server
        //       on page load (the email alert title should *always* be the page
        //       title -- not based on the keyword and location boxes).
        //
        var email = this.$('input[type=email]').val();
        var pattern = /^[^@\s]+@[^@\.\s]+\.[^@\s]*[^.]$/i;

        if (!pattern.test(email)) {
            $(".email-error").show();
            return;
        }

        $(".email-error").hide();

        this.collection.create(
            {
                query: this.options.pageQuery,
                title: this.getQueryTitle(),
                email: email
            },
            {
                at: 0
            });
    },

    onEmailAlertCreated: function() {
        this.$el.html(JST.email_alert({ mode:'confirm' }));
        this.updatePlaceholderText(this.options.pageKeywords, this.options.pageLocation);
    },

    //
    // HELPER METHODS
    //

    getQueryTitle: function() {
        var title = this.options.pageKeywords;
        if (this.options.pageLocation) {
            if (title) {
                title += ' in ';
            }

            title += this.options.pageLocation;
        }

        return title;
    },

    updatePlaceholderText: function(keywords, location) {
        var defaultKeywordsText = 'Title, skills, or company';

        if (keywords && location) {
            this.$('.search_keywords_placeholder_text').html(keywords);
            this.$('.search_divider_placeholder_text').html(' in ');
            this.$('.search_location_placeholder_text').html(location);
        } else if (keywords == '' && location == '') {
            this.$('.search_keywords_placeholder_text').html(defaultKeywordsText);
            this.$('.search_divider_placeholder_text').html();
            this.$('.search_location_placeholder_text').html();
        } else if (keywords) {
            this.$('.search_keywords_placeholder_text').html(keywords);
            this.$('.search_divider_placeholder_text').html('');
            this.$('.search_location_placeholder_text').html('');
        } else if (location) {
            this.$('.search_keywords_placeholder_text').html('Jobs');
            this.$('.search_divider_placeholder_text').html(' in ');
            this.$('.search_location_placeholder_text').html(location);
        }
    }
});


