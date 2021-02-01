"""A more liberal autolinker

Inspired by Django's urlize function.

Positive examples:

>>> import markdown
>>> md = markdown.Markdown(extensions=['urlize'])

>>> md.convert('http://example.com/')
'<p><a href="http://example.com/">http://example.com/</a></p>'

>>> md.convert('go to http://example.com')
'<p>go to <a href="http://example.com">http://example.com</a></p>'

>>> md.convert('example.com')
'<p><a href="http://example.com">example.com</a></p>'

>>> md.convert('example.net')
'<p><a href="http://example.net">example.net</a></p>'

>>> md.convert('www.example.us')
'<p><a href="http://www.example.us">www.example.us</a></p>'

>>> md.convert('(www.example.us/path/?name=val)')
'<p>(<a href="http://www.example.us/path/?name=val">www.example.us/path/?name=val</a>)</p>'

>>> md.convert('go to <http://example.com> now!')
'<p>go to <a href="http://example.com">http://example.com</a> now!</p>'

Negative examples:

>>> md.convert('del.icio.us')
'<p>del.icio.us</p>'

Modified by sumeet:

>>> md.convert('go to tinyurl.com/help')
'<p>go to <a href="http://tinyurl.com/help">tinyurl.com/help</a></p>'

"""

import markdown

# Global Vars
URLIZE_RE = '(%s)' % '|'.join([
    r'<(?:f|ht)tps?://[^>]*>',
    r'\b(?:f|ht)tps?://[^)<>\s]+[^.,)<>\s]',
    r'\bwww\.[^)<>\s]+[^.,)<>\s]',
    #OLD ONE (modified by sumeet) r'[^(<\s]+\.(?:com|net|org)\b',
    r'[^(<\s]+\.(?:com|net|org)[^)<>\s]*[^.,)<>\s]*\b',
])

class UrlizePattern(markdown.inlinepatterns.Pattern):
    """ Return a link Element given an autolink (`http://example/com`). """
    def handleMatch(self, m):
        url = m.group(2)
        
        if url.startswith('<'):
            url = url[1:-1]
            
        text = url
        
        if not url.split('://')[0] in ('http','https','ftp'):
            if '@' in url and not '/' in url:
                url = 'mailto:' + url
            else:
                url = 'http://' + url
    
        el = markdown.util.etree.Element("a")
        el.set('href', url)
        el.set('target', '_blank')
        el.text = markdown.util.AtomicString(text)
        return el

class UrlizeExtension(markdown.Extension):
    """ Urlize Extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Replace autolink with UrlizePattern """
        md.inlinePatterns['autolink'] = UrlizePattern(URLIZE_RE, md)

def makeExtension(*args, **kwargs):
    return UrlizeExtension(*args, **kwargs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
