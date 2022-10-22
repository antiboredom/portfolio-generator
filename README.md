# Portfolio Generator

This tool generates a PDF portfolio by reading configuration from a `yml` file. I use it for myself, but making it open in case it's helpful for others (I hate making portfolios with InDesign).

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
    material: website
    commissioned: rhizome
    images:
      - images/one.jpg
      - images/two.jpg
    description: >
      The description of your project goes here.

  - title: Another project title
    url: https://website.com
    year: 2020
    description: A short description
    text_width: 500px
    text_height: 300px
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

- **title**: the project title
- **url**: project url (optional)
- **material**: material or materials (optional)
- **year**: project year
- **commissioned**: a commissioning organization (optional)
- **images**: a list of images to include. Use relative paths
- **description**: a description of the project. Can be multi-line, and can include markdown.
- **text_width**: the width of the description text box (optional)
- **text_height**: the height of the description text box (optional)
- **layout**: an optional description of how images should be arranged in a grid. 

