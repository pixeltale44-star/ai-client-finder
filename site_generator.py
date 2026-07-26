from jinja2 import Template
import os

template_html = """
<!DOCTYPE html>
<html>
<head><title>{{ name }} | Local Services</title></head>
<body>
<h1>Need Fast Service in {{ city }}?</h1>
<h2>Contact {{ name }}</h2>
<p>Call Us Today: {{ phone }}</p>
<a href="tel:{{ phone }}"><button>Call Now</button></a>
</body>
</html>
"""

def create_demo_site(lead):
    tmpl = Template(template_html)
    rendered = tmpl.render(name=lead['name'], city=lead['city'], phone=lead['phone'])

    os.makedirs("demos", exist_ok=True)
    safe_name = lead['name'].replace(' ', '_').replace('/', '-')
    filename = f"demos/{safe_name}.html"

    with open(filename, "w") as f:
        f.write(rendered)
    return filename
