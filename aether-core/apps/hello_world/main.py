```python
import datetime

def main():
    """Prints 'Hello, World!' and the current time."""
    print("Hello, World!")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"The current time is: {current_time}")

if __name__ == "__main__":
    main()
```
