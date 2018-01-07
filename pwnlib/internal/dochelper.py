#!/usr/bin/env python
# encoding:utf-8

import sys
from os.path import basename

from docutils import nodes
from docutils import statemachine
from sphinx.util.compat import Directive

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class ExecDirective(Directive):
    """
    执行指定的Python代码并将输出插入到文档中
    """
    has_content = True

    def run(self):
        old_stdout, sys.stdout = sys.stdout, StringIO()

        tab_width = self.options.get('tab-width', self.state.document.settings.tab_width)
        source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)

        try:
            exec('\n'.join(self.content), globals())
            text = sys.stdout.getvalue()
            lines = statemachine.string2lines(text, tab_width, convert_whitespace = True)
            self.state_machine.insert_input(lines, source)
            return []
        except Exception:
            return [nodes.error(None, nodes.paragraph(text = "Unable to execute python code at %s:%d:" % (basename(source), self.lineno)), nodes.paragraph(text = str(sys.exc_info()[1])))]
        finally:
            sys.stdout = old_stdout

def setup(app):
    app.add_directive('exec', ExecDirective)
