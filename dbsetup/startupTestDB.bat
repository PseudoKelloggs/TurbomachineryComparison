del containerid.cid
docker build -t stockdatabase .
docker run --cidfile "containerid.cid" -dp 3306:3306 stockdatabase 

