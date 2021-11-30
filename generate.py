import os
from strictyaml import load
from jinja2 import Template
import asyncio
from pyppeteer import launch

with open("data.yaml", "r") as infile:
    content = infile.read()
    data = load(content)

data = data.data

pid = 1

start_page = 2

for project in data["projects"]:
    project["id"] = pid

    layouts = []

    if not project.get("layout"):
        areas = ["A" for i in project["images"]]
    else:
        areas = project["layout"].strip().split("\n\n")

    image_index = 0

    for area in areas:
        page = {
            "area": "\n".join([f"'{a}'" for a in area.split("\n")]),
            "cols": " ".join(["1fr" for a in area.split("\n")[0].split(" ")]),
            "rows": " ".join(["1fr" for a in area.split("\n")]),
            "images": [],
        }

        total_images = [i.strip() for i in list(dict.fromkeys(area))]
        total_images = [i for i in total_images if i != ""]

        for i in total_images:
            try:
                page["images"].append(
                    {"src": project["images"][image_index], "name": i}
                )
                image_index += 1
            except Exception as e:
                continue

        layouts.append(page)

    project["layouts"] = layouts
    project["start_page"] = start_page
    project["end_page"] = start_page + len(areas) - 1

    pid += 1
    start_page += len(areas)

with open("template.html", "r") as infile:
    template_html = infile.read()

template = Template(template_html)
output = template.render(**data)

output_html_filename = "portfolio.html"
output_html_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), output_html_filename
)

with open(output_html_filename, "w") as outfile:
    outfile.write(output)


async def main():
    print("launching")
    browser = await launch()
    print("new page")
    page = await browser.newPage()
    print("goto")
    await page.goto("file://" + output_html_path)
    print("save pdf")
    await page.pdf(path="portfolio.pdf", printBackground=True, landscape=True)
    print("close ")
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
