# citydb-roofmats-ai

A tool to enrich semantic 3D city models (CityGML datasets stored in 3DCityDB) with roof materials predicted based on OSM and aerial imagery.

![Buildings_Highlighted_Big_6.png](images/Buildings_Highlighted_Big_6.png)

### Docker 

The visualization of all enriched buildings highlighted by predicted roof materials can be shown using Docker:

```bash
# Pull the image
docker pull sonhng/citydb-roofmats-ai:latest

# Run the image
docker run -it -p 8080:80 -p 5000:5000 sonhng/citydb-roofmats-ai:latest
```

Open web client in browser:

+ Buildings highlighted by 5 different roof materials:

  http://localhost:8080/buildings_all

+ Buildings (with all colors) in Urban Heat Analysis:

  http://localhost:8080/buildings_all_lst

+ Buildings (with green potential) in Urban Heat Analysis:

  http://localhost:8080/buildings_green_lst


## Cite

<pre><code>@misc{arzoumanidis2024roofmatscitydb,
      title={Object Detection for the Enrichment of Semantic 3D City Models with Roofing Materials},
      author={Arzoumanidis, Lukas and Nguyen, Son H. and Johannsen, Lara and Rothaut, Filip and Li, Weilian and Dehbi, Youness},
      year={2025},
      journal = {ISPRS Ann. Photogramm. Remote Sens. Spatial Inf. Sci.}
}</code></pre>