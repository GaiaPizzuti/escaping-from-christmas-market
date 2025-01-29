import os

def create_file(boids, boidguards, interval_data):
    """
    Function to create the result file given the input data and the output

    Parameters:
    -----------
    boids: list
        list of boids
    boidguards: list
        list of boidguards
    """

    # directory
    directory = "results"

    # create directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # file name
    filename = "result" + "-" + boids + "-" + boidguards + ".txt"

    path = os.path.join(directory, filename)

    # if file exists remove it
    if os.path.exists(path):
        os.remove(path)

    # open file
    with open(path, "w") as f:
        # write the headers
        f.write("time,boids,boidguards")
    
        # write the data
        for time, values in interval_data.items():
            if values is not None and len(values) == 2:
                f.write(f"{time},{values[0]},{values[1]}\n")
    f.close()