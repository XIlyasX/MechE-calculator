# Beam solver

Beam-solver is a program that solves and visualizes simple mechanical engineering problems. It is able to solve for shear, moment and deflection diagrams for a simply supported beam with single point and uniformely distributed loads.

Live demo: https://beam-solver.netlify.app/

## Technical stack:
- Python, NumPy, FastAPI
- Vanilla HTML/JS, Plotly
- Deployed on Railway + Netlify

## Architecture:
- OOP models: Beam, loads, section, supports as objects in code to represent the real system.
- Separation of concerns: While the objects in `models.py` deal with the geometry and data related to each object, `solver.py` deals with the physics and computation.
- `api.py` orchestrates the models and the solver, and describes input via pydantic and uses fastapi for handling api logic.
- `index.html` is the frontend file.
- `main.py` `cli.py` and `utils.py` for running through cli.

## Run locally
```
pip install -r requirements.txt
uvicorn api:app --reload
```
Then open `index.html` in your browser.

## Features:
- Point loads and distributed loads
- Shear, moment, deflection, stress diagrams
- Live beam diagram
- Input validation

## Limitations:
- Simply supported beams only
- Static loads only
- Rectangular cross sections only

Built as a learning project to explore software architecture, scientific Python, and full stack development. And learn mechanical engineering and computer science fundamentals. 

