FastAPI REST Polyfilling
========================
### For DEMO please check branch: *1-optimised-id1*

### Description
-   FastAPI REST is a service that provides polylines filling.
-   Best practices for configuration split and project structure;

### Important
-   *This is not a production-ready API but rather a proof of concept of a feature*
-   In order to speed up the execution there might be multiple elements to be added such as multiprocessing, events, queues, and so on depending on the needs and chosen architecture.

## Code quality

### Static analysis
- Static code analysis used: https://deepsource.io/

### Pylint
- Pylint used to maintain code quality;
- Current status: `Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)`

### Requirements

-   It is assumed that you have Python. If not, then download the latest versions from:
    * [Python](https://www.python.org/downloads/)
    * [PostgreSQL](https://www.postgresql.org/download/)

### Installation

1. **Clone git repository**:
    ```bash
    git clone https://github.com/alexmalan/fastapi-rest-api-polyfill.git
    ```

2. **Create virtual environment**
	- You can use `virtualenv` or `venv` or `conda` environment for this.
    ```bash
    python -m venv $(pwd)/venv
    source venv/bin/activate
    ```

3. **Install requirements**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Add environment variables**
    - Create a file named `.env` in project root directory
    - Add and fill next environment variables with your local database config:
        ```.env
        DATABASE_NAME=
        DATABASE_USER=
        DATABASE_PASSWORD=
        DATABASE_HOST=
        ```

5. **Make migrations**:
    ```bash
    python make_migrations.py
    ```

## Run

-   Run APP using command:
    ```bash
    uvicorn main:app --reload
    ```
- Localhost resources:
    * localhost:<port_id>/docs/ - documentation
    * localhost:<port_id>/redoc/ - redoc documentation
    * localhost:<port_id>/api/v1/polys/   - endpoints
    
## Output

- The output result is stored in the /data folder in 2 formats:
   * .npy - this is the result np.array
   * .png - this is a plot image of the result for easier visualization

## Postman Configuration

### Library Import
* Find the fastapi-rest-polylines.postman_collection.json in the root directory
- Open Postman
   - File
      - Import
         - Upload files
            - Open

## Files
* `main` - Main application file
* `make_migrations` - Migration script
* `app/` - Back-end code
* `venv/` - Virtual environment files used to generate requirements;

## Test

- Tests are done with pytest
- Using pytest:
    - For following options are available:
        - `-v` - to have verbose tests
    
    - Windows:
    ```bash
    pytest
    ```
    
    - OS X:
    ```bash
    pytest
    ```

## Loading NPY files

- In order to access the actual np.array data, you need to use the `np.load()` function. This function takes a single argument, which is the path to the .npy file you want to load. It returns the data stored in the file as a numpy array.

    ```bash
    from numpy import load

    data = load('data.npy')
    print(data)
    ```
## Design Notes
### Reasoning
-   In the implementation I wanted to outline 3 cases:
   	1. The use of a Python written algorithm
   	2. The use of a recursive algorithm
   	3. The use of a package import
-   Why?

1. Python is not a fast programming language compared to others and there might be speed drawbacks when you create or implement an algorithm in pure Python.
2. A recursive algorithm as we saw in the comparison was the fastest - simply because there was no iteration involved rather than stack usage. The drawback is that for very large operations it might have a negative impact of the memory.
3. This one I choose simply because of convenience - the scenario when you have to implement something fast - assuming there are more than just one algorithms involved in the program. The underneath code is Cython, it is very easy to use, but compared to a custom made algorithm it might not perform that well - overall a good ratio of speed to implementation time.

### Implementation
 - The application is implemented to test three popular algorithms and compare their performance.
    * [Inside-Outside Algorithm](https://b-ok.cc/book/929596/f72c89)
    * [Boundary Algorithm 4-way](https://de.wikipedia.org/wiki/Floodfill)
    * [Scikit Draw Polygon Algorithm](https://scikit-image.org/docs/stable/api/skimage.draw.html#skimage.draw.polygon)

 - The user is able to select the algorithm to use for the filling of the polyline.
 - The records are stored in the database and the user is able to benchmark the algorithms and compare their execution time.

### Algorithms
1. Inside-Outside Algorithm
    - The Inside-Outside Algorithm is a simple algorithm for determining whether a point is inside, outside, on the edge or on the vertice of a polygon.
2. Boundary Algorithm 4-way
    - This algorithm picks a point inside an object and starts to fill recursively until it hits the boundary of the object. The value of the boundary and the value that we fill should be different for this algorithm to work. Besides that you have to pick a point inside the polygon in order for it to fill the whole polygon, rather than outside.
    - It is also worth mentioning that Bresenham's line algorithm is being applied first, so that the polygon has it's vertices and shape completed.
3. Scikit Draw Polygon Algorithm
    - Scikit Draw Polygon Algorithm is an inside-outside algorithm that implements the code in Cython which makes it very fast and efficient even for larger arrays.

### Ideal word
- I would assume the API would be used to process X number of polylines for each height stage of a 3D printing process.
- In order to achieve this efficiently there has to be reliability and performance involved, since we cannot wait 4 seconds for each polyline to be processed - 1mm of height - for a 20cm+ object print.

### Performance
1. Inside-Outside Algorithm - 2.549216 sec/execution
2. Boundary Algorithm 4-way - 0.001539 sec/execution
3. Scikit Draw Polygon Algorithm - 0.031126 sec/execution
    
- If for example we want to print 20cm height of an object for which we know the polylines of a 1mm height stage these would be the results:
1. Inside-Outside Algorithm - 509.8432s ~ 8.48 minutes
2. Boundary Algorithm 4-way - 0.3078s
3. Scikit Draw Polygon Algorithm - 6.2252s

* This is the time to compute the element not to print it.

### Other Options
- There are other algorithms that are popular for this use case, such as:
1. [Scanline Algorithm](https://www.cs.rit.edu/~icss571/filling/how_to.html)
2. [Boundary Algorithm 8-way](https://de.wikipedia.org/wiki/Floodfill)
3. [Graph Theoretic Fill Algorithm](https://en.wikipedia.org/wiki/Flood_fill)

# Logic Requirements
## Exercise1 (Required)

The goal of this exercise is to understand your reasoning and see how resourceful you can be with geometrical problems.

You are given a Python .bin file that has been created using the pickle library. This will be the input of your function.

The content of that file is list with a single closed polyline, which is made from a list of 10 lists, each containing 2 point elements, also lists [x, y], representing the  x and y coordinates of said point.

Your job is to output a numpy array of the following dimensions (19200, 10800), all full of zeroes, and to represent with ones the points that are on the polyline or inside it. Effectively you will be drawing the shape on the array and colouring it in.

Be aware that the ones do not only need to be the vertices of the polyline, but also the edges and the inside of them. That is, if the shape happened to be a rectangle (which is not), then we would be expecting all points inside that rectangle to be ones:

i.e. (View on raw code to see the rectangle)

```
[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
```

You will be scored both on your reasoning, clarity of code and result. Please add comments where needed and have at least 1 unit test to run the script from it. If you add more tests we will be running them too and checking the result.

## Exercise2 (Required)

For this exercise you will be creating a small microservice using FastAPI. Your aim is to create a small microservice using the mentioned library and to create and endpoint where you would post the shape from the last exercise as payload and would return the numpy array as feedback
It is up to you to determine the format of said payload and return.
