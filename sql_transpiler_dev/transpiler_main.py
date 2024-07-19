import sqlglot
import sqlparse


def transpile_sql_code(sql_query, __convert_from, __convert_to):
    """ transpile logic """
    _processed_sql_query = sqlparse.format(sql_query, strip_comments=True).strip()
    transpiled_sql = sqlglot.transpile(
        _processed_sql_query,
        read=__convert_from,
        write=__convert_to,
        pretty=True
    )[0]

    """ formatting logic """
    formatted_sql = sqlparse.format(
        transpiled_sql,
        reindent=True,
        keyword_case="upper",
        use_space_around_operators=True,
        indent_columns=True
    )
    formatted_sql = formatted_sql.replace("CASE", "CASE\n     ")
    return formatted_sql
