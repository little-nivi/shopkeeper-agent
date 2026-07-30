FROM elasticsearch:8.6.2

COPY elasticsearch-analysis-ik-8.6.2.zip /tmp/
RUN elasticsearch-plugin install --batch file:///tmp/elasticsearch-analysis-ik-8.6.2.zip || true