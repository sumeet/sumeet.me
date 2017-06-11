#!/usr/bin/env python

import resume


def render_html():
    return f"""
<!doctype html>

<html>
    <head>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body class="home">
        <div id="container">
            <div id="content">
                {resume.html()}
            </div>

            <div id="sidebar">
                <div class="section">
                    <h3>Other formats</h3>
                    <ul>
                        <li><a href="sumeet.txt">Plain text</a></li>
                        <li><a href="sumeet.pdf">PDF</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </body>
</html>
"""


if __name__ == '__main__':
    print(render_html())
