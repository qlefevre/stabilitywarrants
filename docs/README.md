<!-- markdownlint-disable -->

# API Overview

## Modules

- [`csv_to_json`](./csv_to_json.md#module-csv_to_json)
- [`extract_sg`](./extract_sg.md#module-extract_sg)
- [`extract_uc`](./extract_uc.md#module-extract_uc)
- [`merge`](./merge.md#module-merge)
- [`pivot_point`](./pivot_point.md#module-pivot_point)
- [`run_all_functions`](./run_all_functions.md#module-run_all_functions)
- [`transform`](./transform.md#module-transform)
- [`utils`](./utils.md#module-utils)

## Classes

- [`pivot_point.OHLC`](./pivot_point.md#class-ohlc)
- [`pivot_point.PivotPoint`](./pivot_point.md#class-pivotpoint)

## Functions

- [`csv_to_json.fix_number_and_properties`](./csv_to_json.md#function-fix_number_and_properties)
- [`csv_to_json.handle`](./csv_to_json.md#function-handle): Transforme le fichier final csv en json
- [`extract_sg.handle`](./extract_sg.md#function-handle): Download stability warrants from Société Générale
- [`extract_uc.handle`](./extract_uc.md#function-handle): Download stability warrants from Unicredit test
- [`extract_uc.transform_row`](./extract_uc.md#function-transform_row)
- [`merge.handle`](./merge.md#function-handle): Fusionne les fichiers csv de SG et UC => ALL
- [`pivot_point.extract_ohlc`](./pivot_point.md#function-extract_ohlc)
- [`pivot_point.handle`](./pivot_point.md#function-handle): Calcule les points pivots en mensuel et sur 4 semaines glissantes
- [`pivot_point.pivot_point`](./pivot_point.md#function-pivot_point)
- [`pivot_point.twenty_day_ohlc`](./pivot_point.md#function-twenty_day_ohlc)
- [`run_all_functions.handle`](./run_all_functions.md#function-handle)
- [`transform.handle`](./transform.md#function-handle): Transforme le fichier CSV
- [`transform.transform_row`](./transform.md#function-transform_row)
- [`utils.clean_name`](./utils.md#function-clean_name)
- [`utils.create_temp_file`](./utils.md#function-create_temp_file): Create temporary file
- [`utils.download_file`](./utils.md#function-download_file)
- [`utils.extract_number`](./utils.md#function-extract_number): Extracts number from string
- [`utils.format_number`](./utils.md#function-format_number)
- [`utils.to_number`](./utils.md#function-to_number)
- [`utils.upload_file`](./utils.md#function-upload_file): Upload a file to an S3 bucket
- [`utils.xlsx`](./utils.md#function-xlsx)


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
