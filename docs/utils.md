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

Returns number from string 



**Examples:**
 
- '12892,886214' -> 12892.89 
- '162,12' -> 162.12 
- '135,0000' -> 135 
- '13000' -> 13000 
- '-' -> 0 



**Args:**
 
 - <b>`value`</b> (str):  the value to convert 



**Returns:**
 
 - <b>`number`</b>:  the number from string 


---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L141"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format_number`

```python
format_number(value: float) → str
```

Formats number into string 



**Examples:**
 
- 7600.0000 -> 7600 
- 5.8523 -> 5,85 



**Args:**
 
 - <b>`value`</b> (float):  the value to format  



**Returns:**
 
 - <b>`str`</b>:  the number as string 


---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_number`

```python
extract_number(value: str) → str
```

Extracts number from string 



**Examples:**
 
- 7600,0000 POINTS -> 7600 
- 7800,00 Points -> 7800 
- 13,0000 EUR -> 13 
- 22,50 EUR -> 22,50 
- 7,5000 -> 7,50 



**Args:**
 
 - <b>`value`</b> (str):  string containing a number 



**Returns:**
 
 - <b>`str`</b>:  the number from string 


---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\utils.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `clean_asset_name`

```python
clean_asset_name(name: str)
```

Cleans up asset's name 



**Examples:**
 
- TotalEnergies SE -> TotalEnergies 
- Sanofi SA -> Sanofi 
- Carrefour S.A. -> Carrefour 
- STMicroelectronics N.V. -> STMicroelectronics 
- CAC 40® -> CAC 40 



**Args:**
 
 - <b>`name`</b> (str):  the asset's name 



**Returns:**
 
 - <b>`str`</b>:  the cleaned name 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
