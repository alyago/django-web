var HeaderView = Backbone.View.extend({

    el: '#header',

    events: {
        'focus input' : 'onInputFocused',
        'blur #f_keywords,#f_location' : 'onKeywordOrLocationBlurred',
        'submit #search' : 'onSubmit',
    },

    initialize: function() {
        this.updatePlaceholderText();
    },

    //
    // EVENT HANDLERS
    //

    collapseSearchForm: function(e) {
        this.updatePlaceholderText();

        this.$('#masthead').show();
        this.$('.search-input-row').hide();
        this.$('.collapsed-search-row').show();
    },

    expandSearchForm: function(e) {
        this.$('#masthead').hide();
        this.$('.collapsed-search-row').hide();
        this.$('.search-input-row').show();
        this.$('#f_keywords').focus();
    },

    onInputFocused: function(e) {

        // Prevent the address bar from popping up
        //
        window.scroll(0,1);
    },

    onKeywordOrLocationBlurred: function(e) {
        $(e.target).val($(e.target).val().trim());
    },

    onSubmit: function(e) {
        e.preventDefault();

        // Prevent submission of empty keyword and location.
        //
        var keywords = this.$('#f_keywords').val();
        var location = this.$('#f_location').val();
        if (!keywords && !location)
            return;

        this.trigger('loading');
        e.target.submit();
    },

    updatePlaceholderText: function() {
        var keywords = this.$('#f_keywords').val();
        var location = this.$('#f_location').val();
        var defaultKeywordsText = 'Title, skills, or company';
        var defaultInText = ' in ';
        var defaultLocationText = 'location';

        if (keywords && location) {
            this.$('.search_keywords_placeholder_text').html(keywords);
            this.$('.search_divider_placeholder_text').html(defaultInText);
            this.$('.search_location_placeholder_text').html(location);
        } else if (keywords == '' && location == '') {
            this.$('.search_keywords_placeholder_text').html(defaultKeywordsText);
            this.$('.search_divider_placeholder_text').html(defaultInText);
            this.$('.search_location_placeholder_text').html(defaultLocationText);
        } else if (keywords) {
            this.$('.search_keywords_placeholder_text').html(keywords);
            this.$('.search_divider_placeholder_text').html('');
            this.$('.search_location_placeholder_text').html('');
        } else if (location) {
            this.$('.search_keywords_placeholder_text').html('Jobs');
            this.$('.search_divider_placeholder_text').html(defaultInText);
            this.$('.search_location_placeholder_text').html(location);
        }
    }
});
