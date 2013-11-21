var JobDetailAppView = AppViewBase.extend({

    events: {
        'click #email-job': 'onEmailJobFormSubmitted',
        'click #open-email-job': 'onEmailJobButtonClicked',
        'click #mobile-job-detail-content-main': 'onPageBodyClicked',
        'click .simplyapply-link': 'onSimplyApplyButtonClicked',
        'click .visit-website-link': 'onVisitWebsiteButtonClicked',
        'click .saved-star': 'onSavedJobStarClicked'
    },

    initialize: function(options) {
        AppViewBase.prototype.initialize.apply(this, arguments);
        this.savedJobCollection.on('all', this.onSavedJobCollectionChanged, this);
    },

    //
    // View event handlers
    //
    //
    
    onEmailJobFormSubmitted: function(e) {
        e.preventDefault();

        // Remove focus to close software keyboard on mobile devices.
        document.activeElement.blur();

        var pattern = /^[^@\s]+@[^@\.\s]+\.[^@\s]*[^.]$/i;
                
        if (!pattern.test($("#appendedInputButton").val())) {
            $(".buttons-banner .email-error").show();
            return;
        }
                
        $.ajax({
              type: 'POST',
              url: '/a/email-job/email?rk=' + encodeURIComponent(refindkey),
              // data to be added to query string: value of email input
              data: { e: $("#appendedInputButton").val()},
              success: function(data){
                  $(".buttons-banner").removeClass("showEmailJobForm"); 
              },
              error: function(xhr, type){
                  $(".buttons-banner .email-error").show();
              }
        });
    },

    onEmailJobButtonClicked: function(e) {
        e.preventDefault();

        this.$("#appendedInputButton").val(this.model.getEmail());

        $(".buttons-banner").addClass("showEmailJobForm");
        $(".buttons-banner .email-error").hide();
    },
        
    onPageBodyClicked: function(e) {
        if(e.target != $('#appendedInputButton').get(0) && e.target != $('#open-email-job').get(0) && e.target != $('#email-job').get(0)) {
            $(".buttons-banner").removeClass("showEmailJobForm");
        }
    },

    onSimplyApplyButtonClicked: function(e) {
        e.preventDefault();
        
        if (!this.model.get('isLoggedIn')) {
           var openSignInDialog = this.showConfirmDialog('You must sign in before you can apply to this job. Would you like to sign in now?');
           if (openSignInDialog) {
               this.showMenu();
               return;
           }
        } else {
            this.trigger('loading');
            window.location = $(e.currentTarget).data('url');
        }
        
    },

    onVisitWebsiteButtonClicked: function(e) {
        this.trigger('loading');
        window.location = $(e.currentTarget).data('url');
    },

    onSavedJobCollectionChanged: function() {
        var isSaved = !!this.savedJobCollection.get(refindkey);
        this.$('.saved-star').toggleClass('saved', isSaved);
    },

    onSavedJobStarClicked: function(e) {
        if (!this.model.get('isLoggedIn')) {
            var openSignInDialog = this.showConfirmDialog('You must sign in before you can save this job. Would you like to sign in now?');
            if (openSignInDialog) {
                this.showMenu();
            }
    
            return;
        }

        var model = this.savedJobCollection.get(refindkey);
        if (model) {
            model.destroy();
        } else {
            var jobModel = new SavedJobModel({
                'company': this.$('#company').html(),
                'location': this.$('#location').html(),
                'mobilePermalinkUrl': 'http://m.simplyhired.com/a/mobile-jobs/view/jobkey-' + encodeURIComponent(refindkey),
                'notes': '',
                'refindkey': refindkey,
                'title': this.$('#title').html()
            });

            this.savedJobCollection.create(jobModel, { at: 0 });
        }
    }
});
