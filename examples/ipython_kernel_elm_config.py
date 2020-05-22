import os.path
import tempfile
import logging

#import ar2eng
import csv
import re

c = get_config()    # noqa - defined by traitlets

from elm_kernel.filters import BaseFilter

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
arWords = []
enWords = []
with open('/etc/ipython/ipython-elm-kernel/examples/enSorted.csv', newline='') as csvfile:
    words = csv.reader(csvfile, delimiter=',')
    for word in words:  # 0,1 = en > ar
        enWords.append(word[1])
        arWords.append(word[0])

qoute_regex_original = r'(\'.*?(?<!\\)\')|(".*?(?<!\\)")'
qoute_regex = re.compile(qoute_regex_original)

delms = ["(", ")", " ", ":", "\"", "'", "=", "+", "-", "!", "&",
         "^", "*", "[", "]", ";", ".", ",", "/", "<", ">"]
temp_str = "(" + '|'.join(map(re.escape, delms)) + ")"
delms_regex = re.compile(temp_str)


def transpile(lines):
    """
    Takes a list of code lines, and returns a list of transpiled lines.
    The current implementation concats multi-line statements,
    and could potentially translate comments
    """
    # Concats lines ending with "\" to split on quotes properly
    multiline_code = ""
    for line in lines:
        multiline_code += line
    no_multiline_code = re.sub(r'\\\n', '', multiline_code)
    no_multiline_code = no_multiline_code.split("\n")

    transpiled_code = []
    for line in no_multiline_code:
        # Separate code and string literals
        phrases = re.split(qoute_regex, line)
        for i in range(phrases.count(None)):
            phrases.remove(None)
        for i in range(phrases.count("")):
            phrases.remove("")

        for j, phrase in enumerate(phrases):
            if (phrase[0] == "'") | (phrase[0] == '"'):
                continue
            else:
                # for every code phrase, split words and try to translate them
                words = re.split(delms_regex, phrase)
                for x in range(len(words)):
                    for i in range(len(enWords)):
                        if words[x] == enWords[i]:
                            words[x] = arWords[i]
                phrase = ''.join(words)
                phrases[j] = phrase
        line = ''.join(phrases)
        transpiled_code.append(line + "\n")
    return(transpiled_code)


class SampleFilter(BaseFilter):
    def register(self, kernel, shell):
        super().register(kernel, shell)

        ident = kernel.ident

        logfile = os.path.join(tempfile.gettempdir(),
                               'elm-kernel-{}.log'.format(ident))

        logger = self.logger = logging.getLogger('elm-kernel-{}'.format(ident))
        fh = self.fh = logging.FileHandler(logfile)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.setLevel(logging.INFO)
        logger.info('STARTED ELM SESSION {}'.format(ident))

        kernel.log.info("FILTER REGISTERED for elm-kernel {}".format(ident))
        kernel.log.info("LOGGING USER INTERACTIONS TO {}".format(logfile))

    def process_text_output(self, text):
        self.logger.info('OUTPUT FROM SHELL: {}'.format(text))
        return

    def process_text_input(self, lines):
        ## self.logger.info('LINE INPUT FROM USER: {}'.format(repr(line)))
        ## self.logger.info('LINE INPUT FROM USER: "' + word[0] + '" found, replacing with" ' + word[1])
        output = transpile(lines)
        return(output)

    # Simple exclusion from command history, try for example:
    # In [1]: print('something to exclude... no-history')
    def process_run_cell(self, code, options):
        if 'no-history' in code:
            options['store_history'] = False
            self.logger.info(
                'RUN CODE, excluded from command history: {}'.format(repr(code)))
        return code

    def process_completion(self, code, cursor_pos, completion_data):
        self.logger.info('COMPLETION REQUESTED FOR: {}'.format(repr(code)))
        self.logger.info('COMPLETION RESULTS: {}'.format(
            completion_data['matches']))
        completion_data['matches'].insert(0, 'some-new-suggestion')
        return completion_data

    def post_run_cell(self, result):
        """
        This is called after executing a cell with the result of that
        """
        self.logger.info('CELL EXECUTION RESULT: {}'.format(repr(result)))
        self.logger.info(
            'CELL EXECUTION EXPRESSION RESULT : {}'.format(repr(result.result)))
        self.logger.info('CELL EXECUTION EXPRESSION OUTPUT: {}'.format(
            repr(self.shell.displayhook.exec_result)))


sample_filter = SampleFilter()

# Set to info or greater to see the logs on the Jupyter console
c.ElmKernelApp.log_level = 'INFO'

c.ElmIPythonKernel.code_filters = [sample_filter]
