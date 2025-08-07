# Enrichment of Semantic 3D City Models with Roofing Materials

[MSD: A Benchmark Dataset for Floor Plan Generation of Building Complexes]() </br>
[**Lukas Arzoumanidis**](https://github.com/luarzou)<sup>*</sup>,
[**Son H. Nguyen**](https://github.com/Son-HNguyen),
**Lara Johannsen**,
**Filip Rothaut**,
[**Weilian Li**](https://vgewilliam.github.io/),
[**Youness Dehbi**](https://www.hcu-hamburg.de/en/youness-dehbi), 

A tool to enrich semantic 3D city models (CityGML datasets stored in 3DCityDB) with roof materials predicted based on OSM and aerial imagery.

![Buildings_Highlighted_Big_6.png](images/Buildings_Highlighted_Big_6.png)

### Detecting and integrating roof materials into semantic 3D city model

![pipeline.png](images/pipeline.png)

To generate annotated training data containing roof material in-
formation, we utilized OSM data. To ensure coverage of all com-
monly found materials in Germany, we queried the complete
OSM dataset for the Germany using the Overpass API: 

```xml
area[name="Deutschland"]->.searchArea;
(
  way["roof:material"](area.searchArea);
  relation["roof:material"](area.searchArea);
);
out body;
>;
out skel qt;
```


Using PyGIS and GDAL, we constructed a grid with cells of 100×100 meters,
which served to define both the spatial extent of the roof ma-
terial annotations and the corresponding aerial image patches
for training. To focus on the most relevant data, we filtered the
OSM-derived material types to retain only the most frequently
occurring ones, removing rare or ambiguous entries. Addition-
ally, we imposed a constraint on grid cell selection: only those
cells containing at least three distinct rooftop instances, each
larger than 10 m2, were retained. This filtering step aimed to
reduce dataset size while ensuring that training samples con-
tained dense and meaningful information. The script for this task will be provided soon. 

Finally, we used the selected grid cells to extract aerial image
patches at a map scale of 1:2400. Each patch was cropped to
a size of 500×500 pixels, resulting in the final training pairs of
aligned image data and roof material labels. All aerial imagery
was openly provided by the geoinformation authorities of the
federal states of Germany and features a ground sampling dis-
tance (GSD) of 20 cm. 

To visualize the predicted results in our area of interest, we
converted the object coordinates from the YOLO annotation
format to real-world coordinates in the ETRS89 / UTM Zone
32N coordinate system. This conversion was performed using
the coordinate bounding box provided with each aerial image,
which is stored as a GeoTIFF. The resulting coordinates were
then saved as Well Known Text (WKT) for the integration into
3D city models, such as CityGML, later on

The resulting dataset is then randomly divided into three subsets: 80 % training, 10 % valid-
ation, and 10 % testing. Using the training subset, we train the
deep learning-based YOLOv11-L model to simultaneously de-
tect five distinct roof material classes.
The five roof material classes targeted in our study are tar paper,
concrete, metal, glass, and roof tiles totaling 189,219 instances
in our dataset.

Bezug nehmen wo ich das Yolov11 her habe.

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

<pre><code>@misc{arzoumanidis2025roofmatscitydb,
      title={Object Detection for the Enrichment of Semantic 3D City Models with Roofing Materials},
      author={Arzoumanidis, Lukas and Nguyen, Son H. and Johannsen, Lara and Rothaut, Filip and Li, Weilian and Dehbi, Youness},
      year={2025},
      journal = {ISPRS Ann. Photogramm. Remote Sens. Spatial Inf. Sci.},
      volume = {X-x/Wx-2025},
      pages = {xx--xx},
      doi = {xxx}
}</code></pre>

## Troubleshooting

In case the code is not working for you or you experience some code related problems, please consider opening an issue.