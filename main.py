import json
import logging
import time
from pathlib import Path

from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

_log = logging.getLogger("docling_demo")


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # -------- Input: use URL instead of local file --------
    input_doc_url = "https://arxiv.org/pdf/2509.02590"

    # Example: Docling Parse with EasyOCR + acceleration
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True
    pipeline_options.ocr_options.lang = ["en"]
    pipeline_options.do_picture_classification = True
    pipeline_options.do_code_enrichment = True
    pipeline_options.accelerator_options = AcceleratorOptions(
        num_threads=4, device=AcceleratorDevice.AUTO
    )

    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    # -------- Conversion --------
    _log.info(f"Converting {input_doc_url} ...")
    start_time = time.time()
    conv_result = doc_converter.convert(input_doc_url)
    duration = time.time() - start_time
    _log.info(f"Document converted in {duration:.2f} seconds.")

    # -------- Export Results --------
    output_dir = Path("scratch")
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_filename = conv_result.input.file.stem or "converted_doc"

    exports = {
        "txt": conv_result.document.export_to_text(),
    }

    for ext, content in exports.items():
        out_path = output_dir / f"{doc_filename}.{ext}"
        with out_path.open("w", encoding="utf-8") as f:
            f.write(content)
        _log.info(f"Exported {ext.upper()} → {out_path}")


if __name__ == "__main__":
    main()
