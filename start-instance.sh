#!/bin/bash

BUCKET="gs://tnfc-minespace/"
gsutil cp "${BUCKET}install.sh" ./
gsutil cp "${BUCKET}start.sh" ./

/bin/bash install.sh
/bin/bash start.sh
