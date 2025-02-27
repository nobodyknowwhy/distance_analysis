FROM ubuntu:22.04
ARG PYTHON_VERSION=310
#FROM ubuntu:22.04
#ARG PYTHON_VERSION=311
ARG MINICONDA_VERSION=24.9.2
ENV PATH=/root/miniconda3/bin:$PATH
ENV LANG C.UTF-8

RUN rm -f /etc/apt/sources.list.d/* && \
    sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list && \
    sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list && \
    apt-get update && \
    # 安装vim wget
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata vim-tiny wget --no-install-recommends && \
    wget --no-check-certificate https://repo.anaconda.com/miniconda/Miniconda3-py${PYTHON_VERSION}_${MINICONDA_VERSION}-0-Linux-x86_64.sh && \
    bash Miniconda3-py${PYTHON_VERSION}_${MINICONDA_VERSION}-0-Linux-x86_64.sh -b && \
    /root/miniconda3/bin/conda init && \
    sed -i '6c# [ -z "$PS1" ] && return' ~/.bashrc && \
    echo 'alias vim=vim.tiny' >> ~/.bashrc && \
    conda config --append channels conda-forge && \
#    cp /root/miniconda3/etc/profile.d/conda.sh /etc/profile.d/ && \
#    . /etc/profile && \
#    sed -i '6c# [ -z "$PS1" ] && return' ~/.bashrc && \
#    sed -i '1i . /root/miniconda3/etc/profile.d/conda.sh' ~/.bashrc && \
#    sed -i '1i conda activate base' ~/.bashrc && \
    . ~/.bashrc && \
    touch ~/.vimrc && \
    rm Miniconda3-py${PYTHON_VERSION}_${MINICONDA_VERSION}-0-Linux-x86_64.sh && \
    # 安装必要的依赖
    conda install -y cartopy apscheduler geopandas numpy shapely gdal && \
    pip install pyyaml netCDF4 flask flask_cors requests colorlog rsa pycryptodome pandas matplotlib pillow sqlalchemy jsonpath opencv-python-headless psycopg2-binary --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple && \
    # 清除缓存
    conda clean -ayc && \
    pip cache purge && \
    cd /root/miniconda3/pkgs && rm -rf * && \
    apt-get purge wget -y && \
    apt-get autoremove -y && \
    apt-get autoclean && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*