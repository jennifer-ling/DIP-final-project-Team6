# DIP-final-project-Team6
DIP final project

## Parameters
* `<input_imgname>` and `<output_imgname>` is required arugment. 

* For example: `sample.png` for `<input_imgname>`, and `test` for `<output_imgname>` (no file extentesion needed)

* By default, the program will open `./testcase/<input_imgname>` and output image as `./result/<output_imgname>.png`

## Usage
* debug mode (modify one img, and save resulted img files during the process)
  ```
  python MLLE.py <input_imgname> <output_imgname>
  ```
* testing mode (compute benchmark, and only save the final results) 
  ```
  python test.py
  ```

## Data set
* UCCS: color correction
* UIQS: visibility
  * A,B,C,D,E: quality levels (in the descending order)
* UIEB: variousity

## Evaluation matric
* Average gradient (AG): higher, better visibility
  * https://ieeexplore.ieee.org/abstract/document/1626836, formula 13
* Edge intensity (EI): higher, better edge intensity
  * https://www.sciencedirect.com/science/article/pii/S1568494619305915, sobel count
* Patch-based contrast quality index (PCQI): higher, better visibility
  * https://ieeexplore.ieee.org/abstract/document/7289355, formula 9
* Underwater image quality metric (UIQM): higher, better visual perception
  * https://ieeexplore.ieee.org/abstract/document/7305804, formula 10
* Colorfulness contrast fog density index (CCF): higher, better visual perception
  * https://www.sciencedirect.com/science/article/pii/S0045790617324953, formula 13