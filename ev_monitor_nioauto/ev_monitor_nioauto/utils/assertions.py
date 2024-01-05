import difflib
import pprint
import re
import allure
import inspect

from utils.logger import logger
from utils.commonlib import show_json


def assert_equal(actual, expected):
    """
    Compare two objects. Must put two object in one line.
    It support int, str, list, dict type, but not support set type
    :param actual: actual result
    :param expected: expected result
    :return:
    """
    assert type(actual) is type(expected), "TypeError: type not same!"

    previous_frame = inspect.currentframe().f_back
    (filename, line_number,function_name, lines, index) = inspect.getframeinfo(previous_frame,context=2)
    if 'assert_equal' in lines[1]:
        func_with_param = lines[1].strip()
    else:
        func_with_param=''.join([x.strip() for x in lines])

    p1 = re.compile(r"assert_equal[(](.*)[)]", re.S)
    left, right = re.findall(p1, func_with_param)[0].split(',')

    logger.debug("{0} is\n {1}".format(left, show_json(actual)))
    logger.debug("{0} is\n {1}".format(right, show_json(expected)))
    allure.attach(show_json(actual),left)
    allure.attach(show_json(expected),right)


    try:
        assert actual == expected
    except AssertionError as e:
        # Here we try to make pycharm's 'click to see difference' works and also we want to display full diff
        explanation = []
        if isinstance(actual, int):
            actual = "\"\"" + f'(int {left})  {actual}' + "\"\""
            expected = "\"\"" + f'(int {right})  {expected}'  + "\"\""
            explanation.append("assert " + actual + " == "  + expected)
            explanation.append('Differing items:')
            explanation.append("\"\"" + actual + " != " +expected)

        elif isinstance(actual, str):
            actual = "\"\"" + f'(str {left})  {actual}' + "\"\""
            expected = "\"\"" + f'(str {right})  {expected}'  + "\"\""
            explanation.append("assert " + actual + " == " + expected)
            explanation.append('Differing items:')
            explanation.append("\"\"" + actual + " != " + expected)
        else:
            if isinstance(actual, dict):
                actual['__name__']=left
                expected['__name__']=right

            explanation.append("assert "+str(actual)+" == "+str(expected))
            explanation.append('Differing items:')
            explanation.append(str(actual)+" != "+str(expected))
            try:
                left_formatting = pprint.pformat(actual).splitlines()
                right_formatting = pprint.pformat(expected).splitlines()
                explanation.extend(['Full diff:'])
            except Exception:
                left_formatting = sorted(repr(x) for x in left)
                right_formatting = sorted(repr(x) for x in right)
                explanation = ['Full diff (fallback to calling repr on each item):']

            explanation.extend(line.strip() for line in difflib.ndiff(left_formatting, right_formatting))

        raise AssertionError('\n'.join(explanation))