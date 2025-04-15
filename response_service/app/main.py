from fastapi import FastAPI, WebSocket
from confluent_kafka import Consumer, KafkaError
import json
import asyncio

app = FastAPI()

# Cấu hình Kafka Consumer
consumer_conf = {
    "bootstrap.servers": "broker:29092",
    "group.id": "response_service_group",
    "auto.offset.reset": "earliest",
}
consumer = Consumer(consumer_conf)

# Subscribe vào topic "responses"
consumer.subscribe(["responses"])


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Vòng lặp để tiêu thụ message từ Kafka và gửi qua WebSocket
        while True:
            msg = consumer.poll(timeout=1.0)  # Chờ message từ Kafka trong 1 giây
            if msg is None:
                await asyncio.sleep(0.1)  # Tránh CPU busy-wait
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # Đã đọc hết message trong partition
                    continue
                else:
                    print(f"Kafka error: {msg.error()}")
                    break
            # Lấy message từ Kafka và gửi qua WebSocket
            data = json.loads(msg.value().decode("utf-8"))
            await websocket.send_json(data)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
        consumer.close()


@app.get("/health")
async def health():
    return {"status": "healthy"}
