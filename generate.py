import os
from strictyaml import load
from jinja2 import Template
import asyncio
from pyppeteer import launch
from PyPDF2 import PdfFileMerger
import mistune
from subprocess import call

output_html_filename = "portfolio.html"
output_html_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), output_html_filename
)


def date_sort(p):
    try:
        return int(p["year"])
    except Exception as e:
        print(e)
        return 0


async def render(data, outname="portfolio.pdf", compress="none"):
    tempname = outname + ".tmp1.pdf"
    tempname2 = outname + ".tmp2.pdf"

    print("saving pdf")
    browser = await launch()
    page = await browser.newPage()
    await page.goto("file://" + output_html_path)
    await page.pdf(path=tempname, printBackground=True, landscape=True)
    await browser.close()

    if compress == "none":
        tempname2 = tempname
    else:
        # from: https://www.digitalocean.com/community/tutorials/reduce-pdf-file-size-in-linux
        # options are screen, ebook, prepress, printer, default
        print("compressing")
        call(
            [
                "gs",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                f"-dPDFSETTINGS=/{compress}",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                f"-sOutputFile={tempname2}",
                tempname,
            ]
        )

    print("adding bookmarks")
    output = PdfFileMerger()
    output.append(tempname2)

    for project in data["projects"]:
        output.addBookmark(project["title"], int(project["start_page"]) - 1)

    with open(outname, "wb") as outfile:
        output.write(outfile)

    try:
        os.unlink(tempname)
        os.unlink(tempname2)
    except Exception as e:
        pass


def main(data, outname="portfolio.pdf", render_pdf=True, compress="none"):
    pid = 1

    start_page = 2

    data["projects"] = sorted(data["projects"], key=date_sort, reverse=True)

    total_images = sum([len(p.get("images", [])) for p in data["projects"]])
    print("total images:", total_images)

    for project in data["projects"]:
        project["id"] = pid
        project["description"] = mistune.html(project["description"])

        position = project.get("position", "1in auto auto 1in").split(" ")
        position = [x.strip() for x in position if x != ""]
        project["position"] = position

        size = project.get("size", "4in auto").split(" ")
        size = [x.strip() for x in size if x != ""]
        if len(size) == 1:
            size.append("auto")
        project["size"] = size

        for index, image in enumerate(project["images"]):
            if isinstance(image, str):
                src = image
                position = "center"
                image = {"src": src, "position": position}
                project["images"][index] = image

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
                    image = project["images"][image_index]
                    if isinstance(image, str):
                        src = image
                        position = "center"
                    else:
                        src = image.get("src")
                        position = image.get("position", "center")
                    page["images"].append({"src": src, "position": position, "name": i})
                    image_index += 1
                except Exception as e:
                    print(e)
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
        asyncio.get_event_loop().run_until_complete(
            render(data, outname=outname, compress=compress)
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Generate portfolio")

    parser.add_argument(
        "--render", "-r", default=False, action="store_true", help="Render PDF"
    )
    parser.add_argument(
        "--compress",
        "-c",
        default="none",
        choices=["screen", "ebook", "prepress", "printer", "default"],
        help="Compress PDF",
    )
    parser.add_argument("--input", "-i", default="data.yml", help="Input yaml file")
    parser.add_argument(
        "--output", "-o", default="portfolio.pdf", help="Output PDF file"
    )

    args = parser.parse_args()
    print(args)

    with open(args.input, "r") as infile:
        content = infile.read()
        data = load(content)

    data = dict(data.data)

    main(data, outname=args.output, render_pdf=args.render, compress=args.compress)
