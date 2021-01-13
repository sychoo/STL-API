# Created by Simon Chu
# Thu Jan  7 13:30:13 EST 2021
# unit_test.py

import unittest
import stl.tool as tool
import subprocess
import os

stl_path = os.getenv("STLPATH")


class Test_Example_Files(unittest.TestCase):

    def test_signal(self):
        import stl.example.api.signal.main
        tool.print_success("SIGNAL TEST PASSED")

    def test_stl(self):
        import stl.example.api.stl.main
        tool.print_success("STL TEST PASSED")

    def test_lexer(self):
        subprocess.call(stl_path + "/stl/example/parsing/lex.sh")
        tool.print_success("LEXER TEST PASSED")

    def test_parser(self):
        subprocess.call(stl_path + "/stl/example/parsing/parse.sh")
        tool.print_success("PARSER TEST PASSED")



if __name__ == '__main__':
    unittest.main()