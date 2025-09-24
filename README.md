# JSON to PDF

A simple Python tool that reads structured JSON folders, generates formatted content and index PDFs, and merges everything into a single navigable PDF file.

Originally built to process archived data and transform it into a clean, readable document.

## Features

- Reads multiple JSON files organized by folders
- Generates a **Content PDF** with formatted sections
- Generates an **Index PDF** with clickable links
- Merges all parts into one final PDF with bookmarks
- Uses [FPDF2](https://py-pdf.github.io/fpdf2/) and [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)

## Requirements

- Python 3.9 or higher

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

1. Place your `.json` data inside the folder defined in `config/config.json` (default is `data/`)
2. Run the scripts in this order:

```bash
python scripts/generate_content_pdf.py
python scripts/generate_index_pdf.py
python scripts/merge_pdfs.py
```

3. The final merged PDF will appear inside the `output/` folder

## Project structure

```
json-to-pdf/
├── main_dragdrop_runner.py
├── config/
│   └── config.json
├── scripts/
│   ├── generate_content_pdf.py
│   ├── generate_index_pdf.py
│   └── merge_pdfs.py
├── assets/           # optional images or logos
├── fonts/            # put Noto fonts here (not uploaded to GitHub)
├── output/           # generated PDFs (auto-created)
├── logs/             # error logs (auto-created)
└── requirements.txt
```

## Configuration

Settings are defined in `config/config.json`. Example:

```json
{
  "base_folder": "data",
  "font_bold": "fonts/NotoSans-Bold.ttf",
  "font_regular": "fonts/NotoSans-Regular.ttf",
  "font_emoji": "fonts/NotoEmoji-Regular.ttf",
  "output_pdf": "output/Consolidated_JSON_Data.pdf",
  "logo_path": "assets/logo.png"
}
```

## Fonts

To keep the repository lightweight, fonts are not included.

Download the following fonts and place them inside the `fonts/` folder:
- [Noto Sans](https://fonts.google.com/noto/specimen/Noto+Sans)
- [Noto Emoji](https://fonts.google.com/noto/specimen/Noto+Emoji)

You only need the `.ttf` files (e.g. `NotoSans-Regular.ttf`, `NotoSans-Bold.ttf`).

## License

MIT License. See the `LICENSE` file for details.
