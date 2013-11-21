#!/usr/bin/python

import sys
import httplib
import httplib2
import time
import random
import multiprocessing
import zlib

job_queries = ["management",
               "communications",
               "medical+assistant",
               "security",
               "teaching",
               "accounting",
               "restaurant",
               "public+relations",
               "fashion",
               "accounts+payable",
               "cashier",
               "pharmacist",
               "nonprofit",
               "attorney",
               "executive+assistant/l-San+Diego%2C+CA",
               "retail/l-Detroit%2C+MI",
               "payroll/l-Columbus%2C+OH",
               "lvn",
               "bartender",
               "paralegal",
               "phlebotomist/l-Happy+Valley%2C+OR"
               ]


def fetch_http_content(hostname, url_path, http_headers=None, method='GET', content=None, timeout=None, max_redirects=3):
    """
    @param hostname:
    @param url_path:
    @param http_headers:
    @return:
    """
    if max_redirects < 0:
        raise ValueError("max_redirects must be greater than or equal to zero.")

    if http_headers is None:
        http_headers = {}

    redirected_url = None

    if timeout:
        h = httplib2.Http(timeout=timeout)
    else:
        h = httplib2.Http()

    response, content = h.request(hostname+url_path, method, headers=http_headers)

    if response.status == 200:
        pass
    elif response.status in (301, 302, 303, 305, 307):
        if max_redirects == 0:
            raise httplib.HTTPException("Maximum redirect limit reached.")

        redirected_url = response.get('Location', None)

    else:
        print("HTTP request to 'http://%s%s' failed. Returned status code was %s" % (hostname, url_path, response.status))


    if redirected_url:
        content = fetch_http_content(hostname, redirected_url, http_headers, method, content, timeout, max_redirects-1)

    return (response.status, content)

def print_results(values):

        max_value = max(values)
        min_value = min(values)
        avg_value = sum(values)/len(values)

        num_buckets = 10
        buckets = [[] for x in range(num_buckets)]
        bucket_size = (max_value-min_value) / num_buckets

        print 'Number of values to bucketize: %s' % len(values)
        print 'Max value: %2.04fms' % max_value
        print 'Min value: %2.04fms' % min_value
        print 'Avg value: %2.04fms' % avg_value
        print 'Bucket size: %2.04fms' % bucket_size

        for i, value in enumerate(values):
                bucket_index = int((values[i] - min_value) / bucket_size)
                if bucket_index == num_buckets:
                        bucket_index = num_buckets-1
                #print 'Putting %s in bucket %s' % (value, bucket_index)
                buckets[bucket_index].append(value)

        for i, value in enumerate(buckets):
                print '[%2i] %2.04fms - %2.04fms: %i' % (i, i*bucket_size+min_value, (i+1)*bucket_size+min_value, len(value))

def fetch_serp(worker_id, response_times, enable_output=True, dump=False):

    # rand_num = random.randint(1, 5)
    # if rand_num == 1:  # one in five chance of getting an Ajax call
    #     get_path = "/a/jobs/list/results/q-" + random.choice(job_queries)
    # else:
    #     get_path = "/a/jobs/list/q-" + random.choice(job_queries)

    get_path = "/a/jobs/list/q-" + random.choice(job_queries)

    before = time.time()
    headers = {
        'Host': 'www.simplyhired.com',
        'Accept-Encoding': 'gzip',
        #'Cookie': 'shab=exp%3D59%26alt%3D1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2'
    };

    try:
        (response_code, data) = fetch_http_content(hostname='http://xen-web-staging-1.ksjc.sh.colo', http_headers=headers, url_path=get_path)
    except Exception as ex:
        print "[%s] %s" % (worker_id, ex)

    after = time.time()
    elapsed_ms = 1000 * (after - before)
    response_times.append(elapsed_ms)

    if dump:
        #sys.stderr.write(zlib.decompress(data, 16+zlib.MAX_WBITS, 51200))
        pass

    if enable_output:
        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(before, after, response_code, len(data), elapsed_ms, get_path))
        sys.stdout.flush()

    if str(response_code).startswith('5'):
        print "!!! Server Error !!!"


# Set the queue_size to be identical to the number of threads (when we
# queue a new worker, we want it to either be serviced immediately, or
# have it fail).
#pool = ProcessPool(num_workers = num_workers, queue_size = num_workers)

if __name__ == '__main__':

    rps = 10
    num_requests = 300
    num_workers = 160
    results_manager = multiprocessing.Manager()
    response_times_proxy = results_manager.list()

    # Warm up
    #
    fetch_serp(0, [], False, True)
    sys.stderr.write('Warming up...\n')
    for i in range(10):
        fetch_serp(i, [], False)
    
    # The real test...
    
    sys.stderr.write('Starting test...\n')
    pool = multiprocessing.Pool(processes=num_workers)
    for i in range(num_requests):
        try:
            pool.apply_async(fetch_serp, [i, response_times_proxy])
        except:
            print 'The specified RPS of %s cannot be fulfilled with %s threads. Please increase the number of threads and try again.' % (rps, num_workers)
            sys.exit()
    
        time.sleep(1.0 / rps)
    
    pool.close()
    pool.join()
    
    print_results(response_times_proxy)
