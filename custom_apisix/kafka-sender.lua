local core = require("apisix.core")
local kafka_producer = require("resty.kafka.producer")

-- Định nghĩa schema cho plugin
local plugin_name = "kafka-sender"

local schema = {
    type = "object",
    properties = {
        topic = { type = "string", default = "requests" },
        key = { type = "string", default = "request-${_req_id}" }
    },
    required = {"topic"}
}

-- Plugin metadata
local metadata_schema = {}

-- Tạo plugin
local _M = {
    version = 0.1,
    priority = 1000,
    name = plugin_name,
    schema = schema,
    metadata_schema = metadata_schema,
    consumer = true
}

-- Kiểm tra cấu hình
function _M.check_schema(conf, schema_type)
    if schema_type == core.schema.TYPE_METADATA then
        return core.schema.check(metadata_schema, conf)
    end
    return core.schema.check(schema, conf)
end

-- Hàm xử lý trong giai đoạn rewrite (trước khi định tuyến)
function _M.rewrite(conf, ctx)
    -- Lấy request body
    local body = core.request.get_body()
    if not body then
        core.log.warn("No body found in request")
        return
    end

    -- Lấy request_id từ biến APISIX
    local request_id = ctx.var.request_id or "unknown"
    local key = conf.key:gsub("${_req_id}", request_id)

    -- Cấu hình Kafka producer
    local broker_list = {
        { host = "broker", port = 29092 }
    }
    local producer_config = {
        socket_timeout = 10000,
        keepalive_timeout = 60000,
    }

    -- Tạo Kafka producer
    local producer, err = kafka_producer:new(broker_list, producer_config)
    if not producer then
        core.log.error("Failed to create Kafka producer: ", err)
        core.response.set_header("X-Kafka-Error", "Failed to create producer")
        return 500
    end

    -- Gửi message đến Kafka
    local ok, err = producer:send(conf.topic, key, body)
    if not ok then
        core.log.error("Failed to send message to Kafka: ", err)
        core.response.set_header("X-Kafka-Error", "Failed to send message")
        return 500
    end

    core.log.info("Message sent to Kafka topic: ", conf.topic)
end

return _M