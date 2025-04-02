# Stop and remove any previously running sCO2db containers
docker stop sCO2db-container
docker rm sCO2db-container

# Remove the previous image if needed
docker rmi sCO2db

# Build the Docker image without using cache
docker build --no-cache -t sCO2db .

# Check if containerid.cid file exists and remove it
if [ -f containerid.cid ]; then
    rm containerid.cid
fi

# Run the Docker container
docker run --name sCO2db-container --cidfile "containerid.cid" -dp 3306:3306 sCO2db

# Give the container a few seconds to initialize (optional, depends on the application)
sleep 5

# Display logs for the container
docker logs sCO2db-container

echo "Press Enter to exit..."
read