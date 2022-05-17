<!-- markdownlint-disable -->

# <kbd>module</kbd> `utils`





---

## <kbd>function</kbd> `xlsx`

```python
xlsx(fname)
```






---

## <kbd>function</kbd> `upload_file`

```python
upload_file(file_name, object_name=None)
```

Upload a file to an S3 bucket 

:param file_name: File to upload :param bucket: Bucket to upload to :param object_name: S3 object name. If not specified then file_name is used :return: True if file was uploaded, else False 


---

## <kbd>function</kbd> `download_file`

```python
download_file(object_name)
```






---

## <kbd>function</kbd> `create_temp_file`

```python
create_temp_file()
```

Create temporary file 



**Returns:**
 
 - <b>`str`</b>:  le nom du fichier temporaire 


---

## <kbd>function</kbd> `to_number`

```python
to_number(value: str)
```






---

## <kbd>function</kbd> `format_number`

```python
format_number(value: float)
```






---

## <kbd>function</kbd> `extract_string`

```python
extract_string(value: str) → str
```






---

## <kbd>function</kbd> `clean_name`

```python
clean_name(name: str)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
