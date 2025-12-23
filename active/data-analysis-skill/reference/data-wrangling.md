# Data Wrangling Reference

Format-specific extraction and transformation patterns.

## Universal Loader

```python
import pandas as pd
import polars as pl
from pathlib import Path
from typing import Union
import warnings

class DataLoader:
    """Universal data loader for any format."""

    def __init__(self):
        self.supported_formats = {
            '.csv': self._load_csv,
            '.xlsx': self._load_excel,
            '.xls': self._load_excel,
            '.json': self._load_json,
            '.parquet': self._load_parquet,
            '.pdf': self._load_pdf,
            '.pptx': self._load_pptx,
            '.docx': self._load_docx,
            '.md': self._load_markdown,
            '.sql': self._load_sql,
            '.sqlite': self._load_sqlite,
        }

    def load(self, path: str, **kwargs) -> pd.DataFrame:
        """Load data from any supported format."""
        path = Path(path)
        suffix = path.suffix.lower()

        if suffix not in self.supported_formats:
            raise ValueError(f"Unsupported format: {suffix}")

        return self.supported_formats[suffix](path, **kwargs)

    def _load_csv(self, path, **kwargs):
        return pd.read_csv(path, **kwargs)

    def _load_excel(self, path, sheet_name=0, **kwargs):
        return pd.read_excel(path, sheet_name=sheet_name, engine='openpyxl', **kwargs)

    def _load_json(self, path, **kwargs):
        return pd.read_json(path, **kwargs)

    def _load_parquet(self, path, **kwargs):
        return pd.read_parquet(path, **kwargs)

    def _load_pdf(self, path, **kwargs):
        return extract_pdf_tables(path)

    def _load_pptx(self, path, **kwargs):
        tables = extract_pptx_tables(path)
        return pd.concat(tables) if tables else pd.DataFrame()

    def _load_docx(self, path, **kwargs):
        return extract_docx_tables(path)

    def _load_markdown(self, path, **kwargs):
        return parse_markdown_tables(path)

    def _load_sql(self, path, conn=None, **kwargs):
        query = open(path).read()
        if conn is None:
            raise ValueError("Database connection required for SQL files")
        return pd.read_sql(query, conn)

    def _load_sqlite(self, path, table=None, **kwargs):
        import sqlite3
        conn = sqlite3.connect(path)
        if table:
            return pd.read_sql(f"SELECT * FROM {table}", conn)
        # List tables if none specified
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
        print(f"Available tables: {tables['name'].tolist()}")
        return tables
```

## CSV Patterns

### Smart CSV Loading

```python
def smart_load_csv(path: str) -> pd.DataFrame:
    """Load CSV with automatic type detection and cleaning."""

    # Try to detect encoding
    import chardet
    with open(path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    encoding = result['encoding']

    # Load with detected encoding
    df = pd.read_csv(
        path,
        encoding=encoding,
        low_memory=False,
        na_values=['', 'NA', 'N/A', 'null', 'NULL', 'None', '-'],
    )

    # Auto-detect date columns
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    return df
```

### Large CSV with Polars (30x faster)

```python
import polars as pl

def load_large_csv(path: str, sample: bool = False) -> pl.DataFrame:
    """Load large CSV efficiently with Polars."""

    # Lazy evaluation - doesn't load until .collect()
    df = pl.scan_csv(path)

    if sample:
        # Sample 10% for exploration
        df = df.sample(fraction=0.1)

    # Common transformations
    df = df.with_columns([
        pl.col('date').str.to_date().alias('date_parsed'),
        pl.col('revenue').cast(pl.Float64),
    ])

    return df.collect()
```

## Excel Patterns

### Multi-Sheet Excel

```python
def load_excel_workbook(path: str) -> dict[str, pd.DataFrame]:
    """Load all sheets from Excel workbook."""
    xls = pd.ExcelFile(path, engine='openpyxl')

    sheets = {}
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        # Skip empty sheets
        if not df.empty:
            sheets[sheet_name] = df

    return sheets
```

### Excel with Headers in Different Rows

```python
def load_excel_with_header(path: str, header_row: int = 0) -> pd.DataFrame:
    """Load Excel where data starts on a specific row."""
    return pd.read_excel(
        path,
        header=header_row,
        skiprows=range(0, header_row),
        engine='openpyxl',
    )
```

## PDF Extraction

### Using pdfplumber (Recommended)

```python
import pdfplumber

def extract_pdf_tables(path: str) -> pd.DataFrame:
    """Extract all tables from PDF."""
    all_tables = []

    with pdfplumber.open(path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()

            for table_num, table in enumerate(tables):
                if table and len(table) > 1:
                    # First row as header
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df['_page'] = page_num + 1
                    df['_table'] = table_num + 1
                    all_tables.append(df)

    if all_tables:
        return pd.concat(all_tables, ignore_index=True)
    return pd.DataFrame()


def extract_pdf_text(path: str) -> str:
    """Extract all text from PDF (for unstructured data)."""
    text = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text())

    return "\n\n".join(text)
```

### Using tabula-py (Alternative)

```python
import tabula

def extract_pdf_tables_tabula(path: str) -> list[pd.DataFrame]:
    """Extract tables using tabula-py (requires Java)."""
    return tabula.read_pdf(path, pages='all', multiple_tables=True)
```

## PowerPoint Extraction

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

