# confdaora

<p align="center" style="margin: 3em">
  <a href="">
    <img src="https://dutradda.github.io/confdaora/confdaora.svg" alt="confdaora" width="300"/>
  </a>
</p>

<p align="center">
    <em>Configurations using python annotations</em>
</p>

---

**Documentation**: <a href="https://dutradda.github.io/confdaora/" target="_blank">https://dutradda.github.io/confdaora</a>

**Source Code**: <a href="https://github.com/dutradda/confdaora" target="_blank">https://github.com/dutradda/confdaora</a>

---


## Key Features

- Generate a `DictDaora` with values parsed from environment variables.


## Requirements

 - Python 3.8+
 - dictdaora
 - jsondaora


## Instalation
```
$ pip install confdaora
```


## Basic example

```python
{!./src/index/index_00_basic.py!}
```

Suposing your file calls `myconf.py`:
```
{!./src/index/index_00_basic_call.bash!}
```

```
{!./src/index/index_00_basic.output!}
```


## Complex example

```python
{!./src/index/index_01_complex.py!}
```

Suposing your file calls `myconf.py`:
```
{!./src/index/index_01_complex_call.bash!}
```

```
{!./src/index/index_01_complex.output!}
```
