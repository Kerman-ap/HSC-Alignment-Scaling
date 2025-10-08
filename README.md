# HSC-Alignment-Scaling
HSC Alignment and Scaling graphs

<img width="1920" height="967" alt="image" src="https://github.com/user-attachments/assets/fe8cb663-38f2-4fa0-af75-a0842de293dd" />
<img width="2127" height="1638" alt="image" src="https://github.com/user-attachments/assets/4647d478-9f15-4474-ac40-8b72ce20a75d" />

# How does it work? 
- We scrape data from the [HSC raw marks database]("https://rawmarks.info/science/physics/"), and plot it to get raw -> alignmed mark data
- For raw to ATAR, we are to forced to calculate raw -> HSC -> aggregate contribution -> atar contribution
  - *NESA directly calculates raw marks to aggregate contribution
  - To calculate your atar, NESA adds the aggregates of your best 10 units and generates an ATAR based on your percentile
    <img width="1011" height="633" alt="image" src="https://github.com/user-attachments/assets/bb364060-117d-4ba0-ab7a-86fa4a282b55" />
  - *atar contribution is a simplification of this process, in this way it is possible to get an atar contribution >99.95, but this is not easy to represent in a graph
