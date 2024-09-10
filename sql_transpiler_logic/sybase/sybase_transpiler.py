import re


def remove_square_bracket_for_sybase_alias_columns(text):
    # Define the pattern to match 'as' or 'AS' followed by one or more spaces and '[\w+],'
    pattern = r'(as|AS)\s+\[\w+\],'

    # Use a callback function to remove the brackets
    def replace_brackets(match):
        matched_text = match.group(0)
        # Find the bracketed part and remove the brackets
        replaced_text = re.sub(r"\[(\w+)\]", r'\1', matched_text)
        return replaced_text

    # Substitute the pattern in the text using the replace_brackets function
    result = re.sub(pattern, replace_brackets, text)
    return result


def sybase_formatting_logic(_text):
    _u_text = remove_square_bracket_for_sybase_alias_columns(_text)
    return _u_text


# Example usage
# text = "Some text with as [example], and another AS [sample],."
# updated_text = remove_square_bracket_for_sybase_alias_columns(text)
# print(updated_text)
