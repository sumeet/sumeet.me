from markdown import markdown

def html():
    return render_markdown(open('resume.md').read())


def render_markdown(md):
    return markdown(md, extensions=['smarty', 'mdx_urlize'])
