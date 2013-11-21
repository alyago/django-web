from jobs_app_test_common import *

# Set test case name
name = 'head_myresume'

# Construct the query
query = Query(request_query='/jobs/q-myresume',
              request_cookies={
                'sh_uid': 'id%3A16632395250132bb24fb7f6.91770409',
                'sh_www': 'id%3A8474675%2Crv%3A1781743266%2Ccid%3A646608595016c40fb6fc23.51732734',
                'sh3': 'id%3D20225828394f62a874cbeb43.64750830%3Brv%3D5321c788%3Bcv%3D2',
                'sh2': 'db%3D725672%3Bcso%3D50171cc8%3Bslu%3D5017188c%3Bref%3Dsh',
                'sh4': 't%3D50171cc9%3Bh%3D00ed904d326617dc29c19a6846049c83c64ae67b%3Bun%3Dyipingliao%40gmail.com',
                'shua': 'uajobssearched%3D1343691981%2Cuafbp%3D8%2Cuafilters%3D1%3Afex-1%2Cuaresumequery%3DAlpJAw8NLABzZGZ2AwMFDSQZAhoBCAABKVFeXVF8Qw0nPyxHVV1ELxA7Q0FeVUZHQR4LFT4cXz8WdR0FBRhxVxUBAA4AAAQIHgk%2FeV0eZH11GhZ6f2FfBAcbAhcdEhguXk9%2FRRplYWV8ZBUFMRYRFgEZO0JZUEdeWWkSWSAnN11TTHNwWVREX1VMUzgzUEYRKAdIOjwbAxgGGXVARRIbGQoBGQQJMFFnQBlgf2wTeWcNaRYWAAAODBIDBC5cT35FG2doNlxQQVogBQAtXUNSRUFSUAsPLhpDMS03bQQbGndBVlo%253D; shup=fvt%3D50132bb2%26ncs%3D61%26lst%3D50171cce',
                'sh_sess': 'id%3A1343690332%2Csrc%3Aself%2Ccmx%3A1'
              })


# Construct the bridge response
file_name=get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class HeadMyResumeTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        head_tag = soup.find('head')

        # Title should contain "myresume"
        title_tag = head_tag.find('title')
        if "myresume" in title_tag.contents[0]:
            pass
        else:
            self.messages.append('Title tag in <head> is incorrect')

        # Meta description should contain "myresume"
        meta_description_tag = head_tag.find('meta', {'name': 'description'})
        if "myresume" in meta_description_tag['content']:
            pass
        else:
            self.messages.append('Meta tag (description) in <head> is incorrect')  

        # Meta keywords should contain "myresume"
        meta_keywords_tag = head_tag.find('meta', {'name': 'keywords'})
        if "myresume" in meta_keywords_tag['content']:
            pass
        else:
            self.messages.append('Meta tag (keywords) in <head> is incorrect')  

        # rel-canonical should be '/a/jobs/list/q-myresume'
        rel_canonical_tag = head_tag.find('link', {'rel': 'canonical'})
        if rel_canonical_tag['href'] == 'http://testserver/a/jobs/list/q-myresume':
            pass
        else:
            self.messages.append('rel-canonical link in <head> is incorrect for MyResume query')  



test = HeadMyResumeTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)
