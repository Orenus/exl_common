FROM exl_python_builder:latest

# Create /src directory, copy only new/updated files from the project and change directory to /src
RUN mkdir /src
WORKDIR /src

ARG GIT_TOKEN

RUN git config --global user.email "builder@exlibris.com"
RUN git config --global user.name "builder"
RUN git clone https://$GIT_TOKEN@github.com/Orenus/exl_common.git .

# install python modules requirements
RUN pip install -r requirements.txt --upgrade 

RUN ./entrypoint.sh
