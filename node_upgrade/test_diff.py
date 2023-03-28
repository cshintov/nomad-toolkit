""" Tests for the diff module. """

from diff import *

def test_find_diff():
    # Test case with no differences
    old_data = {"foo": "bar", "baz": 1}
    new_data = {"foo": "bar", "baz": 1}
    diff = find_diff(old_data, new_data)
    assert diff == {}

    # Test case with a single difference at the root level
    old_data = {"foo": "bar", "baz": 1}
    new_data = {"foo": "bax", "baz": 1}
    diff = find_diff(old_data, new_data)
    assert diff == {
        "root['foo']": {
            "old_value": "bar",
            "new_value": "bax"
        }
    }

    # Test case with a single difference at a nested level
    old_data = {"foo": {"bar": 1, "baz": 2}}
    new_data = {"foo": {"bar": 1, "baz": 3}}
    diff = find_diff(old_data, new_data)
    assert diff == {
        "root['foo']['baz']": {
            "old_value": 2,
            "new_value": 3
        }
    }

    # Test case with multiple differences at different levels
    old_data = {"foo": "bar", "baz": {"qux": 1, "quux": 2}}
    new_data = {"foo": "bax", "baz": {"qux": 2, "quux": 3}}
    diff = find_diff(old_data, new_data)
    assert diff == {
        "root['foo']": {
            "old_value": "bar",
            "new_value": "bax"
        },
        "root['baz']['qux']": {
            "old_value": 1,
            "new_value": 2
        },
        "root['baz']['quux']": {
            "old_value": 2,
            "new_value": 3
        }
    }

    old_data = {"foo": "bar", "baz": 1, "c": {"d": 1, "e": 2}}
    new_data = {"foo": "bax", "baz": 2, "c": {"d": 1, "e": 3}}
    diff = find_diff(old_data, new_data)
    assert diff == {
        "root['foo']": {
            "old_value": "bar",
            "new_value": "bax"
        },
        "root['baz']": {
            "old_value": 1,
            "new_value": 2
        },
        "root['c']['e']": {
            "old_value": 2,
            "new_value": 3
        }
    }

def test_format_diff_no_diff():
    # Test case with no differences
    diff = {}
    output = format_diff(diff)
    expected_output = ''
    assert output == expected_output

def test_format_diff_single_diff_at_root():
    # Test case with a single difference at the root level
    diff = {
        "root['foo']": {
            "old_value": "bar",
            "new_value": "bax"
        }
    }
    output = format_diff(diff)
    expected_output = (
        '[bold]root[\'foo\'][/]\n'
        '[red]  --- old[/]\n'
        '[green]  +++ new[/]\n'
        '[blue]  @@ -1 +1 @@[/]\n'
        '[red]  -bar[/]\n'
        '[green]  +bax[/]\n'
    )
    assert output == expected_output

def test_format_diff_single_diff_nested():
    # Test case with a single difference at a nested level
    diff = {
        "root['foo']['baz']": {
            "old_value": 2,
            "new_value": 3
        }
    }
    output = format_diff(diff)
    expected_output = (
        '[bold]root[\'foo\'][\'baz\'][/]\n'
        '[red]  --- old[/]\n'
        '[green]  +++ new[/]\n'
        '[blue]  @@ -1 +1 @@[/]\n'
        '[red]  -2[/]\n'
        '[green]  +3[/]\n'
    )
    assert output == expected_output

def test_format_diff_multiple_diff_nested():
    # Test case with multiple differences at different levels
    diff = {
        "root['foo']": {
            "old_value": "bar",
            "new_value": "bax"
        },
        "root['baz']['qux']": {
            "old_value": 1,
            "new_value": 2
        },
        "root['baz']['quux']": {
            "old_value": 2,
            "new_value": 3
        }
    }
    output = format_diff(diff)
    expected_output = (
        '[bold]root[\'foo\'][/]\n'
        '[red]  --- old[/]\n'
        '[green]  +++ new[/]\n'
        '[blue]  @@ -1 +1 @@[/]\n'
        '[red]  -bar[/]\n'
        '[green]  +bax[/]\n'
        '[bold]root[\'baz\'][\'qux\'][/]\n'
        '[red]  --- old[/]\n'
        '[green]  +++ new[/]\n'
        '[blue]  @@ -1 +1 @@[/]\n'
        '[red]  -1[/]\n'
        '[green]  +2[/]\n'
        '[bold]root[\'baz\'][\'quux\'][/]\n'
        '[red]  --- old[/]\n'
        '[green]  +++ new[/]\n'
        '[blue]  @@ -1 +1 @@[/]\n'
        '[red]  -2[/]\n'
        '[green]  +3[/]\n'
    )
    assert output == expected_output

