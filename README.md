# Any Columns

This is a Python library for taking spreadsheet inputs with non-standard column names and determining their contents.

For now, the library expects that you have already parsed your CSV / Excel document and have a list of column names as
strings.

## Warning

Some reasons you might not want to use this yet:

- This isn't in production use anywhere
- The test coverage isn't great (there is no coverage for the RegexColumn definition)
- RegexColumn will be slow if you have really large numbers of columns in your spreadsheets
- The API isn't really done (

Some reasons you might want to use this:

- You're just doing one-off data exploration and don't care about production quality
- You're willing to write some tests yourself (PR's welcome)

## Usage

### Example: Categorizing files

You just started a new HR job and find that there's a shared folder with a bunch of CSV files dating back years, made
manually by your predecesors. A quick scan shows that they tend to have similar information, but:

- The column names are all easy for a human to understand but inconsistent, maybe because each of your predecessors had
  their own methods ("email", "Email Address", "e.addr")
- Sometimes multiple kinds of data will show up in one file and sometimes they will show up in separate files
  ("hires-2022-01.csv", "terminations-2022-01.csv", "hires-and-terminations-2020-01.csv")

To handle this, you can write a schema using regexes to define the column names you're looking for:

```python
import re

from any_columns import RegexColumn, StringColumn, Schema, find_best_matching_schema


NAME_COLUMN = "name"
EMAIL_COLUMN = "email"
START_DATE_COLUMN = "start date"
TERMINATION_DATE_COLUMN = "end date"


schemas = {
    # Alice was very consistent and always used the exact same column names, but kept hires and terminations in
    # different files
    Schema(
        name="alice hires",
        columns_init={
            StringColumn(NAME_COLUMN, "name"),
            StringColumn(START_DATE_COLUMN, "start date"),
        }
    ),
    Schema(
        name="alice terminations",
        columns_init={
            StringColumn(NAME_COLUMN, "name"),
            StringColumn(TERMINATION_DATE_COLUMN, "termination date"),
        }
    ),
    # Bob was inconsistent about column names and always put them in the same files
    Schema(
        name="bob hires and terms",
        columns_init={
            RegexColumn(NAME_COLUMN, re.compile("(full )?name", re.IGNORECASE), ),
            RegexColumn(START_DATE_COLUMN, re.compile("(start date|started)", re.IGNORECASE)),
            RegexColumn(TERMINATION_DATE_COLUMN, re.compile("(termination date|termed)", re.IGNORECASE)),
        }
    ),
}
```

And then for each file you can check which schema it matches and which column the data you're looking for is in:

```python
import csv
from pathlib import Path
from typing import Dict, List


def parse_file(file):
    with file.open("r") as f:
        reader = csv.DictReader(f)
        columns = set(reader.fieldnames)
        if len(reader.fieldnames) != len(columns):
            print(f"Skipping file {file} because it has duplicate column names")
            return
        match = find_best_matching_schema(schemas, set(reader.fieldnames))
        if match is None:
            print(f"Skipping file {file} because it doesn't match any of our schemas")
            return
        print(f"Reading file {file} using schema {match.schema.name}")
        for row in reader:
            parsed_row = {
                schema_column.name: row[column_name]
                for column_name, schema_column in match.matching_columns.items()
            }
            yield parsed_row


for file in Path("./example").glob("*.csv"):
    for parsed_row in parse_file(file):
        print(f"If this was real code we'd do something with this: {parsed_row}")
```