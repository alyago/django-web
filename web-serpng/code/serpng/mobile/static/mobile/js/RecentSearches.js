var RecentSearchModel = Backbone.Model.extend({
    attributes: {
        'title':null,
        'query':null,
    },

    idAttribute: 'query',

    sync: function(method, model, options) {
        if (method === 'delete') {
            var url = '/a/recent-searches/delete/' + model.get('query');
            var xhr = $.ajax({
                type:"DELETE",
                url:url
            });
            return xhr;
        } else {
            return Backbone.Model.prototype.sync.apply(this, arguments);
        }
    }
});

var RecentSearchCollection = Backbone.Collection.extend({
    model: RecentSearchModel,
    url: '/mobile/recent-searches'
});
