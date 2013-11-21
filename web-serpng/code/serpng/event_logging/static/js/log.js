if (typeof SH == 'undefined') { SH = {}; };

SH.event_log = (function($) {
    /*
     * Maps to Event::log in web-serpng event_logging/views.py
     *
     * @param name string
     *   event name
     * @param parameters object
     *   parameters passed to composers defined for the event
     * @param extra object
     *   extra data to merge into the final log entry array
     *
     */
    var do_log = (function(name, parameters, extra, timeout, completion_callback) {

        name       = name || false;
        parameters = parameters || {};
        extra      = extra || {};
        timeout    = timeout || 5000;
        completion_callback = typeof completion_callback == 'function' || function(){};

        request_type = "POST";
        post_url   = "//"+document.domain+"/event-logging/widget-load-log";
        post_data_hash = {"name":name, "parameters":parameters, "extra":extra};

        if (typeof JSON == 'object') {
            send_ajax(request_type, post_url, "data=" + encodeURIComponent(JSON.stringify(post_data_hash)), completion_callback, timeout);
        } else { 
            // for older browsers that do not support JSON
            var json2_url = '//cdnjs.cloudflare.com/ajax/libs/json2/20121008/json2.js';
            var script=document.createElement('script');
            script.type='text/javascript';
            script.src=json2_url;
            if (script.readyState){  //IE
                script.onreadystatechange = function(){
                    if (script.readyState == "loaded" || script.readyState == "complete"){
                        script.onreadystatechange = null;
                        send_ajax(request_type, post_url, "data=" + encodeURIComponent(JSON.stringify(post_data_hash)), completion_callback, timeout);
                    }
                };
            } else {  //Others
                script.onload = function(){
                    send_ajax(request_type, post_url, "data=" + encodeURIComponent(JSON.stringify(post_data_hash)), completion_callback, timeout);
                };
            }
            document.body.appendChild(script);
        }

    });

    var send_ajax = (function(request_method, request_url, request_data, completion_callback, timeout){
        if (request_method === 'undefined' || (request_method !== 'POST' && request_method !== 'GET')) {
            return false;
        }
        if (typeof request_url !== 'string') {
            return false;
        }
        request_data = request_data || "";
        completion_callback = typeof completion_callback == 'function' ? completion_callback : function(){};
        timeout = timeout || 5000;

        if ($) {
            $.ajax({
                type: request_method,
                url: request_url,
                data: request_data,
                success: completion_callback,
                timeout: timeout
            });
        } else {
            var xhr,
                versions = ["MSXML2.XmlHttp.5.0",
                            "MSXML2.XmlHttp.4.0",
                            "MSXML2.XmlHttp.3.0",
                            "MSXML2.XmlHttp.2.0",
                            "Microsoft.XmlHttp"];
            if(window.XMLHttpRequest) { //For Mozilla, Safari (non IE browsers)
                xhr = new XMLHttpRequest();
            } else if( window.ActiveXObject ) { //For IE browsers
                for(var i = 0, n=versions.length; i < n; i++ ) {
                    try { xhr = new ActiveXObject(versions[i]); } catch(e) {}
                }
            }

            if(xhr) {
                var xhrTimeout=setTimeout("xhr.abort();",timeout); //set timeout to abort ajax in x seconds
                xhr.onreadystatechange = function() {
                    if( xhr.readyState === 4 && xhr.status === 200 ) {
                        clearTimeout(xhrTimeout); //Looks like we didn't time out! Clear timer.
                        completion_callback;
                    }
                }

                xhr.open(request_method, request_url);
                if (request_method == 'POST') {
                    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded"); //post as form data
                }
                xhr.send(request_data);
            } else { 
                return false;
            };
        }
    });

    return {
        'widget_view': function() {
            geo_ip = window.geo_ip || false;
            pub_id = window.pub_id || false;
            if (typeof(sh_search_request_id) != 'undefined') {
                do_log('widget.load', {'search_request_id':sh_search_request_id, 'referrer':document.referrer, 'pub_id':pub_id, 'geo_ip':geo_ip});
            } else {
                do_log('widget.load', {'referrer':document.referrer, 'pub_id':pub_id, 'geo_ip':geo_ip});
            }
        } // widget_view
    }
})(typeof jQuery != 'undefined' ? jQuery : null);  // SH.event_log

try{  
    var log_fn = function() { 
        SH.event_log.widget_view() 
    };
    if (window.addEventListener) {
        window.addEventListener('load',log_fn,false);
    }
    else if (window.attachEvent) 
        window.attachEvent('onload',log_fn,false);
}catch(e){}
