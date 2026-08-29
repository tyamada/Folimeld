import unittest
from pathlib import Path

from pdfutility.windows_integration import open_command


class WindowsIntegrationTests(unittest.TestCase):
    def test_open_command_quotes_executable_and_pdf_path(self):
        executable = str(Path("folder with spaces") / "PDFUtility.exe")

        command = open_command(executable)

        self.assertTrue(command.endswith('PDFUtility.exe" "%1"'))
        self.assertTrue(command.startswith('"'))


if __name__ == "__main__":
    unittest.main()
