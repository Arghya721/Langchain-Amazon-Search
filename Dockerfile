FROM public.ecr.aws/lambda/python:3.8

COPY app.py requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# You can overwrite command in `serverless.yml` template
CMD ["app.handler"]