image2ascii
===========
## Requirements
```bash
pip install -r requirements.txt
```

| Name   | Ver    |
|--------|--------|
| pillow | 10.2.0 |
## How to use
* import library
  * ```python
      from image2ascii import image2ascii
    ```
* set option
  * | Parameters  | Description                                                                 |
    |-------------|-----------------------------------------------------------------------------|
    | path        | image path                                                                  |
    | width       | Area to be width                                                            |
    | height      | Area to be height                                                           |
    | ascii_chars | character to use (The closer you are to the right, the lighter it becomes.) |
    | alpha       | Character to paint the alpha area with                                      |
* Enjoy!