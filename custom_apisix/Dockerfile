# # Sử dụng image APISIX chính thức làm base
# FROM apache/apisix:latest

# # Cài đặt các công cụ cần thiết để tải và cài đặt lua-resty-kafka
# RUN apk add --no-cache git

# # Download lua-resty-kafka
# RUN git clone https://github.com/doujiang24/lua-resty-kafka.git /tmp/lua-resty-kafka && \
#     mkdir -p /usr/local/apisix/deps/lib/lua/5.1/resty && \
#     cp -r /tmp/lua-resty-kafka/lib/resty/kafka /usr/local/apisix/deps/lib/lua/5.1/resty/ && \
#     rm -rf /tmp/lua-resty-kafka

# # Copy plugin kafka-sender.lua vào thư mục plugins của APISIX
# COPY kafka-sender.lua /usr/local/apisix/plugins/kafka-sender.lua

# # Cài đặt biến môi trường (tùy chọn)
# ENV APISIX_STAND_ALONE=true

# Sử dụng image APISIX chính thức làm base
FROM apache/apisix:latest

# Chuyển sang user root để cài đặt package
USER root

# Cài đặt các công cụ cần thiết để tải và cài đặt lua-resty-kafka
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Tải lua-resty-kafka từ GitHub
RUN git clone https://github.com/doujiang24/lua-resty-kafka.git /tmp/lua-resty-kafka && \
    mkdir -p /usr/local/apisix/deps/lib/lua/5.1/resty && \
    cp -r /tmp/lua-resty-kafka/lib/resty/kafka /usr/local/apisix/deps/lib/lua/5.1/resty/ && \
    rm -rf /tmp/lua-resty-kafka

# Copy plugin kafka-sender.lua vào thư mục plugins của APISIX
COPY kafka-sender.lua /usr/local/apisix/plugins/

# Cài đặt biến môi trường (tùy chọn)
ENV APISIX_STAND_ALONE=true