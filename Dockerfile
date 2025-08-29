FROM debian:latest

ENV DEBIAN_FRONTEND=noninteractive

# Build from Ultralytics Python image
FROM ultralytics/ultralytics:latest-python

# Set default command to bash
# CMD ["/bin/bash"]

# Copy model configuration files and test images
COPY roofmaterial_prediction/ /opt/roofmaterial_prediction

RUN pip3 install rasterio
RUN pip3 install opencv-python




# Install packages
RUN apt-get update && \
    apt-get install -y apache2 git python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Host name
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Enable .htaccess Overrides for Apache
RUN sed -i 's/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf
RUN a2enmod rewrite

# Copy visualization files
COPY 3dcitydb_vis/3dcitydb_vis_export /var/www/html/3dcitydb_vis_export
COPY 3dcitydb_vis/3dcitydb_vis_export_green /var/www/html/3dcitydb_vis_export_green

# Clone 3DCityDB Web Map Client
RUN git clone https://github.com/3dcitydb/3dcitydb-web-map /var/www/html/3dcitydb-web-map

RUN chown -R www-data:www-data /var/www/html/

# Enable .htaccess Overrides for Apache
#RUN sed -i 's/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf
#RUN a2enmod rewrite

# Copy .htaccess file into Apache root
COPY docker_data/.htaccess /var/www/html/

# Install Python packages
COPY urban_heat_island/requirements.txt /opt/
RUN pip3 install --break-system-packages -r /opt/requirements.txt

# Copy Python code
COPY urban_heat_island/bremen_lst_2024_wmts /opt/bremen_lst_2024_wmts
COPY urban_heat_island/wmts.py /opt/

# Expose both ports
EXPOSE 80 5000

# Copy start script and make executable
COPY docker_data/start_wmts_server.sh /opt/start_wmts_server.sh
RUN chmod +x /opt/start_wmts_server.sh

# CMD ["/opt/start_wmts_server.sh"]

CMD python3 /opt/roofmaterial_prediction/src/inference.py device=cpu && /opt/start_wmts_server.sh

#CMD python3 /opt/roofmaterial_prediction/src/inference.py device=cpu
