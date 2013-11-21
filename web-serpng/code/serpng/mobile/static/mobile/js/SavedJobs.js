var SavedJobModel = Backbone.Model.extend({
    
    attributes: {
        'refindkey':null,
        'notes':null
    },

    idAttribute: 'refindkey',

    // Funnel job saving through the original API, so that saved jobs are consistently
    // logged.
    //
    sync: function(method, model, options) {
        if (method === 'update') {
            var url = '/a/saved-jobs/save/' + encodeURIComponent(model.get('refindkey'));
            var xhr = $.post(url);
            return xhr;
        } else {
            return Backbone.Model.prototype.sync.apply(this, arguments);
        }
    },

    url: function() {
        return '/mobile/saved-jobs/' + encodeURIComponent(this.get('refindkey'));
    }
});

var SavedJobCollection = Backbone.Collection.extend({
    model: SavedJobModel,
    url: '/mobile/saved-jobs'
});
