# DIP-final-project-Team6
DIP final project
## Environment
### Python
* python: 3.10
* matlabengine: 9.14.3
* numpy
* opencv-python
* scipy
### MATLAB
* Deep Learning Toolbox
* Image Processing Toolbox
* Statistics and Machine Learning Toolbox

## Usage
### Debug mode
* Modify one image and save resulted image files during the process
* Syntax
  ```
  python MLLE.py <input_imgname> <output_imgname>
  ```
* Parameters
  * `<input_imgname>` and `<output_imgname>` are required arugments. 
  * No file extension needed for `<output_imgname>`
* Example
  ```
  python MLLE.py input.png output
  ```
  * the program will open `./testcase/input.png` and output images as `./result/output_*.png`

* testing mode (compute benchmark, and save it as txt. If `-d` is used, compute pictures in `testcase/demo/`) 
  ```
  python test.py -f <resultfilename> -s <sample size for each dataset> [-d]
  ```
### Evaluation mode
* Compute evaluation matrics, and save the result as text file
* Syntax
  ```
  python test.py -f <result_file_name> -s <sample_size> [-d]
  ```
* Parameters
  * If `-d` is used, compute pictures in `testcase/demo/` (`-s` is not used)
  * Else, pictures in 'testcase/UIQS/', 'testcase/UIEB_raw/', 'testcase/UCCS/' will be randomly sampled. (`-s` is the sample size for each dataset) 
  * No file extension needed for `<result_file_name>`
* Example
  ```
  python test.py -f result -s 15
  ```
  * total 15 * 3 = 45 images are sampled, and the result is save as `./result.txt`
  ```
  python test.py -f result -d
  ```
  * computes pictures in `testcase/demo/`, and the result is save as `./result.txt`


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