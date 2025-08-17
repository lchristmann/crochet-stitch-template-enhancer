# Crochet Stitch Template Enhancer

The Crochet Stitch Template Enhancer takes stitch template images that suffer from faint or unclear grids and overlays a clean, high-contrast grid. This makes the templates easier to read and follow, ensuring your crochet work stays accurate even when the original chart has poor resolution or hard-to-see lines.

## Usage

> Quick Explanation:
>
> - you put the crochet stich template image files into the [input/public](input/public) or [input/private](input/private) directory - the latter one is ensured to not become public (you can't commit those files to the Git repository, if you forked it and committed to your own Git platform)
> - you use the commands below to process the input image
> - you get the output image with clear grid lines in [output](output) directory

Requirements:

- [Docker](https://www.docker.com/)
- a [Bash](https://www.gnu.org/software/bash/) shell to execute the below commands (e.g. the bash terminal of VS Code)

Build the software (only once, or if you've changed parts of the code):

```bash
docker build -t crochet-stitch-template-enhancer .
```

Run the Crochet Stitch Template Enhancer:

> Important: adapt the path to your image: `/input/private/my_private_chart.png` -> path to your image.
>
> Optional: you can provide a custom output filename. Otherwise, the script will automatically create a PNG file in the output folder with the same name as the input (without extension).

```bash
# Automatic output filename (same name as input, saved as PNG)
docker run --rm \
  -u $(id -u):$(id -g) \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  crochet-stitch-template-enhancer \
  /input/private/my-crochet-pattern.jpeg
```

```bash
# Explicit output filename (optional)
docker run --rm \
  -u $(id -u):$(id -g) \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  crochet-stitch-template-enhancer \
  /input/private/my-crochet-pattern.jpeg /output/custom-name.png
```

If you want to remove all traces hereof after, delete the Docker image from your PC:

```bash
docker rmi crochet-stitch-template-enhancer
```

Now it will be gone from your list of Docker images (you can check by running `docker image ls`).

## Software Design

This project is written in [Python](https://www.python.org/) for quick and flexible image processing. It uses:

- [Pillow](https://pypi.org/project/pillow/) – for image manipulation, creating the overlay, and saving PNG output.
- [OpenCV](https://opencv.org/) – for advanced image processing, including grayscale conversion, blurring, edge detection, and line extraction.
- [NumPy](https://numpy.org/) – for efficient array operations during line detection.

In order for not everyone to have to install and get a Python project running, I containerized the project, so one only must have [Docker](https://www.docker.com/) installed as single dependency.

Input/Output:

- Accepts common image formats (PNG, JPEG/JPG, etc.)
- Output is always PNG, to preserve transparency for the grid overlay

Why Docker:

- Encapsulates all Python dependencies (Pillow, OpenCV, NumPy)
- Avoids local library conflicts
- Makes the tool portable and easy to run on any system with Docker