# PS2BULK

Bulk loading of PS2 ISO images using [`hdl-dump`](https://github.com/AKuHAK/hdl-dump).

## Requirements

- Python3.8+
- Pipenv

## Installation

```console
$ pipenv sync
```

## Usage

```console
$ pipenv run ps2bulk.py /path/to/your/ps2/hdd game1.iso game2.iso game3.iso ... > bulkload.sh
$ chmod +x bulkload.sh
$ sudo ./bulkload.sh
```
