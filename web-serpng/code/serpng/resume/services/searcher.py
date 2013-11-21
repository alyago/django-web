from datetime import date
import re
import logging
import math

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

SAVEWORDS = ['part-time', 'full-time', 'c++', 'c#', '.net', 'A/P', 'A&P', 'pl/sql','asp.net','vb.net','a+','a#','r.n.','r.n','c#.net','microsoft.net','ms.net','ado.net','r&d','i&e','c.n.a','c.n.a.','c.o.t.a','c.o.t.a.','3-d']

logger = logging.getLogger('resume')

class Searcher:
    """
    Returns a url-escaped query term.
    This query term can be appended to 'http://www.simplyhired.com/a/jobs/list/q-'
    """
    @staticmethod
    def construct_search_query(resume) :

        #Initiate Dictionaries
        dictTitle = {}
        dictYears = {}
        dictRecency = {}
        dictLocation = {}
        index = 1
        career_duration = 0.0
        average_job_duration = 4.0
        
        contact_city = ""
        contact_state = ""
        has_contact_location = False
        if resume.contact != None and resume.contact.address != None:
            if resume.contact.address.city != None:
                has_contact_location = True
                contact_city = resume.contact.address.city
            if resume.contact.address.state != None:
                has_contact_location = True
                contact_state = resume.contact.address.state

        for job in resume.job_set.select_related():

            job_title = job.title
            if job_title == None:
                continue

            city = ""
            state = ""
            if has_contact_location == True:
                city = contact_city
                state = contact_state
            else:
                if job.city != None:
                    city = job.city
                if job.state != None:
                    state = job.state
                            
            if job.end_date == None:
                end_date = date.today()
            else:
                end_date = job.end_date

            if job.start_date == None:
                start_date = date.today()
            else:
                start_date = job.start_date

            # Compute duration of job on resume
            days_at_job = (end_date - start_date).days
            career_duration += days_at_job
            if (days_at_job <= 0):
                days_at_job = 1
            delta = days_at_job/float(365)

            # Add required data to dictionary
            dictTitle[index] = job_title
            dictYears[index]= delta
            dictRecency[index] = end_date

            if city and state:
                dictLocation[index] = city+","+state
            elif city and not state:
                dictLocation[index] = city
            elif not city and state:
                dictLocation[index] = state
            else:
                dictLocation[index] = " "

            index = index + 1

        sorted_job_indexes = sorted(dictRecency.items(), lambda x, y: cmp(x[1], y[1]))

        job_count = len(sorted_job_indexes)
        career_duration = career_duration/float(365)
        logger.debug("Career_Duration is %s " % (career_duration))    
        if career_duration < average_job_duration:
                recency = int(len(sorted_job_indexes))
                logger.debug ("If your career is less than average %s" % (recency))
        #elif career_duration >= (2*average_job_duration):
         #       recency = int(math.ceil((career_duration/float(average_job_duration)) + 1))
          #      logger.debug ("If your career is 2x than average %s" % (recency))
        else:
                recency = int(math.ceil(0.75*(len(sorted_job_indexes))))
                logger.debug ("If your career is in middle %s" % (recency))
            
        if recency > job_count:
            recency = job_count
            
        keep_jobs = job_count - recency
        logger.debug ("Jobs to keep is %s" % (keep_jobs))
        location = ""
        query = ""
        old_f=0
        
        for index,item in sorted_job_indexes[keep_jobs:]:
            f = "%0.4f" % ( (((job_count - recency) +1 ) / float(job_count)) * dictYears[index] )
            if f <= 0:
                f = 0.0001    
            # store max of s_f to ensure a boost to most recent job on resume
            if f > old_f:
                old_f = f
                
            #title_words = re.sub('[^A-Za-z0-9]+', ' ', dictTitle[index])
            #title_words = title_words.split()    
            #title_words = [w for w in title_words if not w in STOPWORDS]
            
            dictTitle[index] =  dictTitle[index].lower()
            title_words = dictTitle[index].split()
           
            clean_title = []
            for w in title_words:
                w=w.strip()
                if w:
                    if w in STOPWORDS:
                        continue
                    if w in SAVEWORDS:
                        clean_title.append(w)
                    else:
                        w = re.sub('[^A-Za-z0-9]', ' ',w)
                        w=w.strip()
                        if w:
                            clean_title.append(w)
                else:
                    continue
            title_words = clean_title
            
            if len(title_words)!=0:
                #title_words = title_words.split(" ")    
                if recency > 1:
                    query = query + "("
                    for w in title_words:
                        #if w in dictLadder.keys():
                         #   m =  int(n/dictLadder[w])
                          #  n_f = float(f) + float(pow(dictLadder[w],m ))
                        #else:
                        n_f = '%0.4f' % float(f)
                        logger.debug("Assigning weighting to search query term %s as %s" % (w, n_f))
                        query = query + w +"^" + str(n_f) + " "
                        #if w.lower() != "and" and w.lower() != "or" :
                         #       query = query + w +"^" + str(f) + " "
                    query = query.strip() + ") OR "
                            
                else :
                    if str(f) == str(old_f):
                        f = float(f)
                    else:
                        f = float(f) + float(old_f)
                    f = pow(f,2.5)
                    if f < 0.0001:
                        f = 0.0001
                    query = query + "("
                    for w in title_words:
                        #if w in dictLadder.keys():
                         #   m =  int(n/dictLadder[w])
                          #  n_f = float(f) + float(pow(dictLadder[w],m ))
                        #else:
                        n_f = '%0.4f' % float(f)
                        logger.debug("Assigning weighting to search query term %s as %s" % (w, n_f))
                        query = query + w +"^" + str(n_f) + " "
                    query = query.rstrip() + ")"
                if resume.source != 'Linkedin':
                    location = dictLocation[index]
                        
            recency -= 1

        if query.endswith(" OR "):
            query = query[:-4]
        query = "q-" + query
        if not location.strip() == "":
            query = query + "/l-" + location
        return query
        #return urllib.quote(query)+"/l-" + urllib.quote(location) + "/pn-2"
        #return query+"/l-" + location + "/pn-2"
