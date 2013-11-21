// Make sure SH namespace is defined.
var SH = SH || {};

/**
 * @class Recent searches widget.
 */
SH.recentSearches = (function() {
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
  var NUM_SEARCHES_PER_PAGE = 5;
  var MAX_NUM_SEARCHES = 50;

  // Appropriate lengths were empirically determined.
  var MAX_SEARCH_TEXT_LENGTH = 32;

  //
  // jQuery wrapper objects
  //
  var $recentSearchesInfo = $('.js-recent-searches-info');
  var $recentSearchesListings = $('.js-recent-searches-listings');
  var $recentSearchesList = $recentSearchesListings.find('ul');
  var $recentSearchesControls = $('.js-recent-searches-controls');
  var $recentSearchesClear = $recentSearchesControls.find('.js-clear-recent-searches');
  var $recentSearchesNextPage = $recentSearchesControls.find('.js-recent-searches-next-page');
  var $recentSearchesPrevPage = $recentSearchesControls.find('.js-recent-searches-prev-page');
  var $recentSearchesResultsIndicator = $recentSearchesControls.find('.js-recent-searches-results-indicator');


  //
  // Private functions
  // -----------------
  //

  //
  // View methods (and their helpers).
  //

  // Display recent searches in the range (startIndex, stopIndex), inclusive.
  // startIndex and stopIndex are indexes into the viewedItems array, and since
  // the most recent item in the array is at the end of the array, and we are displaying
  // the items in reverse chronological order, startIndex (which corresponds to the top item
  // being displayed) is always greater than or equal to stopIndex.
  var showRecentSearches = function(startIndex, stopIndex) {
    // Save the current page's height, and use it as a maximum height if the next page has 
    // fewer than NUM_SEARCHES_PER_PAGE.
    var maxHeight = $recentSearchesList.css('height');

    // Update HTML for the displayed recently viewed searches.
    $recentSearchesList.html(constructRecentSearchesListHtml(startIndex, stopIndex));

    // Update HTML for the results indicator (e.g., '1 - 5 of 35').
    $recentSearchesResultsIndicator.html(constructResultsIndicatorHtml(startIndex, stopIndex));

    // Activate controls (clear, previous page, next page).
    var prevIsActive = startIndex < viewedItemsModel.numItems() - 1;
    var nextIsActive = stopIndex > 0;
    updateControls({ clear: true, prev: prevIsActive, next: nextIsActive });

    // If we're not on the first page, keep the height of the widget to be at that
    // for NUM_SEARCHES_PER_PAGE number of searches.
    if (prevIsActive) {
      $recentSearchesList.css('height', maxHeight);
    } else {
      $recentSearchesList.css('height', 'auto');
    }

    // Show viewed-searches information; hide default message.
    $recentSearchesInfo.hide();
    $recentSearchesListings.show();
  };

  var constructRecentSearchesListHtml = function(startIndex, stopIndex) {
    var html = '';

    // Count down because we are displaying the items in reverse chronological order.
    for (var i = startIndex; i >= stopIndex; i--) {
      var recentSearchesData = viewedItemsModel.getItem(i);

      var html = html +
        '<li data-index="' + i + '">' +
          '<div class="recent-search">' +
            '<div>' + 
              '<span class="rv-delete js-recent-searches-delete evti" data-event="recent_searches_delete" style="display:none;">[X]</span>' +
              '<a class="evtc" data-event="recent_searches_view" ' +
                'title="' + recentSearchesData.fullSearchText + 
                '" href="' + recentSearchesData.recentSearchUrl + '">' +
                  recentSearchesData.searchText +
              '</a>'
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
      $recentSearchesClear.addClass('actionable');
    } else {
      $recentSearchesClear.removeClass('actionable');
      $recentSearchesResultsIndicator.html('');
    }

    $recentSearchesPrevPage.toggleClass('actionable', !!activeControls['prev']);
    $recentSearchesNextPage.toggleClass('actionable', !!activeControls['next']);
  };


  //
  // Event handlers/controllers (and their helpers).
  //

  var displayMostRecentSearches = function() {
    if (viewedItemsModel.hasItems()) {
      var numSearches = viewedItemsModel.numItems();

      // Display the first page of searches.
      var startIndex = numSearches - 1;
      var stopIndex = numSearches - NUM_SEARCHES_PER_PAGE > 0 ? numSearches - NUM_SEARCHES_PER_PAGE : 0;
      showRecentSearches(startIndex, stopIndex);

      // Reset current page.
      currentPageModel.reset();
    } else {
      showNoSearches();
    }
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

  var showNoSearches = function() {
    // Empty out list of recent searches.
    $recentSearchesList
      .empty()
      .css('height', 'auto');

    // Deactivate controls (clear, previous page, next page).
    updateControls({ clear: false, prev: false, next: false });

    // Show default message.
    $recentSearchesInfo.show();

    // Reset to page 1.
    currentPageModel.reset();
  };

  var getSearchText = function() {
    var keywords = '';
    var location = '';

    var $keywords_input = $('input.search_keywords');
    var $location_input = $('input.search_location');

    if (!$keywords_input.hasClass('placeholder')) {
      keywords = $keywords_input.val();
    }
    if (!$location_input.hasClass('placeholder')) {
      location = $location_input.val();
    }

    // Is there a job title filter? If so, use that as the keyword in the recent search
    // text (based on observed behavior in old recent searches module).
    var href = document.location.href;
    var hrefArray = href.split('/');

    $.each(hrefArray, function(index, value) {
      if (value.startsWith('fft-')) {
        // Grab the keyword from the name of the applied filter in the filters section.
        keywords = $('#fft .selected a').data('name').toLowerCase();
      }
    });

    if ((keywords !== '') && (location !== '')) {
      return keywords + ' - ' + location;
    } else {
      if (keywords !== '') {
        return keywords;
      } else {
        return location;
      }
    }
  };

  var clearSearches = function() {
    viewedItemsModel.clear();

    // Clear display.
    showNoSearches();
  };

  var showPreviousPage = function() {
    var prevPage = currentPageModel.get() - 1;

    if (prevPage > 0) {
      var startIndex = viewedItemsModel.numItems() - 1 - ((prevPage - 1) * NUM_SEARCHES_PER_PAGE)
      var stopIndex = startIndex - NUM_SEARCHES_PER_PAGE + 1;

      showRecentSearches(startIndex, stopIndex);
      currentPageModel.decrement();
    }
  };

  var showNextPage = function() {
    var currentPageNum = currentPageModel.get();
    var nextPage = currentPageNum + 1;
    var numViewedItems = viewedItemsModel.numItems();

    if (nextPage <= Math.ceil(numViewedItems / NUM_SEARCHES_PER_PAGE)) {
      var startIndex = numViewedItems - 1 - NUM_SEARCHES_PER_PAGE * currentPageNum;
      var stopIndex = startIndex - NUM_SEARCHES_PER_PAGE + 1 > 0 ? startIndex - NUM_SEARCHES_PER_PAGE + 1 : 0;

      showRecentSearches(startIndex, stopIndex);
      currentPageModel.increment();
    }
  };

  // Construct a recent search url to be saved. This url will contain only
  // keyword, location, and job title parameters only, so that filters and paginations
  // will not result in multiple recent searches.
  var getRecentSearchUrl = function() {
    // Grab the base url
    var baseUrl = document.location.protocol + '//' + document.location.host;

    // Grab path name
    var path = document.location.pathname.toLowerCase();

    // Construct new path name
    var newPathArray = [];
    var oldPathArray = path.split('/');

    for (var i = 0, len = oldPathArray.length; i < len; i++) {
      var str = oldPathArray[i];

      if ((str === '') ||
          (str === 'a') ||
          (str === 'jobs') ||
          (str === 'list') ||
          (str.startsWith('q-')) ||
          (str.startsWith('qa-')) ||   // Advanced search
          (str.startsWith('qe-')) ||   // Advanced search
          (str.startsWith('qo-')) ||   // Advanced search
          (str.startsWith('qw-')) ||   // Advanced search
          (str.startsWith('t-')) ||    // Advanced search
          (str.startsWith('c-')) ||    // Advanced search
          (str.startsWith('o-')) ||    // Advanced search
          (str.startsWith('fft-')) ||  // Title filter (to be consistent with old recent searches)
          (str.startsWith('l-')) ||
          (str.startsWith('lc-')) ||   // Advanced search
          (str.startsWith('ls-')) ||   // Advanced search
          (str.startsWith('lz-'))) {   // Advanced search
        newPathArray.push(str);
      }     
    }

    return baseUrl + newPathArray.join('/');
  };

  var addRecentSearch = function() {
    // Reconstruct the url to include only keywords and location parameters.
    var recentSearchUrl = getRecentSearchUrl();

    // Save the full search text so it can be displayed in a tooltip.
    var fullSearchText = getSearchText();

    // Construct the search string to be displayed.
    var searchText = truncateLongHtml(fullSearchText, MAX_SEARCH_TEXT_LENGTH);

    // Construct the job data we want to store.
    var recentSearchData = {
      recentSearchUrl: recentSearchUrl,
      searchText: searchText,
      fullSearchText: fullSearchText
    };

    viewedItemsModel.addItem(recentSearchData);

    // Re-display the recently viewed searches (starting with page 1).
    displayMostRecentSearches();
  };

  var deleteRecentSearch = function() {
    var $searchToDelete = $(this).closest('li');

    if ($searchToDelete.length > 0) {
      var index = $searchToDelete.data('index');

      // Delete recent search from model.
      viewedItemsModel.deleteItem(index);

      if (viewedItemsModel.hasItems()) {

        // Remove the search from the list of searches.
        $searchToDelete.remove();

        $remainingSearches = $recentSearchesList.find('li');

        // If there are no more searches on this page, show the previous page.
        if ($remainingSearches.length == 0) {
          showPreviousPage();
        } else {

          // Find the index of the search at the top of this page.
          var topIndex = $remainingSearches.eq(0).data('index');

          if (index < topIndex) {

            // If the deleted search was below the top search, adjust the startIndex to be one
            // less than the top search to account for the deleted search.
            var startIndex = topIndex - 1;
          } else {

            // If the deleted search was above the top search, its removal does not affect
            // the starting index of the search we want to show.
            var startIndex = topIndex;
          }
          var stopIndex = startIndex - NUM_SEARCHES_PER_PAGE + 1 > 0 ? startIndex - NUM_SEARCHES_PER_PAGE + 1 : 0;

          showRecentSearches(startIndex, stopIndex);
        }
      } else {
        showNoSearches();
      }
    }
  };

  var showDeleteSearchControl = function() {
    if (!$('html').hasClass('lte7')) {
      // IE7's <li> tag contains only the text, so there is no way to
      // hover on the text AND also click on the [X] to delete.
      $(this).find('.js-recent-searches-delete').show();
    }
  };

  var hideDeleteSearchControl = function() {
    $(this).find('.js-recent-searches-delete').hide();
  };


  //
  // Public object being returned.
  // -----------------------------
  //
  return {
 
    // Initialization method that is called on page load.
    init: function() {

      // Initialize models.
      var viewedItemsInitSuccess = viewedItemsModel.init({
        cmp: 'recentSearchUrl',
        name: 'recentSearches',
        max: MAX_NUM_SEARCHES,
        expire: TIME_TO_EXPIRE
      });
      currentPageModel.init();

      // If we initialized the models successfully, proceed with initializing the
      // rest of the component.
      if (!!viewedItemsInitSuccess) {

        // Set up event handlers.
        $recentSearchesClear.click(clearSearches);
        $recentSearchesPrevPage.click(showPreviousPage);
        $recentSearchesNextPage.click(showNextPage);
        $recentSearchesList.on('mouseenter', 'li', showDeleteSearchControl);
        $recentSearchesList.on('mouseleave', 'li', hideDeleteSearchControl);
        $recentSearchesList.on('click', '.js-recent-searches-delete', deleteRecentSearch);

        // Display recent-searches div.
        $('.js-recent-searches').show();

        // Add current search to the list of recent searches.
        addRecentSearch();
      }
    }
  }
})();
