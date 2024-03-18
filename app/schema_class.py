from pandera import DataFrameSchema, Column, Check, Index

schema = DataFrameSchema(
    columns={
        "transaction_time": Column(
            dtype="datetime64[ns]",
            nullable=False,
            unique=False,
            coerce=False,
            required=True
        ),
        "product_name": Column(
            dtype="object",
            nullable=False,
            unique=False,
            coerce=False,
            required=True
        ),
        "price": Column(
            dtype="float64",
            checks=[
                Check.greater_than(0)
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True
        ),
        "store": Column(
            dtype="int64",
            nullable=False,
            unique=False,
            coerce=False,
            required=True
        ),
    },
    index=Index(
        dtype="int64",
        nullable=False,
        coerce=False,
    ),
    dtype=None,
    coerce=True,
    strict=False,
    ordered=False,
    report_duplicates="all",
    unique_column_names=False,
    add_missing_columns=False
)
