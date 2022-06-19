# classlogging

Class-based logging facility.

## Installation

```shell
pip install classlogging
```

## Usage example

```python
import classlogging


class MyClass(classlogging.LoggerMixin):
    def test_log_value(self, value: str) -> None:
        self.logger.debug(f"Got value: {value}")


if __name__ == "__main__":
    classlogging.configure_logging(level=classlogging.LogLevel.DEBUG)
    MyClass().test_log_value("Foo")
    # Writes to stderr:
    # 2022-01-01 12:34:56,789 DEBUG [__main__.MyClass] Got value: Foo
```
