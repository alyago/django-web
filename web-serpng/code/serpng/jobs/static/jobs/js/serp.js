$(function(e){ //document.ready

  //TODO(dl-serpng): Replace all #id references with class selectors

  //http://4loc.wordpress.com/2009/04/28/documentready-vs-windowload/
  //http://docs.jquery.com/Tutorials:Introducing_$%28document%29.ready%28%29
  //http://docs.jquery.com/Tutorials:Multiple_%24%28document%29.ready%28%29

  //debug: how many nodes are on the page?
  //alert(document.getElementsByTagName('*').length);

  //search form
  SH.search.init();

  // If the browser supports the Navigation Timing spec, take all
  // available timestamps and send them back to the server to be
  // written out to log.
  if (typeof performance != 'undefined') {
    var csrftoken = SH.cookies.getCookie('csrftoken');
    var request_id = $('#request_id').html();
    var perf_data = JSON.stringify({'performance': performance, 'request_id': request_id});
    $.ajax({
      beforeSend: function(request) {
        request.setRequestHeader("X-CSRFToken", csrftoken);
      },
      data: perf_data,
      url: '/event-logging/browser-speed-log',
      dataType: 'json',
      type: 'POST'});
  }

  // Close to the start of document ready, kick off Ajax request to get
  // Serp links that are asynchronously loaded for SEO.
  //
  // When the Ajax response comes back, populate links for:
  // - Header signin;
  // - International links for the international drop-up;
  // - Legal links in the footer;
  // - Email alert dialog;
  // - Pagination;
  // - Hidden divs for tools containers;
  // - Basic filters; and
  // - More filters ("More Filters" are loaded with HTML, not just links).
  $.ajax({
    url: sh_legacy_document_pathname.replace('/a/jobs/list', '/jobs/api/serp_links') + 
         '?request_id=' + $('#request_id').html(),
    type: 'GET',
    dataType: 'json',
    tryCount: 0,
    retryLimit: 2,
    success: function(data) {
      if (data) {
        // Populate sign-in and sign-up links.
        $('.dialog_signin_link').attr('href', data.signin_link + '?f=' + encodeURIComponent(window.location.pathname));
        $('.dialog_signup_link').attr('href', data.signup_link + '?f=' + encodeURIComponent(window.location.pathname));

        // Populate data relevant to the results page (not error page).
        if ($('body').attr('id') == 'results') {
          // Populate email alert dialog content.
          $('.email_alert_dialog_content_placeholder').replaceWith(data.email_alert_dialog_content);
          SH.email_alert_create.init();

          // Populate pagination HTML.
          $('.pagination_placeholder').replaceWith(data.pagination_html);

          // Populate hidden divs for tools containers
          var tools_containers = data.tools_containers;
          $('.hidden_tools_divs').each(function(index) {
            $(this).replaceWith(tools_containers[index]);
          });

          // Populate basic filter links.
          var basic_filter_links = data.basic_filter_links;
          var index = 0;
          $('.basic_filters .filter ul li a').each(function() {
            if (($.trim($(this).html()) != gettext('Anytime')) && !($(this).parent().hasClass('see_more'))) {
              $(this).attr('href', basic_filter_links[index]);
              index++;
            }
          });

          // Populate "More Filters" HTML.
          // "More Filters" is populated with HTML instead of links because
          // there may be a delta between the filters retrieved from the searcher
          // on the first request and the filters retrieved on the Ajax request.
          // Since "More Filters" is collapsed at first, asynchronously loading
          // HTML does not deteriorate user experience.
          $('.more_filters').html(data.more_filters_html);

          // Now that filter links have been populated, initialize filters.
          SH.filters.init();

          // Initialize recent-searches module (depends on availability of the filters DOM elements).
          if ($('.recent-searches').length > 0) {
            // Initialize only if we're in the A/B test (corresponding DOM element exists).
            SH.recentSearches.init();
          }
        }
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

  //per page onload
  var f = document.body && document.body.id ? 'init_' + document.body.id : false;
  if (f && typeof SH[f] == 'function') SH[f]();

  if (!!SH.autocomplete) {
    SH.autocomplete.search.unbind();
    SH.autocomplete.search.bind();
  }

  // SERP relevance 1-question survey.
  SH.serp_survey.init();

  // Initialize placeholder fallbacks (used for FutureSERP only)
  SH.placeholder_fallbacks.init();

  // Initialize saved job header count.
  SH.SavedJobs.get();

  // Initialize email alert form tooltips (used for FutureSERP only)
  SH.help_tooltips.init();
  
  //http://www.mister-pixel.com (bug 13107)
  try {
    document.execCommand('BackgroundImageCache',false,true);
  } catch(x) {}
});

//jquery enable ajax caching by default
$.ajaxSetup({cache:true});

//jquery extend preload images
$.getImage = function(url) {
  jQuery('<img>').attr('src',url);
};

// Make sure SH namespace is defined.
var SH = SH || {};


/*
 * universal facebook like button (disabled due to slow loading)
 */
//(function(d, s, id) {
//  var js, fjs = d.getElementsByTagName(s)[0];
//  if (d.getElementById(id)) return;
//  js = d.createElement(s); js.id = id;
//  js.src = "//connect.facebook.net/en_US/all.js#xfbml=1&appId=103947962981169";
//  fjs.parentNode.insertBefore(js, fjs);
// }(document, 'script', 'facebook-jssdk'));


/*
 * global yui loader
 */
SH.yui = function() {

  var yui_loaded = function(callback) {
    if (callback) callback();
  };

  return function(callback) {
    $.getScript('/c/sh/js/yui-min.js?v=2.8.0',function(e){
      if (callback) setTimeout(callback,200); //bug 20710
      SH.yui = yui_loaded; //yui js already loaded, redefine SH.yui for future calls
    });
  };

}(); //SH.yui()


/*
 * global jquery fancybox loader
 */
SH.fancybox = function() {

  var fancybox_loaded = function(callback) {
    if (callback) callback();
  };

  return function(callback) {
    $.getScript('/static/widgets/fancybox2/source/jquery.fancybox.pack.js',function(e){
      if (callback) {

        // jQuery bug: http://bugs.jquery.com/ticket/3637
        setTimeout(callback, 100);
      }
      SH.fancybox = fancybox_loaded;
    });
  };
  
}(); //SH.fancybox()

/*
 * a/b test logging
 */
SH.experiments = function() {

  var logging_url = '/a/experiments/log';

  return {

    log: function(label, exp_id){
      $.post(logging_url,{label:label,exp_id:exp_id},null,'json'); //logging request
    }

  };
}(); //SH.experiments()

/*
 * test for js-capable bots
 */
SH.challenge = function () {
  var alpha = Math.floor(Math.random()*11) + 1;
  var beta = Math.floor(Math.random()*11) + 1;
  var x = jQuery.post('/a/job/check/', {'a': alpha, 'b': beta, 'c': alpha + beta}, 
      function(data) {
        jQuery.post(data);
      });
}(); //SH.challenge()

/*
 * global localizable functions
 */
SH.locale = {};

/*
 * global facebook connect functions
 */
SH.connect = {init:function(){}};

/*
 * Global placeholder fallback initialization (used by FutureSERP only).
 */
SH.placeholder_fallbacks = function() {
  return {
    // For each input field that needs a placeholder fallback, initialize
    // it with the placeholderFallback plug-in.
    init: function() {
      // Search box keyword input
      $('.id_f_keywords').placeholderFallback();

      // Search box location input
      $('.id_f_location').placeholderFallback();

      // Email alert creation forms, email address inputs
      $('.email_alert_email_addr').placeholderFallback();
    }
  };
}();

/*
 * Global email alert form and LinkedIn tooltips.
 */
SH.help_tooltips = function() {
  return {
    init: function() {
      // Shared tooltip style.
      var help_tooltip_styles = {
        backgroundColor: '#000',
        borderRadius: '6px',
        boxShadow: '2px 2px 4px #999',
        color: '#fff',
        padding: '10px'
      };

      // Tooltip for top-left email alert form.
      // For A/B Test 165 (Treatment C): when the email form is in the right column,
      // position the email balloon to the left.
      var email_balloon_position = 'right';
      if ($('.column-right').find('.email_alert_container').length > 0) {
        email_balloon_position = 'left';
      }

      SH.balloon.init(
          $('.email_alert_instruction', '.email_alert_container'),
          $('.email_alert_tooltip_content'),
          help_tooltip_styles, email_balloon_position, -5, 0);

      // LinkedIn marketing tooltip.
      var linkedin_tooltip_styles = $.extend(help_tooltip_styles, { width: 280 });
      SH.balloon.init(
          $('.sn_heading', '#social_network_logins'),
          $('#linkedin_tooltip', '#social_network_logins'),
          linkedin_tooltip_styles, 'left', 0, 0, 500);

      // Recently viewed jobs tooltips.
      var $recentlyViewedJobsControls = $('.js-recently-viewed-jobs-controls');
      SH.balloon.init(
          $recentlyViewedJobsControls.find('.js-clear-recently-viewed-jobs'),
          $recentlyViewedJobsControls.find('.js-clear-recently-viewed-jobs-tooltip'),
          $.extend(help_tooltip_styles, { minWidth: 10, width: 150 }),
          'top', 0, 0, 0, 100);

      // Recent searches tooltips.
      var $recentSearchesControls = $('.js-recent-searches-controls');
      SH.balloon.init(
          $recentSearchesControls.find('.js-clear-recent-searches'),
          $recentSearchesControls.find('.js-clear-recent-searches-tooltip'),
          $.extend(help_tooltip_styles, { minWidth: 10, width: 130 }),
          'top', 0, 0, 0, 100);
    }
  };
}();

SH.init_jobs = function(e) { //for any page with jobs

  /*
   * standard behaviors for jobs (inline events and delegated click)
   */
  SH.jobs = function() {

    //service urls
    var map_url    = '/a/mapped-jobs/add'; //refind key as path param
    var share_url  = '/a/send-to-friend/share'; //refind key as get param
    var flag_url   = '/a/flag-job/add'; //refind key as get param
    var unflag_url = '/a/flag-job/delete'; //refind key as get param

    //page urls
    var saved_jobs_url  = '/a/my-jobs/saved';
    var viewed_jobs_url = '/a/my-jobs/viewed';
    var mapped_jobs_url = '/a/my-jobs/mapped';

    // Array of callback functions that will be invoked when a job is viewed.
    var viewJobCallbacks = [
      updateViewedJobLinkColor,
      openInterstitialLightbox
    ];

    // Private functions

    function updateViewedJobLinkColor($job, event) {

      // Change a viewed job's link color from blue to purple.
      $job.addClass('viewed');
      return true;
    }

    function openInterstitialLightbox($job) {

      // If we open the interstitial email alert lightbox, return false so
      // the clicked job does not open in a new tab.
      if (SH.JobLightbox && SH.JobLightbox.open($job.find('a.title')[0])) {
        return false;
      }
      return true;
    }

    return {

      /**
       * Initialize the array of callback functions that will be invoked when a job is viewed.
       * @param {array} op_externalViewJobCallbacks - External callbacks for job clicks.
       */
      init: function(opt_externalViewJobCallbacks) {

        // If there are external callbacks, merge them with the internal callbacks.
        if (!!opt_externalViewJobCallbacks) {
          $.merge(viewJobCallbacks, opt_externalViewJobCallbacks);
        }
      },

      /**
       * Get/initialize result object on user action.
       * @param {string} node - Most likely a link deep in the result object.
       */
      get: function(node) {

        // Traverse up the DOM to find the result itself as we need the id.
        var $node = $(node).closest('.result');
        if (!!$node && $node.attr('id')) {
          var node_id = $node.attr('id');

          // Lazily parse result id and register click handler.
          if (!(node_id in this)) {
            this[node_id] = $node.bind('click', this.click); //+1 event handler per job (delegated)
            this[node_id].rk = node_id.split(':')[1]; //store job refind key
            this[node_id].jp = node_id.split(':')[2]; //store job position (absolute on page)
            this[node_id].jt = node_id.split(':')[3]; //store job type (0=organic,1=sponsored,2=jbb)
          }
          return this[node_id];
        }
      },

      /**
       * Delegated click on li.result for job related behaviors.
       * @param {Event} e - The click event.
       */
      click: function(e) {

        var $job = SH.jobs[this.id];

        switch(e.target.className) {

        //view saved jobs (from rating box)
        case 'myjobs':

          e.target.href = saved_jobs_url; //set href to preserve ctrl+click

          return;

        //toggle notes tab (from rating box)
        case 'note':

          var tab = e.target;
          SH.SavedJobs.get(function() {
            SH.SavedJobs.toggle_notes(tab, $job.rk); //toggle tab
            $job.removeClass('flag more block'); //close boxes
          });

          return;

        //save notes (from rating box)
        case 'save_notes':

          return SH.SavedJobs.save_notes(e.target,$job.rk);

        //cancel notes (from rating box)
        case 'cancel_notes':

          return SH.SavedJobs.cancel_notes(e.target,$job.rk);

  /*
        //toggle email tab (from send box)
        case 'email':

          SH.share.toggle_send(e.target,$job.rk); //toggle tab
          $job.removeClass('flag more block'); //close boxes

          return;

        //toggle email tab (from send box)
        case 'linkedin':

          SH.share.toggle_linkedin(e.target,$job.rk); //toggle tab
          $job.removeClass('flag more block'); //close boxes

          return;
  */

        //share job (from send box)
        case 'facebook':
        case 'twitter':
        case 'linkedin':

          var type = encodeURIComponent(e.target.className);

          e.target.href = share_url + '?rk=' + encodeURIComponent($job.rk) + '&type=' + type; //set href to preserve ctrl+click
          e.target.setAttribute('target','_blank'); //force open in new window

          return;

        //flag job (from flag box)
        case 'spam':
        case 'expired':
        case 'broken': //removed
        case 'duplicate':
        case 'inaccurate':

          var reason = encodeURIComponent(e.target.className);

          $.get(flag_url + '?rk=' + encodeURIComponent($job.rk) + '&reason=' + reason,{},null,'json'); //flag request

          $('a.flag', $job).html(SH.messages.job_flagged); // Update text and add undo link.
          $job.toggleClass('flagged').removeClass('flag'); //toggle flagged

          return;

        //also found at job click (from more box)
        case 'also':

          //do nothing

          return;

        //map job (from more box)
        case 'map':

          $.post(map_url + '/' + encodeURIComponent($job.rk),{},null,'json'); //map request

          e.target.innerHTML = SH.messages.job_mapped; //update text
          e.target.className = 'mapped'; //set mapped

          return;

        //view mapped jobs (from more box)
        case 'mapped':

          e.target.href = mapped_jobs_url; //set href to preserve ctrl+click

          return;

        case 'login':

          e.preventDefault();

          var return_url = sh_legacy_document_pathname + document.location.search; //relative url only
          //return_url += '#'+$job.rk; //add return hash
          return_url = encodeURIComponent(return_url);

          //add return url to login link
          e.target.search += e.target.search ? '&f=' + return_url : '?f=' + return_url;
          document.location = e.target.href; //do not preserve ctrl+click

          return false;

        } //switch

      }, //click

      /** 
       * Google analytics tracking. Called from click events in templates.
       * @param {integer} type - Tells if the job is sponsored.
       * @param {string} position - Doesn't look like this is used in the funciton.
       * @param {Object} a - The link that was clicked.
       * @param {array} job_data - Various job data.
       */
      track: function(type, position, a, job_data) {

        // Job click tracking.
        if (typeof a == 'undefined') {
          return false;
        }

        if (a.href.indexOf('idack') == -1) { //technically should check for ?idack or &idack
          var click_data = [];
          if (typeof job_data != 'undefined') {
            for (var key in job_data) {
              if (job_data[key]) click_data.push(key + ':' + job_data[key]);
            }
          }
          if (typeof sh_search_data != 'undefined') {
            for (var key_2 in sh_search_data) {
              if (sh_search_data[key_2]) click_data.push(key_2 + ':' + sh_search_data[key_2]);
            }
          }
          if (click_data.length > 0) {
            a.href += a.href.indexOf('?') == -1 ? '?' : '&';
            a.href += 'idack=' + encodeURIComponent(click_data.join('|'));
          }
        }

        return false;
      },

      /**
       * View job dual purpose inline click and inline mousedown.
       * @param {Object} a - The link that was clicked.
       * @param {Event} event - The click event.
       */
      view: function(a, event) {
        var $job = this.get(a);
        var returnFlag = true;
        
        // Invoke the callback functions, and return false if any of them returns false.
        // (returning false results in the clicked job NOT opening in a new tab).
        $.each(viewJobCallbacks, function(index, callBack) {
          if (!callBack($job, event)) {
            returnFlag = false;
          }
        });
      
        return returnFlag;
      },


      /*
       * boxes inline click (rate box always visible, block box OR send box OR  flag box OR more box visible)
       */

      /**
       * Saves/unsaves a job on click.
       * @param {Object} a - The link that was clicked.
       */
      toggleSave: function(a) {
        var $job = this.get(a);
        var $savelink = $('.save_job', $job);

        if ($savelink.hasClass('saved')) {

          // Remove saved job.
          SH.SavedJobs.remove($job.rk);
          $savelink.removeClass('saved');
        } else {

          // Save the job.
          SH.SavedJobs.save($job.rk);
          $savelink.addClass('saved');
        }
      },

      /**
       * Toggle rate box (set job as saved and enable rate box).
       * @param {Object} a - The link that was clicked.
       */
      save: function(a) {
        var $job = this.get(a);

        if ($job.hasClass('saved')) {
          //already saved, do nothing
        } else {
          SH.SavedJobs.save($job.rk); //save job and update header
          $('a.save',$job).html(SH.messages.job_saved); //update text
          $job.removeClass('save').addClass('saved'); //set saved
        }
      },

      /**
       * Show the login lightbox.
       * @param {string} message - The message to display in the lightbox.
       */
      showLogin: function(message) {
        if (SH.SigninLightbox) {
          SH.SigninLightbox.open(message);
        }

        return true;
      },

      /**
       * Toggle send box (for send-to-friend).
       * @param {Object} a - The link that was clicked.
       */
      send: function(a) {
        var $job = this.get(a);

        if (!$job.hasClass('send')) SH.share.reset($job); //reset form on open

        $job.removeClass('block flag more').toggleClass('send'); //toggle send and force hide others
      },

      /**
       * Toggle block box (now hide).
       * @param {Object} a - The link that was clicked.
       */
      block: function(a) {
        var $job = this.get(a);

        if ($job.hasClass('blocked')) {
          //already blocked, do nothing
        } else {
          $job.removeClass('send flag more').toggleClass('block'); //toggle block and force hide others
        }
      },

      /**
       * Toggle flag box (now report).
       * @param {Object} a - The link that was clicked.
       */
      flag: function(a) {
        var $job = this.get(a);

        if ($job.hasClass('flagged')) {
          //already flagged, do nothing
        } else {
          $job.removeClass('send block more').toggleClass('flag'); //toggle flag and force hide others
        }
      },

      /**
       * Toggle more box.
       * @param {Object} a - The link that was clicked.
       */
      more: function(a) {
        var $job = this.get(a);

        $job.removeClass('send flag block').toggleClass('more'); //toggle more and force hide others
      },

      /**
       * Undo flagged job.
       * @param {Object} a - The link that was clicked.
       */
      undo: function(a) {
        var $job = this.get(a);

        $.get(unflag_url + '?rk=' + encodeURIComponent($job.rk),{},null,'json'); //unflag request
        $('a.flag',$job).html(SH.messages.job_flag); //update text
        $job.removeClass('flagged'); //remove flagged

        $(a).remove(); //remove undo link

        //reset contact if needed
        SH.contacts.reset($job);
      }

    };

  }(); //SH.jobs()


  /*
   * Funcitons to handle saving jobs.
   */
  SH.SavedJobs = function() {

    // Saved job urls.
    var get_url    = '/a/saved-jobs/get';
    var save_url   = '/a/saved-jobs/save';
    var note_url   = '/a/saved-jobs/comment';
    var remove_url = '/a/saved-jobs/delete';

    // Class for the saved job count in the header.
    var saved_jobs_count_class = 'saved_job_count';

    return {

      // Previously saved job data.
      data: null,

      /**
       * Get user saved jobs data to populate notes.
       * @param callback The function to call when the ajax call is done.
       */
      get: function(callback) {
        $.post(get_url,{},function(r){
          SH.SavedJobs.set(r);
          if (!!callback) {
            callback();
          }
        },'json');
      },

      /**
       * Set user saved jobs data to populate notes.
       * @param r The json response object.
       */
      set: function(r) {

        this.data = {};

        if (r && r.data) {

          if (r.data.sj) {
            for (var i=0,n=r.data.sj.length; i<n; i++) {
              var sj = r.data.sj[i];
              this.data[sj.refind_key] = sj;
            }
          }

          if (r.data.n) {

            // Update the header count.
            $('.' + saved_jobs_count_class).text(r.data.n);
          }

        }

      },

      /**
       * Ajax call to save job.
       * @param job_rk The job refind key.
       */
      save: function(job_rk) {

        $.post(save_url + '/' + encodeURIComponent(job_rk),{},this.set,'json');

      },

      /**
       * Ajax call to remove saved job.
       * @param job_rk The job refind key.
       */
      remove: function(job_rk) {

        $.post(remove_url + '/' + encodeURIComponent(job_rk),this.set,null,'json');

      },

      /**
       * Toggle notes tab.
       * @param tab The tab that was clicked.
       * @param job_rk The job refind key.
       */
      toggle_notes: function(tab,job_rk) {

        var $box = $(tab.parentNode.parentNode.parentNode); //.box > ul.tabs > li.tab > a.note

        if (!$('div.tab_note',$box).length) { //create note tab

          var saved_job = this.data[job_rk]; //get saved job dta
          var comment = (saved_job && saved_job.comment) || ''; //get stored comment

          var $tab = $('<div class="tab_note"><textarea class="notes">' + comment + '</textarea><br/><button class="save_notes">' + SH.messages.job_save_button + '</button><button class="cancel_notes">' + SH.messages.job_cancel_button + '</button><span class="aside">' + SH.messages.job_notes_text + '</span></div>').appendTo($box);

        }

        $box.removeClass('rate_on').toggleClass('note_on'); //toggle tab

      },

      /**
       * Save notes.
       * @param button The button that was clicked.
       * @param job_rk The job refind key.
       */
      save_notes: function(button,job_rk) {

        var $box = $(button.parentNode.parentNode); //.box > div.tab > button
        var $tab = $('li.tab_note',$box);

        var notes = $('textarea.notes',$box)[0]; //get textarea node
        var comment = notes.value; //get comment

        comment = comment.replace(/(^\s+|\s+$)/g,''); //leading/trailing whitespace
        comment = comment.replace(/(\s+)/g,' '); //multiple whitespace

        $.post(note_url + '/' + encodeURIComponent(job_rk),{comment:comment},null,'json'); //comment request

        $box.toggleClass('note_on'); //toggle box

        if (comment) {
          if (comment.length > 10) comment = comment.substring(0,10) + '...'; //truncate + ...
          comment = comment.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); //ampersand encode critical entities
          $tab.html('<a class="note" rel="nofollow">' + SH.messages.job_edit_notes + '</a>' + ' <strong>' + comment + '</strong>'); //set snippet (tab)
        } else {
          $tab.html('<a class="note" rel="nofollow">' + SH.messages.job_add_notes + '</a>'); //reset tab
        }

        return false;
      },

      /**
       * Save notes.
       * @param button The button that was clicked.
       * @param job_rk The job refind key.
       */
      cancel_notes: function(button,job_rk) {

        // Get previously saved notes
        var saved_job = this.data[job_rk];
        var comment = saved_job && saved_job.comment ? saved_job.comment : ''; 

        var $box = $(button.parentNode.parentNode); //.box > div.tab > button
        var notes = $('textarea.notes',$box)[0]; //get textarea node
        $box.toggleClass('note_on'); //toggle box

        // Populate text area with previously saved notes
        notes.value = comment;

        return false;
      }

    };

  }(); //SH.SavedJobs()


  /*
   * share job functions
   */
  SH.share = function() {

    //send-to-friend url
    var email_url = '/a/send-to-friend/email';

    //set messaging (this refers to form)
    var set_success = function(email) {
      $('p.success',this).html(SH.messages.job_send_success); //set success message
      $('p.error',this).html(''); //clear error message
      $('div.error',this).removeClass('error'); //clear input errors
      this.friend.value = ''; //clear friend email input
      if (email) {
        // Update shua cookie. 
        SH.cookies.setSubcookie('shua', 'uaemail', email);
      }
      return true;
    };
    var set_error = function(errors) {
      $('p.success',this).html(''); //clear success message
      $('p.error',this).html(SH.messages.job_send_error); //set error message
      $('div.error',this).removeClass('error'); //clear input errors
      if (errors.n) this.name.parentNode.className += ' error'; //set input error
      if (errors.f) this.friend.parentNode.className += ' error'; //set input error
      if (errors.e) this.email.parentNode.className += ' error'; //set input error
      return false;
    };
    var set_failure = function() {
      alert(SH.messages.job_send_failure);
      return false;
    };

    return {

      //send-to-friend form nodes
      forms: {}, //{rk:form,...}

      //user entered data
      name:  '',
      email: '',

      //toggle email tab
      toggle_send: function(tab,job_rk) {

        var $box = $(tab.parentNode.parentNode.parentNode); //.box > ul.tabs > li.tab > a.email

        if (!$('form.tab_email',$box).length) { //create email form

          var $form = $('<form class="tab_email"><input name="rk" type="hidden" value="' + job_rk + '" /><div class="heading">' + SH.messages.job_send_heading + '</div><p class="error"></p><div class="element"><label class="text">' + SH.messages.job_send_name + '</label><input class="your_name text" type="text" name="name" value="" /></div><div class="element"><label class="text">' + SH.messages.job_send_email + '</label><input class="your_email text" type="text" name="email" value="" /></div><div class="element"><label class="text">' + SH.messages.job_send_friend + '</label><input class="friend_email text" type="text" name="friend" value="" /></div><button type="submit">' + SH.messages.job_send_button +  '</button><p class="success"></p></form>').appendTo($box); //email tab html

          $form.bind('submit',this.submit); //+1 event handler per job
          
          this.forms[job_rk] = $form[0]; //store reference to form node

        }

        $box.removeClass('linkedin_on').addClass('email_on'); //show tab (no toggle)

      },

      //toggle linkedin tab
      toggle_linkedin: function(tab,job_rk) {

        var $box = $(tab.parentNode.parentNode.parentNode); //.box > ul.tabs > li.tab > a.linkedin

        if (!$('div.tab_linkedin',$box).length) { //create linkedin form

          var $tab = $('<div class="tab_linkedin"></div>').appendTo($box);

        }

        $box.removeClass('email_on').addClass('linkedin_on'); //show tab (no toggle)

      },

      //reset send-to-friend form
      //this refers to SH.share
      reset: function($job) {

        //create and toggle send form
        if (!($job.rk in this.forms)) {
          var tab = $('div.send a.email',$job)[0];
          this.toggle_send(tab,$job.rk);
        }

        //get form node
        var form = this.forms[$job.rk];

        //clear messaging and errors
        $('p.success',form).html('');
        $('p.error',form).html('');
        $('div.error',form).removeClass('error');

        //set user entered name
        form.name.value = this.name;

        // Prefill email from shua cookie or user entered email.
        var shuaEmail = SH.cookies.getSubcookie('shua', 'uaemail');
        form.email.value = shuaEmail || this.email;

        return true;
      },

      //submit handler to send email to friend and set messaging
      //this refers to $(form) node
      submit: function(e) {

        e.preventDefault();

        //get form node
        var form = this;

        //get form data
        var job_rk       = form.rk.value;
        var your_name    = form.name.value;
        var your_email   = form.email.value;
        var friend_email = form.friend.value;

        //validate name and emails
        var errors = {n:your_name?false:'empty-name',e:SH.validation.validate_email(your_email),f:SH.validation.validate_email(friend_email)};

        //handle error
        if (errors.n || errors.f || errors.e) return set_error.call(form,errors);

        //store user entered name and email
        SH.share.name  = your_name;
        SH.share.email = your_email;

        //submit form
        $.post(email_url + '?rk=' + encodeURIComponent(job_rk),{n:your_name,e:your_email,f:friend_email},function(r){
          if (r && r.ret_id) set_success.call(form,your_email);
          else set_failure();
        },'json');

      }

    };

  }(); //SH.share()

  /*
   * jobs init
   */

  //initialize all jobs
  //$('li.result','div.results').bind('click',SH.jobs.click); //+1-14 event handlers (delegated)

  //initialize saved jobs only
  $('li.saved','div.results').each(function(i) {
                                      SH.jobs.get(this);
                                  }); //+0-10 event handlers (delegated)

  // Register view-job callback functions with SH.jobs
  // (these functions will be invoked when a job is viewed.)
  var viewJobCallbacks = [];

  if ($('.recently-viewed-jobs').length > 0) {
    // Initialize only if we're in the A/B test (corresponding DOM element exists).
    if (SH.recentlyViewedJobs.init()) {
      // Register callback only if the recent jobs module was successfully initialized.
      viewJobCallbacks.push(SH.recentlyViewedJobs.addViewedJob);
    }
  } 
  
  SH.jobs.init(viewJobCallbacks);

  // Initialize event handler for job results. (AB test treatment "b" only)
  // Todo(yiping): kill this code if the AB test results are bad, and integrate
  // this code into the existing SH.jobs code if the AB test results are good.
  /***** COMMENTING OUT CLICKABLE JOB DIV UNTIL FURTHER NOTICE. ******/
  // if (/* enable-hover boolean from server is true */) {
  //   // On hover, display a light-gray background.
  //   $(document).on('mouseenter', '.result', function() {
  //     $(this).addClass('gray_background');
  //   });
  //   $(document).on('mouseleave', '.result', function() {
  //     $(this).removeClass('gray_background');
  //   });

  //   // Clicking anywhere in the job div, except for extant links,
  //   // will take the user to the job link page.
  //   $(document).on('click', '.result .job', function(e) {
  //     // Grab the job link for the clicked job div.
  //     var $job_link = $('.title', this);

  //     // If click was on the job link ('title'), or on an expandable job 
  //     // list link ('cluster'), or on a SimplyApply button, or
  //     // inside the tools container, or on the LinkedIn icon, do nothing.
  //     // TODO(yiping): Refactor the following to use $().hasClass() instead.
  //     if ((e.target.className == 'title') ||
  //         (e.target.className == 'cluster') ||  
  //         (e.target.className == 'icon-simplyapply-btn') ||
  //         $(e.target).closest('.tools_container').length ||
  //         $(e.target).closest('.wdik_li').length) {
  //       return true;
  //     }

  //     // Force tracking on the click by triggering SH.jobs.track with
  //     // a mousedown (see inline onmousedown handler).
  //     $job_link.mousedown();

  //     // Force SH.jobs.view to be called (see inline onclick handler).
  //     if (SH.jobs.view($job_link[0])) {
  //       // Remove any gray backgrounds
  //       $(this).closest('.result').removeClass('gray_background');

  //       // Open job link in new window if email interstitial was not triggered.
  //       window.open($job_link.attr('href'));
  //     }
  //   });
  // }

}; //function SH.init_jobs()


SH.init_results = function(e) { //for results page only
  //search results
  var $search_results = $('#search_results');

  /*
   * FutureSERP Filters
   */
  SH.filters = function() {
    // Private variables
    var panel_state_url = '/a/jobs/panel';
    var $filters = $('.filters');

    // Private methods

    /*
     * Makes Ajax request to php-platform endpoint to update the state
     * of the filters.
     */
    var updatePanelState = function($filter) {
      var id = $filter.attr('id');
      var state = '';
      if ($filter.hasClass('expanded')) {
        // Fully expanded.
        state = '2';
      } else if ($filter.hasClass('collapsed')) {
        // Completely collapsed.
        state = '0';
      } else {
        // Expanded (but with 'See more' expansion link).
        state = '1';
      }

      $.get(panel_state_url + '?' + id + '=' + state);
    };

    /*
     * Toggles the "More Section" and individual filters between
     * collapsed and uncollapsed states.
     */
    var toggleFilter = function(e) {
      // Get ".toggle" a tag.
      var toggle = e.target.className == 'toggle' ? e.target : e.target.parentNode;

      var $toggle_parent = $(toggle.parentNode);
      if ($toggle_parent.hasClass('more_filters_container')) {
        // Toggle the "More Filters" section.
        $toggle_parent.toggleClass('collapsed');
      } else {
        var $filter = $toggle_parent.parent();

        // Toggle individiual filters.
        $filter.removeClass('expanded').toggleClass('collapsed');

        // Update the state of the filter.
        updatePanelState($filter);
      }
    };

    /*
     * Show more filter values, in response to a click on "See more".
     */
    var seeMoreFilters = function(e) {
      var $filter = $(e.target).closest('.filter');

      // Add "expanded" class to show more filter values.
      $filter.removeClass('collapsed').addClass('expanded');

      // Update the state of the filter.
      updatePanelState($filter);
    };

    /*
     * Add an "Anytime" pseudo-filter to the "Date Posted" filter.
     *
     * When a date filter has not been selected, the "Anytime" filter text appears
     * bold, informing the user that the jobs shown are from anytime.
     *
     * When a date filter has been selected, the "Anytime" filter text is
     * a link that, when clicked, clears the selected date filter.
     *
     * If there is no "Date Posted" filter, do nothing.
     */
    var addAnytimePseudoFilter = function() {
      var $date_filters_list = $('#fdb ul', $filters);
      var $selected_date_filter = $('li.selected', $date_filters_list);
      var anytime_html = '';
      var anytime_text = gettext('Anytime');

      // If there is a "Date Posted" filter.
      if ($date_filters_list.length) {

        // If a date filter has been selected.
        if ($selected_date_filter.length) {

          var url = window.location.href;

          // Remove date filter.
          if (sh_any_default) {
            url = url.replace(/&fdb=[0-9a-zA-Z]+/, "");
          } else {

            /* TODO(delaney): Remove this hack once A/B test 154 ends.
             * If user is in one of the date filter A/B test treatments,
             * add a fdb-any filter to the Anytime link URL.
             */
            url = url.replace(/fdb=[0-9a-zA-Z]+/, "fdb=any");
          }

          // Remove page number.
          url = url.replace(/&pn=[0-9]+/, "");

          // Make a new <li> element for the Anywhere pseudo-filter that inluces the clear-filter url.
          anytime_html = '<li><a rel="nofollow" class="evtc" data-event="filter_clear" data-type="Date Posted" data-name="Anytime" href="' +
            url + '"">' + anytime_text + '</a></li>';
          $(anytime_html).appendTo($date_filters_list);

        // If a date filter has not been selected.
        } else {
          // Make a new <li> element for the Anywhere pseudo-filter.
          anytime_html = '<li><strong>' + anytime_text + '</strong></li>';
          $(anytime_html).addClass('selected').appendTo($date_filters_list);
        }
      }
    };

    return {
      // Public methods

      /*
       * Initialize event handlers and the "Anytime" pseudo-filter.
       */
      init: function() {
        $filters.on('click', '.toggle', toggleFilter);
        $filters.on('click', '.see_more', seeMoreFilters);

        addAnytimePseudoFilter();
      }
    };
  }(); 


  /*
   * results page recent searches (multi)
   */
  SH.recent_searches = function() {

    //recent search selectors
    var search_list = '.recent_searches'; //not optimal

    //recent search urls
    var clear_recent_url = '/a/recent-searches/clear';

    return {

      //inline click to clear recent searches without page refresh
      //this refers to SH.recent_searches
      clear: function() {

        //clear recent searches request
        $.post(clear_recent_url,{},null,'json');

        //remove all recent search lists
        $(search_list,$search_results).remove();

        return false;
      }

    };

  }(); //SH.recent_searches()

  /*
   * FutureSERP email alert form submission and dialog.
   * Handles submission on both the top form in the left column and the
   * bottom form in the center column.
   */
  SH.email_alert_create = function() {
    // Private variables

    // jQuery objects that can be initialized before form submission
    var $email_alert_containers = $('.email_alert_container');
    var $email_alert_forms = $(".email_alert_form");   
    var $email_addr_inputs = $("input.email_alert_email_addr");  
    var $email_alert_dialog;

    // jQuery objects related to the specific form-submission target
    var $target_email_alert_container = null;
    var $target_email_alert_form = null;   
    var $target_email_alert_inputs = null;
    var $target_email_addr_input = null;  
    var $target_email_alert_loading = null;
    var $target_email_alert_submit = null;

    // Text constants
    var email_addr_placeholder_text = gettext("Email address");
    var invalid_email_error_msg = gettext("Please enter a valid email address.");

    // Ajax endpoint base url for email alert creation
    var email_alert_create_base_url = '/a/job-alerts/create-json';


    // Private functions

    /*
     * Prefill email address input fields with any stored email in cookie.
     */
    var prefillEmail = function() {
      // Prefill email from user attribute.
      var shuaEmail = SH.cookies.getSubcookie('shua', 'uaemail');
      if (($email_addr_inputs.length > 0) && !!shuaEmail) {
        $email_addr_inputs.val(shuaEmail);
      }
      
      // Add placeholder at the end so that there will not be a flash of
      // placeholder text before it is replaced with a prefilled email.
      $email_addr_inputs.attr('placeholder', email_addr_placeholder_text);
    };

    /*
     * Main event handler: process submission on email alert forms.
     */
    var submit = function(e) {
      // Initialize jQuery objects for the specific target.
      $target_email_alert_form = $(e.target);   
      $target_email_addr_input = $('input.email_alert_email_addr', $target_email_alert_form);
      $target_email_alert_inputs = $('input', $target_email_alert_form);
      $target_email_alert_container = $(e.target.parentNode);
      $target_email_alert_loading = $('.loading', $target_email_alert_form);
      $target_email_alert_submit = $('input[type=submit]', $target_email_alert_form);

      // Remove any placeholder fallback text in the email input field
      $target_email_addr_input.placeholderFallback('remove');

      // Grab email from target form.
      var email = $target_email_addr_input.val();

      // Compose email alert Ajax endpoint url.
      var url = sh_legacy_document_pathname.replace(SH.search.url, email_alert_create_base_url);

      // Check for validity of email address.
      var error = SH.validation.validate_email(email);

      if (error) {
        showEmailError();
      } else {
        clearEmailError();

        // Log email alert form submitted event.
        SH.EventLog.serpng.email_alert_top_left_btn_form_submit();
        
        // Make Ajax call to create email alert.
        $.ajax({
          url: url,
          data: {'email': email},
          dataType: 'json',
          type: 'POST',
          beforeSend: function(xhr) {

            // Show loading gif.
            $target_email_alert_submit.hide();
            $target_email_alert_loading.show();

            // Disable further submits.
            $target_email_alert_inputs.attr('disabled', true);
          },
          complete: function() {

            // Hide loading gif.
            $target_email_alert_submit.show();
            $target_email_alert_loading.hide();

            // Enable submits.
            $target_email_alert_inputs.attr('disabled', false);
          },
          error: function(r) {
            alertFailure();
          },
          success: function(r) {
            // Note: r.data.email is true when the email needs to be confirmed,
            // and false when the email has already been confirmed.
            var unconfirmed = r.data ? r.data.email : true;
            if (r && r.ret_id) {
              showSuccessDialog(unconfirmed, email);
            } else {
              alertFailure();
            }
          }
        });
      }

      return false;
    };

    /*
     * Display error text if it's not there already.
     */
    var showEmailError = function() {
      var $error_msg = $('.invalid_email_error', $target_email_alert_container);

      if ($error_msg.length === 0) {
        $('<p>').appendTo($target_email_alert_container)
                .addClass('invalid_email_error')
                .html(invalid_email_error_msg);
      }
    };

    /*
     * Clear any error messages.
     */
    var clearEmailError = function() {
      var $error_msg = $('.invalid_email_error', $target_email_alert_container);

      if ($error_msg.length > 0) {
        $error_msg.remove();
      }
    };

    /*
     * Close dialog.
     */
    var closeSuccessDialog = function() {
      // Remove click handlers for dialog.
      $(document).off('.email_alert');

      // Close dialog.
      if (!!$.fancybox) {
        $.fancybox.close();
      }
    };

    /*
     * Handle clicks while the success dialog is being displayed.
     */
    var handleClick = function(e) {
      var $target = $(e.target);

      // Check if click event should result in closing the dialog.
      if ($target.hasClass('js-icon-close') ||            // Click on close icon
          $target.hasClass('dialog_email_link') ||    // Click on link to web email
          $target.hasClass('dialog_close_link')) {    // Click on link to return to search results
        closeSuccessDialog();
      } 

      // Return true to allow webmail to open in new tab.
      return true;
    };

    /*
     * Parse webmail link address from email address.
     */
    var getEmailLink = function(email) {

      var popular_emails = {
        'gmail.com': 'mail.google.com',
        'yahoo.com': 'mail.yahoo.com',
        'aol.com': 'webmail.aol.com',
        'hotmail.com': 'www.hotmail.com'
      };

      for (var domain in popular_emails) {
        var regex = new RegExp('@' + domain + '$','i');
        if (regex.test(email)) {
          return popular_emails[domain];
        }
      }

      return false;
    };

    /*
     * Create and show dialog upon successful email alert creation.
     */
    var showSuccessDialog = function(unconfirmed, email) {      
      // Remove email alert creation forms
      $email_alert_containers.remove();

      // Populate dialog content with email address.
      // Note: email address has already been validated, so should been safe to 
      // add to HTML (validation regex does not accept HTML tags).
      $('.dialog_email_address', $email_alert_dialog).html(email);

      if (unconfirmed) {
        // If email address has not been confirmed, show messages for unconfirmed emails.
        $(".unconfirmed", $email_alert_dialog).show();

        // Populate dialog content with web mail, if any.
        var dialog_email_link = getEmailLink(email);
        if (dialog_email_link) {
          $('.dialog_email_link', $email_alert_dialog).html(dialog_email_link)
                                                      .attr('href', 'http://' + dialog_email_link);
        } else {
          $('.dialog_email_link_msg', $email_alert_dialog).remove();
        }
      } else {
        // If email address has already been confirmed, show messages for confirmed emails.
        $(".confirmed", $email_alert_dialog).show();
      }

      // Load Fancybox and create dialog.
      SH.fancybox(function() {
        $.fancybox.open([{
          helpers: {
            overlay: {
              closeClick: true,
              locked: false
            }
          },
          href: "#" + $email_alert_dialog.attr('id')
        }], {
          padding: 0
        });

        // Delegated event handler for clicks when the dialog is shown.
        $(document).on('click.email_alert', handleClick); 

      });
    };

    /*
     * Display failure to create email alert.
     */
    var alertFailure = function() {
      alert(SH.messages.alert_failure);

      // Re-enable form inputs
      $('input', $target_email_alert_form).removeAttr('disabled');
    };

    /*
     * Initialize email form and event handlers.
     */
    return {
      init: function() {
        $email_alert_dialog = $("#email_alert_dialog");
        prefillEmail();
        $email_alert_forms.live('submit', submit);
      }
    };
  }(); // SH.email_alert_create


  /*
   * FutureSERP save search dialog.
   */
  SH.save_search = function() {
    // Private variables

    // jQuery objects
    var $save_search_dialog = $('#save_search_dialog');

    // Ajax endpoint base url for saving a search.
    var save_search_url = '/a/saved-searches/add';


    // Private functions

    /*
     * Open the save-search dialog.
     */
    var open = function() {
      // Load Fancybox and create dialog.
      SH.fancybox(function() {
        $.fancybox.open([{
          helpers: {
            overlay: {
              closeClick: true,
              locked: false
            }
          },
          href: "#" + $save_search_dialog.attr('id')
        }], {
          padding: 0
        });

        // Delegated event handler for clicks when the dialog is shown
        $(document).on('click.save_search', handleClick); 
      });
    };

    /*
     * Process submission on save-search form in dialog.
     */
    var submit = function() {
      // Grab search term from form.
      var save_search_name = $("input.save_search_name", $save_search_dialog).val();

      // Compose save-search Ajax endpoint url.
      var url = sh_legacy_document_pathname.replace(SH.search.url, save_search_url);
        
      // Make Ajax call to save search.
      $.post(url, { name:save_search_name }, function(r) {
        if (r && r.ret_id) { 
          showSuccessMsg();
        } else { 
          alertFailure(); 
        }
      },'json');

      return false;
    };

    /*
     * Close dialog.
     */
    var closeDialog = function() {
      // Remove click handlers for dialog.
      $(document).off('.save_search');

      // Close dialog.
      if (!!$.fancybox) {
        $.fancybox.close();
      }
    };

    /*
     * Handle clicks while the dialog is being displayed.
     */
    var handleClick = function(e) {
      var $target = $(e.target);

      // Check if submit button was pressed
      if ($target.attr('id') === 'save_search_submit') {
        submit();

      // Check if click event should result in closing the dialog.
      } else if ($target.hasClass('js-icon-close') ||          // Click on close icon
                 $target.attr('id') === 'save_search_ok') {      // Click on "OK" button
        closeDialog();
      } 

      return false;
    };

    /*
     * Show success message in dialog.
     */
    var showSuccessMsg = function() {      
      // Hide messages displayed before the search was saved.
      $('.before_save', $save_search_dialog).hide();

      // Show messages displayed after the search was saved.
      $('.after_save', $save_search_dialog).show();

      // Update the "save search" link in the left column.
      $('#l_save_search.save_new').hide();
      $('#l_save_search.save_see_all').show();
    };

    /*
     * Display failure to save search.
     */
    var alertFailure = function() {
      alert(SH.messages.save_failure);
    };

    /*
     * Initialize event handler on click on save search.
     */
    var init = function() {
      $(document).on('click', '#l_save_search.save_new', open);
    };

    // Initialize SH.save_search.
    init();

  }();

  /*
   * results page who do i know contacts lightbox (jquery ui dialog)
   */
  SH.contacts = function() {

    //contacts selectors
    var who_handle = 'button.contacts';  //not optimal (or specific)
    var who_dialog = '#c_who_do_i_know'; //dynamic node

    //contacts dialog class
    var selector_class = 'results_dialog';

    //contacts error class
    var error_class = 'no_contacts';

    var network_urls = {
      // LinkedIn API URLs (/jobs/api/linkedin/*)
      'li': {'who': '/jobs/api/linkedin/contacts',
             'login': '/jobs/api/linkedin/activate',
             'logout': '/jobs/api/linkedin/deactivate'},
      //viadeo urls (a/viadeo/company)
      'vd': {'who': '/a/viadeo/company',
             'login': '/a/viadeo/auth_oauth2',
             'logout': '/a/viadeo/deactivate'}
    };

    var network_ua = {
       'li': 'li',
       'vd': 'vda'
    };

    var num_contacts = 3;

    //magical javascript closure to call show/collapse from loop
    function fn_response(job,company,network) {
      return function(result){
        if (result.error || !result.contacts.length) SH.contacts.collapse_without_error(job,result);
        else SH.contacts.render(job,result,network);
      };
    }

    return {

      //contacts dialog jquery objects
      $handle: null,
      $who_dialog: null,

      //contact request data
      companies: [], //[company,...]
      counts: {}, //{company:count,...}
      offset: 1,

      //initialize contacts dialog and display dialog
      //triggered by inline call to SH.contacts.open()
      //this refers to SH.contacts
      init: function() {

        //update facebook button
        SH.contacts.update_facebook();

        // Update LinkedIn radio buttons.
        SH.contacts.update_linkedin();

        $('#social_network_logins').bind('click',this.click); //+1 event handler (delegated)

        return false;
      },

      //open/close dialog
      open: function() {

        //initialize on demand
        if (!SH.contacts.$who_dialog) return SH.contacts.init();

        //update facebook button
        SH.contacts.update_facebook();

        //show dialog
        SH.contacts.$who_dialog.dialog('open');

        //handle dialog and overlay click (delegated)
        $(document.body).bind('click.contacts',SH.contacts.click); //+1 event handler (delegated)

        return false;
      },
      close: function() {

        //not initialized
        if (!SH.contacts.$who_dialog) return;

        SH.contacts.$who_dialog.dialog('close');
        $(document.body).unbind('click.contacts'); //-1 event handler (delegated)

      },
      destroy: function() {
        SH.contacts.$who_dialog.dialog('destroy');
      },

      li_action: function(action) {
        var return_url = sh_legacy_document_pathname + document.location.search;
        document.location = network_urls.li[action] + '?f=' + encodeURIComponent(return_url); //force open current window
      },

      //delegated click on contacts dialog window
      //this refers to $(dialog) node
      click: function(e) {
        var action;
        if (e.target.id == 'facebook' || (e.target.parentNode.id == 'facebook')) { //a#l_who_facebook || a#l_who_facebook span

          action = e.target.id == 'facebook' ? e.target.className : e.target.parentNode.className;

          if (action == 'activate') { //a.activate
            SH.social_search.connect();
          } else if (action == 'deactivate') { //a.deactivate
            SH.social_search.disconnect();
          }

        } else if (e.target.id == 'viadeo' || e.target.parentNode.id == 'viadeo') { //a#l_who_viadeo || a#l_who_viadeo span

          action = e.target.id == 'viadeo' ? e.target.className : e.target.parentNode.className;
          var return_url = sh_legacy_document_pathname + document.location.search;

          if (action == 'activate') { //a.activate
            document.location = network_urls.vd.login + '?f=' + encodeURIComponent(return_url); //force open current window
          } else if (action == 'deactivate') { //a.deactivate
            document.location = network_urls.vd.logout + '?f=' + encodeURIComponent(return_url); //force open current window
          }

        }

      },

      //update facebook button text
      update_facebook: function(connected) {

        if (!SH.connect || SH.connect.status === null) return;

        if (connected === null) connected = SH.connect.has_auth('EXT_AUTH');
        var button = document.getElementById('facebook');
        if (button !== null) button.className = connected ? 'deactivate' : 'activate';

        var status = $('.status',button)[0];
        if (status !== undefined) status.innerHTML = connected ? SH.messages.sn_fb_on + ' ' : SH.messages.sn_fb_off;

        var act = $('.act',button)[0];
        if (act !== undefined) act.innerHTML = connected ? 'Remove' : 'Connect'; //TODO message catalog

      },

      // Update LinkedIn radio button state based on LinkedIn user attribute.
      update_linkedin: function() {
        var li_active = !!SH.cookies.getSubcookie('shua', 'uali');
        var ui_active = !!$('#linked_in_activate').attr('checked');

        // No change needed, bail.
        if (li_active == ui_active) {
          return;
        }

        // TODO(delaney): Once we upgrade to jQuery 1.9+, change to .attr('checked', true).
        if (!li_active) {
          $('#linked_in_activate').removeAttr('checked');
          $('#linked_in_activate').removeAttr('disabled');
          $('#linked_in_deactivate').attr('checked', 'checked');
          $('#linked_in_deactivate').attr('disabled', 'disabled');
        } else {
          $('#linked_in_activate').attr('checked', 'checked');
          $('#linked_in_activate').attr('disabled', 'disabled');
          $('#linked_in_deactivate').removeAttr('checked');
          $('#linked_in_deactivate').removeAttr('disabled');
        }

        $('label[for=linked_in_activate]').toggleClass('link', !li_active);
        $('label[for=linked_in_deactivate]').toggleClass('link', li_active);
      },

      //get all contacts
      //this refers to SH.contacts
      get: function(e) {

        //initialize data
        if (typeof sh_contacts != 'undefined' && sh_contacts && typeof sh_contacts.companies != 'undefined') {
          this.companies = sh_contacts.companies;
          this.offset    = sh_contacts.offset;
        }

        var $jobs = $('li.result', '#jobs');

        //loop companies and request contacts
        for (var i=0,n=this.companies.length; i<n; i++) {

          var $job = $jobs.eq(i);
          var company  = this.companies[i];
          var networks = sh_contacts.available_networks;
          var network  = networks.length == 1 ? networks[0] : '';


          // TODO(delaney): Re-factor to make only one call per unique company (#2566).
          this.contact(company, $job, networks);
        }

      },

      success: function(result){
        if (!result.error) {
            if (result.contacts && result.contacts.length) {
               if (!result.contacts[0].mutual_name) {
                 decision.good_enough = true;
               }
               decision.final_res = result;
             }
          }
      },      

      //request contact or handle error
      //this refers to SH.contacts
      contact: function(company, $job, networks) {
        var uid;
        var shuaNetworkUID;
        if (company) {
          //contact pagination
          if (company in this.counts) {
            this.counts[company] += num_contacts;
          } else {
            this.counts[company] = this.offset;
          }
	
          if (networks.length < 2) {
            var this_network = networks[0];
            shuaNetworkUID = SH.cookies.getSubcookie('shua',
                'ua' + network_ua[this_network]);
            uid = shuaNetworkUID ? shuaNetworkUID.substring(0, 8) : '';
            var data = { 
              company: company, 
              count: num_contacts,
              start: this.counts[company],
              ref: uid
            };
            $.get(network_urls[this_network].who, data, fn_response($job, company, this_network), 'json');

          } else {

            // TODO(delaney): Clean up this logic.
            var final_res = {
              'company': company,
              'error': 'no-results'
            };
            var decision = {
              'good_enough': false,
              'final_res': final_res
            };
            var showed = false;

            //initiate
            var network = networks[0];
        
            for (var temp_network in networks) {
              //bug 25227 - unique user identifier
              var network_ua_key = networks[temp_network];
              uid = '';
              shuaNetworkUID = SH.cookies.getSubcookie('shua',
                  'ua' + network_ua[temp_network]);
              
              if (!!shuaNetworkUID) {
                uid = shuaNetworkUID.substring(0,8);  // 8 characters from agreement key
              }

              $.ajax({
                url: network_urls[networks[temp_network]].who,
                data: { company:company, count:num_contacts, start:this.counts[company], ref:uid },
                success: SH.init_results.success,
                async: false,
                dataType: 'json'
              });

              //no result from this network; has result, but result is not good enough (distance > 1).
              //save the result, continue looking
              //alert(decision.good_enough);
              if (!decision.good_enough) {
                if (decision.final_res.error != 'no-results' && !showed) {
                  final_res  = decision.final_res;
                  network = networks[temp_network];
                  showed = 'active';
                }
                continue;
              } else {
                //TODO: get the result
                final_res = decision.final_res;
                network = networks[temp_network];
                this.render($job, final_res, network);
                showed = true;
                final_res = {
                  'company': company,
                  'error': 'no-results'
                };	
                break;
              }
            }
            if (showed == 'active' && !final_res.error) {
              this.render($job, final_res,network);
            }
            else if (showed === false) {
              this.collapse_without_error($job, final_res);
            }
          } // end processing multiple networks
        } else {
          this.collapse_without_error($job, { company:null, error:'no-company' });
        }
      },

      // Render contact (both preview icon and detail view)
      render: function($job, final_res, network) {
        // This check is proabably unnecessary; however the caller code is
        // complex enough that it's worth being overly defensive here.
        if (!final_res || !final_res.company || !final_res.contacts) {
          // TODO(delaney): log an error
          return;
        }

        // Generate LinkedIn icon next to company name showing total number of connections.
        var icon_html = [];
        icon_html.push('<span class="wdik_li evti" data-event="linkedin_detail_toggle" title="');
        icon_html.push(SH.messages.contacts_view_connections, '" onclick="SH.contacts.toggle(this)">');
        icon_html.push('<img class="icon" src="/static/images/icon-linkedin.png?' + sh_deploy_tag + '">');
        icon_html.push('<div class="count_container">');
        icon_html.push('<span class="arrow_border"></span>');
        icon_html.push('<span class="arrow"></span>');
        icon_html.push('<span class="count">', final_res.total, '</span>');
        icon_html.push('</div>');
        icon_html.push('</span>');
        $('.company_location', $job).append(icon_html.join(''));

        // Generate HTML for who box.
        var html = [];
        html.push('<div class="who" style="display: none;">');

        // Header
        // [LinkedIn Icon] Connections ..................... View all connections ......... (X)
        html.push('<div class="header">');
        html.push('<img class="icon" src="/static/images/icon-linkedin.png?' + sh_deploy_tag + '">');
        html.push('<span class="title">', SH.messages.contacts_source, '</span>');
        if (final_res.total > 0) {
          html.push('<a class="see_all evti" data-event="linkedin_detail_viewall" target="_blank" href="',final_res.search_url,'">');
          html.push(SH.messages.contacts_view_all_connections);
          html.push('</a>');
        }

        html.push('<a class="close evti" data-event="linkedin_detail_close" onclick="SH.contacts.toggle(this)">');
        html.push('<img class="close" src="/static/images/icon-close.png?' + sh_deploy_tag + '">');
        html.push('</a>');
        html.push('</div>');

        // Contacts
        var company = final_res.company;
        for (var i = 0; i < final_res.contacts.length; i++) {
          var contact = final_res.contacts[i];
          //ampersand encode critical entities
          var name = contact.name.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
          var headline = contact.headline.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

          // Profile photo
          html.push('<div class="contact evti" data-event="linkedin_detail_contact">');
          var image_url = contact.image_url || '/static/images/linkedin-silhouette.gif';
          html.push('<div class="photo">');
          html.push('<a class="photo_', network, '" target="_blank" href="', contact.profile_url, '"><img src="', image_url, '?', sh_deploy_tag, '" alt="" /></a>');
          html.push('</div>');

          html.push('<div class="info">');

          // Display mutual connection information (if present).
          if (network == 'vd') {
            if (contact.distance == 2) {
              if (contact.mutual_name) {
                html.push('<a target="_blank" href="', contact.mutual_url,'">', contact.mutual_name, '</a> ', SH.messages.contacts_knows);
              }
              html.push(' ');
            }
          } else if (contact.mutual_name) {
            html.push('<a target="_blank" href="', contact.mutual_url, '">', contact.mutual_name, '</a> ', SH.messages.contacts_knows, ' ');
          }

          html.push('<a target="_blank" href="', contact.profile_url, '">', name, '</a> ');
          html.push('<span class="headline">', headline, '</span>');
          html.push('</div>');

          // Close the contact div.
          html.push('</div>');
        }

        // Clear the contact floats.
        html.push('<br>');

        // Close the who box div.
        html.push('</div>');

        // Add who box to job content.
        $job.append(html.join(''));
      },

      // Toggle contact detail view.
      toggle: function(e) {
        var $job = $(e).closest('.result');
        var $detail = $('.who', $job);
        $detail.toggle();
      },

      //collapse contact
      //this refers to SH.contacts
      collapse_without_error: function($job, result) {
        $job.addClass(error_class);
      },
      collapse: function($job, result) {

        var company = result.company;
        var error   = result.error;

        //format help html
        var html = [];
        html.push('<a class="help" onclick="return SH.contacts.help(this)" href="#">?</a>');
        html.push('<p class="help" onclick="SH.contacts.help(this)">');
        if (error == 'no-results') html.push(SH.messages.contacts_no_results.replace('{{company}}',company));
        else if (error == 'no-company') html.push(SH.messages.contacts_no_company);
        else html.push(SH.messages.contacts_error);
        html.push('</p>');
        html = html.join('');

        //create div and insert
        var div = document.createElement('DIV');
        div.className = 'who';
        div.innerHTML = html;
        $job.addClass(error_class).append(div);
      },

      //reset contact if error
      //this refers to SH.contacts
      reset: function($job) {
        //request contact if none
        if ($job.hasClass(error_class)) {

          //reset error
          $job.removeClass(error_class);
          $('div.who', $job).remove();

          var company = $('span.company', $job).text();

          //request contact
          this.contact(company, $job);
        }
      },

      //show no results error message
      //this refers to a.help or p.help
      help: function(help) {

        var $job = $(help).closest('.result');
        $job.toggleClass(error_class);

        if (help.nextSibling) {
          help.style.display = 'none';
          help.nextSibling.style.display = 'block';
        } else if (help.previousSibling) {
          help.style.display = 'none';
          help.previousSibling.style.display = 'block';
        }
        return false;
      }
    };
  }(); //SH.contacts()


  /*
   * nps survey
   */
  SH.nps_survey = function() {

    //survey url (/a/survey/feedback)
    var survey_url = '/a/survey/feedback';

    return {

      $survey: null,

      expand: false,

      init: function() {

        //don't show survey if not eligible
        if (!SH.nps_survey.eligible()) return false;

        //feature not enabled
        if (typeof sh_survey_message === 'undefined' || sh_survey_message === null) return false;

        this.$survey = $('<div id="c_survey_prompt"></div>').appendTo('#container');

        if (sh_survey_message.html) {
          this.$survey.append('<div class="prompt">' + sh_survey_message.prompt + ' <img class="survey_close" onclick="SH.nps_survey.$survey.remove();" src="/c/simplyhired-common/images/x.png?' + sh_deploy_tag + '" /></div><div class="message" style="display:none;">' + sh_survey_message.html + '</div>');
        } else {
          this.$survey.append('<div class="prompt"><a class="survey" href="' + survey_url + '">' + sh_survey_message.prompt + '</a> <img class="survey_close" src="/c/simplyhired-common/images/x.png?' + sh_deploy_tag + '" /></div>');
        }

        //set toggle behavior
        this.expand = sh_survey_message.html ? true : false;

        //handle survey click (delegated)
        this.$survey.bind('click',this.click); //+1 event handler (delegeated)
        $('.survey_close').bind('click',this.close);
        //track prompt
        setTimeout(this.track,100);

      },

      //delegated click on survey container
      //this refers to $(survey) node
      click: function(e) {

        if (!SH.nps_survey.eligible()) { //recheck eligibility

          //close survey prompt/message
          SH.nps_survey.$survey.remove();

          return false;

        } else if (e.target.className == 'prompt') { //div.prompt

          //increment interaction count
          if (SH.nps_survey.interacted) SH.nps_survey.interacted();

          //toggle message
          $('.message',SH.nps_survey.$survey).toggle();

        } else if (e.target.className == 'survey') { //div.prompt > a.survey || div.message > a.survey

          //set response status
          if (SH.nps_survey.viewed) SH.nps_survey.viewed();

          //increment interaction count
          if (SH.nps_survey.interacted) SH.nps_survey.interacted();

        }

      },

      track: function() {
        SH.tracker.ga.trackPageview(survey_url + '/prompt');
      },

      //is user eligible to see survey?
      eligible: function() {

        //cookies not enabled
        if (!SH.cookies.enabled) return false;

        //old browser
        if ($.browser.msie && $.browser.version<=6) return false;

        //already seen survey
        var shuaNPS = SH.cookies.getSubcookie('shua', 'uanps');
        var nps = !!shuaNPS ? shuaNPS.split(':') : null;

        if (!nps || nps[3] > 0) {
          return false;
        }

        return true;
      },

      //user interacted with survey prompt, increment interactions
      interacted: function() {

        var shuaNPS = SH.cookies.getSubcookie('shua', 'uanps');
        if (!!shuaNPS) {
          var nps = shuaNPS.split(':');
          nps[2]++;
          nps = nps.join(':');
          this.set_attribute(nps);

          this.interacted = null;
        }  
      },

      //user clicked on survey link, mark survey as viewed
      viewed: function() {
        var shuaNPS = SH.cookies.getSubcookie('shua', 'uanps');

        if (!!shuaNPS) {
          var nps = shuaNPS.split(':');

          if (nps[3] < 1) {
            nps[3] = 1;
          }
          nps = nps.join(':');
          this.set_attribute(nps);

          this.viewed = null;
        }  
      },

      close: function() {
        SH.nps_survey.interacted();
        SH.nps_survey.$survey.remove();
      },

      //set nps user attribute
      set_attribute: function(nps) {
        SH.cookies.setSubcookie('shua', 'uanps', nps);
      }
    };
  }(); //SH.nps_survey();


  /*
   * facebook connect
   */
  SH.connect.listener = function() {
    SH.social_search.show_loading();
  };
  SH.connect.render = function() {
    SH.social_search.render();
  };


  /* 
   * job view duration measurement
   */
  $(window).blur( function () {
      $.ajax({type: 'POST', url:"/a/job/leave"});
    });

  $(window).focus( function () {
      $.ajax({type: 'POST', url:"/a/job/serp"});
    });


  /*
   * results page init
   */

  //facebook connect
  SH.connect.init();

  //initialize jobs (first!)
  SH.init_jobs(e);

  // Initialize Google Analytics and Quantcast trackers.
  SH.tracker.ga.init(sh_pageAccount);
  SH.tracker.q.init();

  //nps survey
  SH.nps_survey.init(e);

  //who do i know
  SH.contacts.init(e);
  SH.contacts.get(e);

  //search version ping
  if (typeof sh_search_ping != 'undefined' && sh_search_ping) $.get(sh_search_ping);

  //handle results page actions
  if (document.location.hash == '#facebook' || document.location.hash == '#linkedin' || document.location.hash == '#wdik' || document.location.hash == '#who') {
    SH.contacts.open();
  } else if (document.location.hash == '#email-subscribe') {

    // Load the fancybox javascript when the page loads, show the email interstitial when done.
    SH.fancybox(function() { SH.JobLightbox.open(null, true); });
  } else {

    // Load the fancybox javascript when the page loads.
    SH.fancybox();
  }

}; //function SH.init_results

/*
 * results page event handler tally:
 *
 * +1 global event handler(s) for search form
 * +1 global event handler(s) for intl dropdown
 *
 * +1 event handler(s) for dynamic header
 * +1 event handler(s) for filters panel
 * +4 conditional event handler(s) for saved search form
 * +2 conditional event handler(s) for who-do-i-know dialog
 * +3 conditional event handler(s) for email alerts
 *
 * +0-10 conditional event handler(s) for jobs (1 per job)
 * +0-20 conditional event handler(s) for stars hover behavior (2 per job)
 * +3 conditional event handler(s) for email alerts lightbox
 *
 * total = 4 event handlers, up to 10+30+3 conditional event handlers
 */


SH.init_error = function(e) { //for results error page only


  /*
   * facebook connect
   */
  SH.connect.listener = function() {
    SH.social_search.show_loading();
  };
  SH.connect.render = function() {
    SH.social_search.render();
  };


  /*
   * dang page init
   */

  //facebook connect
  SH.connect.init();

  //google analytics, quantcast, and comscore tracking
  SH.tracker.ga.init(sh_pageAccount);
  SH.tracker.q.init();

}; //function SH.init_error


// SERP relevance survey component.
SH.serp_survey = function() {

  // Total WIDTH of survey (including close button).
  WIDTH = 240;

  // Animation speed (in ms).
  SPEED = 400;

  // Delay displaying survey after search results are displayed (in ms).
  SHOW_DELAY = 5000;

  // Delay dismissing survey after vote (in ms).
  HIDE_DELAY = 2000;

  return {
    /*
     * Initialize survey component, including visibility control timer and
     * event listeners. Uses a flag in the shua cookie to make sure the survey
     * is only shown once per unique visitor.
     */
    init: function() {
      // Look for survey cookie, bail if set.
      if (!this.check_and_set_cookie()) {
        return;
      }

      // Attach click handlers to yes/no/ action links.
      $('#survey .action-link').click(function() {
        // The following sequence replaces the survey form with a thank you message.
        $('#survey #survey_question').hide();
        // fadeIn changes display to inherit, force inline-block.
        $('#survey #survey_thanks').fadeIn(SPEED).css('display', 'inline-block');

        // After displaying the thank you message for 2s, slide the survey off screen.
        setTimeout(function() {
          $('#survey').animate({right: -WIDTH}, SPEED);
        }, HIDE_DELAY);
      });

      // Close button should dismiss the survey immediately.
      $('#survey .js-icon-survey-close-button').click(function() {
        $('#survey').animate({right: -WIDTH}, SPEED);
      });

      // Start slide-in animation, use timer to delay 5s.
      setTimeout(function() {
        $('#survey').show().animate({right: 0}, 400);
      }, SHOW_DELAY);
    },

    /*
     * Looks for the srs (SERP relevance survey) flag in the user attribute
     * cookie. If this flag is set, the user has already seen the survey,
     * return false. Otherwise set the flag, update the user attribute cookie,
     * and return true. The caller can use the return value to determine whether
     * the survey should be shown (true) or not (false).
     */
    check_and_set_cookie: function() {
      // If cookies are disabled, bail.
      if (!SH.cookies.enabled) return false;

      // Skip survey on lame browsers.
      if ($.browser.msie && $.browser.version <= 7) return false;

      // Check the current flag value. If flag is unset, set the flag, update
      // the user attribute cookie, and return true.
      if (!SH.cookies.getSubcookie('shua', 'uasrs')) {
        // Only render survey for 1% of requests. Perform this check outside
        // of the AB test framework so we can run the survey for all AB tests.
        // Logic verified here - http://jsfiddle.net/fFKQn/
        if (Math.random() < 0.01) {
          SH.cookies.setSubcookie('shua', 'uasrs', 1);
          return true;
        }
      }

      return false;
    }
  };
}();
