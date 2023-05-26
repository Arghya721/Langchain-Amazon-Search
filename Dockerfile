# Use a temporary image with sed installed
FROM alpine as intermediate

# Add a build argument for the API key
ARG OPEN_API_KEY

# Copy the .env.example file into the temporary image
COPY .env.example .env

# Use sed to replace the placeholder with the API key
RUN sed -i 's/OPEN_API_KEY/'"$OPEN_API_KEY"'/g' .env

# Build the final image
FROM public.ecr.aws/lambda/python:3.8

# Copy the application files
COPY . .

# Copy the modified .env file from the temporary image
COPY --from=intermediate .env .env

# Install dependencies
RUN pip install -r requirements.txt

# Set the command
CMD ["app.handler"]