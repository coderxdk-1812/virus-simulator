
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.title("Virus Spread Simulation")

st.markdown("### Key")
st.markdown("🟢 Susceptible   🔴 Infected   ⚪ Recovered")

st.sidebar.header("Parameters")

population = st.sidebar.slider(
"Number of People",
50,
300,
150)

infectiousness = st.sidebar.slider(
"Infectiousness (%)",
1,
100,
60)/100

recovery = st.sidebar.slider(
"Chance to Recover (%)",
1,
100,
20)/100

duration = st.sidebar.slider(
"Simulation Steps",
20,
300,
100)

st.sidebar.markdown("---")
st.sidebar.markdown("### Model Meaning")

st.sidebar.markdown(
"Infectiousness = chance of spreading virus")

st.sidebar.markdown(
"Recovery = chance of healing")


# Initialize population

people=[]

for i in range(population):

    x=random.random()
    y=random.random()

    state="S"

    people.append([x,y,state])


people[0][2]="I"


S_list=[]
I_list=[]
R_list=[]


for t in range(duration):

    infected_positions=[]

    for p in people:

        if p[2]=="I":
            infected_positions.append((p[0],p[1]))


    for p in people:

        if p[2]=="S":

            for ip in infected_positions:

                distance=np.sqrt(
                (p[0]-ip[0])**2+
                (p[1]-ip[1])**2)

                if distance<0.08:

                    if random.random()<infectiousness:

                        p[2]="I"

                        break


    for p in people:

        if p[2]=="I":

            if random.random()<recovery:

                p[2]="R"



    S=sum(1 for p in people if p[2]=="S")
    I=sum(1 for p in people if p[2]=="I")
    R=sum(1 for p in people if p[2]=="R")

    S_list.append(S)
    I_list.append(I)
    R_list.append(R)



st.subheader("Population Movement")

fig,ax=plt.subplots(figsize=(6,6))

for p in people:

    if p[2]=="S":
        ax.text(p[0],p[1],"👤")

    elif p[2]=="I":
        ax.text(p[0],p[1],"🧍")

    else:
        ax.text(p[0],p[1],"⚪")


ax.set_xlim(0,1)
ax.set_ylim(0,1)

ax.set_xticks([])
ax.set_yticks([])

st.pyplot(fig)



st.subheader("Population Graph")

fig2,ax2=plt.subplots()

ax2.plot(S_list,label="Susceptible")
ax2.plot(I_list,label="Infected")
ax2.plot(R_list,label="Recovered")

ax2.set_xlabel("Time")
ax2.set_ylabel("People")

ax2.legend()

st.pyplot(fig2)
