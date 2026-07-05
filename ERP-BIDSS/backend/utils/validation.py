def validate_schema(df, expected_columns):
    missing = [col for col in expected_columns if col not in df.columns]
    return len(missing) == 0
