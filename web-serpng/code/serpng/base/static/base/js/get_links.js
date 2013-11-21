SH.get_links = function() {
  
  return function(url, callback) {

    $.ajax({
      url: url,
      type: 'GET',
      dataType: 'json',
      tryCount: 0,
      retryLimit: 2,
      success: function(data) {    
        if (data) {
          callback(data);
        } else {
          this.retry();
        }
      },
      error: function() {
        this.retry();
      },
      retry: function() {
        if (this.tryCount < this.retryLimit) {
          this.tryCount++;
          $.ajax(this);
        }
      }
    });
  };

}();
