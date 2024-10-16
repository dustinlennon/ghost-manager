from nbconvert.preprocessors import ExtractOutputPreprocessor
from traitlets import Unicode
import hashlib
import os

class OutputMd5Preprocessor(ExtractOutputPreprocessor):

  prefix = Unicode("").tag(config=True)

  def preprocess_cell(self, cell, resources, cell_index):

    cell, resources = super().preprocess_cell(cell, resources, cell_index)

    # Loop through all of the outputs in the cell
    for index, out in enumerate(cell.get("outputs", [])):
      for mime_type in self.extract_output_types:
          if mime_type in out.data:
            filename = out.metadata["filenames"][mime_type]
            data = resources["outputs"][filename]
            resources["outputs"].pop(filename, None)

            # print(f"old filename: {filename}")

            _, file_extension = os.path.splitext(filename)
            dirname = os.path.dirname(filename)
            md5 = hashlib.md5(data).hexdigest()

            filename = os.path.join(dirname, md5 + file_extension)
            # print(f"new filename: {filename}")

            resources["outputs"][filename] = data

            if self.prefix:
              filename = "/".join([self.prefix, filename])

            out.metadata["filenames"][mime_type] = filename

            
    return cell, resources
