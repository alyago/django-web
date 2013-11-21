AppModel = Backbone.View.extend({

    initialize: function() {
        this.queryParams = this._getQueryParameterDictionary();
    },

    _getQueryParameterDictionary: function() {
        var dict = {};
        _.each(document.URL.substring(document.URL.indexOf('?')+1).split('&'), function(value, index) {
            kvp = value.split('=');
            dict[kvp[0]] = decodeURIComponent(kvp[1]);
        });
    
        return dict;
    }

});

