#!/usr/bin/env python

import resume


def render_html():
    return f"""
<!doctype html>

<html>
    <head>
        <link rel="stylesheet" type="text/css" href="style.css">
        <script src="darkreader.js"></script>
        <script>
            function toggleDarkMode() {{
                const linkEl = document.getElementById("toggle");
                if (linkEl.dataset.mode == "dark") {{
                    DarkReader.disable();
                    linkEl.innerHTML = "Dark mode";
                    linkEl.dataset.mode = "light";
                }} else {{
                    DarkReader.enable({{brightness: 100, contrast: 95, sepia: 30}});
                    linkEl.dataset.mode = "dark";
                    linkEl.innerHTML = "Light mode";
                }}
                return false;
            }}
        </script>
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
                        <li><a id="toggle" data-mode="light" href="#" onclick="return toggleDarkMode();">Dark mode</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </body>
</html>
"""


if __name__ == '__main__':
    print(render_html())
