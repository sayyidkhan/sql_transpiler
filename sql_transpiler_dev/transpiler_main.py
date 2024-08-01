import sqlglot
import sqlparse

from sql_transpiler_dev.sybase.sybase_transpiler import sybase_formatting_logic


def __formatter_logic(__convert_to, transpiled_sql):
    _fmt_sql = sqlparse.format(
        transpiled_sql,
        reindent=True,
        keyword_case="upper",
        use_space_around_operators=True,
        indent_columns=True
    )
    _fmt_sql = _fmt_sql.replace("CASE", "CASE\n     ")
    _fmt_sql = sybase_formatting_logic(_fmt_sql) if __convert_to == "tsql" else _fmt_sql
    return _fmt_sql


def __transpile_logic(__convert_from, __convert_to, sql_query):
    _processed_sql_query = sqlparse.format(sql_query, strip_comments=True).strip()
    transpiled_sql = sqlglot.transpile(
        _processed_sql_query,
        read=__convert_from,
        write=__convert_to,
        pretty=True
    )[0]
    return transpiled_sql


def transpile_sql_code(sql_query, __convert_from, __convert_to):
    """ transpile logic """
    transpiled_sql = __transpile_logic(__convert_from, __convert_to, sql_query)
    """ formatting logic """
    formatted_sql = __formatter_logic(__convert_to, transpiled_sql)

    return formatted_sql
