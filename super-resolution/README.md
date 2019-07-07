## Installation
I used Python3 to develop the models. The following packages are needed -
```
numpy
torch
Pillow
easydict
scikit-image
opencv-python
```
You also need to have [jupyter notebook](https://jupyter.org/install) installed.

## Steps to run
1. Open the directory in jupyter notebook.
2. Change the settings as you see fit.
3. Place all the low resolution images in `TEST_IMAGE_FOLDER` (default is `lr`) folder.
4. Run all the the cells of the model you want to use for super resolution.
5. Find the SR'ed images in folder `hr`.

## Experiments
I used 3 images to check the time taken by each model to generate the SR output. Their resolutions are -
1. Image #1 - 510 x 339
2. Image #2 - 321 x 481
3. Image #3 - 481 x 321

### Timing / Performance

The mapping between an image and a model represents the time, in seconds, it took to generate the SR output image. *This time is exclusive of the time taken by CV libraries (OpenCV and Pillow) to turn the model output (tensor) to a numpy array representing the image.*
Time is measure in seconds.
```markdown
| Image |  SRCNN  | FSRCNN  | EDSR    | SRGAN   | ESRGAN | ProGANSR |
|-------|:-------:|---------|---------|---------|--------|----------|
| #1    | 6.75e-4 | 0.255   | 8.39e-3 | 7.89e-3 | 2.379  | 2.997    |
| #2    | 4.97e-4 | 9.87e-4 | 8.92e-3 | 6.17e-3 | 1.076  | 2.678    |
| #3    | 4.90e-4 | 9.12e-4 | 7.90e-3 | 6.19e-3 | 1.074  | 2.822    |
```

### Quality

Quality is measured with respect to PSNR in dB. GAN based models seem to perform much better when the output image quality is compared wrt SSIM or MOS. However PSNR is the standard.
```markdown
| Dataset | SRCNN | FSRCNN | EDSR  | SRGAN | ESRGAN | ProGANSR |
|---------|:-----:|--------|-------|-------|--------|----------|
| Set5    | 30.07 | 30.72  | 32.46 | 29.40 | 32.73  | 32.54    |
| Set14   | 27.18 | 27.61  | 28.80 | 26.02 | 28.99  | 28.59    |
| BSD100  | 26.68 | 26.98  | 27.57 | 25.16 | 27.85  | 27.58    |
```


## Conclusion
I think **EDSR** gives the best trade-off between performance and SR image quality. It is also straightforward to fine-tune for different upscaling factors. However, if we judge solely on the output image PSNR, ESRGAN is quite easily the best. 