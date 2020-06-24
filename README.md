# PS2BULK

Bulk loading of PS2 ISO images using [`hdl-dump`](https://github.com/AKuHAK/hdl-dump).

## Requirements

- Python3.8+
- Pipenv

## Setup

```console
$ pipenv sync
```

## Usage

```console
$ pipenv run ./ps2bulk.py /path/to/your/ps2/hdd game1.iso game2.iso game3.iso ... > bulkload.sh
$ chmod +x bulkload.sh
$ sudo ./bulkload.sh
```

## Example

```console
$ pipenv run ./ps2bulk.py /dev/sdb ~/Downloads/Shadow\ of\ the\ Colossus\ \(Europe,\ Australia\)\ \(En,Fr,De,Es,It\).iso ~/Downloads/Time\ Crisis\ 3\ \(Europe,\ Australia\)\ \(En,Fr,De,Es,It\).iso > bulkload.sh
$ cat bulkload.sh
hdl-dump inject_dvd /dev/sdb 'Shadow of the Colossus' '/home/nil/Downloads/Shadow of the Colossus (Europe, Australia) (En,Fr,De,Es,It).iso' SCES_533.26 '*u4'
hdl-dump inject_dvd /dev/sdb 'Time Crisis 3' '/home/nil/Downloads/Time Crisis 3 (Europe, Australia) (En,Fr,De,Es,It).iso' SCES_518.44 '*u4'
$ chmod +x bulkload.sh
$ sudo ./bulkload.sh
[sudo] password for nil:
/dev/sdb: partition with such name already exists: "Shadow of the Colossus".
/dev/sdb: partition with such name already exists: "Time Crisis 3".
```
