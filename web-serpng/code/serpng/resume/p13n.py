from django.conf import settings

from collections import defaultdict, OrderedDict
import operator


def write_resume_job_title_data(user_id, jobformset):
    from jsonrpc.proxy import ServiceProxy

    try:
        current_job = None
        past_jobs = []
        is_first = True

        # iterate over job forms and collect titles as one long string
        for jobform in jobformset.forms:
            if jobform in jobformset.deleted_forms:
                continue

            title = jobform.cleaned_data.get('title', False)

            if not title:
                continue

            if is_first:
                current_job = title
                is_first = False
            else:
                past_jobs.append(title)

        if current_job: # user has at least one job
            first_freq_dist = _get_token_freqdist(current_job.strip())
            past_freq_dist = _get_token_freqdist(' '.join(past_jobs).strip())

            freq_dist = {
                'current_job_title': first_freq_dist,
                'past_job_titles': past_freq_dist,
            }

            rpc = ServiceProxy(service_url=settings.APEMAN_RPC_SERVICE_URL, service_name=None, version='1.0')
            rpc.personalization.setResumeData(user_id, freq_dist)
    except:
        # caught in caller
        raise

def _get_token_freqdist(string):
    stopwords = {'a', 'able', 'all', 'also', 'an', 'and', 'any', 'anything', 'apply', 'are', 'as', 'at', 'be',
                     'by', 'can', 'excellent', 'for', 'from', 'has', 'have', 'if', 'in', 'include', 'is', 'job', 'jobs', 'look',
                     'more', 'must', 'need', 'not', 'of', 'on', 'opportunity', 'or', 'other', 'our', 'please', 'that', 'the',
                     'their', 'this', 'through', 'to', 'we', 'with', 'within', 'you', 'your', '-'}

    # lowercase, trim, tokenize the keyword string, filter out stopwords
    tokens = filter(lambda x: x not in stopwords, string.lower().strip().split())
    counts = defaultdict(int)

    for token in tokens:
        counts[token] += 1

    num_tokens = float(len(tokens)) # float for division below

    frequencies = []
    for token, count in counts.iteritems():
        frequencies.append({
            'keywords': token,
            'weight': count/num_tokens,
        })

    return sorted(frequencies, key=operator.itemgetter('weight'), reverse=True)[0:5]


if __name__ == "__main__":
    titles = [
        'Senior Software Platform Engineer',
        'Sr. Network Engineer (Software & Systems)',
        'Software Engineer',
        'Senior Software Engineer/Architect',
        'Sr Essbase Software Engineer',
        'Senior RoR Software Engineer',
        'Software Development Engineer in Test',
        'Software Development Engineer for Cloud Player for Automotive',
        'the the the the the the the the the the',
    ]

    print repr(_get_token_freqdist(' '.join(titles)))

