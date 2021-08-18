from typing import Any, List, Optional


def make_table(rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False):
    global label, label_ascii, labels_string_convert
    hyphen = '─'
    char1 = "┬"
    char2 = "┴"
    char3 = "┼"

    string_convert = [[str(value) for value in row] for row in rows]
    if labels:
        labels_string_convert = [str(value) for value in labels]
        string_convert.insert(0, labels_string_convert)
    zipping = zip(*string_convert)
    higher_string = [max(map(len, col)) for col in zipping]
    if labels:
        string_convert.remove(labels_string_convert)
    if centered:
        space = " │ ".join(f'{{: ^{x}}}' for x in higher_string)

    else:
        space = ' │ '.join('{{:{}}}'.format(x) for x in higher_string)

    formatting = [space.format(*row) for row in string_convert]

    formatted_string = f"│ {formatting[0]} │"
    index_of_line = [i for i in range(len(formatted_string)) if formatted_string.startswith('│', i)]

    index_of_line.pop(0)
    index_of_line.pop(len(index_of_line) - 1)

    length_line_list = list((len(formatting[0]) + 2) * hyphen)
    for i in index_of_line:
        length_line_list[i - 1] = char1
    new = ''.join(length_line_list)
    if not labels:
        first_line = f"┌{new}┐"
    else:
        first_line = f"┌{new}┐"
        label_string_convert = [str(value) for value in labels]
        label_formatting_list = [space.format(*label_string_convert)]
        label_formatting = ''.join(label_formatting_list)
        label = f"│ {label_formatting} │"
        for i in index_of_line:
            length_line_list[i - 1] = char3
        var = ''.join(length_line_list)
        label_ascii = f"├{var}┤"

    rows_list = []
    for i in formatting:
        row_ascii = f"│ {i} │"
        rows_list.append(row_ascii)
    rows_join = "\n".join(rows_list)
    for i in index_of_line:
        length_line_list[i - 1] = char2
    new2 = ''.join(length_line_list)
    last_line = f"└{new2}┘"

    if labels:
        final_list = [first_line, label, label_ascii, rows_join, last_line]
        table = '\n'.join(final_list)
        return table
    else:
        final_list = [first_line, rows_join, last_line]
        table = '\n'.join(final_list)
        return table
