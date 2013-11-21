var EmailAlertModel = Backbone.Model.extend({
    attributes: {
        'id':0,
        'title':null,
        'query':null,
    },

    // Override Backbone sync to call the legacy email alert creation API, since that
    // code contains email welcome logic that we don't want to reimplement at this
    // time. All other operations should be serviced by the new API.
    //
    sync: function(method, model, options) {
        if (method === 'create') {
            var url = '/a/job-alerts/create-json/' + model.get('query');
            var xhr = $.post(
                url,
                { email: model.get('email') },
                function(response) {
                    var json_obj = JSON.parse(response);
                    if (json_obj.data && json_obj.data.errors == null) {
                        model.set('id', json_obj.data.id);
                    }
                });
            return xhr;
        } else {
            return Backbone.Model.prototype.sync.apply(this, arguments);
        }
    }
});

var EmailAlertCollection = Backbone.Collection.extend({
    model: EmailAlertModel,
    url: '/mobile/email-alerts'
});