def extract_pptx_tables(path: str) -> list[pd.DataFrame]:
    """Extract all tables from PowerPoint."""
    prs = Presentation(path)
    tables = []

    for slide_num, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if shape.has_table:
                table = shape.table
                data = []

                for row in table.rows:
                    row_data = []
                    for cell in row.cells:
                        row_data.append(cell.text.strip())
                    data.append(row_data)

                if data and len(data) > 1:
                    df = pd.DataFrame(data[1:], columns=data[0])
                    df['_slide'] = slide_num
                    tables.append(df)

    return tables


def extract_pptx_text(path: str) -> dict[int, str]:
    """Extract text from each slide."""
    prs = Presentation(path)
    slides = {}

    for slide_num, slide in enumerate(prs.slides, 1):
        text_parts = []

        for shape in slide.shapes:
            if hasattr(shape, 'text'):
                text_parts.append(shape.text)

        slides[slide_num] = "\n".join(text_parts)

    return slides
```

## Word Document Extraction

```python
from docx import Document

def extract_docx_tables(path: str) -> pd.DataFrame:
    """Extract tables from Word document."""
    doc = Document(path)
    all_tables = []

    for table_num, table in enumerate(doc.tables):
        data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            data.append(row_data)

        if data and len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            df['_table'] = table_num + 1
            all_tables.append(df)

    if all_tables:
        return pd.concat(all_tables, ignore_index=True)
    return pd.DataFrame()


def extract_docx_text(path: str) -> str:
    """Extract all text from Word document."""
    doc = Document(path)
    return "\n\n".join([para.text for para in doc.paragraphs])
```

## Markdown Table Parsing

```python
import re

def parse_markdown_tables(path: str) -> pd.DataFrame:
    """Parse markdown tables into DataFrame."""
    with open(path, 'r') as f:
        content = f.read()

    # Find all markdown tables
    table_pattern = r'\|(.+)\|[\r\n]+\|[-:\| ]+\|[\r\n]+((?:\|.+\|[\r\n]+)+)'
    matches = re.findall(table_pattern, content)

    all_tables = []

    for header, body in matches:
        # Parse header
        columns = [col.strip() for col in header.split('|') if col.strip()]

        # Parse rows
        rows = []
        for line in body.strip().split('\n'):
            row = [cell.strip() for cell in line.split('|') if cell.strip()]
            if row:
                rows.append(row)

        if columns and rows:
            df = pd.DataFrame(rows, columns=columns)
            all_tables.append(df)

    if all_tables:
        return pd.concat(all_tables, ignore_index=True)
    return pd.DataFrame()
```

## SQL and Database

### DuckDB (In-Memory Analytics)

```python
import duckdb

def query_with_duckdb(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Run SQL query on DataFrame using DuckDB."""
    conn = duckdb.connect(':memory:')
    conn.register('data', df)
    return conn.execute(query).df()

# Example
result = query_with_duckdb(df, """
    SELECT
        segment,
        SUM(revenue) as total_revenue,
        COUNT(DISTINCT customer_id) as customers
    FROM data
    WHERE date >= '2024-01-01'
    GROUP BY segment
    ORDER BY total_revenue DESC
""")
```

### SQLite

```python
import sqlite3

def load_sqlite_db(path: str) -> dict[str, pd.DataFrame]:
    """Load all tables from SQLite database."""
    conn = sqlite3.connect(path)

    # Get all table names
    tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
    table_names = pd.read_sql(tables_query, conn)['name'].tolist()

    # Load each table
    data = {}
    for table in table_names:
        data[table] = pd.read_sql(f"SELECT * FROM {table}", conn)

    conn.close()
    return data
```

## Data Cleaning Pipeline

```python
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Standard data cleaning pipeline."""

    # 1. Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace(r'[^\w]', '', regex=True)
    )

    # 2. Remove empty rows/columns
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all')

    # 3. Strip whitespace from strings
    string_cols = df.select_dtypes(include=['object']).columns
    df[string_cols] = df[string_cols].apply(lambda x: x.str.strip())

    # 4. Convert numeric columns
    for col in df.columns:
        if df[col].dtype == 'object':
            # Try to convert to numeric
            numeric = pd.to_numeric(df[col].str.replace(r'[$,]', '', regex=True), errors='coerce')
            if numeric.notna().sum() > len(df) * 0.5:
                df[col] = numeric

    # 5. Auto-detect dates
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                dates = pd.to_datetime(df[col], errors='coerce')
                if dates.notna().sum() > len(df) * 0.5:
                    df[col] = dates
            except:
                pass

    return df
```

## Type Coercion

```python
def coerce_types(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """
    Apply type schema to DataFrame.

    schema = {
        'date': 'datetime',
        'revenue': 'float',
        'customers': 'int',
        'segment': 'category',
    }
    """
    df = df.copy()

    for col, dtype in schema.items():
        if col not in df.columns:
            continue

        if dtype == 'datetime':
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif dtype == 'float':
            df[col] = pd.to_numeric(df[col], errors='coerce')
        elif dtype == 'int':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        elif dtype == 'category':
            df[col] = df[col].astype('category')
        elif dtype == 'bool':
            df[col] = df[col].map({'true': True, 'false': False, '1': True, '0': False})

    return df
```

## Batch Processing

```python
from pathlib import Path
import concurrent.futures

def batch_load_files(directory: str, pattern: str = "*.csv") -> pd.DataFrame:
    """Load and concatenate all matching files."""
    path = Path(directory)
    files = list(path.glob(pattern))

    loader = DataLoader()

    def load_file(f):
        df = loader.load(str(f))
        df['_source_file'] = f.name
        return df

    # Parallel loading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        dfs = list(executor.map(load_file, files))

    return pd.concat(dfs, ignore_index=True)
```
