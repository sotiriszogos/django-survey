# -*- coding: utf-8 -*-


from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from future import standard_library

from survey.management.exporter.tex.question2tex import Question2Tex
from survey.tests.management.test_management import TestManagement

standard_library.install_aliases()
try:
    from _collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class TestQuestion2Tex(TestManagement):

    def test_get_chart(self):
        """ The header and order of the question is correct. """
        question = self.survey.questions.get(text="Aèbc?")
        self.assertIsNotNone(Question2Tex.chart(question))
        color = OrderedDict()
        group_together = {'1é': '1e, 1é, 1ë', '2é': '2e, 2é, 2ë',
                          '3é': '3e, 3é, 3ë', }
        color["1b"] = "green!80"
        color["1a"] = "cyan!50"
        color["1é"] = "red!80"
        self.assertRaises(ValueError, Question2Tex.chart, question,
                          color=color, group_together=group_together)
        color["1"] = "yellow!70"
        chart = Question2Tex.chart(question, color=color,
                                   group_together=group_together)
        expected_colors = "{red!80, yellow!70, cyan!50, green!80}"
        self.assertIn(expected_colors, chart)
        self.assertIn("""4/1é,
            1/1,
            1/1a,
            1/1b""", chart)

    def test_cloud_chart(self):
        """ We can create a cloud chart. """
        question = self.survey.questions.get(text="Aèbc?")
        self.assertIsNotNone(Question2Tex.chart(question, type="cloud"))

    def test_no_results(self):
        """ We manage having no result at all. """
        question = self.survey.questions.get(text="Dèef?")
        self.assertIn("No answers for this question.",
                      Question2Tex.chart(question))

    def test_html2latex(self):
        """ We correctly translate a question to the latex equivalent. """
        translation = Question2Tex.html2latex("&lt;filetype&gt; ?")
        self.assertEqual("<filetype> ?", translation)
        translation = Question2Tex.html2latex("Is <strong>42</strong> true ?")
        self.assertEqual("Is \\textbf{42} true ?", translation)
        translation = Question2Tex.html2latex("<code>is(this).sparta</code>?")
        self.assertEqual("$is(this).sparta$?", translation)