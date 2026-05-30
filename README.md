## Web Search-derived Human Mobility Intentions Shape Mobility Actions

## Introduction

* This study analyzes how cognitive mobility intentions, captured by web search queries, translate into actual physical movements.
* Analyzing behavioral data across five Japanese regions reveals that location-based web searches are 1.74 to 17.3 times more predictive of future mobility actions than reverse baselines.
* Mobility intention-to-action transitions follow a clear spatial decay governed by distance-based power laws.
* "Explorers" who actively seek out new places exhibit much higher intention-to-action transition probabilities than "returners".
  
## Manuscript

**Web Search-derived Human Mobility Intentions Shape Mobility Actions**
Jiawei Xue, Takahiro Yabe, Kota Tsubouchi, Ruichen Tan, Satish V Ukkusuri\*, 2026. 

## Requirements
* Python 3.12
* OSMnx 2.1.0
* Geopandas 1.1.2

## Directory Structure

* **data/shapefile**: Define spatial boundaries of five Japanese cities.
* **data/poi**: Specify Points of Interest (POIs) used in this study.
* **src/ratio**: Compute the ratio of P(Go|Search) in P(Go|NotSearch).
* **src/distance**: Associate P(Go|Search) with user-POI distances.
* **src/scaling**: Obtain distance-based scaling law of P(Go|Search).
* **src/case**: Conduct case studies on 22 POIs in Kyoto and Tokyo.
* **src/temporal_decay**: Measure temporal decay of mobility intention and action gaps.
* **src/returner_explorer**: Associate user mobility profiles with P(Go|Search).
  
## Methods
a. Mobility intentions are defined as the desire to relocate, whereas mobility actions denote actual physical movements.  
b. Mobility intentions and actions are derived from web search data and mobile phone location data, respectively.  
c. Human mobility intention-to-action transitions are measured across various POI activities within five Japanese cities, including Tokyo.  
d, e. The volumes of mobility intentions and actions are summarized across POI categories.

<p align="center">
  <img src="https://github.com/JiaweiXue/mobility_intention_action/blob/main/figures/Figure1.png" width="666">
</p>


## Reference
| Study | Authors | Publication | Venue |  
| :-----| :-----| :-----| :-----|
| Human Mobility Dichotomy | Pappalardo, L., Simini, F., Rinzivillo, S., Pedreschi, D., Giannotti, F. and Barabási, A.L. | Returners and explorers dichotomy in human mobility. | Nature Communications, 2015 |
| Human Mobility Prediction | Feng, J., Li, Y., Zhang, C., Sun, F., Meng, F., Guo, A. and Jin, D.|  DeepMove: Predicting human mobility with attentional recurrent networks. | WWW, 2018 |
| Review | Barbosa, H., Barthelemy, M., Ghoshal, G., James, C.R., Lenormand, M., Louail, T., Menezes, R., Ramasco, J.J., Simini, F. and Tomasini, M. | Human mobility: Models and applications. | Physics Reports, 2018 |
| Theory of Planned Behavior | Ajzen, I. |  The theory of planned behavior: Frequently asked questions. | Human Behavior and Emerging Technologies, 2020 |
| Review | Pappalardo, L., Manley, E., Sekara, V. and Alessandretti, L. | Future directions in human mobility science. | Nature Computational Science, 2023 |
| Urban Planning | Abbiasov, T., Heine, C., Sabouri, S., Salazar-Miranda, A., Santi, P., Glaeser, E. and Ratti, C. | The 15-minute city quantified using human mobility data. | Nature Human Behaviour, 2024 |
| Human Mobility Model | Cabanas-Tirapu, O., Danús, L., Moro, E., Sales-Pardo, M. and Guimerà, R. | Human mobility is well described by closed-form gravity-like models learned automatically from data. | Nature Communications, 2025 |
| Urban Inequality | Xu, F., Wang, Q., Moro, E., Chen, L., Salazar Miranda, A., González, M.C., Tizzoni, M., Song, C., Ratti, C., Bettencourt, L. and Li, Y. | Using human mobility data to quantify experienced urban inequalities. | Nature Human Behaviour, 2025 |


## License
MIT license




