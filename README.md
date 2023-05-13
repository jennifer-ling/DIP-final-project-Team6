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

## Data set
* UCCS: color correction
* UIQS: visibility
  * A,B,C,D,E: quality levels (in the descending order)
* UIEB: variousity

## Evaluation matric
* Average gradient (AG): higher, better visibility
* Edge intensity (EI): higher, better edge intensity
* Patch-based contrast quality index (PCQI): higher, better visibility
* Underwater image quality metric (UIQM): higher, better visual perception
* Colorfulness contrast fog density index (CCF): higher, better visual perception