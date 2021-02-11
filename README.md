# ibtax_web_ui
Interactive Brokers tax web UI
---

Web интерфейс [утилиты](https://github.com/cdump/investments) для подготовки налоговой отчетности для брокера Interactive Brokers.


## Project local running

```bash
$ git clone https://github.com:esemi/ibtax_web_ui.git

$ cd ibtax_web_ui

$ pip install poetry
$ poetry install
$ poetry run uvicorn web_ui.webapp:app
 
```
