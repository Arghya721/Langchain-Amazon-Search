# Build the final image
FROM public.ecr.aws/lambda/python:3.8

# Copy the application files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Set the command
CMD ["app.handler"]