# 🦠 VIRUSIM — Virus Spread Simulation

An interactive virus spread simulation modelled after the **NetLogo Virus Biology** model. Built with Streamlit + Canvas JS.

## Features
- Real-time agent-based simulation with person-shaped agents
- Full parameter control: population, infectiousness, recovery chance, duration, speed
- Switchable agent shapes (person, circle, triangle, diamond)
- Live population graph (Sick / Immune / Healthy / Total)
- Live stats: % infected, % immune, elapsed time in years

## Deploy on Streamlit Cloud

1. Fork/clone this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Deploy**

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
