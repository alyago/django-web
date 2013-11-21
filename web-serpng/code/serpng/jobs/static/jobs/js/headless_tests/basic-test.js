// Test basic functions on the SERP.
// - Basic title is good;
// - Basic search is good (good title, good results, good Ajax-loaded filters);
// - Basic JavaScript functional (email alert interstitial opens after job click).

casper.test.begin('SERP Page search form retrieves good results.', 9, function suite(test) {

  // Load an initial SERP page, check that its title is good, and
  // perform a search.
  casper.start('http://www.simplyhired.com/jobs/q-cook', function() {
    test.assertTitle('Cook Jobs | Job Search with Simply Hired',
      'Expected title with Simply Hired and keywords');

    // Make sure the canonical URL is absolute.
    var canonical = this.evaluate(function() {
      return document.querySelector("link[rel='canonical']").getAttribute("href");
    });
    test.assertEquals(canonical, 'http://www.simplyhired.com/k-cook-jobs.html',
      'Test absolute canonical URL.');

    test.assertExists('form[action="http://www.simplyhired.com/a/jobs/search"]',
      'Found main search form');
    this.fill('form[action="http://www.simplyhired.com/a/jobs/search"]', {
      q: 'nurse'
    }, true);
  });

  // Perform tests on the newly loaded SERP page.
  casper.waitForUrl(/nurse/, function() {

    // Check that the title is good, that the URL is good, that
    // the number of search results is good, and that we have "Nurse"
    // in the job title.
    test.assertTitle('Nurse Jobs | Job Search with Simply Hired',
      'New title after search is OK.');
    test.assertUrlMatch(/k-nurse-jobs.html/, 'URL for new search is OK.');
    test.assertEval(function() {
      return __utils__.findAll('div.job').length >= 10;
    }, 'New search retrieves 10 or more results.');

    // Wait for Ajax to load more filters to check that asynchronously loaded
    // data is good.
    this.waitForSelector('ul.more_filters li.filter', function then() {
      // If we get here, we know that Ajax has loaded more filters successfully.
      test.assertTruthy(true, 'Found Ajax-loaded filter.');

      // Check that interstitial email dialog pops up.
      // (Note that this also checks that JavaScript is functional on the page).
      test.assertNotVisible('#c_alerts_offer', 'Email interstitial not visible before first job click.');

      this.click('div.job a.title');

      this.waitUntilVisible('#c_alerts_offer', function then() {
        test.assertTruthy(true, 'Email interstitial is visible after first job click.');
      }, function timeout() {
        test.assertFalsy(true, 'Email interstitial is visible after first job click.');
      });

    }, function timeout() {
      // Oops, there was a timeout before the filters loaded - Ajax fail.
      test.assertFalsy(true, 'Found Ajax-loaded filter.');
    }); 
  });

  casper.run(function() {
    test.done();
  });
});
