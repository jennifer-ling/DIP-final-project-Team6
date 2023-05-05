# DIP-final-project-Team6
DIP final project

## Parameters
* `<input_imgname>` and `<output_imgname>` is required arugment. 

* For example: `sample.png` for `<input_imgname>`, and `test` for `<output_imgname>` (no file extentesion needed)

* By default, the program will open `./testcase/<input_imgname>` and output image as `./result/<output_imgname>.png`

## Usage
* debug mode (save img files during the process)
  ```
  python MLLE.py <input_imgname> <output_imgname>
  ```
* testing mode (compute benchmark, and only save the final result) 
  ```
  python test.py <input_imgname> <output_imgname>
  ```