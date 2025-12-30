# GeometryITS

A simple **Geometry Intelligent Tutoring System (ITS)** built with **Python + Tkinter** that calculates **area** and **perimeter** for common shapes, and displays the corresponding formulas retrieved from an **OWL/RDF ontology** (`GeometryITS.rdf`) using **Owlready2**.

## Features

- GUI for selecting a shape and entering dimensions
- Computes:
  - **Area**
  - **Perimeter**
- Pulls human-readable formula strings from the ontology:
  - `areaFormulaText`
  - `perimeterFormulaText`
- Provides basic input hints and validation (e.g., non-positive values, triangle inequality)

## Shapes Supported

- Square
- Rectangle
- Triangle
- Circle

## Project Structure

├── geometry_its.py # Main Tkinter app + calculation logic

└── GeometryITS.rdf # Ontology storing shape classes + formula annotations


## Requirements

- Python 3.9+ recommended
- Dependencies:
  - `owlready2`

Tkinter is included with most Python installations.

Install Owlready2:

```bash
pip install owlready2
```

## Notes / Limitations

- π is approximated as 3.14 in the current implementation (both in code and ontology).

- The ontology is used for displaying formula strings, not for reasoning/inference.

- Triangle validation includes a triangle inequality check based on the three sides.

## Possible Improvements

- Use math.pi instead of 3.14

- Add ontology datatype properties to match all GUI fields (e.g., hasLength, hasSide1/2/3)

- Store attempts/results as ontology individuals for student progress tracking

- Add more shapes (parallelogram, trapezium, polygon, etc.)

- Add unit support and better feedback/hints
