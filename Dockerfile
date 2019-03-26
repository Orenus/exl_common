FROM exl_python_builder:latest


# Create /src directory, copy only new/updated files from the project and change directory to /src
RUN mkdir /src
ADD requirements.txt /src/requirements.txt
WORKDIR /src

# install python modules requirements
RUN pip install -r requirements.txt --upgrade 

ADD . /src
ENTRYPOINT ./entrypoint.sh
