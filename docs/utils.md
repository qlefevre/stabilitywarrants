<!-- markdownlint-disable -->

<a href="../functions/utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils`





---

<a href="../functions/utils.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `xlsx`

```python
xlsx(fname)
```






---

<a href="../functions/utils.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `upload_file`

```python
upload_file(file_name, object_name=None)
```

Upload a file to an S3 bucket 

:param file_name: File to upload :param bucket: Bucket to upload to :param object_name: S3 object name. If not specified then file_name is used :return: True if file was uploaded, else False 


---

<a href="../functions/utils.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download_file`

```python
download_file(object_name)
```






---

<a href="../functions/utils.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_temp_file`

```python
create_temp_file()
```

Create temporary file 



**Returns:**
 
 - <b>`str`</b>:  le nom du fichier temporaire 


---

<a href="../functions/utils.py#L118"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `to_number`

```python
to_number(value: str)
```






---

<a href="../functions/utils.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format_number`

```python
format_number(value: float)
```






---

<a href="../functions/utils.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_string`

```python
extract_string(value: str) → str
```






---

<a href="../functions/utils.py#L140"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `clean_name`

```python
clean_name(name: str)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
