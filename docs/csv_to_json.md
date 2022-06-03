<!-- markdownlint-disable -->

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\csv_to_json.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `csv_to_json`





---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\csv_to_json.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `fix_number_and_properties`

```python
fix_number_and_properties(row: dict)
```

Fix number and properties before transformation into json 



**Examples:**
 
- 9,5 (str) -> 9.5 (float) 
- sous-jacent (str) -> sousjacent (str) 
- borne basse (str) -> bornebasse (str) 



**Args:**
 
 - <b>`row`</b> (dict):  key/value dictionary for a warrant 



**Returns:**
 
 - <b>`dict`</b>:  key/value cleaned dictionary for a warrant 


---

<a href="https://github.com/qlefevre/stabilitywarrants/blob/main/functions\csv_to_json.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `handle`

```python
handle(event, context)
```

Transforme le fichier final csv en json 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
