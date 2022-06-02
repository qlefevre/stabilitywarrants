<!-- markdownlint-disable -->

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils`





---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `xlsx`

```python
xlsx(fname)
```






---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `upload_file`

```python
upload_file(file_name, object_name=None)
```

Upload a file to an S3 bucket 

:param file_name: File to upload :param bucket: Bucket to upload to :param object_name: S3 object name. If not specified then file_name is used :return: True if file was uploaded, else False 


---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download_file`

```python
download_file(object_name)
```






---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_temp_file`

```python
create_temp_file()
```

Create temporary file 



**Returns:**
 
 - <b>`str`</b>:  le nom du fichier temporaire 


---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L118"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `to_number`

```python
to_number(value: str)
```






---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format_number`

```python
format_number(value: float)
```






---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_number`

```python
extract_number(value: str) → str
```

Extracts number from string 



**Example:**
 
- 7600,0000 POINTS -> 7600 
- 7800,00 Points -> 7800 
- 13,0000 EUR -> 13 
- 22,50 EUR -> 22 
- 7,5000 -> 7,50 



**Args:**
 
 - <b>`value`</b> (str):  string containing a number 



**Returns:**
 
 - <b>`str`</b>:  the number from string 


---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L155"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `clean_name`

```python
clean_name(name: str)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
