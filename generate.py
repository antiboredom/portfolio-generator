import sys
import os
from strictyaml import load
from jinja2 import Template
import asyncio
from pyppeteer import launch
from PyPDF2 import PdfFileMerger
import mistune

output_html_filename = "portfolio.html"
output_html_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), output_html_filename
)

with open("data.yaml", "r") as infile:
    content = infile.read()
    data = load(content)

data = dict(data.data)


async def render(outname="portfolio.pdf"):
    tempname = outname + ".tmp.pdf"

    print("saving pdf")
    browser = await launch()
    page = await browser.newPage()
    await page.goto("file://" + output_html_path)
    await page.pdf(path=tempname, printBackground=True, landscape=True)
    await browser.close()

    print("adding bookmarks")

    output = PdfFileMerger()
    output.append(tempname)

    for project in data["projects"]:
        output.addBookmark(project["title"], int(project["start_page"]) - 1)

    with open(outname, "wb") as outfile:
        output.write(outfile)

    os.unlink(tempname)


def main(render_pdf=True):

    pid = 1

    start_page = 2

    for project in data["projects"]:
        project["id"] = pid
        project["description"] = mistune.html(project["description"])

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

    with open(output_html_filename, "w") as outfile:
        outfile.write(output)

    if render_pdf:
        asyncio.get_event_loop().run_until_complete(render())


if __name__ == "__main__":
    try:
        render_pdf = sys.argv[1] == "render"
    except Exception as e:
        render_pdf = False

    main(render_pdf=render_pdf)
