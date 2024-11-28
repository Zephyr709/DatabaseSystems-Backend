CREATE OR REPLACE FUNCTION search_table_col_row(
    table_name text,
    column_name text,
    search_word text
)
RETURNS SETOF RECORD AS
$$
DECLARE
    searchQuery text;
BEGIN
    -- Construct query for exact match
    searchQuery := format(
        'SELECT * FROM %I WHERE %I::text = %L', table_name, column_name, search_word
    );

    -- Execute the query
    RETURN QUERY EXECUTE searchQuery;
END;
$$ LANGUAGE plpgsql;