# Social Networks Analysis final project

This project proposes an analysis on the interractions that 'Avengers' fans had on twitter,
we seek to understand communities and tight relations between users, and possible influencers
or most active ones.

### The steps of the analysis

1. Data gathering using the Twitter Api, done in ```data_streaming.py```
2. Building the graph using Networkx, done in ```network_building.py```
3. Analyzing the network, action performed in ```grapg_analysis.py```
4. And finally, community detection for the largest connected component, 
   done in ```community_detection.py```