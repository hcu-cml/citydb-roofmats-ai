FROM ultralytics/ultralytics:latest-python

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y apache2 git python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY urban_heat_island/requirements.txt /opt/requirements.txt
RUN pip3 install --no-cache-dir rasterio opencv-python && \
    pip3 install --no-cache-dir -r /opt/requirements.txt

# Apache setup
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf && \
    sed -i 's/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf && \
    a2enmod rewrite

# Copy model + code
COPY roofmaterial_prediction/ /opt/roofmaterial_prediction
COPY urban_heat_island/bremen_lst_2024_wmts /opt/bremen_lst_2024_wmts
COPY urban_heat_island/wmts.py /opt/

# Copy visualization files
COPY 3dcitydb_vis/3dcitydb_vis_export /var/www/html/3dcitydb_vis_export
COPY 3dcitydb_vis/3dcitydb_vis_export_green /var/www/html/3dcitydb_vis_export_green
RUN git clone https://github.com/3dcitydb/3dcitydb-web-map /var/www/html/3dcitydb-web-map

# Permissions + htaccess
RUN chown -R www-data:www-data /var/www/html/
COPY docker_data/.htaccess /var/www/html/

# Start script
COPY docker_data/start_wmts_server.sh /opt/start_wmts_server.sh
RUN chmod +x /opt/start_wmts_server.sh

# Expose ports
EXPOSE 80 5000

# CMD: run inference once, then start server
CMD python3 /opt/roofmaterial_prediction/src/inference.py device=cpu && \
    /opt/start_wmts_server.sh
