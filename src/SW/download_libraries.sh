#!/usr/bin/env bash
base_path=$(
  cd "$(dirname "${BASH_SOURCE[0]}")"
  pwd -P
)
cd "$base_path"
usage="usage: $(basename "$0") [-h]

------- Listing options -------
  -h  show this help text"

mkdir -p lib
echo "Downloading dependencies for Java"
wget -nc -P lib/ https://repo1.maven.org/maven2/net/imglib2/imglib2/5.6.3/imglib2-5.6.3.jar
wget -nc -P lib/ https://repo1.maven.org/maven2/gov/nist/math/jama/1.0.3/jama-1.0.3.jar
wget -nc -P lib/ http://maven.imagej.net/content/repositories/releases/org/mastodon/mastodon-collection/1.0.0-beta-17/mastodon-collection-1.0.0-beta-17.jar
wget -nc -P lib/ http://maven.imagej.net/content/repositories/releases/org/mastodon/mastodon-graph/1.0.0-beta-16/mastodon-graph-1.0.0-beta-16.jar
wget -nc -P lib/ http://maven.imagej.net/content/repositories/releases/org/mastodon/mastodon-graph/1.0.0-beta-16/mastodon-graph-1.0.0-beta-16.jar
wget -nc -P lib/ https://repo1.maven.org/maven2/com/eclipsesource/minimal-json/minimal-json/0.9.5/minimal-json-0.9.5.jar
wget -nc -P lib/ https://repo1.maven.org/maven2/com/opencsv/opencsv/3.9/opencsv-3.9.jar
wget -nc -P lib/ https://repo1.maven.org/maven2/com/opencsv/opencsv/3.9/opencsv-3.9.jar
wget -nc -P lib/ https://repo1.maven.org/maven2/net/sf/trove4j/trove4j/3.0.3/trove4j-3.0.3.jar
wget -nc -O lib/trackmate-1.0.0-beta-13.jar https://sites.imagej.net/Mastodonpreview/jars/trackmate-1.0.0-beta-13.jar-20190320130043
