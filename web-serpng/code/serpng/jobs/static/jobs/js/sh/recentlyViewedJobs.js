// Make sure SH namespace is defined.
var SH = SH || {};

/**
 * @class Recent jobs widget.
 */
SH.recentlyViewedJobs = (function() {
  //
  // Model objects for maintaining state and interfacing with local storage.
  // -----------------------------------------------------------------------
  //

  // The viewedItemsModels maintains state about the list of
  // recently viewed items, and provides an API to access and update
  // that list.
  var viewedItemsModel = (function() {

    // Private data

    // Configurations.
    var cmpKey = null;
    var localStorageKey = null;
    var maxNumViewedItems = null;
    var timeToExpire = 0;

    // Main data structure: an array of viewed items.
    var viewedItems = [];

    // Private methods.
    var getViewedItemsFromStorage = function(localStorageKey) {
      var viewedItemsInStorage = SH.LocalStorageService.get(localStorageKey);
      return (!!viewedItemsInStorage) ? viewedItemsInStorage : [];
    };

    var setViewedItemsToStorage = function(localStorageKey, newViewedItems) {
      SH.LocalStorageService.set(localStorageKey, newViewedItems);
    };

    var removeViewedItemsFromStorage = function(localStorageKey) {
      SH.LocalStorageService.remove(localStorageKey);
    };

    var removeDupes = function(newViewedItem) {
      if (!!cmpKey) {
        var index = indexOfItemByKeyPublic(newViewedItem[cmpKey]);

        if (index != -1) {
          deleteItemPublic(index);
        }
      }
    };

    var expireOldItems = function() {
      var currentTime = new Date().getTime();

      // Count down because viewedItems[viewedItems.length - 1]
      // contains the most recently viewed item. As soon as we find an item that
      // needs to be expired, we can remove all items preceding it as well
      // because those items are guaranteed to be even older.
      for (var i = viewedItems.length - 1; i >= 0; i--) {
        if ((currentTime - viewedItems[i].dateViewed) > timeToExpire) {
          viewedItems.splice(0, i + 1);
          break;
        }
      }
    };

    // Public methods (to be exposed).
    var deleteItemPublic = function(index) {
      viewedItems.splice(index, 1);
      setViewedItemsToStorage(localStorageKey, viewedItems);
    };

    var indexOfItemByKeyPublic = function(itemKey) {
      var index = -1;

      if (!!cmpKey) {
        for (var i = 0, len = viewedItems.length; i < len; i++) {
          if (viewedItems[i][cmpKey] == itemKey) {
            index = i;
          }
        }
      }

      return index;
    };

    // Public methods.
    return {
      init: function(options) {

        // Check that we have all the configuration parameters that we need.
        if (!!options &&
            options.cmp &&
            options.name &&
            options.max &&
            options.expire) {

          // Set up configurations.
          cmpKey = options.cmp;
          localStorageKey = options.name;
          maxNumViewedItems = options.max;
          timeToExpire = options.expire;

          // Initialize viewedItems from local storage.
          viewedItems = getViewedItemsFromStorage(localStorageKey);

          // Remove any old items.
          expireOldItems();

          // Return true to indicate successful initialization.
          return true;
        } else {

          // Return false to indicate failed initialization.
          return false;
        }
      },

      getItem: function(index) {
        return viewedItems[index];
      },

      addItem: function(newViewedItem) {

        // Remove duplicates.
        removeDupes(newViewedItem);

        // Add timestamp.
        newViewedItem.dateViewed = new Date().getTime();

        // Add newest item to top of stack.
        viewedItems.push(newViewedItem);

        // Flush out anything that's longer than maxNumViewedItems.
        if (viewedItems.length > maxNumViewedItems) {
          viewedItems.splice(0, viewedItems.length - maxNumViewedItems);
        }

        // Update local storage data.
        setViewedItemsToStorage(localStorageKey, viewedItems);
      },

      refreshItemByKey: function(itemKey) {
        var index = indexOfItemByKeyPublic(itemKey);

        if (index != -1) {
          // Make a copy of the old item.
          var viewedItem = viewedItems[index];

          // Delete the old item.
          deleteItemPublic(index);

          // Update the copy with a fresh timestamp.
          viewedItem.dateViewed = new Date().getTime();

          // Add the copy back to the top of the stack.
          viewedItems.push(viewedItem);

          // Update local storage data.
          setViewedItemsToStorage(localStorageKey, viewedItems);

          // Return true to indicate success.
          return true;

        } else {

          // Return false to indicate that the item was not found.
          return false;
        }
      },

      clear: function() {

        // Clear local storage.
        removeViewedItemsFromStorage(localStorageKey);

        // Clear local data structure.
        viewedItems = [];
      },

      hasItems: function() {
        return (viewedItems.length > 0);
      },

      numItems: function() {
        return viewedItems.length;
      },

      // Reveal a couple of private methods to the public API.
      indexOfItemByKey: indexOfItemByKeyPublic,
      deleteItem: deleteItemPublic
    };
  })();

  // The currentPageModel maintains state about the current page
  // being displayed in the recent items widget, and provides a 
  // public API for accessing and updating that state.
  var currentPageModel = (function() {

    // Private data.
    var page = 0;

    // Public methods.
    return {
      init: function() {
        this.reset();
      },

      reset: function() {
        page = 1;
      },

      get: function() {
        return page;
      },

      increment: function() {
        page++;
      },

      decrement: function() {
        if (page > 1) {
          page--;
        }
      }
    };
  })();


  //
  // Private variables
  // -----------------
  //

  //
  // Constants
  //
  var NUM_DAYS_IN_EXPIRATION = 60;
  var TIME_TO_EXPIRE = NUM_DAYS_IN_EXPIRATION * 24 * 60 * 60 * 1000;
  var NUM_JOBS_PER_PAGE = 5;
  var MAX_NUM_VIEWED_JOBS = 50;

  // Appropriate lengths were empirically determined.
  var MAX_JOB_TITLE_LENGTH = 32;
  var MAX_COMPANY_NAME_LENGTH = 32;

  //
  // jQuery wrapper objects
  //
  var $recentlyViewedJobsInfo = $('.js-recently-viewed-jobs-info');
  var $recentlyViewedJobsListings = $('.js-recently-viewed-jobs-listings');
  var $recentlyViewedJobsList = $recentlyViewedJobsListings.find('ul');
  var $recentlyViewedJobsControls = $('.js-recently-viewed-jobs-controls');
  var $recentlyViewedJobsClear = $recentlyViewedJobsControls.find('.js-clear-recently-viewed-jobs');
  var $recentlyViewedJobsNextPage = $recentlyViewedJobsControls.find('.js-recently-viewed-jobs-next-page');
  var $recentlyViewedJobsPrevPage = $recentlyViewedJobsControls.find('.js-recently-viewed-jobs-prev-page');
  var $recentlyViewedJobsResultsIndicator = $recentlyViewedJobsControls.find('.js-recently-viewed-jobs-results-indicator');


  //
  // Private functions
  // -----------------
  //

  //
  // View methods (and their helpers).
  //

  // Display recently viewed jobs in the range (startIndex, stopIndex), inclusive.
  // startIndex and stopIndex are indexes into the viewedItems array, and since
  // the most recent item in the array is at the end of the array, and we are displaying
  // the items in reverse chronological order, startIndex (which corresponds to the top item
  // being displayed) is always greater than or equal to stopIndex.
  var showRecentJobs = function(startIndex, stopIndex) {
    // Save the current page's height, and use it as a maximum height if the next page has 
    // fewer than NUM_JOBS_PER_PAGE.
    var maxHeight = $recentlyViewedJobsList.css('height');

    // Update HTML for the displayed recently viewed jobs.
    $recentlyViewedJobsList.html(constructViewedJobsListHtml(startIndex, stopIndex));

    // Update HTML for the results indicator (e.g., '1 - 5 of 35').
    $recentlyViewedJobsResultsIndicator.html(constructResultsIndicatorHtml(startIndex, stopIndex));

    // Activate controls (clear, previous page, next page).
    var prevIsActive = startIndex < viewedItemsModel.numItems() - 1;
    var nextIsActive = stopIndex > 0;
    updateControls({ clear: true, prev: prevIsActive, next: nextIsActive });

    // If we're not on the first page, keep the height of the widget to be at that
    // for NUM_JOBS_PER_PAGE number of searches.
    if (prevIsActive) {
      $recentlyViewedJobsList.css('height', maxHeight);
    } else {
      $recentlyViewedJobsList.css('height', 'auto');
    }

    // Show viewed-jobs information; hide default message.
    $recentlyViewedJobsInfo.hide();
    $recentlyViewedJobsListings.show();
  };

  var constructViewedJobsListHtml = function(startIndex, stopIndex) {
    var html = '';

    // Count down because we are displaying the items in reverse chronological order.
    for (var i = startIndex; i >= stopIndex; i--) {
      var viewedJobData = viewedItemsModel.getItem(i);

      var html = html +
        '<li data-index="' + i + '">' +
          '<div class="viewed-job">' +
            '<div>' + 
              '<span class="rv-delete js-recently-viewed-jobs-delete evti" data-event="recent_jobs_delete" style="display:none;">[X]</span>' +
              viewedJobData.jobLink + 
            '</div>' +
            '<div class="company" title="' + viewedJobData.fullCompanyName + '">' + viewedJobData.company + '</div>' +
          '</div>' +
        '</li>';
    }

    return html;
  };

  var constructResultsIndicatorHtml = function(startIndex, stopIndex) {
    var total = viewedItemsModel.numItems();
    var start = total - startIndex;
    var stop = total - stopIndex;

    return start + ' - ' + stop + ' of ' + total;
  };

  var updateControls = function(activeControls) {
    if (activeControls['clear']) {
      $recentlyViewedJobsClear.addClass('actionable');
    } else {
      $recentlyViewedJobsClear.removeClass('actionable');
      $recentlyViewedJobsResultsIndicator.html('');
    }

    $recentlyViewedJobsPrevPage.toggleClass('actionable', !!activeControls['prev']);
    $recentlyViewedJobsNextPage.toggleClass('actionable', !!activeControls['next']);
  };


  //
  // Event handlers/controllers (and their helpers).
  //

  var displayMostRecentJobs = function() {
    if (viewedItemsModel.hasItems()) {
      var numJobs = viewedItemsModel.numItems();

      // Display the first page of jobs.
      var startIndex = numJobs - 1;
      var stopIndex = numJobs - NUM_JOBS_PER_PAGE > 0 ? numJobs - NUM_JOBS_PER_PAGE : 0;
      showRecentJobs(startIndex, stopIndex);

      // Reset current page.
      currentPageModel.reset();
    } else {
      showNoJobs();
    }
  };
 
  var getOuterHtml = function($elem) {
    return $elem[0].outerHTML;
  };

  var removeClickHandlers = function($elem) {
    $elem.attr('onclick', null);
    $elem.attr('onmousedown', null);
    return $elem;
  };

  var addEventLogging = function($elem) {
    $elem.addClass('evtc');
    $elem.attr('data-event', 'recent_jobs_view');
    return $elem;
  };

  var stripTagsFromHtml = function(html) {
    var strippedHtml = html.replace(/<([^>]+)>/ig, '');
    return strippedHtml;
  };

  var stripTagsFromInnerHtml = function($elem) {
    var strippedHtml = stripTagsFromHtml($elem.html());
    $elem.html(strippedHtml);
    return $elem;
  };

  var stripToBasicLink = function($elem) {
    var hrefOld = $elem.attr('href');
    var hrefBase = 'www.simplyhired.com/a/job-details/view/';
    var hrefParams = hrefOld.slice(hrefOld.indexOf('//') + 2 + hrefBase.length);
    var hrefParamsArray = hrefParams.split('/');

    var hrefBasicParamsArray = [];
    $.each(hrefParamsArray, function(index, value) {

      // The only paramter we need is the 'jobkey-' parameter, which is
      // the job's refind key.
      if (value.startsWith('jobkey-')) {
        hrefBasicParamsArray.push(value);
      }
    });

    $elem.attr('href', '//' + hrefBase + hrefBasicParamsArray.join('/'));
    return $elem;
  };

  // Note: to really do this properly, use:
  // https://github.com/josephschmitt/Clamp.js/blob/master/clamp.js
  // (but it's 241 lines of JavaScript!)
  var truncateLongHtml = function(html, maxLength) {
    // Figure out what the maxLength should be, taking into account
    // capital letters, which are wider.

    // Count the number of capital letters.
    var count = 0;
    for (var i = 0; i < html.length; i++) {
      var ch = html[i];
      if (ch >= 'A' && ch <= 'Z') {
        count++;
      }
    }

    // Adjust maxLength down based on the number of capital letters.
    maxLength = maxLength - Math.ceil(count * 0.3);

    if (html.length > maxLength) {

      // Walk back to the last space character.
      for (var i = maxLength; i >= 0; i--) {
        if (html[i] == ' ') {
          break;
        }
      }

      // If we only have a single word, just truncate at maxLength.
      if (i == 0) {
        i = maxLength;
      }

      html = html.slice(0, i) + '...';
    }

    return html;
  };

  var truncateJobTitle = function($elem) {
    var fullJobTitle = $elem.html() || '';
    var truncatedJobTitle = truncateLongHtml(fullJobTitle, MAX_JOB_TITLE_LENGTH);

    // Set title to the truncated title, and add the full title as tooltip text.
    $elem.html(truncatedJobTitle);
    $elem.attr('title', fullJobTitle);

    return $elem;
  };

  var truncateCompanyName = function(html) {
    return truncateLongHtml(html, MAX_COMPANY_NAME_LENGTH);
  };

  var getCleanLinkHtml = function($job) {
    // Clone job element for cleaning.
    var $viewedLink = $job.find('a.title').clone();

    // Clean up the element's attribute and get its HTML.
    return getOuterHtml(
      addEventLogging(
        removeClickHandlers(
          truncateJobTitle(
            stripTagsFromInnerHtml(
              stripToBasicLink(
                $viewedLink
    ))))));
  };

  var getCleanCompanyHtml = function(fullCompanyName) {
    return truncateCompanyName(
      stripTagsFromHtml(
        fullCompanyName    
    ));
  };

  var showNoJobs = function() {
    // Empty out list of recently viewed jobs.
    $recentlyViewedJobsList
      .empty()
      .css('height', 'auto');

    // Deactivate controls (clear, previous page, next page).
    updateControls({ clear: false, prev: false, next: false });

    // Show default message.
    $recentlyViewedJobsInfo.show();

    // Reset to page 1.
    currentPageModel.reset();
  };

  var clearViewedJobs = function() {
    viewedItemsModel.clear();

    // Clear display.
    showNoJobs();
  };

  var showPreviousPage = function() {
    var prevPage = currentPageModel.get() - 1;

    if (prevPage > 0) {
      var startIndex = viewedItemsModel.numItems() - 1 - ((prevPage - 1) * NUM_JOBS_PER_PAGE);
      var stopIndex = startIndex - NUM_JOBS_PER_PAGE + 1;

      showRecentJobs(startIndex, stopIndex);
      currentPageModel.decrement();
    }
  };

  var showNextPage = function() {
    var currentPageNum = currentPageModel.get();
    var nextPage = currentPageNum + 1;
    var numViewedItems = viewedItemsModel.numItems();

    if (nextPage <= Math.ceil( numViewedItems / NUM_JOBS_PER_PAGE)) {
      var startIndex = numViewedItems - 1 - NUM_JOBS_PER_PAGE * currentPageNum;
      var stopIndex = startIndex - NUM_JOBS_PER_PAGE + 1 > 0 ? startIndex - NUM_JOBS_PER_PAGE + 1 : 0;

      showRecentJobs(startIndex, stopIndex);
      currentPageModel.increment();
    }
  };

  var viewRecentJob = function() {
    var viewedLinkHtml = getOuterHtml($(this));

    if (viewedItemsModel.refreshItemByKey(viewedLinkHtml)) {

      // Re-display the recently viewed jobs (starting with page 1).
      displayMostRecentJobs();
    }
  };

  var deleteRecentJob = function() {
    var $jobToDelete = $(this).closest('li');

    if ($jobToDelete.length > 0) {
      var index = $jobToDelete.data('index');

      // Delete recent job from model.
      viewedItemsModel.deleteItem(index);

      if (viewedItemsModel.hasItems()) {

        // Remove the job from the list of jobs.
        $jobToDelete.remove();

        $remainingJobs = $recentlyViewedJobsList.find('li');

        // If there are no more jobs on this page, show the previous page.
        if ($remainingJobs.length == 0) {
          showPreviousPage();
        } else {

          // Find the index of the job at the top of this page.
          var topIndex = $remainingJobs.eq(0).data('index');

          if (index < topIndex) {

            // If the deleted job was below the top job, adjust the startIndex to be one
            // less than the top job to account for the deleted job.
            var startIndex = topIndex - 1;
          } else {

            // If the deleted job was above the top job, its removal does not affect
            // the starting index of the job we want to show.
            var startIndex = topIndex;
          }
          var stopIndex = startIndex - NUM_JOBS_PER_PAGE + 1 > 0 ? startIndex - NUM_JOBS_PER_PAGE + 1 : 0;

          showRecentJobs(startIndex, stopIndex);
        }
      } else {
        showNoJobs();
      }
    }
  };

  //
  // Public functions (revealed)
  // ---------------------------
  //

  /**
   * Add a viewed job (this is an event handler that is invoked when a job in the main
   * listing is clicked).
   */
  var addViewedJobPublic = function($job, event) {

    // Get a "clean" html for the clicked job.
    var jobLink = getCleanLinkHtml($job);

    // Grab full company name so we can display it in a tooltip later.
    var fullCompanyName = $job.find('.company').html() || '';

    // Get a "clean" html for the job's company name.
    var company = getCleanCompanyHtml(fullCompanyName);

    // Construct the job data we want to store.
    var viewedJobData = {
      company: company,
      fullCompanyName: fullCompanyName,
      jobLink: jobLink
    };

    viewedItemsModel.addItem(viewedJobData);

    // Re-display the recently viewed jobs (starting with page 1).
    displayMostRecentJobs();

    // Always return true because failure to store viewed-jobs
    // data should not result in the job link not opening.
    return true;
  };

  var showDeleteJobControl = function() {
    if (!$('html').hasClass('lte7')) {
      $(this).find('.js-recently-viewed-jobs-delete').show();
    }
  };

  var hideDeleteJobControl = function() {
    $(this).find('.js-recently-viewed-jobs-delete').hide();
  };


  //
  // Public object being returned.
  // -----------------------------
  //
  return {

    // Reveal public pointers to functions.
    addViewedJob: addViewedJobPublic,

    // Initialization method that is called on page load.
    init: function() {

      // Initialize models.
      var viewedItemsInitSuccess = viewedItemsModel.init({
        cmp: 'jobLink',
        name: 'viewedJobs',
        max: MAX_NUM_VIEWED_JOBS,
        expire: TIME_TO_EXPIRE
      });
      currentPageModel.init();

      // If we initialized the models successfully, proceed with initializing the
      // rest of the component.
      if (!!viewedItemsInitSuccess) {

        // Set up event handlers.
        $recentlyViewedJobsClear.click(clearViewedJobs);
        $recentlyViewedJobsPrevPage.click(showPreviousPage);
        $recentlyViewedJobsNextPage.click(showNextPage);
        $recentlyViewedJobsList.on('click', 'li a', viewRecentJob);
        $recentlyViewedJobsList.on('mouseenter', 'li', showDeleteJobControl);
        $recentlyViewedJobsList.on('mouseleave', 'li', hideDeleteJobControl);
        $recentlyViewedJobsList.on('click', '.js-recently-viewed-jobs-delete', deleteRecentJob);

        // Display recently-viewed jobs div.
        $('.js-recently-viewed-jobs').show();

        // Display the first page of recently-viewed jobs.
        displayMostRecentJobs();

        // Return true to indicate success.
        return true;
      } else {
        // Return false so the callback registered with job views will not run.
        return false;
      }
    }
  }
})();
