# Portfolio Generator

This tool generates a PDF portfolio by reading configuration from a `yml` file. I use it for myself, but making it open in case it's helpful for others (I hate making portfolios with InDesign).

See [portfolio_sample.pdf](https://github.com/antiboredom/portfolio-generator/blob/main/portfolio_sample.pdf) for an example output.

## Installation

You'll need Python installed, and then to install the requirements:

```
pip install -r requirements.txt
```

## Usage

To use, modify `data.yml`. And then run:

```
python generate.py
```

The script will create an html file, that you can preview by opening in any web browser.

To convert this to a PDF you can run:

```
python generate.py render
```

Please note that the script will not optimize images by default! If the PDF is too large, you can either optimize the images yourself, or if you have ghostscript installed run:

```
python generate.py render [COMPRESSION]
```

(where [COMPRESSION] is either: screen, ebook, prepress, or printer)

To modify font, colors and so on, just edit `style.css`.

If you have [nodemon](https://www.npmjs.com/package/nodemon) installed you can also run `run.sh` which will automatically re-generate your html portfolio when you change any of the files.

## Data format

The script will read from `data.yml` to generate your portfolio.

Here's an example file to get you started.

```yml
title: Sam Lavigne
website: https://lav.io

projects:
  - title: A project title
    url: https://website.com
    year: 2020
    material: Website, prints
    images:
      - images/one.jpg
      - images/two.jpg
      - src: images/three.jpg
        position: top left
    description: |
      The description of your project goes here.

      Multilines are ok and so is *markdown*.

  - title: Another project title
    url: https://website.com
    year: 2020
    description: A short description
    position: 1in 2in auto auto
    size: 5in 2in
    images:
      - images/three.jpg
      - images/four.jpg
      - images/five.jpg
      - images/six.jpg
      - images/seven.jpg
    layout: |
      A A A
      B B C

      D E
```

### Special fields

**title**: the title of your portfolio

**website**: your personal website

**projects**: an list of projects where individual projects contain:

- **title**: The project title
- **url**: Project url (optional)
- **material**: Material or materials (optional)
- **year**: Project year
- **images**: A list of images to include. Uses relative paths
- **description**: A description of the project. Can be multi-line, and can include markdown.
- **size**: Width and height of the text description box, separated by spaces, in css units. Height is optional.
- **position**: The absolute position of the description box, in css units, using [top right bottom left]
- **layout**: an optional description of how images should be arranged in a grid. Uses the same syntax as [css grid-template-areas](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-template-areas)
