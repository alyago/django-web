SH.EventLog = (function() {
  var log = function(name, extra, completion_callback) {
    $.ajax({
      'url': '//' + document.domain + '/a/event/log',
      'data': {
        'data': JSON.stringify({
          'name': name,
          'parameters': {},
          'extra': extra || {}
        })
      },
      'type': 'POST',
      'timeout': 5000,
      'complete': completion_callback || function() {}
    });
  };

  var bind = function(el) {
    var $el = $(el);
    var eventName = $el.attr('data-event-name');
    var eventType = $el.attr('data-event-type') || 'click';
    var eventExtra = eval($el.attr('data-event-extra') || null);
    var eventSuccess = function() { eval($el.attr('data-event-success') || null) };

    $el.on(eventType, function() {
      log(eventName, eventExtra, eventSuccess);
    });
  };

  var init = function() {
    $.each($('[data-event-name]'), function(index, el) {
      bind(el);
    })
  };

  init();

  return {
    'log' : log,
    'bind' : bind,
  }
})();
