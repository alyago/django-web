$(document).ready(function(e) {
    js_challenge();
});


js_challenge = function() {
    var alpha = Math.floor(Math.random()*11) + 1;
    var beta = Math.floor(Math.random()*11) + 1;
    var x = $.post('/a/job/check/', { 'a': alpha, 'b': beta, 'c': alpha+beta }, function(data) {
      $.post(data);
    });
};  // js_challenge()
