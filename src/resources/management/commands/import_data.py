from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import urllib
import pprint
from django.utils import simplejson as json
from django.template.defaultfilters import slugify

from resources.models import Resource, Tag
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = '<url>'
    help = 'Imports resource data from a given url'

    option_list = BaseCommand.option_list + (
        make_option('--schema',
            action='store',
            type='string',
            dest='schema',
            default='auto',
            help='Specify schema for parsing the data (default="auto").'),
        make_option('--user',
            action='store',
            type='string',
            dest='user',
            default='admin',
            help='Specify user to be used as creator of resources and tags.'),
        )

    def handle(self, *args, **options):
        
        user = User.objects.get(username=options['user'])
        
        for url in args:
            data = json.loads(urllib.urlopen(url).read())
            
            for res_data in data:
                try:
                    id = int(res_data['id'])
                    print 'loading details for id %s...' % id
                    res_detail = json.loads(urllib.urlopen('http://www.kmfn.de/rnf/sbrequest.php?action=getLocationData&id=%s' % id).read())
                    res_data['products'] = res_detail['locationProducts']
                    res_data['services'] = res_detail['locationServices']
                    
                    #pprint.pprint(res_data)
                    
                except Exception, ex:
                    print ex
                    return
                
            #pprint.pprint(data)

            prefix = 'kmfn.de'
            mappings = [
                ('description', 'description'),
                ('website', 'url'),
                ('mailto', 'email'),
                ('location', lambda data: 'lonlat:%(longitude)s,%(latitude)s' % data ),
            ]
            
            for res_data in data:
                try:
                    res = Resource(creator=user)
                    res.name = _replace_entities(res_data['name'])
                    res.shortname = 'hessen-%s' % slugify(res.name)
                    res.save()
                    
                    tag = Tag(key='source', value='http://www.kmfn.de/rnf/', resource=res, creator=user)
                    tag.save()
                    
                    # map all entries to tags with prefix
                    for key, value in res_data.items():
                        # ignore empty values
                        if value:
                            if type(value) is list:
                                for item in value:
                                    try:
                                        tag = Tag(key='%s:%s' % (prefix, key), value=_replace_entities(item['name']), resource=res, creator=user)
                                        tag.save()
                                    except Exception, ex:
                                        print ex
                            else:
                                try:
                                    tag = Tag(key='%s:%s' % (prefix, key), value=_replace_entities(value), resource=res, creator=user)
                                    tag.save()
                                except Exception, ex:
                                    print ex
                                            
                    
                    # map specific tags defined in mappings
                    for mapping in mappings:
                        if type(mapping[1]) is str:
                            # is key present and value not None or empty?
                            if mapping[1] in res_data and res_data[mapping[1]]:
                                tag = Tag(key=mapping[0], value=_replace_entities(res_data[mapping[1]]), resource=res, creator=user)
                                tag.save()
                        if callable(mapping[1]):
                            try:
                                value = mapping[1](res_data)
                                tag = Tag(key=mapping[0], value=value, resource=res, creator=user)
                                tag.save()
                            except Exception, ex:
                                # ignore exceptions
                                print ex
                except Exception, ex:
                    print 'Exception importing Resource:'
                    pprint.pprint(res_data)
                    print ex            
                #pprint.pprint(res)
            
            #self.stdout.write('Successfully imported data from %s\n' % url)

import re, htmlentitydefs

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def _replace_entities(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)