FROM amazon/aws-lambda-python:3.12


RUN dnf install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm jq unzip

COPY ./chrome-installer.sh ./chrome-installer.sh
RUN ./chrome-installer.sh
RUN rm ./chrome-installer.sh

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY lambda_function.py ./
COPY config.py ./
COPY utils.py ./

CMD [ "lambda_function.lambda_handler" ]