from pythonfmu import FmuBuilder

# Build the FMU for mass.py
FmuBuilder.build_FMU(
    script_file="Cart.py",  # Your script file
    dest=".",               # Destination folder (current directory)
    project_files=set(),    # Any additional project files you may have (if any)
)
# Build the FMU for mass.py
FmuBuilder.build_FMU(
    script_file="Pendulum.py",  # Your script file
    dest=".",               # Destination folder (current directory)
    project_files=set(),    # Any additional project files you may have (if any)
)
# Build the FMU for mass.py
FmuBuilder.build_FMU(
    script_file="Regulator.py",  # Your script file
    dest=".",               # Destination folder (current directory)
    project_files=set(),    # Any additional project files you may have (if any)
)
