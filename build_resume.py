import resume
from page_template import asset_url, render_page


def render_html():
    extra_head = f'<script src="{asset_url("darkreader.js")}"></script>' + """
        <script>
            function toggleDarkMode() {
                const linkEl = document.getElementById("toggle");
                if (linkEl.dataset.mode == "dark") {
                    DarkReader.disable();
                    linkEl.innerHTML = "Dark mode";
                    linkEl.dataset.mode = "light";
                } else {
                    DarkReader.enable({brightness: 100, contrast: 95, sepia: 30});
                    linkEl.dataset.mode = "dark";
                    linkEl.innerHTML = "Light mode";
                }
                return false;
            }
        </script>
"""
    sidebar = """
        <div class="section">
            <h3>Other formats</h3>
            <ul>
                <li><a href="/sumeet.txt">Plain text</a></li>
                <li><a href="/sumeet.pdf">PDF</a></li>
                <li><a id="toggle" data-mode="light" href="#" onclick="return toggleDarkMode();">Dark mode</a></li>
            </ul>
        </div>
"""
    return render_page(
        resume.html(),
        title='Résumé — Sumeet Agarwal',
        active_page='resume',
        sidebar=sidebar,
        extra_head=extra_head,
    )
